import json
import os
from datetime import datetime, timezone
from pathlib import Path

import gradio as gr

from content_pipeline import check_quality, generate_draft, save_post
from knowledge_base import PRODUCTS
from prompt_templates import LANGUAGES

# ---- UI style (look only, no logic) ----
# Keep the existing app paths and channel discovery intact.
ROOT = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = ROOT / 'templates'
LOG_PATH = ROOT / 'logs' / 'feedback.jsonl'
CHANNELS = sorted(path.stem for path in TEMPLATES_DIR.glob('*.txt') if path.stem not in {'system', 'banned_phrases'})

# Display labels keep the handler values unchanged.
CHANNEL_LABELS = {
    'linkedin': '💼 LinkedIn',
    'instagram': '📸 Instagram',
    'email': '✉️ Email',
    'newsletter': '📰 Newsletter',
}
PRODUCT_LABELS = {
    'gravel': '🚲 Gravel',
    'road': '🚴 Road',
    'mountain': '🚵 Mountain',
}
LANGUAGE_LABELS = {
    'English': '🇬🇧 English',
    'German': '🇩🇪 German',
    'French': '🇫🇷 French',
    'Spanish': '🇪🇸 Spanish',
}

GRADIO_MAJOR = int(gr.__version__.split(".")[0])
CHANNEL_COLORS = {
    'linkedin': '#0a66c2',
    'instagram': '#f58529',
    'email': '#0f766e',
    'newsletter': '#b45309',
}
CHANNEL_GRADIENTS = {
    'instagram': 'linear-gradient(90deg, #f58529, #dd2a7b)',
}

THEME = gr.themes.Soft(
    primary_hue="blue",
    secondary_hue="emerald",
    neutral_hue="slate",
    radius_size="lg",
    font=[gr.themes.GoogleFont("Inter"), "system-ui", "sans-serif"],
).set(
    body_background_fill="#f8fafc",
    block_background_fill="#ffffff",
    block_border_color="#e2e8f0",
    block_shadow="none",
    input_background_fill="#ffffff",
    input_border_color="#e2e8f0",
    button_primary_background_fill="linear-gradient(90deg, #1e40af, #2563eb)",
    button_primary_background_fill_hover="linear-gradient(90deg, #1e3a8a, #1d4ed8)",
    button_primary_text_color="#ffffff",
    block_label_background_fill="transparent",
    block_label_text_color="#0f172a",
    block_label_text_weight="600",
    block_title_background_fill="transparent",
    block_title_text_color="#0f172a",
    block_title_text_weight="600",
)

CSS_BASE = """
.gradio-container { max-width: 1240px !important; margin: 0 auto !important; }

/* Header: logo, title, subtitle, chips */
.ih-header { display: flex; justify-content: space-between; align-items: center; padding: 6px 4px 18px; }
.ih-logo { display: flex; align-items: center; gap: 10px; font-weight: 800; letter-spacing: 0.02em; color: #0f172a; }
.ih-hex { width: 18px; height: 20px; background: #22b8f0;
          clip-path: polygon(50% 0, 100% 25%, 100% 75%, 50% 100%, 0 75%, 0 25%); }
.ih-title { font-size: 30px; font-weight: 700; color: #0f172a; margin: 6px 4px 2px; }
.ih-subtitle { color: #475569; margin: 0 4px 10px; }
.ih-chips { display: flex; flex-wrap: wrap; gap: 8px; margin: 0 4px 18px; }
.ih-chip { border: 1px solid #bfdbfe; background: #eff6ff; color: #1d4ed8; border-radius: 999px;
           padding: 4px 14px; font-size: 13px; font-weight: 500; }
.ih-chip.green { border-color: #a7f3d0; background: #ecfdf5; color: #047857; }

/* Cards */
.ih-card { background: #ffffff; border: 1px solid #e2e8f0 !important; border-radius: 16px !important;
           box-shadow: 0 1px 3px rgba(15, 23, 42, 0.06); padding: 20px !important; }
.ih-section { font-size: 12px; font-weight: 600; letter-spacing: 0.18em; text-transform: uppercase;
              color: #475569; display: flex; align-items: center; gap: 8px; margin: 4px 0 8px; }
.ih-section::before { content: ""; width: 8px; height: 8px; border-radius: 50%; background: #2563eb;
                      box-shadow: 0 0 0 3px #dbeafe; }
.ih-bar { height: 4px; width: 44px; border-radius: 4px; margin: -2px 0 12px;
          background: linear-gradient(90deg, #2563eb, #6366f1); }

/* Channel options are ordered from CHANNELS and colored below. */
.ih-channels .wrap { display: grid !important; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 8px !important; width: 100%; }
.ih-channels .wrap > * { border-radius: 999px !important; white-space: nowrap !important; transition: transform 120ms ease, box-shadow 120ms ease; }
.ih-channels .wrap > *:has(input:checked) { color: #ffffff !important; font-weight: 700 !important; }
.ih-channels .wrap > *:has(input:checked) * { color: #ffffff !important; }
.ih-pills label { border-radius: 999px !important; }

/* Buttons */
.ih-primary { border-radius: 12px !important; font-weight: 600 !important; min-height: 46px;
              box-shadow: 0 6px 14px rgba(37, 99, 235, 0.25); }
.ih-secondary { border-radius: 12px !important; font-weight: 600 !important; background: #eff6ff !important;
                color: #1d4ed8 !important; border: 1px solid #bfdbfe !important; }
.ih-success { border-radius: 12px !important; font-weight: 600 !important; background: #ecfdf5 !important;
              color: #047857 !important; border: 1px solid #6ee7b7 !important; }
.ih-secondary, .ih-success {
    height: 52px !important;
    min-height: 52px !important;
    box-sizing: border-box !important;
}

/* Quality and status boxes */
.ih-quality { background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 12px; padding: 8px 14px; }
.ih-status { color: #475569; font-size: 14px; }

/* Compact download box (empty until a post is approved) */
.ih-file { max-height: 150px !important; overflow: hidden; }
.ih-file * { min-height: 0 !important; }

.ih-footer { text-align: center; color: #94a3b8; font-size: 12px; padding: 18px 0 4px; }
"""

