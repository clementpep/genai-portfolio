"""
User interface module.
Contains Gradio interface construction and HTML components.
"""

from .interface import create_interface
from .components import (
    generate_card_html,
    generate_skills_card_html,
    generate_header_html,
    generate_stats_html,
    generate_footer_html,
)

__all__ = [
    "create_interface",
    "generate_card_html",
    "generate_skills_card_html",
    "generate_header_html",
    "generate_stats_html",
    "generate_footer_html",
]
