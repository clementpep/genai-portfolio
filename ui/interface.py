"""
Gradio interface construction for the portfolio application.

This module handles the creation of the entire Gradio interface including
navigation, carousel, timeline, and chat components.
"""

import gradio as gr
import os
from typing import Tuple

from config.settings import COLORS, LOGOS_PATH
from config.css import get_custom_css
from core.data_loader import portfolio_loader
from core.agent import agent_manager
from ui.components import (
    generate_card_html,
    generate_header_html,
    generate_stats_html,
    generate_footer_html,
)
from utils.helpers import embed_image_base64


def create_interface() -> gr.Blocks:
    """
    Create the main Gradio interface with all components.

    Returns:
        gr.Blocks: Configured Gradio interface ready to launch
    """
    portfolio_data = portfolio_loader.load()

    with gr.Blocks(
        css=get_custom_css(),
        theme=gr.themes.Soft(
            primary_hue=gr.themes.colors.emerald,
            secondary_hue=gr.themes.colors.stone,
            neutral_hue=gr.themes.colors.slate,
            font=[gr.themes.GoogleFont("Inter"), "system-ui", "sans-serif"],
        ),
        title="Clément Peponnet - Portfolio GenAI & Agentic",
    ) as app:

        # State variables for carousel navigation
        category_state = gr.State("experiences")

        # Get the most recent experience for initial display
        experiences = portfolio_data.get("experiences", [])
        initial_index = _get_most_recent_index(experiences)
        index_state = gr.State(initial_index)

        # Header
        gr.HTML(generate_header_html())

        # Stats section
        gr.HTML(generate_stats_html(portfolio_data))

        # Navigation tabs
        with gr.Row():
            exp_btn = gr.Button("🚀 Expériences", elem_classes="nav-button")
            cert_btn = gr.Button("🏆 Certifications", elem_classes="nav-button")
            skills_btn = gr.Button("💡 Expertise & Skills", elem_classes="nav-button")
            edu_btn = gr.Button("🎓 Études", elem_classes="nav-button")

        # Carousel display
        gr.HTML('<div style="margin: 3rem 0 1rem 0;"></div>')

        with gr.Row(elem_classes="carousel-wrapper"):
            prev_btn = gr.Button("◀", elem_classes="carousel-nav-btn", scale=1)
            with gr.Column(scale=6, elem_classes="carousel-container"):
                initial_experience = (
                    experiences[initial_index]
                    if experiences
                    else portfolio_data["experiences"][0]
                )
                carousel_html = gr.HTML(
                    generate_card_html(initial_experience, "experiences")
                )
            next_btn = gr.Button("▶", elem_classes="carousel-nav-btn", scale=1)

        # Timeline HTML display
        timeline_html = gr.HTML()

        # Create hidden buttons for timeline navigation
        timeline_buttons = _create_timeline_buttons(portfolio_data)

        # Connect navigation event handlers
        _setup_navigation_handlers(
            exp_btn,
            cert_btn,
            skills_btn,
            edu_btn,
            prev_btn,
            next_btn,
            carousel_html,
            timeline_html,
            category_state,
            index_state,
            timeline_buttons,
        )

        # Initialize timeline display
        timeline_html.value = _generate_initial_timeline(experiences, initial_index)

        # Navigation instruction
        gr.HTML(
            f"""
        <p style="text-align: center; color: {COLORS['text_muted']}; font-size: 0.85rem; margin-top: 1rem;">
            💡 Cliquez sur les points de la timeline ou utilisez les flèches ◀ ▶ pour naviguer
        </p>
        """
        )

        # Chat interface
        _create_chat_interface(portfolio_data)

        # Footer
        model_info = agent_manager.get_model_info()
        gr.HTML(generate_footer_html(model_info))

    return app


def _get_most_recent_index(items: list) -> int:
    """
    Get the index of the most recent item based on date/period.

    Args:
        items: List of portfolio items

    Returns:
        int: Index of the most recent item
    """
    if not items:
        return 0

    sorted_items = sorted(
        items,
        key=lambda x: x.get("date", x.get("period", "0000")),
        reverse=True,
    )
    most_recent = sorted_items[0]
    return items.index(most_recent)


