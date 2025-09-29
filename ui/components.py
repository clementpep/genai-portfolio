"""
UI component generation for the portfolio application.

This module handles the generation of HTML components for displaying
portfolio items like experience cards, skill cards, certifications, etc.
"""

from typing import Dict
from config.settings import TECH_LINKS
from utils.helpers import embed_image_base64, get_tech_logo_paths


def generate_card_html(item: Dict, category: str) -> str:
    """
    Generate HTML for a portfolio item card with improved logo handling.

    Args:
        item: Portfolio item data dictionary
        category: Category type (experiences, skills, certifications, education)

    Returns:
        str: Generated HTML for the card
    """
    # Special handling for skills category
    if category == "skills":
        return generate_skills_card_html(item)

    # Extract basic information
    icon = item.get("icon", "")
    title = item.get("title", "")
    name = item.get("name", "")  # For certifications
    subtitle = item.get("client", item.get("issuer", item.get("school", "")))
    location = item.get("location", "")  # For education
    description = item.get("description", item.get("focus", ""))
    duration = item.get("duration", item.get("year", ""))
    techs = item.get("technologies", item.get("skills", []))
    impact = item.get("impact", "")
    achievement = item.get("achievement", "")

    # Logo handling with better error management
    client_logo_url = None
    if "client_logo" in item and item["client_logo"]:
        logo_data = embed_image_base64(item["client_logo"])
        if logo_data:
            client_logo_url = logo_data

    # Logo HTML - either image or emoji fallback
    if client_logo_url:
        logo_html = f'<img src="{client_logo_url}" alt="{subtitle}" />'
    else:
        logo_html = f'<div style="font-size: 2.2rem;">{icon or "📌"}</div>'

    # Generate tech badges with logos and clickable links
    tech_badges_html = _generate_tech_badges(techs)

    # Build title section with improved layout
    title_section = _generate_title_section(category, title, name, subtitle, location)

    # Build meta information
    meta_html = _generate_meta_section(duration, impact, achievement)

    # Return final card HTML
    return f"""
    <div class="card">
        <div class="card-header">
            <div class="card-logo">{logo_html}</div>
            {title_section}
        </div>
        <div class="card-content">{description}</div>
        {meta_html}
        {tech_badges_html}
    </div>
    """


def generate_skills_card_html(skill_category: Dict) -> str:
    """
    Generate HTML specifically for skills cards.

    Args:
        skill_category: Skills category data dictionary

    Returns:
        str: Generated HTML for skills card
    """
    category = skill_category.get("category", "")
    icon = skill_category.get("icon", "💡")
    skills = skill_category.get("skills", [])

    skills_html = ""
    for skill in skills:
        skills_html += f"<li>{skill}</li>"

    return f"""
    <div class="card">
        <div class="category-title">
            <span class="category-icon">{icon}</span>
            {category}
        </div>
        <div class="card-content">
            <ul class="skills-list">
                {skills_html}
            </ul>
        </div>
    </div>
    """


def _generate_tech_badges(techs: list) -> str:
    """
    Generate HTML for technology badges with logos and links.

    Args:
        techs: List of technology names

    Returns:
        str: HTML string containing all tech badges
    """
    tech_badges_html = []

    for tech in techs[:6]:
        tech_name = tech if isinstance(tech, str) else str(tech)

        # Try multiple possible paths for tech logos
        logo_data = None
        logo_paths = get_tech_logo_paths(tech_name)

        for path in logo_paths:
            logo_data = embed_image_base64(path)
            if logo_data:
                break

        # Get link for technology
        tech_link = TECH_LINKS.get(tech_name.lower(), "#")

        if logo_data:
            # Logo with link if available
            if tech_link != "#":
                tech_badges_html.append(
                    f'<a href="{tech_link}" target="_blank" class="tech-badge" title="{tech_name} - Click to visit">'
                    f'<img src="{logo_data}" alt="{tech_name}" /></a>'
                )
            else:
                tech_badges_html.append(
                    f'<span class="tech-badge" title="{tech_name}"><img src="{logo_data}" alt="{tech_name}" /></span>'
                )
        else:
            # Fallback: show text
            if tech_link != "#":
                tech_badges_html.append(
                    f'<a href="{tech_link}" target="_blank" class="tech-badge" title="{tech_name} - Click to visit">{tech_name}</a>'
                )
            else:
                tech_badges_html.append(
                    f'<span class="tech-badge" title="{tech_name}">{tech_name}</span>'
                )

    # Join all tech badges in centered container
    if tech_badges_html:
        return f'<div class="tech-badges-container">{"".join(tech_badges_html)}</div>'
    return ""


