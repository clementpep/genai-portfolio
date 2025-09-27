"""
Premium GenAI Portfolio Application
Deployed on Hugging Face Spaces with Gradio interface
"""

import gradio as gr
import yaml
import os
from typing import List, Dict, Optional
from litellm import completion
import json


# Load portfolio data from YAML file
def load_portfolio_data() -> Dict:
    """Load portfolio data from YAML configuration file"""
    with open("portfolio_data.yaml", "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


PORTFOLIO = load_portfolio_data()

# Premium color scheme - Apple-inspired
COLORS = {
    "primary": "#007AFF",
    "secondary": "#5856D6",
    "background": "#000000",
    "surface": "#1C1C1E",
    "surface_elevated": "#2C2C2E",
    "text_primary": "#FFFFFF",
    "text_secondary": "#8E8E93",
    "accent": "#30D158",
    "gradient_start": "#007AFF",
    "gradient_end": "#5856D6",
}

# Custom CSS for premium Apple-like design
CUSTOM_CSS = f"""
@import url('https://fonts.googleapis.com/css2?family=SF+Pro+Display:wght@300;400;500;600;700&display=swap');

.gradio-container {{
    font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Segoe UI', sans-serif !important;
    background: linear-gradient(180deg, {COLORS['background']} 0%, #1a1a1a 100%) !important;
    max-width: 1400px !important;
    margin: 0 auto !important;
}}

.premium-header {{
    background: linear-gradient(135deg, {COLORS['gradient_start']}, {COLORS['gradient_end']});
    padding: 3rem 2rem;
    border-radius: 24px;
    text-align: center;
    margin-bottom: 2rem;
    box-shadow: 0 20px 60px rgba(0, 122, 255, 0.3);
}}

.premium-header h1 {{
    color: white;
    font-size: 3rem;
    font-weight: 700;
    margin-bottom: 0.5rem;
    letter-spacing: -0.02em;
}}

.premium-header p {{
    color: rgba(255, 255, 255, 0.9);
    font-size: 1.25rem;
    font-weight: 400;
}}

.carousel-container {{
    position: relative;
    min-height: 500px;
    padding: 2rem 0;
    display: flex;
    align-items: center;
    justify-content: center;
}}

.card {{
    background: {COLORS['surface_elevated']};
    border-radius: 20px;
    padding: 2rem;
    width: 100%;
    max-width: 600px;
    min-height: 400px;
    box-shadow: 0 10px 40px rgba(0, 0, 0, 0.4);
    border: 1px solid rgba(255, 255, 255, 0.1);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}}

.card:hover {{
    transform: translateY(-4px);
    box-shadow: 0 20px 60px rgba(0, 122, 255, 0.2);
}}

.card-header {{
    display: flex;
    align-items: center;
    gap: 1rem;
    margin-bottom: 1.5rem;
}}

.card-icon {{
    font-size: 3rem;
    filter: drop-shadow(0 4px 8px rgba(0, 122, 255, 0.4));
}}

.card-title {{
    font-size: 1.75rem;
    font-weight: 600;
    color: {COLORS['text_primary']};
    margin-bottom: 0.5rem;
}}

.card-subtitle {{
    font-size: 1rem;
    color: {COLORS['primary']};
    font-weight: 500;
}}

.card-content {{
    color: {COLORS['text_secondary']};
    line-height: 1.6;
    margin-bottom: 1.5rem;
}}

.tech-badge {{
    display: inline-block;
    padding: 0.4rem 0.8rem;
    background: rgba(0, 122, 255, 0.15);
    border: 1px solid rgba(0, 122, 255, 0.3);
    border-radius: 12px;
    color: {COLORS['primary']};
    font-size: 0.875rem;
    font-weight: 500;
    margin: 0.25rem;
}}

.timeline {{
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 2rem;
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
    background: linear-gradient(90deg, transparent, {COLORS['primary']}, transparent);
    transform: translateY(-50%);
}}

.timeline-dot {{
    width: 16px;
    height: 16px;
    border-radius: 50%;
    background: {COLORS['surface_elevated']};
    border: 2px solid {COLORS['text_secondary']};
    cursor: pointer;
    transition: all 0.3s;
    position: relative;
    z-index: 1;
}}

.timeline-dot.active {{
    background: linear-gradient(135deg, {COLORS['gradient_start']}, {COLORS['gradient_end']});
    border-color: {COLORS['primary']};
    transform: scale(1.5);
    box-shadow: 0 0 20px rgba(0, 122, 255, 0.6);
}}

.timeline-label {{
    position: absolute;
    top: -30px;
    left: 50%;
    transform: translateX(-50%);
    font-size: 0.75rem;
    color: {COLORS['text_secondary']};
    white-space: nowrap;
}}

.timeline-dot.active .timeline-label {{
    color: {COLORS['primary']};
    font-weight: 600;
}}

.nav-button {{
    background: {COLORS['surface_elevated']};
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 16px;
    padding: 1rem 1.5rem;
    color: {COLORS['text_primary']};
    font-size: 1rem;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.3s;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}}

.nav-button:hover {{
    background: {COLORS['primary']};
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(0, 122, 255, 0.3);
}}

.nav-button.active {{
    background: linear-gradient(135deg, {COLORS['gradient_start']}, {COLORS['gradient_end']});
    box-shadow: 0 8px 24px rgba(0, 122, 255, 0.4);
}}

.chat-message {{
    padding: 1rem;
    border-radius: 16px;
    margin-bottom: 0.75rem;
    max-width: 80%;
    word-wrap: break-word;
}}

.chat-message.user {{
    background: linear-gradient(135deg, {COLORS['gradient_start']}, {COLORS['gradient_end']});
    margin-left: auto;
    color: white;
}}

.chat-message.assistant {{
    background: {COLORS['surface_elevated']};
    border: 1px solid rgba(255, 255, 255, 0.1);
    color: {COLORS['text_primary']};
}}

.stats-container {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 1.5rem;
    margin: 2rem 0;
}}

.stat-card {{
    background: {COLORS['surface_elevated']};
    border-radius: 20px;
    padding: 1.5rem;
    text-align: center;
    border: 1px solid rgba(255, 255, 255, 0.1);
}}

.stat-value {{
    font-size: 2.5rem;
    font-weight: 700;
    background: linear-gradient(135deg, {COLORS['gradient_start']}, {COLORS['gradient_end']});
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}}

.stat-label {{
    color: {COLORS['text_secondary']};
    font-size: 0.875rem;
    margin-top: 0.5rem;
}}

button {{
    border-radius: 12px !important;
}}

.gr-button-primary {{
    background: linear-gradient(135deg, {COLORS['gradient_start']}, {COLORS['gradient_end']}) !important;
    border: none !important;
}}
"""


# Chat function using LiteLLM
def chat_with_ai(message: str, history: List) -> str:
    """
    Process chat message using LiteLLM with GPT-4o-mini

    Args:
        message: User's message
        history: Chat history

    Returns:
        AI assistant's response
    """
    try:
        # Build context from portfolio data
        context = f"""You are an AI assistant representing Clément's GenAI & Agentic AI portfolio.

Key Information:
- Expert in GenAI, Agentic AI, and MCP (Model Context Protocol)
- Tech Lead with experience in multi-agent systems
- Certifications: {', '.join([cert['name'] for cert in PORTFOLIO['certifications']])}
- Recent projects include: multi-agent systems, MCP servers, GenAI translation MVP

When answering questions:
1. Be professional yet approachable
2. Highlight relevant experiences and skills
3. Provide specific examples from the portfolio
4. Keep responses concise and valuable

Available data:
- {len(PORTFOLIO['experiences'])} professional experiences
- {len(PORTFOLIO['skills'])} skill categories
- {len(PORTFOLIO['certifications'])} certifications
"""

        # Prepare messages for LiteLLM
        messages = [{"role": "system", "content": context}]

        # Add conversation history
        for user_msg, assistant_msg in history:
            messages.append({"role": "user", "content": user_msg})
            messages.append({"role": "assistant", "content": assistant_msg})

        # Add current message
        messages.append({"role": "user", "content": message})

        # Call LiteLLM (requires API key in environment)
        response = completion(
            model="gpt-4o-mini", messages=messages, temperature=0.7, max_tokens=500
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"I apologize, but I encountered an error: {str(e)}. Please try again or rephrase your question."


# Generate HTML for carousel card
def generate_card_html(item: Dict, category: str) -> str:
    """Generate HTML for a portfolio item card"""

    icon_map = {
        "experiences": "🚀",
        "skills": "💡",
        "certifications": "🏆",
        "education": "🎓",
    }

    icon = item.get("icon", icon_map.get(category, "📌"))
    title = item.get("title", "")
    subtitle = item.get("client", item.get("issuer", item.get("school", "")))
    description = item.get("description", item.get("focus", ""))
    duration = item.get("duration", item.get("year", ""))
    techs = item.get("technologies", item.get("skills", []))

    tech_badges = "".join(
        [f'<span class="tech-badge">{tech}</span>' for tech in techs[:6]]
    )

    return f"""
    <div class="card">
        <div class="card-header">
            <div class="card-icon">{icon}</div>
            <div>
                <div class="card-title">{title}</div>
                {f'<div class="card-subtitle">{subtitle}</div>' if subtitle else ''}
            </div>
        </div>
        <div class="card-content">
            {description}
        </div>
        {f'<div style="margin-bottom: 1rem; color: {COLORS["text_secondary"]};">📅 {duration}</div>' if duration else ''}
        <div style="margin-top: auto;">
            {tech_badges}
        </div>
    </div>
    """


# Generate timeline HTML
def generate_timeline_html(items: List[Dict], active_index: int) -> str:
    """Generate HTML for interactive timeline"""

    dots_html = []
    for i, item in enumerate(items):
        date = item.get("date", item.get("year", item.get("period", "")))
        active_class = "active" if i == active_index else ""

        dots_html.append(
            f"""
        <div class="timeline-dot {active_class}" onclick="updateCarousel({i})">
            <div class="timeline-label">{date}</div>
        </div>
        """
        )

    return f"""
    <div class="timeline">
        {''.join(dots_html)}
    </div>
    <script>
    function updateCarousel(index) {{
        // This would trigger the carousel update
        console.log('Timeline clicked:', index);
    }}
    </script>
    """


# Build Gradio interface
def create_interface():
    """Create the main Gradio interface"""

    with gr.Blocks(
        css=CUSTOM_CSS,
        theme=gr.themes.Soft(
            primary_hue="blue", secondary_hue="purple", neutral_hue="slate"
        ),
        title="Clément - Portfolio GenAI & Agentic",
    ) as app:

        # State for carousel navigation
        category_state = gr.State("experiences")
        index_state = gr.State(0)

        # Header
        gr.HTML(
            f"""
        <div class="premium-header">
            <h1>Clément - Portfolio GenAI & Agentic</h1>
            <p>Expert GenAI | Tech Lead Agents & MCP | Azure AI Engineer</p>
            <p style="margin-top: 1rem; font-size: 1rem; opacity: 0.9;">
                Convaincu par le potentiel de la GenAI et de l'Agentic AI, 
                j'accompagne mes clients de l'idéation à l'industrialisation
            </p>
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
            exp_btn = gr.Button("🚀 Expériences", variant="primary")
            skills_btn = gr.Button("💡 Expertise & Skills")
            cert_btn = gr.Button("🏆 Certifications")
            edu_btn = gr.Button("🎓 Études")

        # Carousel display
        with gr.Row():
            prev_btn = gr.Button("◀", scale=1)
            carousel_html = gr.HTML(
                generate_card_html(PORTFOLIO["experiences"][0], "experiences"),
                elem_classes="carousel-container",
            )
            next_btn = gr.Button("▶", scale=1)

        # Timeline
        timeline_html = gr.HTML(generate_timeline_html(PORTFOLIO["experiences"], 0))

        # Navigation functions
        def update_category(category: str):
            """Update displayed category"""
            items = PORTFOLIO.get(category, [])
            if items:
                card = generate_card_html(items[0], category)
                timeline = generate_timeline_html(items, 0)
                return card, timeline, category, 0
            return carousel_html.value, timeline_html.value, category, 0

        def navigate_carousel(direction: int, category: str, current_index: int):
            """Navigate carousel left or right"""
            items = PORTFOLIO.get(category, [])
            if not items:
                return carousel_html.value, timeline_html.value, current_index

            new_index = (current_index + direction) % len(items)
            card = generate_card_html(items[new_index], category)
            timeline = generate_timeline_html(items, new_index)
            return card, timeline, new_index

        # Connect navigation buttons
        exp_btn.click(
            update_category,
            inputs=[gr.State("experiences")],
            outputs=[carousel_html, timeline_html, category_state, index_state],
        )
        skills_btn.click(
            update_category,
            inputs=[gr.State("skills")],
            outputs=[carousel_html, timeline_html, category_state, index_state],
        )
        cert_btn.click(
            update_category,
            inputs=[gr.State("certifications")],
            outputs=[carousel_html, timeline_html, category_state, index_state],
        )
        edu_btn.click(
            update_category,
            inputs=[gr.State("education")],
            outputs=[carousel_html, timeline_html, category_state, index_state],
        )

        prev_btn.click(
            navigate_carousel,
            inputs=[gr.State(-1), category_state, index_state],
            outputs=[carousel_html, timeline_html, index_state],
        )
        next_btn.click(
            navigate_carousel,
            inputs=[gr.State(1), category_state, index_state],
            outputs=[carousel_html, timeline_html, index_state],
        )

        # Chat interface
        gr.Markdown("## 💬 Assistant IA - Powered by GPT-4o-mini")

        chatbot = gr.Chatbot(
            height=400, label="Chat with AI Assistant", avatar_images=(None, "🤖")
        )

        with gr.Row():
            msg = gr.Textbox(
                placeholder="Posez une question sur mon profil, mes expériences GenAI...",
                label="",
                scale=9,
            )
            send_btn = gr.Button("Envoyer", variant="primary", scale=1)

        gr.Examples(
            examples=[
                "Quels sont tes projets avec des agents IA ?",
                "Parle-moi de ton expérience avec MCP",
                "Quelles technologies maîtrises-tu pour la GenAI ?",
                "Quel est ton projet le plus impactant ?",
            ],
            inputs=msg,
        )

        # Chat functionality
        def respond(message, history):
            response = chat_with_ai(message, history)
            history.append((message, response))
            return "", history

        msg.submit(respond, [msg, chatbot], [msg, chatbot])
        send_btn.click(respond, [msg, chatbot], [msg, chatbot])

        # Footer
        gr.HTML(
            """
        <div style="text-align: center; margin-top: 3rem; padding: 2rem; border-top: 1px solid rgba(255, 255, 255, 0.1);">
            <p style="color: #8E8E93; font-size: 0.875rem;">
                © 2025 Clément - Portfolio GenAI & Agentic | Built with Gradio & LiteLLM
            </p>
        </div>
        """
        )

    return app


# Launch application
if __name__ == "__main__":
    app = create_interface()
    app.launch()