def _create_timeline_buttons(portfolio_data: dict) -> list:
    """
    Create hidden buttons for timeline navigation.

    Args:
        portfolio_data: Full portfolio data

    Returns:
        list: List of Gradio buttons
    """
    max_items = max(
        len(portfolio_data.get("experiences", [])),
        len(portfolio_data.get("skills", [])),
        len(portfolio_data.get("certifications", [])),
        len(portfolio_data.get("education", [])),
    )

    timeline_buttons = []
    with gr.Column(visible=False):
        for i in range(max_items):
            btn = gr.Button(f"Timeline {i}", elem_classes="timeline-btn")
            btn.elem_id = f"timeline-btn-{i}"
            btn.elem_attributes = {"data-timeline-index": str(i)}
            timeline_buttons.append(btn)

    return timeline_buttons


def _setup_navigation_handlers(
    exp_btn,
    cert_btn,
    skills_btn,
    edu_btn,
    prev_btn,
    next_btn,
    carousel_html,
    timeline_html,
    category_state,
    index_state,
    timeline_buttons,
):
    """
    Connect all navigation event handlers.

    Args:
        exp_btn, cert_btn, skills_btn, edu_btn: Category navigation buttons
        prev_btn, next_btn: Carousel navigation buttons
        carousel_html: Carousel display component
        timeline_html: Timeline display component
        category_state: Current category state
        index_state: Current index state
        timeline_buttons: List of timeline buttons
    """
    # Category button handlers
    exp_btn.click(
        lambda: update_category("experiences"),
        outputs=[carousel_html, timeline_html, category_state, index_state],
    )
    skills_btn.click(
        lambda: update_category("skills"),
        outputs=[carousel_html, timeline_html, category_state, index_state],
    )
    cert_btn.click(
        lambda: update_category("certifications"),
        outputs=[carousel_html, timeline_html, category_state, index_state],
    )
    edu_btn.click(
        lambda: update_category("education"),
        outputs=[carousel_html, timeline_html, category_state, index_state],
    )

    # Carousel navigation handlers
    prev_btn.click(
        lambda cat, idx: navigate_carousel(-1, cat, idx),
        inputs=[category_state, index_state],
        outputs=[carousel_html, timeline_html, index_state],
    )
    next_btn.click(
        lambda cat, idx: navigate_carousel(1, cat, idx),
        inputs=[category_state, index_state],
        outputs=[carousel_html, timeline_html, index_state],
    )

    # Timeline button handlers
    for i, btn in enumerate(timeline_buttons):
        btn.click(
            lambda idx=i: jump_to_index(idx, category_state.value),
            inputs=[category_state],
            outputs=[carousel_html, timeline_html, index_state],
        )


def _generate_initial_timeline(items: list, initial_index: int) -> str:
    """
    Generate the initial timeline HTML.

    Args:
        items: List of items for the timeline
        initial_index: Index of the initially selected item

    Returns:
        str: Timeline HTML
    """
    sorted_items = sorted(
        enumerate(items),
        key=lambda x: x[1].get("date", x[1].get("year", x[1].get("period", "0000"))),
    )

    timeline_items_html = []
    for idx, (original_index, item) in enumerate(sorted_items):
        date = item.get("date", item.get("year", item.get("period", "")))
        active_class = "active" if original_index == initial_index else ""

        timeline_items_html.append(
            f"""
        <div class="timeline-item {active_class}" 
             onclick="document.querySelector('[data-timeline-index=\\"{original_index}\\"]').click()">
            <div class="timeline-dot"></div>
            <div class="timeline-label">{date}</div>
        </div>
        """
        )

    return f'<div class="timeline">{"".join(timeline_items_html)}</div>'


