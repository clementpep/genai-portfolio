"""
Main application for Clement's GenAI Portfolio on Hugging Face Space
Combines React frontend with SmolAgent backend
"""

import gradio as gr
from smolagents import CodeAgent, InferenceClientModel, tool
import json
import logging
from typing import List, Optional, Dict

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Portfolio data (same as in backend)
PORTFOLIO_DATA = {
    "experiences": [
        {
            "id": "exp1",
            "title": "MVP GenAI Traduction",
            "client": "Wavestone",
            "sector": "Digital Transformation",
            "duration": "13 mois",
            "period": "2024-12",
            "technologies": [
                "Azure AI Foundry",
                "Mistral Large",
                "ReactJS",
                "Flask",
                "Docker",
            ],
            "description": "Tech lead équipe 5 développeurs sur traducteur GenAI Mistral Large. Web app fullstack ReactJS + Flask. Présentation Ex-Com et déploiement luxe.",
            "impact": "Industrialisation réussie chez grand compte luxe",
        },
        {
            "id": "exp2",
            "title": "Système Multi-Agents SentinelOne",
            "client": "Hugging Face x Gradio",
            "sector": "Climate Tech",
            "duration": "Hackathon",
            "period": "2024-11",
            "technologies": ["SmolAgent", "LiteLLM", "Gradio", "FastMCP", "NASA FIRMS"],
            "description": "2e prix Hackathon HF catégorie AI Agents parmi 600+ projets. Système multi-agents analyse risques climatiques.",
            "impact": "2e prix international, reconnaissance communauté AI",
        },
        # Add all other experiences from backend...
    ],
    "skills": {
        "Agents & MCP": [
            "Azure AI Agents",
            "Hugging Face SmolAgent",
            "FastMCP",
            "MCP Shield",
            "Dataiku LLM Mesh",
        ],
        "GenAI Frameworks": [
            "Azure AI Foundry",
            "Azure AI Search",
            "LlamaIndex",
            "LangChain",
            "Copilot Studio",
        ],
        "Web Development": ["FastAPI", "Django", "Flask", "React", "Docker", "Azure"],
        "Data & ML": [
            "Python",
            "TensorFlow",
            "PyTorch",
            "Scikit-learn",
            "Pandas",
            "PySpark",
        ],
    },
    "certifications": [
        {"name": "Azure AI Engineer Associate", "issuer": "Microsoft", "year": "2024"},
        {"name": "Dataiku GenAI Practitioner", "issuer": "Dataiku", "year": "2024"},
        {"name": "Hugging Face MCP Course", "issuer": "Hugging Face", "year": "2025"},
    ],
    "education": [
        {
            "school": "Arts & Métiers ParisTech",
            "degree": "Diplôme Ingénieur",
            "year": "2020",
            "achievement": "Classé 38/120, Médaille d'argent",
        },
        {
            "school": "ETS Montréal",
            "degree": "Spécialisation Data Science",
            "year": "2019",
            "focus": "Machine Learning & Deep Learning",
        },
    ],
}


# Define SmolAgent tools
@tool
def list_experiences(
    client: Optional[str] = None,
    sector: Optional[str] = None,
    technology: Optional[str] = None,
) -> str:
    """List Clement's professional experiences with optional filtering.

    Args:
        client: Filter by client name
        sector: Filter by sector
        technology: Filter by technology used
    """
    experiences = PORTFOLIO_DATA["experiences"]

    if client:
        experiences = [e for e in experiences if client.lower() in e["client"].lower()]
    if sector:
        experiences = [e for e in experiences if sector.lower() in e["sector"].lower()]
    if technology:
        experiences = [
            e
            for e in experiences
            if any(technology.lower() in tech.lower() for tech in e["technologies"])
        ]

    if not experiences:
        return "Aucune expérience trouvée avec ces critères."

    result = f"J'ai trouvé {len(experiences)} expérience(s):\n\n"
    for exp in experiences:
        result += f"**{exp['title']}** chez {exp['client']} ({exp['duration']})\n"
        result += f"  {exp['description']}\n"
        result += f"  Technologies: {', '.join(exp['technologies'][:3])}...\n\n"

    return result


