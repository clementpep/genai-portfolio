# hybrid_app.py - Hybrid Gradio + React integration
"""
Hybrid application combining React frontend with SmolAgent backend
Serves both Gradio interface and React app in iframes
"""

import gradio as gr
from smolagents import CodeAgent, InferenceClientModel, tool
import subprocess
import os
import time
import json
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
import uvicorn
from threading import Thread

# Initialize FastAPI for serving React build
fastapi_app = FastAPI()

fastapi_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Portfolio data
PORTFOLIO_DATA = {
    "experiences": [
        # Copy all experiences from previous artifacts
    ],
    "skills": {
        # Copy all skills
    },
    "certifications": [
        # Copy all certifications
    ],
    "education": [
        # Copy all education
    ],
}


# SmolAgent tools (same as before)
@tool
def list_experiences(client: str = None, technology: str = None) -> str:
    """List Clement's experiences"""
    # Implementation from previous artifact
    pass


@tool
def get_skills(category: str = None) -> str:
    """Get technical skills"""
    # Implementation
    pass


@tool
def search_portfolio(query: str) -> str:
    """Search portfolio content"""
    # Implementation
    pass


# Initialize SmolAgent
model = InferenceClientModel(model_id="Qwen/Qwen2.5-Coder-32B-Instruct")
agent = CodeAgent(
    model=model, tools=[list_experiences, get_skills, search_portfolio], max_steps=6
)


# API endpoint for React chat
@fastapi_app.post("/api/chat")
async def react_chat(request: Request):
    data = await request.json()
    message = data.get("message", "")

    try:
        result = agent.run(message)
        response = (
            result.get("output", str(result))
            if isinstance(result, dict)
            else str(result)
        )
        return JSONResponse({"response": response})
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)


# Serve React build files
if os.path.exists("frontend/build"):
    fastapi_app.mount("/static", StaticFiles(directory="frontend/build"), name="static")


# Start FastAPI server in background
def run_fastapi():
    uvicorn.run(fastapi_app, host="0.0.0.0", port=8001)


# Main Gradio interface
def create_gradio_interface():
    with gr.Blocks(
        title="Clément - Portfolio GenAI & Agentic",
        theme=gr.themes.Soft(),
        css="""
        .tab-nav button {
            font-size: 1.1rem !important;
            padding: 0.75rem 1.5rem !important;
        }
        .gradio-container {
            max-width: 1600px !important;
        }
        """,
    ) as demo:

        gr.HTML(
            """
            <div style="background: linear-gradient(135deg, #667eea, #764ba2); 
                        padding: 2rem; border-radius: 12px; color: white; text-align: center; margin-bottom: 2rem;">
                <h1 style="font-size: 2.5rem; margin-bottom: 1rem;">
                    🚀 Portfolio GenAI & Agentic - Clément
                </h1>
                <p style="font-size: 1.2rem; opacity: 0.95;">
                    Expert GenAI | Tech Lead Agents & MCP | Azure AI Engineer
                </p>
            </div>
        """
        )

        with gr.Tabs():
            # Tab 1: Interactive React Portfolio
            with gr.TabItem("📱 Portfolio Interactif", id=0):
                gr.HTML(
                    """
                    <div style="height: 800px; width: 100%; border-radius: 12px; overflow: hidden; 
                                box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                        <iframe 
                            src="http://localhost:8001/static/index.html" 
                            width="100%" 
                            height="100%" 
                            frameborder="0"
                            style="border: none;">
                        </iframe>
                    </div>
                    <p style="text-align: center; margin-top: 1rem; opacity: 0.7;">
                        Interface React avec carrousel 3D, timeline interactive et chatbot intégré
                    </p>
                """
                )

            # Tab 2: SmolAgent Chat
            with gr.TabItem("🤖 Assistant IA Direct", id=1):
                with gr.Row():
                    with gr.Column(scale=2):
                        chatbot = gr.Chatbot(
                            label="Chat avec SmolAgent",
                            height=600,
                            bubble_full_width=False,
                        )

                        msg = gr.Textbox(
                            placeholder="Posez une question sur mes expériences, compétences...",
                            label="Votre message",
                        )

                        with gr.Row():
                            clear = gr.Button("🗑️ Effacer")
                            submit = gr.Button("📤 Envoyer", variant="primary")

                    with gr.Column(scale=1):
                        gr.Markdown(
                            """
                        ### 💡 Questions suggérées
                        
                        - Quels projets multi-agents as-tu réalisés ?
                        - Parle-moi de ton expérience avec MCP
                        - Quelles sont tes certifications GenAI ?
                        - Comment as-tu utilisé SmolAgent ?
                        - Quel est ton projet le plus impactant ?
                        
                        ### 🔧 Capacités de l'assistant
                        
                        L'assistant peut:
                        - Rechercher dans mes expériences
                        - Filtrer par technologie ou client
                        - Analyser les correspondances avec vos besoins
                        - Suggérer des projets pertinents
                        """
                        )

            # Tab 3: Portfolio Details
            with gr.TabItem("📊 Détails & Métriques", id=2):
                with gr.Row():
                    with gr.Column():
                        gr.Markdown(
                            """
                        ### 🏆 Réalisations clés
                        
                        | Projet | Impact | Technologies |
                        |--------|--------|--------------|
                        | Multi-Agents ALSTOM | 50 ETP économisés | Dataiku LLM Mesh |
                        | SentinelOne | 2e prix Hackathon | SmolAgent, LiteLLM |
                        | MCP Servers | 500+ utilisateurs | Azure AKS, LibreChat |
                        | GenAI Translation | Déploiement luxe | Mistral Large |
                        """
                        )

                    with gr.Column():
                        gr.Markdown(
                            """
                        ### 📈 Métriques
                        
                        - **6+ projets GenAI majeurs** en production
                        - **80,000+ validations/an** automatisées
                        - **6,000+ utilisateurs** produits internes
                        - **50+ pitchs GenAI** commerciaux
                        - **3 certifications** AI/Cloud
                        """
                        )

                gr.Markdown(
                    """
                ### 🛠️ Stack Technique Complète
                
                **Agents & Orchestration**
                ```
                Azure AI Agents | SmolAgent | FastMCP | MCP Shield
                Dataiku LLM Mesh | LibreChat | Copilot Studio
                ```
                
                **Frameworks GenAI**
                ```
                LangChain | LlamaIndex | LangGraph | n8n
                Azure AI Foundry | Azure AI Search | Ollama
                ```
                
                **Infrastructure & DevOps**
                ```
                Docker | Kubernetes | Azure (AKS, ACR, App Service)
                CI/CD | GitLab | GitHub Actions | Terraform
                ```
                """
                )

        # Chat functionality
        def respond(message, history):
            try:
                result = agent.run(message)
                response = (
                    result.get("output", str(result))
                    if isinstance(result, dict)
                    else str(result)
                )
                history.append((message, response))
                return "", history
            except Exception as e:
                history.append((message, f"Erreur: {str(e)}"))
                return "", history

        msg.submit(respond, [msg, chatbot], [msg, chatbot])
        submit.click(respond, [msg, chatbot], [msg, chatbot])
        clear.click(lambda: None, None, chatbot, queue=False)

        return demo


# Main execution
if __name__ == "__main__":
    # Start FastAPI in background
    fastapi_thread = Thread(target=run_fastapi, daemon=True)
    fastapi_thread.start()
    time.sleep(2)  # Wait for FastAPI to start

    # Launch Gradio
    demo = create_gradio_interface()
    demo.launch(server_name="0.0.0.0", server_port=7860)
