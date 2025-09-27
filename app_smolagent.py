"""
Premium GenAI Portfolio Application - SmolAgent Version
Alternative implementation using Hugging Face SmolAgent instead of LiteLLM
"""

import gradio as gr
import yaml
from typing import List, Dict, Optional
from smolagents import CodeAgent, InferenceClientModel, tool


# Load portfolio data
def load_portfolio_data() -> Dict:
    """Load portfolio data from YAML configuration file"""
    with open("portfolio_data.yaml", "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


PORTFOLIO = load_portfolio_data()


# Define tools for SmolAgent
@tool
def search_experiences(
    technology: Optional[str] = None,
    client: Optional[str] = None,
    keyword: Optional[str] = None,
) -> str:
    """
    Search through Clément's professional experiences.

    Args:
        technology: Filter by technology (e.g., 'MCP', 'Azure', 'SmolAgent')
        client: Filter by client name
        keyword: Search keyword in title or description

    Returns:
        Formatted string with matching experiences
    """
    experiences = PORTFOLIO["experiences"]
    results = []

    for exp in experiences:
        match = True

        if technology:
            if not any(
                technology.lower() in tech.lower()
                for tech in exp.get("technologies", [])
            ):
                match = False

        if client and match:
            if client.lower() not in exp.get("client", "").lower():
                match = False

        if keyword and match:
            search_text = f"{exp.get('title', '')} {exp.get('description', '')}".lower()
            if keyword.lower() not in search_text:
                match = False

        if match:
            results.append(exp)

    if not results:
        return "No experiences found matching the criteria."

    output = f"Found {len(results)} experience(s):\n\n"
    for exp in results:
        output += f"**{exp['title']}** at {exp['client']} ({exp['duration']})\n"
        output += f"{exp['description'][:200]}...\n"
        output += f"Technologies: {', '.join(exp['technologies'][:5])}\n"
        output += f"Impact: {exp['impact']}\n\n"

    return output


@tool
def get_skills(category: Optional[str] = None) -> str:
    """
    Get Clément's technical skills.

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

    output = "Technical Skills:\n\n"
    for skill_set in skills_data:
        output += f"**{skill_set['category']}** {skill_set['icon']}\n"
        output += "• " + "\n• ".join(skill_set["skills"][:4]) + "\n\n"

    return output


@tool
def get_certifications() -> str:
    """Get all certifications"""
    certs = PORTFOLIO.get("certifications", [])

    output = "Certifications:\n\n"
    for cert in certs:
        output += f"• **{cert['name']}** - {cert['issuer']} ({cert['year']})\n"
        output += f"  {cert['description']}\n\n"

    return output


@tool
def analyze_match(requirements: str) -> str:
    """
    Analyze how Clément's profile matches specific requirements.

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


# Initialize SmolAgent
model = InferenceClientModel(
    model_id="Qwen/Qwen2.5-Coder-32B-Instruct", temperature=0.7
)

agent = CodeAgent(
    model=model,
    tools=[search_experiences, get_skills, get_certifications, analyze_match],
    max_steps=6,
    verbosity_level=1,
)

# Premium styling (same as main app)
COLORS = {
    "primary": "#007AFF",
    "secondary": "#5856D6",
    "background": "#000000",
    "surface": "#1C1C1E",
    "surface_elevated": "#2C2C2E",
    "text_primary": "#FFFFFF",
    "text_secondary": "#8E8E93",
    "gradient_start": "#007AFF",
    "gradient_end": "#5856D6",
}

CUSTOM_CSS = f"""
@import url('https://fonts.googleapis.com/css2?family=SF+Pro+Display:wght@300;400;500;600;700&display=swap');

.gradio-container {{
    font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', sans-serif !important;
    background: linear-gradient(180deg, {COLORS['background']} 0%, #1a1a1a 100%) !important;
    max-width: 1400px !important;
}}

.premium-card {{
    background: {COLORS['surface_elevated']};
    border-radius: 20px;
    padding: 2rem;
    border: 1px solid rgba(255, 255, 255, 0.1);
    box-shadow: 0 10px 40px rgba(0, 0, 0, 0.4);
}}

.chat-bubble {{
    padding: 1rem;
    border-radius: 16px;
    margin: 0.5rem 0;
    max-width: 80%;
}}

.user-message {{
    background: linear-gradient(135deg, {COLORS['gradient_start']}, {COLORS['gradient_end']});
    margin-left: auto;
    color: white;
}}

.assistant-message {{
    background: {COLORS['surface_elevated']};
    border: 1px solid rgba(255, 255, 255, 0.1);
}}
"""


# Chat function
def chat_with_smolagent(message: str, history: List) -> str:
    """
    Process chat message using SmolAgent

    Args:
        message: User's message
        history: Chat history

    Returns:
        Agent's response
    """
    try:
        result = agent.run(message)

        # Extract response
        if isinstance(result, dict):
            response = result.get("output", str(result))
        else:
            response = str(result)

        return response

    except Exception as e:
        return f"I apologize, but I encountered an error: {str(e)}. Please rephrase your question."


# HTML generators (same as main app)
def generate_card_html(item: Dict, category: str) -> str:
    """Generate HTML for portfolio card"""
    icon = item.get("icon", "📌")
    title = item.get("title", "")
    subtitle = item.get("client", item.get("issuer", item.get("school", "")))
    description = item.get("description", "")
    techs = item.get("technologies", item.get("skills", []))

    tech_badges = "".join(
        [
            f'<span style="display: inline-block; padding: 0.4rem 0.8rem; '
            f"background: rgba(0, 122, 255, 0.15); border: 1px solid rgba(0, 122, 255, 0.3); "
            f'border-radius: 12px; margin: 0.25rem; font-size: 0.875rem;">{tech}</span>'
            for tech in techs[:6]
        ]
    )

    return f"""
    <div style="background: {COLORS['surface_elevated']}; border-radius: 20px; 
                padding: 2rem; min-height: 400px; 
                border: 1px solid rgba(255, 255, 255, 0.1);
                box-shadow: 0 10px 40px rgba(0, 0, 0, 0.4);">
        <div style="font-size: 3rem; margin-bottom: 1rem;">{icon}</div>
        <h3 style="font-size: 1.75rem; font-weight: 600; color: white; margin-bottom: 0.5rem;">{title}</h3>
        {f'<p style="color: {COLORS["primary"]}; font-weight: 500; margin-bottom: 1rem;">{subtitle}</p>' if subtitle else ''}
        <p style="color: {COLORS['text_secondary']}; line-height: 1.6; margin-bottom: 1.5rem;">{description}</p>
        <div>{tech_badges}</div>
    </div>
    """


# Create interface
def create_smolagent_interface():
    """Create Gradio interface with SmolAgent"""

    with gr.Blocks(
        css=CUSTOM_CSS,
        theme=gr.themes.Soft(primary_hue="blue", secondary_hue="purple"),
        title="Clément - Portfolio GenAI (SmolAgent)",
    ) as app:

        # Header
        gr.HTML(
            f"""
        <div style="background: linear-gradient(135deg, {COLORS['gradient_start']}, {COLORS['gradient_end']});
                    padding: 3rem 2rem; border-radius: 24px; text-align: center; margin-bottom: 2rem;
                    box-shadow: 0 20px 60px rgba(0, 122, 255, 0.3);">
            <h1 style="color: white; font-size: 3rem; font-weight: 700; margin-bottom: 0.5rem;">
                Clément - Portfolio GenAI & Agentic
            </h1>
            <p style="color: rgba(255, 255, 255, 0.9); font-size: 1.25rem;">
                Expert GenAI | Tech Lead Agents & MCP | Azure AI Engineer
            </p>
            <p style="color: rgba(255, 255, 255, 0.8); margin-top: 1rem;">
                Powered by SmolAgent & Qwen2.5-Coder-32B
            </p>
        </div>
        """
        )

        # Carousel section
        category_state = gr.State("experiences")
        index_state = gr.State(0)

        with gr.Row():
            exp_btn = gr.Button("🚀 Expériences", variant="primary")
            skills_btn = gr.Button("💡 Skills")
            cert_btn = gr.Button("🏆 Certifications")
            edu_btn = gr.Button("🎓 Études")

        carousel_html = gr.HTML(
            generate_card_html(PORTFOLIO["experiences"][0], "experiences")
        )

        # Navigation
        def update_category(category: str):
            items = PORTFOLIO.get(category, [])
            if items:
                return generate_card_html(items[0], category), category, 0
            return carousel_html.value, category, 0

        exp_btn.click(
            update_category,
            inputs=[gr.State("experiences")],
            outputs=[carousel_html, category_state, index_state],
        )
        skills_btn.click(
            lambda: update_category("skills"),
            outputs=[carousel_html, category_state, index_state],
        )
        cert_btn.click(
            lambda: update_category("certifications"),
            outputs=[carousel_html, category_state, index_state],
        )
        edu_btn.click(
            lambda: update_category("education"),
            outputs=[carousel_html, category_state, index_state],
        )

        # Chat interface
        gr.Markdown("## 🤖 SmolAgent Assistant - Powered by Qwen2.5-Coder-32B")

        chatbot = gr.Chatbot(
            height=450,
            label="Chat with SmolAgent",
            avatar_images=(None, "🤖"),
            bubble_full_width=False,
        )

        with gr.Row():
            msg = gr.Textbox(
                placeholder="Ask about experiences, skills, or match analysis...",
                label="Your question",
                scale=9,
            )
            send_btn = gr.Button("Send", variant="primary", scale=1)

        gr.Examples(
            examples=[
                "What are your multi-agent projects?",
                "Tell me about your MCP experience",
                "What GenAI technologies do you master?",
                "Analyze match for: Senior GenAI Engineer role with Azure and LangChain",
            ],
            inputs=msg,
        )

        def respond(message, history):
            response = chat_with_smolagent(message, history)
            history.append((message, response))
            return "", history

        msg.submit(respond, [msg, chatbot], [msg, chatbot])
        send_btn.click(respond, [msg, chatbot], [msg, chatbot])

        # Footer
        gr.HTML(
            """
        <div style="text-align: center; margin-top: 3rem; padding: 2rem; 
                    border-top: 1px solid rgba(255, 255, 255, 0.1);">
            <p style="color: #8E8E93; font-size: 0.875rem;">
                © 2025 Clément | Built with SmolAgent, Gradio & Hugging Face
            </p>
        </div>
        """
        )

    return app


if __name__ == "__main__":
    app = create_smolagent_interface()
    app.launch()