@tool
def get_skills(category: Optional[str] = None) -> str:
    """Get Clement's technical skills.

    Args:
        category: Skill category filter
    """
    skills = PORTFOLIO_DATA["skills"]

    if category:
        matching = [k for k in skills.keys() if category.lower() in k.lower()]
        if matching:
            return f"Compétences {matching[0]}:\n• " + "\n• ".join(skills[matching[0]])
        return f"Catégorie '{category}' non trouvée"

    result = "Compétences techniques:\n\n"
    for cat, items in skills.items():
        result += f"**{cat}:**\n• " + "\n• ".join(items[:3]) + "...\n\n"
    return result


@tool
def search_portfolio(query: str) -> str:
    """Search across all portfolio content.

    Args:
        query: Search query
    """
    query_lower = query.lower()
    results = []

    for exp in PORTFOLIO_DATA["experiences"]:
        if (
            query_lower
            in f"{exp['title']} {exp['description']} {' '.join(exp['technologies'])}".lower()
        ):
            results.append(f"• {exp['title']} - {exp['client']}")

    if not results:
        return f"Aucun résultat pour '{query}'"

    return f"Résultats pour '{query}':\n" + "\n".join(results[:5])


model = InferenceClientModel(
    model_id="Qwen/Qwen2.5-Coder-32B-Instruct", max_tokens=2048, temperature=0.7
)

agent = CodeAgent(
    model=model,
    tools=[list_experiences, get_skills, search_portfolio],
    max_steps=6,
    verbosity_level=0,
)


# Chat function for Gradio
def chat_with_agent(message: str, history: List):
    """Process chat message with SmolAgent"""
    try:
        # Run agent with the query
        result = agent.run(message)

        # Extract response
        if isinstance(result, dict) and "output" in result:
            response = result["output"]
        else:
            response = str(result)

        return response
    except Exception as e:
        logger.error(f"Chat error: {e}")
        return f"Désolé, une erreur s'est produite. Veuillez réessayer."


