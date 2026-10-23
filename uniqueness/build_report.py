"""Build portable, offline HTML and Markdown from unchanged captured outputs."""

import html
import json
from pathlib import Path

METHOD = '''Five fixed requests covering three product families and all four channels; ten generations, one per arm per request. The original three pairs were preserved; newsletter and Instagram were appended in a second batch under the same model and source-file hashes.
The generic baseline uses the same API model, language, format instructions and accuracy guidance,
without company documents. Our arm uses the real generate_draft pipeline with company context,
brand rules and banned-phrase guidance. This tests the whole product package, not the KB alone.
The customer here is the marketing user requesting content, not a support-ticket sender.
This is an API baseline, not a test of the ChatGPT application. Temperature is 0.7;
generation order alternates. All outputs are retained verbatim, including weaknesses.
Automated checks measure house style and length, not truth, persuasiveness or native-language quality.
One sample per case is illustrative, not statistical proof. No independent blind review was conducted.'''

RUBRIC = '''Review factual grounding (claims trace to the selected KB section; preserve model qualifiers),
useful specificity (features connected to relevant rider benefits), brand voice (direct, concise,
British English, category-appropriate) and brief/format adherence. For each dimension use
0 = fails, 1 = mixed, 2 = meets, with quotations and a KB reference. Do not hide invented claims
inside an aggregate score. Unsupported does not mean factually false; the KB itself needs review.
Scores and winner remain pending until evidence is reviewed; no LLM-as-judge scores are invented.'''


def channel_preview(channel, output):
    # Presentation chrome is separate from the unedited, expandable raw response.
    esc = html.escape
    avatar = '<span class="avatar" aria-hidden="true">C</span>'
    identity = f'<div class="identity">{avatar}<div><b>CANYON</b><small>Marketing draft · preview only</small></div><span class="more" aria-hidden="true">•••</span></div>'
    if channel == 'linkedin':
        return f'<div class="platform linkedin"><div class="appbar"><b class="linkedin-logo">in</b><span>LinkedIn · post preview</span></div>{identity}<div class="social-copy">{esc(output)}</div><div class="social-actions" aria-hidden="true"><span>Like</span><span>Comment</span><span>Repost</span><span>Send</span></div></div>'
    if channel == 'instagram':
        # Decorative landscape, not a bike photo or a generated campaign asset.
        landscape = '''<div class="insta-media"><svg viewBox="0 0 600 450" role="img" aria-label="Decorative trail illustration for the layout; not a generated campaign image"><rect width="600" height="450" fill="#e7e4da"/><circle cx="452" cy="100" r="39" fill="#c7b48c"/><path d="M0 290 150 95 310 290 450 160 600 320V450H0Z" fill="#a3b2a3"/><path d="M0 350 210 215 380 355 510 250 600 320V450H0Z" fill="#557368"/><path d="M260 450 340 370 280 330 320 285" fill="none" stroke="#ede3cd" stroke-width="20"/><text x="30" y="395" fill="white" font-size="23" font-family="sans-serif" letter-spacing="4">TRAIL NOTES</text></svg><span>Layout illustration · not generated content</span></div>'''
        return f'<div class="platform instagram"><div class="appbar"><b class="instagram-logo">Instagram</b><span>Caption preview</span></div>{identity}{landscape}<div class="insta-actions" aria-hidden="true"><span>♡</span><span>◯</span><span>↗</span><span class="bookmark">▱</span></div><div class="social-copy"><b class="handle">canyon</b> {esc(output)}</div></div>'
    # Separate the model's actual Subject/Preview fields from its body.
    lines = output.splitlines(keepends=True)
    subject = ''
    preview = ''
    body = []
    for line in lines:
        if line.startswith('Subject:') and not subject:
            subject = line[len('Subject:'):].strip()
        elif line.startswith('Preview:') and not preview:
            preview = line[len('Preview:'):].strip()
        else:
            body.append(line)
    body_text = ''.join(body).strip()
    newsletter = channel == 'newsletter'
    body_html = esc(body_text)
    if newsletter:
        # Highlight only existing short section titles; never invent editorial copy.
        paragraphs = body_text.split('\n\n')
        styled = []
        for paragraph in paragraphs:
            first, separator, rest = paragraph.partition('\n')
            if separator and len(first.split()) <= 7 and not first.rstrip().endswith(('.', '!', '?', ',')):
                styled.append(f'<h4>{esc(first.strip())}</h4><div class="mail-paragraph">{esc(rest)}</div>')
            else:
                styled.append(f'<div class="mail-paragraph">{esc(paragraph)}</div>')
        body_html = ''.join(styled)
    label = 'Newsletter' if newsletter else 'Email'
    return f'<div class="platform mail {"newsletter" if newsletter else "email"}"><div class="appbar"><span>Inbox / {label} preview</span><span aria-hidden="true">☆</span></div><div class="mail-envelope"><h3>{esc(subject)}</h3>{identity}<p class="preheader">{esc(preview)}</p></div><div class="mail-paper">{"<div class=\"newsletter-masthead\">CANYON<span>THE RIDER EDIT / NEWSLETTER PREVIEW</span></div>" if newsletter else ""}<div class="mail-copy">{body_html}</div></div></div>'


