"""
Utility functions for the portfolio application.

This module contains helper functions for image encoding and other utilities.
"""

import os
import base64
from typing import Optional


def embed_image_base64(rel_path: str, base_dir: Optional[str] = None) -> Optional[str]:
    """
    Convert a local image file into a base64-embedded data URI string.

    Args:
        rel_path: Relative path to the image from repo root
        base_dir: Base directory for resolving the relative path (optional)

    Returns:
        Optional[str]: Base64 data URI string or None if file not found

    Example:
        >>> logo = embed_image_base64("logos/clients/wavestone.png")
        >>> if logo:
        ...     html = f'<img src="{logo}" alt="Logo" />'
    """
    if base_dir is None:
        base_dir = os.path.dirname(os.path.dirname(__file__))

    abs_path = os.path.join(base_dir, rel_path)

    if not os.path.exists(abs_path):
        print(f"Warning: Image not found at {abs_path}")
        return None

    try:
        with open(abs_path, "rb") as f:
            encoded = base64.b64encode(f.read()).decode("utf-8")

        # Determine MIME type based on file extension
        ext = os.path.splitext(rel_path)[1].lower()
        mime_map = {
            ".png": "image/png",
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".svg": "image/svg+xml",
            ".webp": "image/webp",
            ".gif": "image/gif",
        }
        mime = mime_map.get(ext, "image/png")

        return f"data:{mime};base64,{encoded}"

    except Exception as e:
        print(f"Error encoding image {rel_path}: {e}")
        return None


def get_tech_logo_paths(tech_name: str) -> list:
    """
    Generate possible paths for a technology logo.

    Args:
        tech_name: Name of the technology

    Returns:
        list: List of possible file paths to try
    """
    tech_base = (
        tech_name.lower()
        .replace(" ", "_")
        .replace("-", "_")
        .replace("/", "_")
        .replace(".", "_")
    )

    return [
        f"logos/technologies/{tech_base}.png",
        f"logos/technologies/{tech_base}.svg",
        f"logos/{tech_base}.png",
        f"logos/{tech_base}.svg",
    ]


def format_duration(duration: str) -> str:
    """
    Format a duration string for display.

    Args:
        duration: Duration string (e.g., "12 mois", "3 jours")

    Returns:
        str: Formatted duration with icon
    """
    return f"📅 {duration}"


def format_impact(impact: str) -> str:
    """
    Format an impact string for display.

    Args:
        impact: Impact description

    Returns:
        str: Formatted impact with icon
    """
    return f"🎯 {impact}"


def format_achievement(achievement: str) -> str:
    """
    Format an achievement string for display.

    Args:
        achievement: Achievement description

    Returns:
        str: Formatted achievement with icon
    """
    return f"🏅 {achievement}"