# Create Gradio interface
with gr.Blocks(
    title="Clément - Portfolio GenAI & Agentic",
    theme=gr.themes.Soft(
        primary_hue="blue", secondary_hue="purple", font=gr.themes.GoogleFont("Inter")
    ),
    css="""
    .gradio-container {
        max-width: 1400px !important;
        margin: auto !important;
    }
    .portfolio-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 12px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
    }
    .portfolio-section {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
    }
    """,
) as demo:

    # Header
    gr.HTML(
        """
        <div class="portfolio-header">
            <h1 style="font-size: 2.5rem; margin-bottom: 1rem;">
                🚀 Clément - Portfolio GenAI & Agentic
            </h1>
            <p style="font-size: 1.2rem; opacity: 0.95;">
                Expert technique GenAI | Tech Lead Agents & MCP | Azure AI Engineer
            </p>
            <p style="margin-top: 1rem; opacity: 0.9;">
                Convaincu par le potentiel de la GenAI et de l'Agentic AI, j'accompagne mes clients 
                sur toutes les étapes de leurs projets, de l'idéation à l'industrialisation
            </p>
        </div>
    """
    )

    with gr.Row():
        # Left column - Portfolio content
        with gr.Column(scale=2):
            # Quick stats
            gr.HTML(
                """
                <div class="portfolio-section">
                    <h3>📊 En bref</h3>
                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 1rem; margin-top: 1rem;">
                        <div style="text-align: center; padding: 1rem; background: rgba(59, 130, 246, 0.1); border-radius: 8px;">
                            <div style="font-size: 2rem; font-weight: bold; color: #3b82f6;">6+</div>
                            <div>Projets GenAI majeurs</div>
                        </div>
                        <div style="text-align: center; padding: 1rem; background: rgba(139, 92, 246, 0.1); border-radius: 8px;">
                            <div style="font-size: 2rem; font-weight: bold; color: #8b5cf6;">3</div>
                            <div>Certifications AI</div>
                        </div>
                        <div style="text-align: center; padding: 1rem; background: rgba(16, 185, 129, 0.1); border-radius: 8px;">
                            <div style="font-size: 2rem; font-weight: bold; color: #10b981;">50+</div>
                            <div>Pitchs GenAI</div>
                        </div>
                    </div>
                </div>
            """
            )

            # Main experiences
            with gr.Accordion("🚀 Expériences GenAI & Agentiques", open=True):
                gr.Markdown(
                    """
                ### Projets phares
                
                **🏆 Système Multi-Agents SentinelOne** - *2e prix Hackathon HF x Gradio*
                - Conception système multi-agents (SmolAgent + LiteLLM)
                - Analyse risques climatiques temps réel (NASA FIRMS, Open-Meteo)
                - Déploiement sur HF Spaces, intégration serveur MCP
                
                **🤖 Workflow Multi-Agents Dataiku - ALSTOM** - *Projet vitrine COMEX*
                - Pipeline 12 agents sur Dataiku LLM Mesh
                - Automatisation validation 80K+ Purchase Requisitions/an
                - Impact: économie 50 ETP
                
                **🔧 Serveurs MCP - Client Transport**
                - 3 serveurs MCP: Bing Search, Microsoft Graph, Python Interpreter
                - Déploiement Azure Kubernetes (AKS)
                - Intégration LibreChat pour 500+ utilisateurs
                
                **🌐 MVP GenAI Traduction - Wavestone**
                - Tech lead équipe 5 développeurs
                - Architecture multi-LLMs avec Mistral Large
                - Déploiement grand compte luxe
                """
                )

            # Skills
            with gr.Accordion("💡 Expertises & Compétences", open=False):
                gr.Markdown(
                    """
                ### Domaines d'expertise
                
                **Agents & MCP**
                - Azure AI Agents, SmolAgent, FastMCP
                - Dataiku LLM Mesh, MCP Shield
                - Orchestration multi-agents
                
                **Frameworks GenAI**
                - Azure AI Foundry, LangChain, LlamaIndex
                - Copilot Studio, n8n, LangGraph
                - RAG & Vector Databases
                
                **Développement & DevOps**
                - React, FastAPI, Flask, Streamlit
                - Docker, Azure (AKS, ACR, App Service)
                - CI/CD, GitLab, GitHub Actions
                """
                )

            # Certifications
            with gr.Accordion("🏅 Certifications", open=False):
                gr.Markdown(
                    """
                - **Azure AI Engineer Associate** (Microsoft, 2024)
                - **Dataiku GenAI Practitioner** (Dataiku, 2024)
                - **Hugging Face MCP Course** (HuggingFace, 2025)
                """
                )

        # Right column - AI Chat
        with gr.Column(scale=1):
            gr.HTML(
                """
                <div style="background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%); 
                            padding: 1rem; border-radius: 12px 12px 0 0; color: white; text-align: center;">
                    <h3 style="margin: 0;">🤖 Assistant IA - SmolAgent</h3>
                    <p style="margin: 0.5rem 0 0 0; opacity: 0.9; font-size: 0.9rem;">
                        Powered by Qwen2.5-Coder-32B
                    </p>
                </div>
            """
            )

            chatbot = gr.Chatbot(
                label="",
                height=500,
                bubble_full_width=False,
                avatar_images=(None, "🤖"),
            )

            msg = gr.Textbox(
                label="",
                placeholder="Posez une question sur mon profil, mes expériences GenAI...",
                lines=2,
            )

            with gr.Row():
                clear = gr.Button("🗑️ Effacer", size="sm")
                submit = gr.Button("📤 Envoyer", variant="primary", size="sm")

            # Example questions
            gr.Examples(
                examples=[
                    "Quels sont tes projets avec des agents IA ?",
                    "Parle-moi de ton expérience avec MCP",
                    "Quelles technologies maîtrises-tu pour la GenAI ?",
                    "As-tu travaillé sur des projets multi-agents ?",
                    "Quel est ton projet le plus impactant ?",
                ],
                inputs=msg,
                label="Questions suggérées",
            )

    # Footer
    gr.HTML(
        """
        <div style="text-align: center; margin-top: 2rem; padding: 1rem; opacity: 0.7;">
            <p>
                <a href="https://github.com/clement-portfolio" target="_blank">GitHub</a> • 
                <a href="https://linkedin.com/in/clement" target="_blank">LinkedIn</a> • 
                <a href="mailto:clement@example.com">Contact</a>
            </p>
            <p style="margin-top: 0.5rem; font-size: 0.9rem;">
                © 2025 Clément - Portfolio GenAI & Agentic | Built with SmolAgent & Gradio
            </p>
        </div>
    """
    )

    # Chat functionality
    msg.submit(chat_with_agent, [msg, chatbot], [chatbot])
    submit.click(chat_with_agent, [msg, chatbot], [chatbot])
    clear.click(lambda: None, None, chatbot, queue=False)

if __name__ == "__main__":
    demo.launch()
