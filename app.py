"""
Premium GenAI Portfolio Application
Deployed on Hugging Face Spaces with Gradio
Enhanced with dark green/cream/gray premium design
"""

import gradio as gr
import yaml
import os
from typing import List, Dict, Optional, Tuple
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Determine which LLM to use based on environment
USE_HF_MODEL = os.getenv("USE_HF_MODEL", "true").lower() == "true"

if USE_HF_MODEL:
    from smolagents import CodeAgent, InferenceClientModel, tool
else:
    from litellm import completion


# Load portfolio data from YAML file
def load_portfolio_data() -> Dict:
    """Load portfolio data from YAML configuration file"""
    with open("portfolio_data.yaml", "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


PORTFOLIO = load_portfolio_data()

# Premium color scheme - Dark Green, Cream, Gray
COLORS = {
    "primary": "#2D5016",  # Dark forest green
    "primary_light": "#4A7C2E",  # Lighter forest green
    "secondary": "#F5F5DC",  # Cream/Beige
    "accent": "#8FBC8F",  # Sage green
    "background": "#1A1A1A",  # Very dark gray
    "surface": "#2C2C2C",  # Dark gray surface
    "surface_elevated": "#3A3A3A",  # Elevated surface
    "text_primary": "#F5F5DC",  # Cream text
    "text_secondary": "#B8B8B8",  # Light gray text
    "gradient_start": "#2D5016",
    "gradient_end": "#4A7C2E",
    "border": "#4A4A4A",
}

# Custom CSS for premium stone-textured design
CUSTOM_CSS = f"""
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=Inter:wght@300;400;500;600&display=swap');

.gradio-container {{
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    background: 
        linear-gradient(90deg, 
            rgba(42, 42, 42, 0.05) 1px, 
            transparent 1px),
        linear-gradient(
            rgba(42, 42, 42, 0.05) 1px, 
            transparent 1px),
        linear-gradient(180deg, {COLORS['background']} 0%, #0f0f0f 100%) !important;
    background-size: 60px 60px, 60px 60px, 100% 100% !important;
    max-width: 1400px !important;
    margin: 0 auto !important;
    padding: 2rem !important;
}}

.premium-header {{
    background: linear-gradient(135deg, {COLORS['gradient_start']}, {COLORS['gradient_end']});
    padding: 3rem 2rem;
    border-radius: 24px;
    text-align: center;
    margin-bottom: 3rem;
    box-shadow: 0 20px 60px rgba(45, 80, 22, 0.4);
    border: 1px solid {COLORS['primary_light']};
}}

.premium-header h1 {{
    color: {COLORS['secondary']};
    font-family: 'Playfair Display', serif;
    font-size: 3rem;
    font-weight: 700;
    margin-bottom: 0.5rem;
    letter-spacing: -0.02em;
}}

.premium-header p {{
    color: {COLORS['secondary']};
    font-size: 1.1rem;
    font-weight: 400;
    opacity: 0.95;
}}

.social-links {{
    display: flex;
    justify-content: center;
    gap: 1.5rem;
    margin-top: 1.5rem;
}}

.social-link {{
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.6rem 1.2rem;
    background: rgba(245, 245, 220, 0.1);
    border: 1px solid {COLORS['secondary']};
    border-radius: 12px;
    color: {COLORS['secondary']};
    text-decoration: none;
    transition: all 0.3s ease;
    font-weight: 500;
}}

.social-link:hover {{
    background: {COLORS['secondary']};
    color: {COLORS['primary']};
    transform: translateY(-2px);
    box-shadow: 0 8px 20px rgba(245, 245, 220, 0.3);
}}

.carousel-container {{
    position: relative;
    min-height: 500px;
    padding: 2rem 0;
    display: flex;
    align-items: center;
    justify-content: center;
    perspective: 1000px;
}}

.card {{
    background: {COLORS['surface_elevated']};
    border-radius: 24px;
    padding: 2.5rem;
    width: 100%;
    max-width: 650px;
    min-height: 420px;
    box-shadow: 0 15px 50px rgba(0, 0, 0, 0.5);
    border: 2px solid {COLORS['border']};
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
}}

.card:hover {{
    transform: translateY(-8px);
    box-shadow: 0 25px 70px rgba(45, 80, 22, 0.3);
    border-color: {COLORS['primary_light']};
}}

.card-header {{
    display: flex;
    align-items: center;
    gap: 1.5rem;
    margin-bottom: 1.5rem;
    padding-bottom: 1.5rem;
    border-bottom: 1px solid {COLORS['border']};
}}

.card-logo {{
    width: 80px;
    height: 80px;
    border-radius: 16px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: linear-gradient(135deg, {COLORS['gradient_start']}, {COLORS['gradient_end']});
    font-size: 2.5rem;
    box-shadow: 0 8px 20px rgba(45, 80, 22, 0.3);
}}

.card-title {{
    font-family: 'Playfair Display', serif;
    font-size: 1.75rem;
    font-weight: 600;
    color: {COLORS['text_primary']};
    margin-bottom: 0.5rem;
}}

.card-subtitle {{
    color: {COLORS['primary_light']};
    font-weight: 500;
    font-size: 1rem;
}}

.card-content {{
    color: {COLORS['text_secondary']};
    line-height: 1.7;
    margin-bottom: 1.5rem;
    font-size: 0.95rem;
}}

.card-meta {{
    display: flex;
    align-items: center;
    gap: 0.5rem;
    color: {COLORS['text_secondary']};
    font-size: 0.9rem;
    margin-bottom: 1.5rem;
}}

.tech-badge {{
    display: inline-block;
    padding: 0.5rem 1rem;
    background: rgba(45, 80, 22, 0.2);
    border: 1px solid {COLORS['primary_light']};
    border-radius: 16px;
    color: {COLORS['accent']};
    font-size: 0.85rem;
    font-weight: 500;
    margin: 0.3rem;
    transition: all 0.3s ease;
}}

.tech-badge:hover {{
    background: {COLORS['primary']};
    color: {COLORS['secondary']};
    transform: scale(1.05);
}}

.timeline {{
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 3rem;
    padding: 2rem 0;
    position: relative;
    margin-top: 2rem;
}}

.timeline::before {{
    content: '';
    position: absolute;
    top: 50%;
    left: 10%;
    right: 10%;
    height: 2px;
    background: linear-gradient(90deg, 
        transparent, 
        {COLORS['primary']}, 
        {COLORS['primary_light']},
        {COLORS['primary']}, 
        transparent);
    transform: translateY(-50%);
}}

.timeline-item {{
    display: flex;
    flex-direction: column;
    align-items: center;
    cursor: pointer;
    transition: all 0.3s ease;
    position: relative;
    z-index: 1;
}}

.timeline-dot {{
    width: 18px;
    height: 18px;
    border-radius: 50%;
    background: {COLORS['surface']};
    border: 3px solid {COLORS['border']};
    transition: all 0.3s ease;
    margin-bottom: 0.5rem;
}}

.timeline-item.active .timeline-dot {{
    background: linear-gradient(135deg, {COLORS['gradient_start']}, {COLORS['gradient_end']});
    border-color: {COLORS['primary_light']};
    transform: scale(1.4);
    box-shadow: 0 0 20px rgba(74, 124, 46, 0.6);
}}

.timeline-label {{
    font-size: 0.75rem;
    color: {COLORS['text_secondary']};
    white-space: nowrap;
    transition: all 0.3s ease;
}}

.timeline-item.active .timeline-label {{
    color: {COLORS['primary_light']};
    font-weight: 600;
    font-size: 0.85rem;
}}

.nav-button {{
    background: {COLORS['surface']} !important;
    border: 2px solid {COLORS['border']} !important;
    border-radius: 16px !important;
    padding: 1rem 1.5rem !important;
    color: {COLORS['text_primary']} !important;
    font-size: 1rem !important;
    font-weight: 500 !important;
    cursor: pointer;
    transition: all 0.3s ease !important;
}}

.nav-button:hover {{
    background: {COLORS['primary']} !important;
    border-color: {COLORS['primary_light']} !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 24px rgba(45, 80, 22, 0.3) !important;
}}

.carousel-nav-btn {{
    background: {COLORS['surface']} !important;
    border: 2px solid {COLORS['border']} !important;
    border-radius: 50% !important;
    width: 50px !important;
    height: 50px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    color: {COLORS['text_primary']} !important;
    font-size: 1.5rem !important;
    cursor: pointer !important;
    transition: all 0.3s ease !important;
}}

.carousel-nav-btn:hover {{
    background: {COLORS['primary']} !important;
    border-color: {COLORS['primary_light']} !important;
    transform: scale(1.1) !important;
}}

.stats-container {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 1.5rem;
    margin: 2rem 0 3rem 0;
}}

.stat-card {{
    background: {COLORS['surface']};
    border: 2px solid {COLORS['border']};
    border-radius: 20px;
    padding: 2rem 1.5rem;
    text-align: center;
    transition: all 0.3s ease;
}}

.stat-card:hover {{
    transform: translateY(-4px);
    border-color: {COLORS['primary_light']};
    box-shadow: 0 12px 30px rgba(45, 80, 22, 0.2);
}}

.stat-value {{
    font-family: 'Playfair Display', serif;
    font-size: 2.5rem;
    font-weight: 700;
    color: {COLORS['primary_light']};
    margin-bottom: 0.5rem;
}}

.stat-label {{
    color: {COLORS['text_secondary']};
    font-size: 0.9rem;
}}

.chat-container {{
    background: {COLORS['surface']};
    border: 2px solid {COLORS['border']};
    border-radius: 24px;
    padding: 2rem;
    margin-top: 3rem;
}}

.chat-header {{
    font-family: 'Playfair Display', serif;
    font-size: 1.8rem;
    color: {COLORS['text_primary']};
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: 0.75rem;
}}

button.primary {{
    background: linear-gradient(135deg, {COLORS['gradient_start']}, {COLORS['gradient_end']}) !important;
    border: none !important;
    color: {COLORS['secondary']} !important;
}}

button.primary:hover {{
    box-shadow: 0 8px 24px rgba(45, 80, 22, 0.4) !important;
}}

.gr-button {{
    border-radius: 12px !important;
}}

.gr-input, .gr-textbox {{
    background: {COLORS['surface']} !important;
    border: 2px solid {COLORS['border']} !important;
    border-radius: 12px !important;
    color: {COLORS['text_primary']} !important;
}}

.gr-input:focus, .gr-textbox:focus {{
    border-color: {COLORS['primary_light']} !important;
}}
"""


# SmolAgent tools
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
    experiences = PORTFOLIO["experiences"]
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
    skills_data = PORTFOLIO.get("skills", [])

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
    certs = PORTFOLIO.get("certifications", [])

    output = "Clement's Certifications:\n\n"
    for cert in certs:
        output += f"• **{cert['name']}** - {cert['issuer']} ({cert['year']})\n"
        output += f"  {cert['description']}\n\n"

    return output


@tool
def list_clement_education() -> str:
    """Get Clement's educational background"""
    education = PORTFOLIO.get("education", [])

    output = "Clement's Education:\n\n"
    for edu in education:
        output += f"**{edu['school']}** - {edu['degree']} ({edu['year']})\n"
        if "achievement" in edu:
            output += f"  Achievement: {edu['achievement']}\n"
        if "focus" in edu:
            output += f"  Focus: {edu['focus']}\n"
        output += "\n"

    return output


@tool
def analyze_profile_match(requirements: str) -> str:
    """
    Analyze how Clement's profile matches specific requirements.

    Args:
        requirements: Job description or project requirements

    Returns:
        Analysis of profile match with recommendations
    """
    req_lower = requirements.lower()
    matches = {"experiences": [], "skills": [], "strength": 0}

    # Search experiences
    for exp in PORTFOLIO["experiences"]:
        exp_text = f"{exp['title']} {exp['description']}".lower()
        techs_text = " ".join(exp["technologies"]).lower()

        if any(word in exp_text or word in techs_text for word in req_lower.split()):
            matches["experiences"].append(exp["title"])
            matches["strength"] += 3

    # Search skills
    for skill_set in PORTFOLIO.get("skills", []):
        for skill in skill_set["skills"]:
            if any(word in skill.lower() for word in req_lower.split()):
                matches["skills"].append(skill)
                matches["strength"] += 1

    # Build analysis
    output = f"Profile Match Analysis for: {requirements}\n\n"

    if matches["experiences"]:
        output += f"**Relevant Experiences ({len(matches['experiences'])}):**\n"
        output += "• " + "\n• ".join(matches["experiences"][:5]) + "\n\n"

    if matches["skills"]:
        output += f"**Matching Skills ({len(matches['skills'])}):**\n"
        output += "• " + "\n• ".join(set(matches["skills"][:8])) + "\n\n"

    # Match strength assessment
    if matches["strength"] > 15:
        output += "✅ **Excellent Match**: Strong alignment with requirements\n"
    elif matches["strength"] > 8:
        output += "👍 **Good Match**: Relevant experience and skills\n"
    elif matches["strength"] > 3:
        output += "💡 **Partial Match**: Some relevant experience\n"
    else:
        output += (
            "📚 **Learning Opportunity**: Fast learner ready to acquire new skills\n"
        )

    return output


# Initialize agent based on environment
if USE_HF_MODEL:
    model = InferenceClientModel(
        model_id="Qwen/Qwen2.5-Coder-32B-Instruct",
        temperature=0.7,
        token=os.getenv("HF_TOKEN"),
    )

    agent = CodeAgent(
        model=model,
        tools=[
            list_clement_experiences,
            list_clement_skills,
            list_clement_certifications,
            list_clement_education,
            analyze_profile_match,
        ],
        max_steps=6,
        verbosity_level=0,
    )


def chat_with_agent(message: str, history: List) -> Tuple[str, List]:
    """
    Process chat message using SmolAgent or LiteLLM

    Args:
        message: User's message
        history: Chat history

    Returns:
        Tuple of (empty string for input, updated history)
    """
    try:
        if USE_HF_MODEL:
            # Use SmolAgent
            result = agent.run(message)
            response = (
                result.get("output", str(result))
                if isinstance(result, dict)
                else str(result)
            )
        else:
            # Use LiteLLM
            context = f"""You are an AI assistant representing Clément Peponnet's GenAI & Agentic AI portfolio.

Key Information:
- Expert in GenAI, Agentic AI, and MCP (Model Context Protocol)
- Tech Lead with experience in multi-agent systems
- Certifications: {', '.join([cert['name'] for cert in PORTFOLIO['certifications']])}
- Recent projects: multi-agent systems, MCP servers, GenAI translation MVP

Portfolio Summary:
- {len(PORTFOLIO['experiences'])} professional experiences
- {len(PORTFOLIO.get('skills', []))} skill categories
- {len(PORTFOLIO['certifications'])} certifications

Answer questions professionally and highlight relevant experiences."""

            messages = [{"role": "system", "content": context}]

            for user_msg, assistant_msg in history:
                messages.append({"role": "user", "content": user_msg})
                messages.append({"role": "assistant", "content": assistant_msg})

            messages.append({"role": "user", "content": message})

            llm_response = completion(
                model=os.getenv("LITELLM_MODEL", "gpt-4o-mini"),
                messages=messages,
                api_key=os.getenv("OPENAI_API_KEY"),
                temperature=0.7,
                max_tokens=500,
            )

            response = llm_response.choices[0].message.content

        history.append((message, response))
        return "", history

    except Exception as e:
        error_msg = f"I encountered an error: {str(e)}. Please try again."
        history.append((message, error_msg))
        return "", history


# Generate HTML for carousel card
def generate_card_html(item: Dict, category: str) -> str:
    """Generate HTML for a portfolio item card"""

    icon = item.get("icon", "📌")
    title = item.get("title", "")
    subtitle = item.get("client", item.get("issuer", item.get("school", "")))
    description = item.get("description", item.get("focus", ""))
    duration = item.get("duration", item.get("year", ""))
    techs = item.get("technologies", item.get("skills", []))
    impact = item.get("impact", "")

    tech_badges = "".join(
        [f'<span class="tech-badge">{tech}</span>' for tech in techs[:6]]
    )

    return f"""
    <div class="card">
        <div class="card-header">
            <div class="card-logo">{icon}</div>
            <div style="flex: 1;">
                <div class="card-title">{title}</div>
                {f'<div class="card-subtitle">{subtitle}</div>' if subtitle else ''}
            </div>
        </div>
        <div class="card-content">{description}</div>
        {f'<div class="card-meta">📅 {duration}</div>' if duration else ''}
        {f'<div class="card-meta">🎯 {impact}</div>' if impact else ''}
        <div style="margin-top: auto;">{tech_badges}</div>
    </div>
    """


# Generate timeline HTML
def generate_timeline_html(items: List[Dict], active_index: int) -> str:
    """Generate HTML for interactive timeline"""

    timeline_items = []
    for i, item in enumerate(items):
        date = item.get("date", item.get("year", item.get("period", "")))
        active_class = "active" if i == active_index else ""

        timeline_items.append(
            f"""
        <div class="timeline-item {active_class}" data-index="{i}">
            <div class="timeline-dot"></div>
            <div class="timeline-label">{date}</div>
        </div>
        """
        )

    return f'<div class="timeline">{"".join(timeline_items)}</div>'


# Create Gradio interface
def create_interface():
    """Create the main Gradio interface"""

    with gr.Blocks(
        css=CUSTOM_CSS,
        theme=gr.themes.Soft(
            primary_hue="green", secondary_hue="stone", neutral_hue="slate"
        ),
        title="Clément Peponnet - Portfolio GenAI & Agentic",
    ) as app:

        # State variables
        category_state = gr.State("experiences")
        index_state = gr.State(0)

        # Header with social links
        gr.HTML(
            f"""
        <div class="premium-header">
            <h1>Clément Peponnet</h1>
            <p>Portfolio GenAI & Agentic</p>
            <p style="margin-top: 0.5rem; opacity: 0.9;">
                Expert GenAI | Tech Lead Agents & MCP | Azure AI Engineer
            </p>
            <p style="margin-top: 1rem; font-size: 1rem; opacity: 0.85;">
                Convaincu par le potentiel de la GenAI et de l'Agentic AI,<br>
                j'accompagne mes clients de l'idéation à l'industrialisation
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
        )

        # Stats section
        gr.HTML(
            f"""
        <div class="stats-container">
            <div class="stat-card">
                <div class="stat-value">{len(PORTFOLIO['experiences'])}</div>
                <div class="stat-label">Projets GenAI majeurs</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{len(PORTFOLIO['certifications'])}</div>
                <div class="stat-label">Certifications AI</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">50+</div>
                <div class="stat-label">Pitchs GenAI</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">6000+</div>
                <div class="stat-label">Utilisateurs produits</div>
            </div>
        </div>
        """
        )

        # Navigation tabs
        with gr.Row():
            exp_btn = gr.Button("🚀 Expériences", elem_classes="nav-button")
            skills_btn = gr.Button("💡 Expertise & Skills", elem_classes="nav-button")
            cert_btn = gr.Button("🏆 Certifications", elem_classes="nav-button")
            edu_btn = gr.Button("🎓 Études", elem_classes="nav-button")

        # Carousel display
        with gr.Row():
            with gr.Column(scale=1):
                prev_btn = gr.Button("◀", elem_classes="carousel-nav-btn")
            with gr.Column(scale=10):
                carousel_html = gr.HTML(
                    generate_card_html(PORTFOLIO["experiences"][0], "experiences"),
                    elem_classes="carousel-container",
                )
            with gr.Column(scale=1):
                next_btn = gr.Button("▶", elem_classes="carousel-nav-btn")

        # Timeline
        timeline_html = gr.HTML(generate_timeline_html(PORTFOLIO["experiences"], 0))

        # Navigation functions
        def update_category(category: str):
            items = PORTFOLIO.get(category, [])
            if items:
                card = generate_card_html(items[0], category)
                timeline = generate_timeline_html(items, 0)
                return card, timeline, category, 0
            return carousel_html.value, timeline_html.value, category, 0

        def navigate_carousel(direction: int, category: str, current_index: int):
            items = PORTFOLIO.get(category, [])
            if not items:
                return carousel_html.value, timeline_html.value, current_index

            new_index = (current_index + direction) % len(items)
            card = generate_card_html(items[new_index], category)
            timeline = generate_timeline_html(items, new_index)
            return card, timeline, new_index

        # Connect navigation buttons
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

        # Chat interface
        gr.HTML(
            """
        <div class="chat-header">
            🤖 Assistant IA - SmolAgent
        </div>
        """
        )

        chatbot = gr.Chatbot(
            height=450, label="", avatar_images=(None, "🤖"), bubble_full_width=False
        )

        with gr.Row():
            msg = gr.Textbox(
                placeholder="Posez une question sur le profil de Clément...",
                label="",
                scale=9,
                lines=1,
            )
            send_btn = gr.Button("Envoyer", variant="primary", scale=1)

        gr.Examples(
            examples=[
                "Quels sont les projets avec des agents IA ?",
                "Parle-moi de l'expérience avec MCP",
                "Quelles technologies GenAI maîtrise Clément ?",
                "Analyse le match pour : Senior GenAI Engineer avec Azure",
            ],
            inputs=msg,
            label="Questions suggérées",
        )

        # Chat functionality
        msg.submit(chat_with_agent, [msg, chatbot], [msg, chatbot])
        send_btn.click(chat_with_agent, [msg, chatbot], [msg, chatbot])

        # Footer
        model_info = (
            "Qwen2.5-Coder-32B (HuggingFace)"
            if USE_HF_MODEL
            else f"{os.getenv('LITELLM_MODEL', 'GPT-4o-mini')} (LiteLLM)"
        )
        gr.HTML(
            f"""
        <div style="text-align: center; margin-top: 3rem; padding: 2rem; 
                    border-top: 2px solid {COLORS['border']};">
            <p style="color: {COLORS['text_secondary']}; font-size: 0.9rem;">
                © 2025 Clément Peponnet - Portfolio GenAI & Agentic
            </p>
            <p style="color: {COLORS['text_secondary']}; font-size: 0.8rem; margin-top: 0.5rem;">
                Built with Gradio & {model_info}
            </p>
        </div>
        """
        )

    return app


# Launch application
if __name__ == "__main__":
    app = create_interface()
    app.launch(server_name="0.0.0.0", server_port=7860, show_error=True, share=True)
