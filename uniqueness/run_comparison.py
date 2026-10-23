"""M6: paired real generations; preserve raw evidence and render the report."""

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from content_pipeline import check_quality, generate_draft
from llm_integration import MODEL, call_llm
from build_report import build_report

HERE = Path(__file__).resolve().parent
CASES = [
    ('linkedin', 'gravel', 'autumn weekend adventures on mixed terrain'),
    ('email', 'road', 'comfortable long-distance rides for your next big day out'),
    ('linkedin', 'mountain', 'confidence and control on technical trails'),
    ('newsletter', 'gravel', 'planning a weekend bikepacking adventure'),
    ('instagram', 'mountain', 'finding confidence on rocky trails'),
]


def save(data, path):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')


def run():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--render-only', action='store_true', help='No API calls; rebuild reports from results.json')
    parser.add_argument('--append-channels', action='store_true', help='Append newsletter/Instagram only, preserving the original three cases')
    args = parser.parse_args()
    result_path = HERE / 'results.json'
    if args.render_only:
        build_report(HERE)
        return
    if result_path.exists() and not args.append_channels:
        raise SystemExit('results.json exists. Archive it before a new run; never overwrite evidence.')
    # Record file hashes so later KB changes cannot silently redefine this test.
    files = sorted((ROOT / 'knowledge_base').rglob('*.md')) + sorted((ROOT / 'templates').glob('*.txt'))
    data = {'date_utc': datetime.now(timezone.utc).isoformat(), 'model': MODEL,
            'temperature': 0.7, 'status': 'running', 'cases': [],
            'source_sha256': {p.relative_to(ROOT).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in files}}
    start = 0
    if args.append_channels:
        original = json.loads(result_path.read_text(encoding='utf-8'))
        if original['status'] != 'complete' or len(original['cases']) != 3:
            raise SystemExit('Append requires exactly three complete original cases.')
        if original['model'] != MODEL or original['source_sha256'] != data['source_sha256']:
            raise SystemExit('Model or KB/templates changed; do not mix different comparison conditions.')
        backup = HERE / 'results.original-three.json'
        with backup.open('x', encoding='utf-8') as output:
            output.write(result_path.read_text(encoding='utf-8'))
        data = original
        data['extension_utc'] = datetime.now(timezone.utc).isoformat()
        data['status'] = 'running'
        start = 3
    save(data, result_path)
    try:
        for index, (channel, product, topic) in enumerate(CASES[start:], start + 1):
            request = f'Write a Canyon Bicycles {channel} marketing draft about {product} bikes. Topic: {topic}. Write in British English.'
            # Share the same output-format instructions with both arms.
            template = (ROOT / 'templates' / f'{channel}.txt').read_text(encoding='utf-8')
            format_brief = template.split('OUTPUT FORMAT', 1)[1].strip()
            case = {'id': index, 'channel': channel, 'product': product, 'topic': topic,
                    'request': request, 'generic': {}, 'system': {}}
            data['cases'].append(case)
            case['generic']['system_prompt'] = 'You are a helpful marketing copywriter. Be accurate. Do not invent specifications, prices, offers or URLs.'
            case['generic']['user_prompt'] = request + '\n\nOUTPUT FORMAT\n' + format_brief
            # Alternate ordering to avoid always generating the same arm first.
            for arm in (('generic', 'system') if index % 2 else ('system', 'generic')):
                if arm == 'generic':
                    output = call_llm(case[arm]['user_prompt'], system_prompt=case[arm]['system_prompt'])
                else:
                    def capture(user_prompt, system_prompt):
                        case['system'].update(user_prompt=user_prompt, system_prompt=system_prompt)
                        return call_llm(user_prompt, system_prompt=system_prompt)
                    with patch('content_pipeline.call_llm', side_effect=capture):
                        output = generate_draft(channel, product, topic, 'English')
                case[arm]['output'] = output
                case[arm]['quality'] = check_quality(output, channel)
                save(data, result_path)
                print(f'{index}/{len(CASES)} {channel}/{product}: {arm} captured', flush=True)
        data['status'] = 'complete'
    except Exception as error:
        data['status'] = 'failed'
        data['error'] = f'{type(error).__name__}: {error}'
        raise
    finally:
        save(data, result_path)
        build_report(HERE)


if __name__ == '__main__':
    run()
