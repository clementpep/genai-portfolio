"""
SmolAgent Backend for Clement's GenAI & Agentic Portfolio
Uses custom tools to query portfolio data and provide intelligent responses
"""

from smolagents import CodeAgent, InferenceClientModel, tool
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import yaml
import json
import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI
app = FastAPI(title="Portfolio SmolAgent Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Portfolio data store (same as before but structured for tools)
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
        {
            "id": "exp3",
            "title": "Serveurs MCP",
            "client": "Client Transport Confidentiel",
            "sector": "Transport",
            "duration": "4 mois",
            "period": "2024-09",
            "technologies": [
                "MCP",
                "LibreChat",
                "Azure AKS",
                "Microsoft Graph",
                "Python",
            ],
            "description": "3 serveurs MCP: Bing Search, Microsoft Graph M365, Python Interpreter. Déploiement Azure AKS.",
            "impact": "Automatisation complète processus recherche et documentation",
        },
        {
            "id": "exp4",
            "title": "Workflow Multi-Agents Dataiku",
            "client": "ALSTOM",
            "sector": "Transport",
            "duration": "4 mois",
            "period": "2024-06",
            "technologies": ["Dataiku LLM Mesh", "Multi-Agent", "GenAI"],
            "description": "Pipeline 12 agents Dataiku LLM Mesh. Validation automatique 80K+ Purchase Requisitions/an.",
            "impact": "Économie 50 ETP, projet vitrine COMEX",
        },
        {
            "id": "exp5",
            "title": "Server MCP PowerPoint",
            "client": "Wavestone",
            "sector": "Produit Interne",
            "duration": "4 mois",
            "period": "2024-05",
            "technologies": ["MCP", "Docker", "Azure", "Copilot Studio", "MCPOps"],
            "description": "Produit GenAI interne génération PowerPoint. CI/CD Azure avec MCP Shield.",
            "impact": "6000+ utilisateurs, gain productivité significatif",
        },
        {
            "id": "exp6",
            "title": "PoC GenAI Enquêtes",
            "client": "Wavestone",
            "sector": "Analytics",
            "duration": "6 mois",
            "period": "2024-03",
            "technologies": ["LlamaIndex", "GPT4", "Streamlit", "Azure OpenAI", "BERT"],
            "description": "Chatbot RAG analyse enquêtes satisfaction. Base vectorielle LlamaIndex, retrievers SPARSE/DENSE.",
            "impact": "POC transformé en solution production",
        },
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
            "n8n",
            "LangGraph",
        ],
        "Web Development": [
            "FastAPI",
            "Django",
            "Flask",
            "React",
            "Docker",
            "Azure (AKS, ACR, App Service)",
        ],
        "Data & ML": [
            "Python",
            "TensorFlow",
            "PyTorch",
            "Scikit-learn",
            "Pandas",
            "PySpark",
        ],
        "Cloud & DevOps": [
            "Azure",
            "Docker",
            "Kubernetes",
            "CI/CD",
            "GitLab",
            "GitHub Actions",
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


# Custom Tools for SmolAgent
@tool
def list_experiences(
    client: Optional[str] = None,
    sector: Optional[str] = None,
    technology: Optional[str] = None,
    period: Optional[str] = None,
) -> str:
    """List Clement's professional experiences with optional filtering.

    Args:
        client: Filter by client name (e.g., 'Wavestone', 'ALSTOM')
        sector: Filter by sector (e.g., 'Transport', 'Digital Transformation')
        technology: Filter by technology used (e.g., 'MCP', 'Azure')
        period: Filter by time period (e.g., '2024')
    """
    experiences = PORTFOLIO_DATA["experiences"]

    # Apply filters
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
    if period:
        experiences = [e for e in experiences if period in e["period"]]

    if not experiences:
        return "Aucune expérience trouvée avec ces critères."

    result = f"J'ai trouvé {len(experiences)} expérience(s):\n\n"
    for exp in experiences:
        result += f"**{exp['title']}** chez {exp['client']} ({exp['duration']}, {exp['period']})\n"
        result += f"  Secteur: {exp['sector']}\n"
        result += f"  Description: {exp['description']}\n"
        result += f"  Impact: {exp['impact']}\n"
        result += f"  Technologies: {', '.join(exp['technologies'])}\n\n"

    return result


@tool
def get_skills(category: Optional[str] = None) -> str:
    """Get Clement's technical skills, optionally filtered by category.

    Args:
        category: Skill category like 'Agents', 'GenAI', 'Web', 'Data', 'Cloud'
    """
    skills = PORTFOLIO_DATA["skills"]

    if category:
        # Find matching category
        matching_categories = [
            k for k in skills.keys() if category.lower() in k.lower()
        ]
        if matching_categories:
            result = f"Compétences en {matching_categories[0]}:\n"
            result += "• " + "\n• ".join(skills[matching_categories[0]])
            return result
        else:
            return f"Aucune catégorie de compétences trouvée pour '{category}'"

    # Return all skills
    result = "Voici l'ensemble de mes compétences techniques:\n\n"
    for category, items in skills.items():
        result += f"**{category}:**\n"
        result += "• " + "\n• ".join(items) + "\n\n"

    return result


@tool
def get_certifications() -> str:
    """Get all of Clement's certifications."""
    certs = PORTFOLIO_DATA["certifications"]

    result = "Mes certifications:\n\n"
    for cert in certs:
        result += f"• **{cert['name']}** - {cert['issuer']} ({cert['year']})\n"

    return result


@tool
def get_education() -> str:
    """Get Clement's educational background."""
    education = PORTFOLIO_DATA["education"]

    result = "Ma formation académique:\n\n"
    for edu in education:
        result += f"**{edu['school']}** - {edu['degree']} ({edu['year']})\n"
        if "achievement" in edu:
            result += f"  Réussite: {edu['achievement']}\n"
        if "focus" in edu:
            result += f"  Spécialisation: {edu['focus']}\n"
        result += "\n"

    return result


@tool
def search_portfolio(query: str) -> str:
    """Search across all portfolio content for relevant information.

    Args:
        query: Search query (e.g., 'Azure', 'multi-agent', 'hackathon')
    """
    query_lower = query.lower()
    results = []

    # Search in experiences
    for exp in PORTFOLIO_DATA["experiences"]:
        if (
            query_lower in exp["title"].lower()
            or query_lower in exp["description"].lower()
            or query_lower in exp["client"].lower()
            or any(query_lower in tech.lower() for tech in exp["technologies"])
        ):
            results.append(
                f"Expérience: {exp['title']} chez {exp['client']} - {exp['description'][:100]}..."
            )

    # Search in skills
    for category, skills_list in PORTFOLIO_DATA["skills"].items():
        matching_skills = [s for s in skills_list if query_lower in s.lower()]
        if matching_skills:
            results.append(f"Compétences en {category}: {', '.join(matching_skills)}")

    # Search in certifications
    for cert in PORTFOLIO_DATA["certifications"]:
        if query_lower in cert["name"].lower() or query_lower in cert["issuer"].lower():
            results.append(f"Certification: {cert['name']} ({cert['issuer']})")

    if not results:
        return f"Aucun résultat trouvé pour '{query}'"

    return f"Résultats pour '{query}':\n\n• " + "\n• ".join(results)


@tool
def analyze_expertise_match(requirements: str) -> str:
    """Analyze how Clement's profile matches specific requirements or job description.

    Args:
        requirements: Description of requirements or skills needed
    """
    req_lower = requirements.lower()
    matches = {"experiences": [], "skills": [], "certifications": []}

    # Keywords to search for
    keywords = req_lower.split()

    # Check experiences
    for exp in PORTFOLIO_DATA["experiences"]:
        exp_text = f"{exp['title']} {exp['description']} {' '.join(exp['technologies'])}".lower()
        if any(keyword in exp_text for keyword in keywords):
            matches["experiences"].append(exp["title"])

    # Check skills
    for category, skills_list in PORTFOLIO_DATA["skills"].items():
        for skill in skills_list:
            if any(keyword in skill.lower() for keyword in keywords):
                matches["skills"].append(skill)

    # Check certifications
    for cert in PORTFOLIO_DATA["certifications"]:
        if any(keyword in cert["name"].lower() for keyword in keywords):
            matches["certifications"].append(cert["name"])

    # Build response
    result = f"Analyse de correspondance pour: {requirements}\n\n"

    if matches["experiences"]:
        result += f"**Expériences pertinentes ({len(matches['experiences'])}):**\n"
        result += "• " + "\n• ".join(matches["experiences"][:5]) + "\n\n"

    if matches["skills"]:
        result += f"**Compétences correspondantes ({len(matches['skills'])}):**\n"
        result += "• " + "\n• ".join(matches["skills"][:10]) + "\n\n"

    if matches["certifications"]:
        result += f"**Certifications pertinentes:**\n"
        result += "• " + "\n• ".join(matches["certifications"]) + "\n\n"

    if not any(matches.values()):
        result += "Aucune correspondance directe trouvée, mais je peux acquérir rapidement de nouvelles compétences!"
    else:
        match_score = (
            len(matches["experiences"]) * 3
            + len(matches["skills"]) * 2
            + len(matches["certifications"]) * 2
        )
        if match_score > 15:
            result += "✅ **Excellente correspondance!** Mon profil correspond très bien aux besoins."
        elif match_score > 8:
            result += "👍 **Bonne correspondance!** J'ai plusieurs compétences et expériences pertinentes."
        else:
            result += (
                "💡 **Correspondance partielle** avec potentiel d'évolution rapide."
            )

    return result


@tool
def get_recent_projects(months: int = 6) -> str:
    """Get Clement's most recent projects within specified months.

    Args:
        months: Number of months to look back (default: 6)
    """
    # Calculate cutoff date
    current_date = datetime.datetime(2025, 1, 1)  # Adjust as needed

    # Sort experiences by period (most recent first)
    sorted_experiences = sorted(
        PORTFOLIO_DATA["experiences"], key=lambda x: x["period"], reverse=True
    )

    # Take top N recent projects
    recent_projects = sorted_experiences[: min(months // 2, len(sorted_experiences))]

    if not recent_projects:
        return "Aucun projet récent trouvé."

    result = f"Mes {len(recent_projects)} projets les plus récents:\n\n"
    for i, exp in enumerate(recent_projects, 1):
        result += f"{i}. **{exp['title']}** ({exp['period']})\n"
        result += f"   Client: {exp['client']}\n"
        result += f"   Impact: {exp['impact']}\n"
        result += f"   Tech stack: {', '.join(exp['technologies'][:5])}\n\n"

    return result


# Initialize SmolAgent
final_answer = FinalAnswerTool()

# System prompt for the agent
SYSTEM_PROMPT = {
    "system": """Tu es l'assistant IA personnel de Clément, expert GenAI & Agentic AI.
    
Tu as accès à toutes les informations sur son profil professionnel:
- Expériences en GenAI, agents, MCP, et transformation digitale
- Compétences techniques (SmolAgent, Azure AI, LangChain, etc.)
- Certifications (Azure AI Engineer, Dataiku GenAI, HuggingFace MCP)
- Formation (Arts & Métiers, ETS Montréal)

Ton rôle est de:
1. Présenter le profil de Clément de manière valorisante et pertinente
2. Mettre en avant ses expériences les plus adaptées aux questions
3. Suggérer comment ses compétences peuvent répondre aux besoins
4. Être professionnel mais accessible

Utilise les outils disponibles pour fournir des informations précises et actualisées.
Réponds en français de préférence, sauf si on te parle en anglais.""",
    "user": "{{query}}",
    "assistant": "{{agent_response}}",
}

# Create agent instance
model = InferenceClientModel(
    model_id="Qwen/Qwen2.5-Coder-32B-Instruct",
    token=None,  # Will use HF_TOKEN from environment
)

agent = CodeAgent(
    model=model,
    tools=[
        list_experiences,
        get_skills,
        get_certifications,
        get_education,
        search_portfolio,
        analyze_expertise_match,
        get_recent_projects,
        final_answer,
    ],
    max_steps=8,
    verbosity_level=1,
    prompt_templates=SYSTEM_PROMPT,
)


# API Endpoints
class ChatRequest(BaseModel):
    message: str
    history: Optional[List[Dict[str, str]]] = None


class ChatResponse(BaseModel):
    response: str


@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """
    Chat endpoint for the portfolio assistant
    """
    try:
        # Run agent with the user query
        result = agent.run(request.message)

        # Extract the response (final_answer content)
        if isinstance(result, dict) and "output" in result:
            response = result["output"]
        else:
            response = str(result)

        return ChatResponse(response=response)

    except Exception as e:
        logger.error(f"Error in chat endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "agent": "SmolAgent Portfolio Assistant",
        "model": "Qwen2.5-Coder-32B",
        "tools_count": len(agent.tools),
    }


@app.get("/api/tools")
async def list_tools():
    """List available tools for debugging"""
    return {
        "tools": [tool.name for tool in agent.tools],
        "description": "Tools available for querying Clement's portfolio",
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
