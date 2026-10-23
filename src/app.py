import json
import os
from datetime import datetime, timezone
from pathlib import Path

import gradio as gr

from content_pipeline import check_quality, generate_draft, save_post
from knowledge_base import PRODUCTS
from prompt_templates import LANGUAGES

ROOT = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = ROOT / 'templates'
LOG_PATH = ROOT / 'logs' / 'feedback.jsonl'
CHANNELS = sorted(path.stem for path in TEMPLATES_DIR.glob('*.txt') if path.stem not in {'system', 'banned_phrases'})


def log_feedback(action, channel, product, language, topic, feedback, quality):
    # Logging is best effort and must not interrupt a request.
    try:
        LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
        record = {
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'action': action,
            'channel': channel,
            'product': product,
            'language': language,
            'topic': topic,
            'feedback_text': feedback,
            'quality_ok': bool(quality.get('ok', False)) if quality else False,
            'word_count': quality.get('word_count', 0) if quality else 0,
        }
        with LOG_PATH.open('a', encoding='utf-8') as log_file:
            log_file.write(json.dumps(record, ensure_ascii=False) + '\n')
    except Exception:
        pass


def quality_markdown(quality):
    # Show OK or only the checks that need attention.
    problems = []
    if quality['banned_phrases_found']:
        problems.append('Banned phrases: ' + ', '.join(quality['banned_phrases_found']))
    if quality['em_dashes']:
        problems.append(f"Em dashes: {quality['em_dashes']}")
    if quality['markdown_symbols']:
        problems.append(f"Markdown: {quality['markdown_symbols']} formatting markers")
    if quality['emoji_count'] > 2:
        problems.append(f"Emojis: {quality['emoji_count']} (limit 2)")
    if quality['hashtag_count'] > 3:
        problems.append(f"Hashtags: {quality['hashtag_count']} (limit 3)")
    if not quality['word_count_ok']:
        problems.append(f"Word count: {quality['word_count']} (outside the channel range)")
    if not problems:
        return f"- OK ({quality['word_count']} words)"
    return '\n'.join(f'- {problem}' for problem in problems)


def generate_handler(channel, product, language, topic):
    # Generate a draft and report its quality.
    if not topic or not topic.strip():
        message = 'Enter a topic before generating a draft.'
        log_feedback('Generate', channel, product, language, topic or '', '', None)
        return '', '', '', message
    try:
        draft = generate_draft(channel, product, topic, language)
        quality = check_quality(draft, channel)
        log_feedback('Generate', channel, product, language, topic, '', quality)
        return draft, quality_markdown(quality), '', 'Draft generated. Review and edit it before approving.'
    except (ValueError, ConnectionError) as error:
        log_feedback('Generate', channel, product, language, topic, '', None)
        return '', '', '', str(error)


def rewrite_handler(channel, product, language, topic, feedback):
    # Regenerate the draft using the marketer's feedback.
    if not topic or not topic.strip():
        message = 'Enter a topic before rewriting the draft.'
        log_feedback('Rewrite', channel, product, language, topic or '', feedback or '', None)
        return '', '', '', message
    if not feedback or not feedback.strip():
        message = 'Enter feedback before rewriting the draft.'
        log_feedback('Rewrite', channel, product, language, topic, feedback or '', None)
        return '', '', '', message
    try:
        draft = generate_draft(channel, product, topic, language, feedback=feedback)
        quality = check_quality(draft, channel)
        log_feedback('Rewrite', channel, product, language, topic, feedback, quality)
        return draft, quality_markdown(quality), '', 'Draft rewritten. Review and edit it before approving.'
    except (ValueError, ConnectionError) as error:
        log_feedback('Rewrite', channel, product, language, topic, feedback, None)
        return '', '', '', str(error)


def approve_handler(draft, channel, product, language, topic):
    # Save exactly the current editable draft and return its download path.
    if not draft or not draft.strip():
        message = 'There is no draft to approve. Generate a draft first.'
        log_feedback('Approve', channel, product, language, topic or '', '', None)
        return None, '', message
    try:
        quality = check_quality(draft, channel)
        output_path = save_post(draft, channel, product, topic, language, quality)
        log_feedback('Approve', channel, product, language, topic, '', quality)
        return output_path, quality_markdown(quality), f"Approved post saved: {output_path}"
    except (ValueError, ConnectionError) as error:
        log_feedback('Approve', channel, product, language, topic, '', None)
        return None, '', str(error)


def build_app():
    # Keep the request controls and result tools side by side.
    with gr.Blocks(title='Canyon Content Workbench') as app:
        gr.Markdown('# Canyon Content Workbench')
        with gr.Row():
            with gr.Column():
                channel_input = gr.Radio(
                    choices=CHANNELS,
                    value='linkedin' if 'linkedin' in CHANNELS else (CHANNELS[0] if CHANNELS else None),
                    label='Channel',
                )
                product_input = gr.Dropdown(choices=PRODUCTS, value=PRODUCTS[0], label='Product')
                language_input = gr.Dropdown(choices=LANGUAGES, value='English', label='Language')
                topic_input = gr.Textbox(label='Topic', placeholder='What should the post be about?')
                generate_button = gr.Button('Generate', variant='primary')
            with gr.Column():
                draft_output = gr.Textbox(label='Draft', lines=14, interactive=True)
                quality_output = gr.Markdown(label='Quality')
                feedback_input = gr.Textbox(label='Feedback', placeholder='How should the draft change?')
                rewrite_button = gr.Button('Rewrite with feedback')
                approve_button = gr.Button('Approve + save')
                download_output = gr.File(label='Download approved post')
                status_output = gr.Markdown(label='Status')

        request_inputs = [channel_input, product_input, language_input, topic_input]
        request_outputs = [draft_output, quality_output, feedback_input, status_output]
        generate_button.click(generate_handler, inputs=request_inputs, outputs=request_outputs)
        rewrite_button.click(
            rewrite_handler,
            inputs=request_inputs + [feedback_input],
            outputs=request_outputs,
        )
        approve_button.click(
            approve_handler,
            inputs=[draft_output, channel_input, product_input, language_input, topic_input],
            outputs=[download_output, quality_output, status_output],
        )
    return app


demo = build_app()

if __name__ == '__main__':
    demo.launch(server_name="0.0.0.0", server_port=int(os.environ.get("PORT", 7860)))