def _generate_title_section(
    category: str, title: str, name: str, subtitle: str, location: str
) -> str:
    """
    Generate the title section of a card based on category.

    Args:
        category: Card category
        title: Main title
        name: Name (for certifications)
        subtitle: Subtitle text
        location: Location (for education)

    Returns:
        str: HTML for title section
    """
    if category == "certifications" and name:
        return f"""
            <div style="flex: 1;">
                <div class="card-subtitle">{subtitle}</div>
                <div class="card-title" style="margin-top: 0.5rem;">{name}</div>
            </div>
        """
    elif category == "education":
        location_html = (
            f'<div class="card-location">{location}</div>' if location else ""
        )
        subtitle_html = (
            f'<div class="card-subtitle">{subtitle}</div>' if subtitle else ""
        )
        return f"""
            <div style="flex: 1;">
                <div class="card-title">{title}</div>
                {subtitle_html}
                {location_html}
            </div>
        """
    else:
        subtitle_html = (
            f'<div class="card-subtitle">{subtitle}</div>' if subtitle else ""
        )
        return f"""
            <div style="flex: 1;">
                <div class="card-title">{title}</div>
                {subtitle_html}
            </div>
        """


def _generate_meta_section(duration: str, impact: str, achievement: str) -> str:
    """
    Generate the metadata section of a card.

    Args:
        duration: Duration or year
        impact: Impact description
        achievement: Achievement description

    Returns:
        str: HTML for meta section
    """
    meta_html = ""

    if duration:
        meta_html += f'<div class="card-meta">📅 {duration}</div>'
    if impact:
        meta_html += f'<div class="card-meta">🎯 {impact}</div>'
    if achievement:
        meta_html += f'<div class="card-meta">🏅 {achievement}</div>'

    return meta_html


def generate_header_html() -> str:
    """
    Generate the header HTML with social links.

    Returns:
        str: HTML for the header section
    """
    return """
        <div class="premium-header">
            <h1>Clément Peponnet</h1>
            <p>Portfolio GenAI & Agentic</p>
            <p style="margin-top: 0.5rem; opacity: 0.9;">
                Expert GenAI | Tech Lead | Azure AI Engineer
            </p>
            <p style="margin-top: 1rem; font-size: 1rem; opacity: 0.85;">
                Convaincu par le potentiel de la GenAI, de l'Agentic AI, et du MCP<br>
                j'accompagne mes clients du prototypage à l'industrialisation, pour maximiser l'impact métier de ces technologies.
            </p>
            <div class="social-links">
                <a href="https://www.linkedin.com/in/clément-peponnet-b26906194" target="_blank" class="social-link">
                    <svg width="20" height="20" fill="currentColor" viewBox="0 0 24 24">
                        <path d="M19 0h-14c-2.761 0-5 2.239-5 5v14c0 2.761 2.239 5 5 5h14c2.762 0 5-2.239 5-5v-14c0-2.761-2.238-5-5-5zm-11 19h-3v-11h3v11zm-1.5-12.268c-.966 0-1.75-.79-1.75-1.764s.784-1.764 1.75-1.764 1.75.79 1.75 1.764-.783 1.764-1.75 1.764zm13.5 12.268h-3v-5.604c0-3.368-4-3.113-4 0v5.604h-3v-11h3v1.765c1.396-2.586 7-2.777 7 2.476v6.759z"/>
                    </svg>
                    LinkedIn
                </a>
                <a href="https://github.com/clementpep" target="_blank" class="social-link">
                    <svg width="20" height="20" fill="currentColor" viewBox="0 0 24 24">
                        <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
                    </svg>
                    GitHub
                </a>
            </div>
        </div>
    """


def generate_stats_html(portfolio_data: Dict) -> str:
    """
    Generate the statistics section HTML.

    Args:
        portfolio_data: Full portfolio data dictionary

    Returns:
        str: HTML for the stats section
    """
    num_experiences = len(portfolio_data.get("experiences", []))
    num_certifications = len(portfolio_data.get("certifications", []))

    return f"""
        <div class="stats-container">
            <div class="stat-card">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">🚀</div>
                <div class="stat-value">{num_experiences}</div>
                <div class="stat-label">Projets GenAI majeurs</div>
            </div>
            <div class="stat-card">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">🏆</div>
                <div class="stat-value">{num_certifications}</div>
                <div class="stat-label">Certifications AI</div>
            </div>
            <div class="stat-card">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">🥇</div>
                <div class="stat-value">2</div>
                <div class="stat-label">Hackathons</div>
            </div>
            <div class="stat-card">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">💼</div>
                <div class="stat-value">50+</div>
                <div class="stat-label">Pitchs GenAI</div>
            </div>
        </div>
    """


def generate_footer_html(model_info: str) -> str:
    """
    Generate the footer HTML with model information.

    Args:
        model_info: Information about the active model

    Returns:
        str: HTML for the footer
    """
    from config.settings import COLORS

    return f"""
        <div class="footer">
            <p style="color: {COLORS['text_primary']}; font-size: 1rem; font-weight: 500; margin-bottom: 0.5rem;">
                © 2025 Clément Peponnet - Portfolio GenAI & Agentic
            </p>
            <p style="color: {COLORS['text_secondary']}; font-size: 0.875rem;">
                Built with Gradio & {model_info}
            </p>
        </div>
    """
