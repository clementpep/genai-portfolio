"""
SmolAgent tools for portfolio interaction.

This module contains all the agent tools that allow querying Clement's portfolio data,
including experiences, skills, certifications, education, and profile matching analysis.
"""

from typing import Optional
from smolagents import tool
from core.data_loader import portfolio_loader


@tool
def list_clement_experiences(
    technology: Optional[str] = None,
    client: Optional[str] = None,
    sector: Optional[str] = None,
) -> str:
    """
    List Clement's professional experiences with optional filters.

    Args:
        technology: Filter by technology (e.g., 'MCP', 'Azure', 'SmolAgent')
        client: Filter by client name
        sector: Filter by sector (e.g., 'Transport', 'Digital Transformation')

    Returns:
        Formatted string with matching experiences
    """
    experiences = portfolio_loader.get_experiences()
    results = []

    for exp in experiences:
        match = True

        if technology and match:
            if not any(
                technology.lower() in tech.lower()
                for tech in exp.get("technologies", [])
            ):
                match = False

        if client and match:
            if client.lower() not in exp.get("client", "").lower():
                match = False

        if sector and match:
            if sector.lower() not in exp.get("sector", "").lower():
                match = False

        if match:
            results.append(exp)

    if not results:
        return "No experiences found matching the criteria."

    output = f"Found {len(results)} experience(s):\n\n"
    for exp in results:
        output += f"**{exp['title']}** at {exp['client']} ({exp['duration']})\n"
        output += f"Description: {exp['description'][:180]}...\n"
        output += f"Technologies: {', '.join(exp['technologies'][:5])}\n"
        output += f"Impact: {exp['impact']}\n\n"

    return output


@tool
def list_clement_skills(category: Optional[str] = None) -> str:
    """
    Get Clement's technical skills by category.

    Args:
        category: Filter by skill category (e.g., 'Agents', 'GenAI', 'Web')

    Returns:
        Formatted string with skills
    """
    skills_data = portfolio_loader.get_skills()

    if category:
        matching = [s for s in skills_data if category.lower() in s["category"].lower()]
        if matching:
            skill_set = matching[0]
            return f"**{skill_set['category']}**:\n• " + "\n• ".join(
                skill_set["skills"]
            )
        return f"No skill category found matching '{category}'"

    output = "Clement's Technical Skills:\n\n"
    for skill_set in skills_data:
        output += f"**{skill_set['category']}** {skill_set.get('icon', '')}\n"
        output += "• " + "\n• ".join(skill_set["skills"][:4]) + "\n\n"

    return output


@tool
def list_clement_certifications() -> str:
    """Get all of Clement's certifications"""
    certs = portfolio_loader.get_certifications()

    output = "Clement's Certifications:\n\n"
    for cert in certs:
        output += f"• **{cert['name']}** - {cert['issuer']} ({cert['year']})\n"
        output += f"  {cert['description']}\n\n"

    return output


@tool
def list_clement_education() -> str:
    """Get Clement's educational background"""
    education = portfolio_loader.get_education()

    output = "Clement's Education:\n\n"
    for edu in education:
        output += f"**{edu['school']}** - {edu['degree']} ({edu['year']})\n"
        if "location" in edu:
            output += f"  Location: {edu['location']}\n"
        if "achievement" in edu:
            output += f"  Achievement: {edu['achievement']}\n"
        if "focus" in edu:
            output += f"  Focus: {edu['focus']}\n"
        output += "\n"

    return output


# List of all available tools for easy reference
AVAILABLE_TOOLS = [
    list_clement_experiences,
    list_clement_skills,
    list_clement_certifications,
    list_clement_education,
]


def get_tools_description() -> str:
    """
    Generate a formatted description of all available tools for system prompts.

    Returns:
        str: Formatted string describing all tools
    """
    return """
Available Tools:
1. list_clement_experiences(technology, client, sector) - Search professional experiences with filters
2. list_clement_skills(category) - Get technical skills by category
3. list_clement_certifications() - List all certifications
4. list_clement_education() - Get educational background
"""