def _create_chat_interface(portfolio_data: dict):
    """
    Create the chat interface section.

    Args:
        portfolio_data: Full portfolio data
    """
    wavebot_logo = embed_image_base64("logos/technologies/wavebot.png")
    wavebot_img = (
        f'<img src="{wavebot_logo}" class="wavebot-logo" alt="WaveBot" />'
        if wavebot_logo
        else "🤖"
    )

    gr.HTML(
        f"""
    <div style="margin-top: 4rem;"></div>
    <div class="chat-header">
        {wavebot_img}
        <span><span class="agent-name">PeponeAgent</span> - Un agent IA spécialisé sur mon profil</span>
    </div>
    <p style="color: {COLORS['text_secondary']}; margin-bottom: 1.5rem; font-size: 0.95rem;">
        Posez-lui vos questions sur mon profil, mes expériences GenAI & Agentic, mes compétences techniques ou demandez-lui une analyse de correspondance avec vos besoins.
    </p>
    """
    )

    chatbot_avatar = os.path.join(LOGOS_PATH, "technologies", "wavebot.png")

    with gr.Column(elem_classes="chat-container"):
        chatbot = gr.Chatbot(
            height=400,
            label="",
            avatar_images=(None, chatbot_avatar),
            bubble_full_width=False,
            show_label=False,
            elem_classes="gradio-chatbot",
        )

        with gr.Row(elem_classes="chat-input-container"):
            msg = gr.Textbox(
                placeholder="Ex: Quels projets multi-agents as-tu réalisés ?",
                label="",
                scale=10,
                lines=1,
                show_label=False,
                container=False,
                elem_id="msg-input",
            )

            send_btn = gr.Button(
                "➤",
                variant="primary",
                scale=1,
                size="md",
                elem_id="send-btn",
            )

    gr.Examples(
        examples=[
            "En quoi Clément serait adapté pour un post de tech lead GenAI ?",
            "Quelle expérience Clément a-t-il avec le MCP ?",
            "Quelles technologies GenAI maîtrise Clément ?",
        ],
        inputs=msg,
        label="Questions suggérées",
    )

    # Chat functionality using agent_manager
    msg.submit(agent_manager.chat, [msg, chatbot], [msg, chatbot])
    send_btn.click(agent_manager.chat, [msg, chatbot], [msg, chatbot])


# Navigation functions
def update_category(category: str) -> Tuple:
    """
    Update the displayed category and show the most recent item.

    Args:
        category: Category name to display

    Returns:
        Tuple: (card_html, timeline_html, category, index)
    """
    portfolio_data = portfolio_loader.load()
    items = portfolio_data.get(category, [])

    if items:
        sorted_items = sorted(
            items,
            key=lambda x: x.get("date", x.get("year", x.get("period", "0000"))),
            reverse=True,
        )
        most_recent_item = sorted_items[0]
        most_recent_index = items.index(most_recent_item)

        card = generate_card_html(most_recent_item, category)
        timeline = _generate_timeline_html(items, most_recent_index)

        return card, timeline, category, most_recent_index

    return "", "", category, 0


def navigate_carousel(direction: int, category: str, current_index: int) -> Tuple:
    """
    Navigate through carousel items.

    Args:
        direction: Direction to navigate (-1 for prev, 1 for next)
        category: Current category
        current_index: Current item index

    Returns:
        Tuple: (card_html, timeline_html, new_index)
    """
    portfolio_data = portfolio_loader.load()
    items = portfolio_data.get(category, [])

    if not items:
        return "", "", current_index

    new_index = (current_index + direction) % len(items)
    card = generate_card_html(items[new_index], category)
    timeline = _generate_timeline_html(items, new_index)

    return card, timeline, new_index


def jump_to_index(target_index: int, category: str) -> Tuple:
    """
    Jump to specific index from timeline click.

    Args:
        target_index: Index to jump to
        category: Current category

    Returns:
        Tuple: (card_html, timeline_html, target_index)
    """
    portfolio_data = portfolio_loader.load()
    items = portfolio_data.get(category, [])

    if not items or target_index >= len(items):
        return "", "", 0

    card = generate_card_html(items[target_index], category)
    timeline = _generate_timeline_html(items, target_index)

    return card, timeline, target_index


def _generate_timeline_html(items: list, active_index: int) -> str:
    """
    Generate timeline HTML with proper active state.

    Args:
        items: List of items
        active_index: Index of the active item

    Returns:
        str: Timeline HTML
    """
    sorted_for_timeline = sorted(
        enumerate(items),
        key=lambda x: x[1].get("date", x[1].get("year", x[1].get("period", "0000"))),
    )

    timeline_items_html = []
    for idx, (original_index, item) in enumerate(sorted_for_timeline):
        date = item.get("date", item.get("year", item.get("period", "")))
        active_class = "active" if original_index == active_index else ""

        timeline_items_html.append(
            f"""
        <div class="timeline-item {active_class}" 
             onclick="document.querySelector('[data-timeline-index=\\"{original_index}\\"]').click()">
            <div class="timeline-dot"></div>
            <div class="timeline-label">{date}</div>
        </div>
        """
        )

    return f'<div class="timeline">{"".join(timeline_items_html)}</div>'