def build_report(folder):
    folder = Path(folder)
    data = json.loads((folder / 'results.json').read_text(encoding='utf-8'))
    review_path = folder / 'review.json'
    review = json.loads(review_path.read_text(encoding='utf-8')) if review_path.exists() else {}
    esc = html.escape
    complete = data['status'] == 'complete'
    title = review.get('headline', 'Real outputs captured; evidence review pending' if complete else 'Comparison not complete')
    summary = review.get('summary', 'No winner is claimed until both outputs have been reviewed against the source documents.')
    reviewer = review.get('reviewer', 'Evidence review pending.')
    md = [f'# M6 — Generic AI vs Canyon\n\n{title}\n\n{summary}\n\nReviewer: {reviewer}\n', f'## Method\n\n{METHOD}\n\nModel: {data["model"]}; date UTC: {data["date_utc"]}; status: {data["status"]}.\n', f'## Review rubric\n\n{RUBRIC}\n']
    cards = []
    # Current production checks have no newsletter/Instagram length bounds.
    extra_ranges = {'newsletter': (200, 280), 'instagram': (80, 150)}
    counts = {arm: sum(bool(c.get(arm, {}).get('quality', {}).get('ok')) for c in data['cases']) for arm in ('generic', 'system')}
    for case in data['cases']:
        pair = []
        md.append(f'## {case["id"]}. {case["product"].title()} / {case["channel"]}\n\nRequest: {case["request"]}\n')
        for arm, label in (('generic', 'Generic AI'), ('system', 'Canyon system')):
            item = case.get(arm, {})
            output = item.get('output', 'No output captured.')
            q = item.get('quality', {})
            metrics = f'{q.get("word_count", "—")} words · house-style checks: ' + ('pass' if q.get('ok') else 'needs review')
            if case['channel'] in extra_ranges and q:
                low, high = extra_ranges[case['channel']]
                length_ok = low <= q['word_count'] <= high
                metrics += f'; template length ({low}-{high}): ' + ('pass' if length_ok else 'FAIL')
                metrics += '; production length check is unbounded'
            preview = channel_preview(case['channel'], output)
            pair.append(f'<article class="{arm}"><div class="eyebrow">{label}</div><p class="metrics">{esc(metrics)}</p>{preview}<details class="raw-response"><summary>Original response, verbatim</summary><div class="draft">{esc(output)}</div></details></article>')
            md.append(f'### {label} — verbatim\n\n{output}\n\nAutomated checks: {metrics}.\n')
        notes = review.get('cases', {}).get(str(case['id']), [])
        note_html = ''.join(f'<li>{esc(note)}</li>' for note in notes)
        if not notes:
            note_html = '<li>Evidence review pending; do not claim a winner.</li>'
        md.append('### Evidence review\n\n' + ('\n'.join('- ' + note for note in notes) if notes else 'Pending.') + '\n')
        cards.append(f'<section><div class="case-number">CASE {case["id"]:02d} / {esc(case["channel"].upper())}</div><h2>{esc(case["product"].title())}</h2><p class="brief">{esc(case["request"])}</p><div class="pair">{"".join(pair)}</div><div class="evidence"><h3>What the evidence shows</h3><ul>{note_html}</ul></div></section>')
    css = '''*{box-sizing:border-box}body{margin:0;background:#f3f2ed;color:#202c2b;font:17px/1.6 system-ui,sans-serif}main{max-width:1360px;margin:auto;padding:48px 40px}.eyebrow,.case-number{font-size:12px;letter-spacing:2px;text-transform:uppercase;font-weight:700}header{border-bottom:3px solid #244d43;padding-bottom:32px}h1{font-size:clamp(32px,5vw,58px);line-height:1.1;max-width:950px;margin:18px 0}h2{font-size:34px;margin:8px 0}h3{font-size:18px}p{max-width:1000px}.summary{font-size:21px}.strip{display:flex;gap:40px;padding:22px 0;font-size:15px}.strip strong{font-size:24px;color:#244d43}section{padding:40px 0;border-bottom:1px solid #b8c2bb}.pair{display:grid;grid-template-columns:1fr 1fr;gap:24px}article{padding:28px;background:#fff;border-top:4px solid #7c8583;min-width:0}article.system{border-top-color:#246452}.metrics{font-size:13px;color:#54625d}.draft{white-space:pre-wrap;overflow-wrap:anywhere;font-size:16px}.evidence{padding:12px 24px;background:#e3ebe5;margin-top:20px}details{margin:24px 0}button{padding:10px 20px;background:#244d43;color:white;border:0;cursor:pointer}footer{font-size:13px;margin-top:32px}a{color:#245d4d}@media(max-width:800px){main{padding:24px 16px}.pair{grid-template-columns:1fr}.strip{flex-wrap:wrap}}@media print{body{background:white}main{padding:0}button{display:none}section{break-before:page}article,.evidence{break-inside:avoid}.draft{font-size:11px}.pair{gap:12px}h1{font-size:36px}}'''
    css += '''
    .pair{align-items:start}article{padding:20px;background:transparent}.platform{background:white;border:1px solid #d8ddda;border-radius:12px;overflow:hidden;font-size:15px;line-height:1.55}.appbar{display:flex;align-items:center;justify-content:space-between;padding:12px 18px;border-bottom:1px solid #e4e7e5;font-size:12px;color:#66736c;gap:12px}.linkedin-logo{background:#0a66c2;color:white;font:bold 22px Arial;padding:0 5px;border-radius:2px}.identity{display:flex;align-items:center;gap:10px;padding:18px}.identity b{display:block;font-size:14px;letter-spacing:1px}.identity small{display:block;font-size:11px;color:#69756f}.avatar{background:#182b24;color:white;border-radius:50%;width:40px;height:40px;display:grid;place-items:center;font:bold italic 25px Arial;flex-shrink:0}.more{margin-left:auto;color:#64716a}.social-copy{white-space:pre-wrap;overflow-wrap:anywhere;padding:0 20px 24px}.social-actions{display:flex;justify-content:space-around;border-top:1px solid #e0e5e1;color:#63716a;font-size:12px;font-weight:600;padding:15px 8px}.instagram-logo{font:italic bold 23px Georgia;color:#202020}.insta-media{position:relative}.insta-media svg{display:block;width:100%;height:auto}.insta-media>span{position:absolute;bottom:10px;right:10px;background:#ffffffde;color:#30473b;font-size:9px;padding:3px 7px}.insta-actions{display:flex;gap:17px;padding:10px 18px;font-size:26px;line-height:1.3}.bookmark{margin-left:auto}.handle{font-size:13px}.mail .appbar{background:#f7f8fa}.mail-envelope{padding:18px;border-bottom:1px solid #e3e7e4}.mail-envelope h3{font-size:20px;line-height:1.3;margin:0}.mail-envelope .identity{padding:18px 0 6px}.preheader{color:#64716a;font-size:12px;margin:8px 0 0}.mail-paper{padding:28px 24px}.mail-copy{white-space:pre-wrap;overflow-wrap:anywhere;font-size:15px}.newsletter .mail-paper{background:#efeee8;padding:20px}.newsletter .mail-copy{padding:24px;background:#fff;white-space:normal}.newsletter-masthead{padding:30px 24px;background:#203e34;color:white;font:bold italic 31px Arial;letter-spacing:3px}.newsletter-masthead span{display:block;font:10px system-ui;letter-spacing:2px;margin-top:9px}.mail-paragraph{white-space:pre-wrap;margin:0 0 18px}.mail-copy h4{font-size:20px;line-height:1.2;margin:20px 0 10px}.raw-response{font-size:12px}.raw-response .draft{font-size:13px;padding:12px;background:white}.preview-note{font-size:13px;color:#596b60}@media print{article{padding:8px;break-inside:auto}.platform{border-radius:4px;font-size:10px}.social-copy,.mail-copy{font-size:10px}.identity{padding:10px}.mail-paper,.newsletter .mail-copy{padding:14px}.insta-media svg{max-height:180px}.raw-response{display:none}.mail-envelope h3{font-size:15px}}
    '''
    document = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>M6 | Canyon vs generic AI</title><style>{css}</style></head><body><main><header><div class="eyebrow">Canyon Content Workbench / M6 Evidence</div><h1>{esc(title)}</h1><p class="summary">{esc(summary)}</p><div class="strip"><span><strong>{len(data["cases"])}</strong> fixed requests</span><span><strong>2</strong> approaches</span><span><strong>1</strong> shared model</span></div><p>House-style checks passed: generic {counts['generic']}/{len(data['cases'])}; Canyon {counts['system']}/{len(data['cases'])}. These are partial formatting checks, not factual accuracy scores. Newsletter/Instagram template length is checked separately below because the production checker has no bounds for those channels.</p><p class="preview-note">Channel mockups for presentation only. Profile labels, interface controls and newsletter masthead are layout chrome; no actual posts, sends, engagement data or generated campaign images are shown. Both approaches use identical styling.</p><button onclick="window.print()">Print / save as PDF</button></header><details><summary>Method, controls and limits</summary><p>{esc(METHOD)}</p><p>{esc(RUBRIC)}</p></details>{''.join(cards)}<footer>Model: {esc(data['model'])} · UTC: {esc(data['date_utc'])} · Status: {esc(data['status'])}<br>Sources: <a href="results.json">exact prompts, outputs and source hashes</a> · <a href="comparison.md">Markdown report</a> · <a href="../knowledge_base/primary/product_specs.md">product knowledge base</a></footer></main></body></html>'''
    document = document.replace('<footer>', '<footer><p>Reviewer: ' + esc(reviewer) + '</p>')
    (folder / 'comparison.html').write_text(document, encoding='utf-8')
    (folder / 'comparison.md').write_text('\n'.join(md), encoding='utf-8')