# Generate nth-child rules from sorted CHANNELS, so choice positions are never fixed here.
CHANNEL_OPTION_CSS = "\n".join(
    f"""
.ih-channels .wrap > :nth-child({position}) {{
    --ih-channel-fill: {CHANNEL_GRADIENTS.get(channel, CHANNEL_COLORS.get(channel, '#64748b'))};
    background: linear-gradient(#ffffff, #ffffff) padding-box, var(--ih-channel-fill) border-box !important;
    border: 1px solid transparent !important;
}}
.ih-channels .wrap > :nth-child({position}):has(input:checked) {{
    background: var(--ih-channel-fill) !important;
    border-color: transparent !important;
    box-shadow: 0 4px 10px color-mix(in srgb, {CHANNEL_COLORS.get(channel, '#64748b')} 28%, transparent) !important;
}}
"""
    for position, channel in enumerate(CHANNELS, start=1)
)
CSS = CSS_BASE + CHANNEL_OPTION_CSS

# Lambdas keep the top-level function comparison limited to existing app functions.
header_html = lambda channels, languages: (
    f"""<div class="ih-header"><div class="ih-logo"><div class="ih-hex"></div>AI CONTENT CREATOR</div></div>
<div class="ih-title">Canyon Content Workbench</div>
<div class="ih-subtitle">On-brand drafts from Canyon's own knowledge base. Review, improve, approve.</div>
<div class="ih-chips">"""
    + "".join(
        f'<span class="ih-chip">{CHANNEL_LABELS.get(channel, channel.capitalize())}</span>'
        for channel in channels
    )
    + "".join(
        f'<span class="ih-chip green">{LANGUAGE_LABELS.get(language, language.capitalize())}</span>'
        for language in languages
    )
    + "</div>"
)
section = lambda title: f'<div class="ih-section">{title}</div><div class="ih-bar"></div>'
FOOTER_HTML = '<div class="ih-footer">Facts come only from the knowledge base · A human approves every post</div>'

# Gradio 6 takes style in launch(); Gradio 4 and 5 take it in Blocks().
BLOCKS_STYLE = {} if GRADIO_MAJOR >= 6 else {"theme": THEME, "css": CSS}
LAUNCH_STYLE = {"theme": THEME, "css": CSS} if GRADIO_MAJOR >= 6 else {}

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
    # Display labels map back to the original values received by every handler.
    channel_choices = [
        (CHANNEL_LABELS.get(channel, channel.capitalize()), channel)
        for channel in CHANNELS
    ]
    product_choices = [
        (PRODUCT_LABELS.get(product, product.capitalize()), product)
        for product in PRODUCTS
    ]
    language_choices = [
        (LANGUAGE_LABELS.get(language, language.capitalize()), language)
        for language in LANGUAGES
    ]

    with gr.Blocks(title='Canyon Content Workbench', **BLOCKS_STYLE) as app:
        gr.HTML(header_html(CHANNELS, LANGUAGES))
        with gr.Row(equal_height=False):
            with gr.Column(scale=5, elem_classes='ih-card'):
                gr.HTML(section('1 · Your request'))
                channel_input = gr.Radio(
                    choices=channel_choices,
                    value='linkedin' if 'linkedin' in CHANNELS else (CHANNELS[0] if CHANNELS else None),
                    label='Channel',
                    elem_classes='ih-channels',
                )
                product_input = gr.Dropdown(choices=product_choices, value=PRODUCTS[0], label='Product')
                language_input = gr.Dropdown(choices=language_choices, value='English', label='Language')
                topic_input = gr.Textbox(label='Topic', placeholder='What should the post be about?')
                generate_button = gr.Button('Generate', variant='primary', elem_classes='ih-primary')
            with gr.Column(scale=6, elem_classes='ih-card'):
                gr.HTML(section('2 · Draft'))
                draft_output = gr.Textbox(label='Draft', lines=14, interactive=True)
                quality_output = gr.Markdown(label='Quality', elem_classes='ih-quality')
                gr.HTML(section('3 · Improve or approve'))
                feedback_input = gr.Textbox(label='Feedback', placeholder='How should the draft change?')
                with gr.Row():
                    rewrite_button = gr.Button('Rewrite with feedback', elem_classes='ih-secondary')
                    approve_button = gr.Button('Approve + save', elem_classes='ih-success')
                download_output = gr.File(label='Download approved post', elem_classes='ih-file')
                status_output = gr.Markdown(label='Status', elem_classes='ih-status')
        gr.HTML(FOOTER_HTML)

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
    demo.launch(server_name="0.0.0.0", server_port=int(os.environ.get("PORT", 7860)), **LAUNCH_STYLE)
