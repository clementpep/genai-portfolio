"""
Premium GenAI Portfolio Application
Deployed on Hugging Face Spaces with Gradio
Enhanced with dark green/cream/gray premium design
Version: 2.2 - Fixed timeline navigation, chat styling, and HF model fallback system
"""

import gradio as gr
import yaml
import os
import base64
from typing import List, Dict, Optional, Tuple
from dotenv import load_dotenv
import requests
import time

# Load environment variables
load_dotenv()

logos_path = os.path.join(os.path.dirname(__file__), "logos")

# Determine which LLM to use based on environment
USE_HF_MODEL = os.getenv("USE_HF_MODEL", "true").lower() == "true"
USE_SMOLAGENT_WITH_LITELLM = (
    os.getenv("USE_SMOLAGENT_WITH_LITELLM", "false").lower() == "true"
)

# Free HuggingFace models to try in order of preference
FREE_HF_MODELS = [
    "Qwen/Qwen2.5-Coder-32B-Instruct",
    "HuggingFaceH4/zephyr-7b-beta",
]

if USE_HF_MODEL or USE_SMOLAGENT_WITH_LITELLM:
    from smolagents import CodeAgent, tool

    if USE_HF_MODEL:
        from smolagents import InferenceClientModel
    else:
        from smolagents import LiteLLMModel
else:
    from litellm import completion


def load_portfolio_data() -> Dict:
    """
    Load portfolio data from YAML configuration file

    Returns:
        Dict: Portfolio configuration including experiences, skills, certifications, education
    """
    with open("portfolio_data.yaml", "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


PORTFOLIO = load_portfolio_data()

# Technology links for clickable logos - comprehensive mapping
TECH_LINKS = {
    "azure ai foundry": "https://ai.azure.com/",
    "azure ai search": "https://azure.microsoft.com/en-us/products/ai-services/ai-search/",
    "azure": "https://azure.microsoft.com/",
    "azure kubernetes": "https://azure.microsoft.com/en-us/products/kubernetes-service/",
    "mistral": "https://mistral.ai/",
    "react": "https://react.dev/",
    "flask": "https://flask.palletsprojects.com/",
    "docker": "https://www.docker.com/",
    "power automate": "https://powerautomate.microsoft.com/",
    "copilot studio": "https://www.microsoft.com/en-us/microsoft-copilot/microsoft-copilot-studio",
    "teams": "https://www.microsoft.com/en-us/microsoft-teams/group-chat-software",
    "smolagent": "https://github.com/huggingfaceh4/smolagents",
    "litellm": "https://docs.litellm.ai/",
    "gradio": "https://gradio.app/",
    "mcp": "https://modelcontextprotocol.io/",
    "librechat": "https://librechat.ai/",
    "microsoft graph": "https://developer.microsoft.com/en-us/graph",
    "mcp shield": "https://github.com/modelcontextprotocol/servers",
    "dataiku": "https://www.dataiku.com/",
    "ariba": "https://www.sap.com/products/spend-management/procurement-solutions.html",
}

# Premium color scheme - Luxury Dark Green, Cream, Light Gray
COLORS = {
    "primary": "#1f4135",  # Premium dark green
    "primary_light": "#2d5949",  # Lighter premium green
    "secondary": "#F5F5DC",  # Cream/Beige
    "accent": "#7fa890",  # Sage green accent
    "background": "#f8f9fa",  # Light gray background
    "surface": "#ffffff",  # White surface
    "surface_elevated": "#ffffff",  # Elevated white surface
    "text_primary": "#1a1a1a",  # Dark gray text
    "text_secondary": "#6c757d",  # Medium gray text
    "text_muted": "#adb5bd",  # Muted gray
    "gradient_start": "#1f4135",
    "gradient_end": "#2d5949",
    "border": "#dee2e6",  # Light border
    "shadow": "rgba(31, 65, 53, 0.1)",
}

# Custom CSS for premium stone-textured design with image fixes and rounded chat components
CUSTOM_CSS = f"""
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=Inter:wght@300;400;500;600&display=swap');

.gradio-container {{
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    background-image: url('/logos/textures/metal_brushed.png') !important;
    background-color: {COLORS['background']};
    background-repeat: repeat;
    background-size: auto;
    background-position: center center !important;
    background-blend-mode: multiply;
    max-width: 1400px !important;
    margin: 0 auto !important;
    padding: 2rem !important;
}}

.premium-header {{
    background: linear-gradient(135deg, {COLORS['gradient_start']}, {COLORS['gradient_end']});
    padding: 3.5rem 2.5rem;
    border-radius: 24px;
    text-align: center;
    margin-bottom: 3rem;
    box-shadow: 0 10px 40px {COLORS['shadow']}, 0 2px 8px rgba(0, 0, 0, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.2);
}}

.premium-header h1 {{
    color: white;
    font-family: 'Playfair Display', serif;
    font-size: 3rem;
    font-weight: 700;
    margin-bottom: 0.75rem;
    letter-spacing: -0.02em;
}}

.premium-header p {{
    color: rgba(255, 255, 255, 0.95);
    font-size: 1.1rem;
    font-weight: 400;
    line-height: 1.6;
}}

.social-links {{
    display: flex;
    justify-content: center;
    gap: 1.5rem;
    margin-top: 2rem;
}}

.social-link {{
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.75rem 1.5rem;
    background: rgba(255, 255, 255, 0.15);
    border: 1px solid rgba(255, 255, 255, 0.3);
    border-radius: 16px;
    color: white;
    text-decoration: none;
    transition: all 0.3s ease;
    font-weight: 500;
    backdrop-filter: blur(10px);
}}

.social-link:hover {{
    background: white;
    color: {COLORS['primary']};
    transform: translateY(-2px);
    box-shadow: 0 8px 20px rgba(255, 255, 255, 0.3);
}}

/* Carousel / card sizing improvements */
.carousel-wrapper {{
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 1.5rem;
    margin: 2rem 0;
    min-height: 480px;
    width: 100%;
}}

.carousel-container {{
    flex: 6;
    max-width: 1100px;
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
    perspective: 1000px;
    padding: 0 1rem;
}}

.card {{
    background: {COLORS['surface']};
    border-radius: 24px;
    padding: 2.5rem;
    width: 100%;
    max-width: 1000px;
    min-height: 420px;
    box-shadow: 0 4px 20px {COLORS['shadow']}, 0 1px 3px rgba(0, 0, 0, 0.05);
    border: 1px solid {COLORS['border']};
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    display: flex;
    flex-direction: column;
    margin: 0 auto;
}}

.card:hover {{
    transform: translateY(-4px);
    box-shadow: 0 12px 40px {COLORS['shadow']}, 0 4px 12px rgba(0, 0, 0, 0.08);
    border-color: {COLORS['primary_light']};
}}

.card-header {{
    display: flex;
    align-items: flex-start;
    gap: 1.5rem;
    margin-bottom: 1.5rem;
    padding-bottom: 1.5rem;
    border-bottom: 2px solid {COLORS['border']};
}}

/* Fixed logo container with proper aspect ratio preservation */
.card-logo {{
    width: 80px;
    height: 80px;
    border-radius: 20px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: {COLORS['surface']};
    border: 2px solid {COLORS['border']};
    font-size: 2.5rem;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
    flex-shrink: 0;
    transition: all 0.3s ease;
    overflow: hidden;
}}

.card-logo:hover {{
    border-color: {COLORS['primary_light']};
    box-shadow: 0 4px 12px {COLORS['shadow']};
}}

/* Fixed logo image aspect ratio */
.card-logo img {{
    width: 100%;
    height: 100%;
    object-fit: contain;
    border-radius: 14px;
    background: transparent;
    padding: 6px;
}}

.card-title {{
    font-family: 'Playfair Display', serif;
    font-size: 1.75rem;
    font-weight: 600;
    color: {COLORS['text_primary']};
    margin-bottom: 0.5rem;
    line-height: 1.3;
}}

.card-subtitle {{
    color: {COLORS['primary']};
    font-weight: 500;
    font-size: 1rem;
}}

.card-content {{
    color: {COLORS['text_secondary']};
    line-height: 1.7;
    margin-bottom: 1.5rem;
    font-size: 0.95rem;
    flex: 1;
}}

.card-meta {{
    display: flex;
    align-items: center;
    gap: 0.5rem;
    color: {COLORS['text_muted']};
    font-size: 0.9rem;
    margin-bottom: 1rem;
}}

/* Fixed tech badge images */
.tech-badge {{
    display: inline-flex;
    align-items: center;
    justify-content: center;
    padding: 0.6rem;
    background: rgba(31, 65, 53, 0.08);
    border: 1px solid {COLORS['border']};
    border-radius: 20px;
    color: {COLORS['primary']};
    font-size: 0.85rem;
    font-weight: 500;
    margin: 0.3rem;
    transition: all 0.3s ease;
    cursor: help;
    text-decoration: none;
}}

.tech-badge:hover {{
    background: {COLORS['primary']};
    color: white;
    transform: translateY(-2px);
    box-shadow: 0 4px 12px {COLORS['shadow']};
    text-decoration: none;
}}

.tech-badge a, .tech-badge a:visited {{
    color: inherit;
    text-decoration: none;
}}

/* Fixed tech badge images with proper sizing */
.tech-badge img {{
    width: 28px;
    height: 28px;
    min-height: 28px;
    max-height: 28px;
    object-fit: contain;
    border-radius: 4px;
    display: block;
}}

.tech-badges-container {{
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 0.5rem;
    margin-top: auto;
    padding-top: 1rem;
}}

.timeline {{
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 3rem;
    padding: 2.5rem 0;
    position: relative;
    margin-top: 2rem;
    overflow-x: auto;
    padding-bottom: 1.5rem;
}}

.timeline::before {{
    content: '';
    position: absolute;
    top: calc(2.5rem + 10px);
    left: 0;
    width: 100%;
    height: 3px;
    background: linear-gradient(90deg, 
        transparent, 
        {COLORS['border']},
        {COLORS['primary_light']},
        {COLORS['border']},
        transparent);
    z-index: 0;
}}

/* Timeline buttons - invisible but clickable */
.timeline-btn {{
    background: transparent !important;
    border: none !important;
    padding: 0 !important;
    margin: 0 !important;
    width: auto !important;
    height: auto !important;
    box-shadow: none !important;
    cursor: pointer !important;
}}

.timeline-btn:hover {{
    background: transparent !important;
    transform: none !important;
}}

.timeline-item {{
    display: flex;
    flex-direction: column;
    align-items: center;
    cursor: pointer;
    transition: all 0.3s ease;
    position: relative;
    z-index: 1;
    flex: 0 0 auto;
    min-width: 50px;
}}

.timeline-dot {{
    width: 20px;
    height: 20px;
    border-radius: 50%;
    background: {COLORS['surface']};
    border: 3px solid {COLORS['border']};
    transition: all 0.3s ease;
    margin-bottom: 0.75rem;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}}

.timeline-item:hover .timeline-dot {{
    transform: scale(1.2);
    border-color: {COLORS['primary_light']};
    box-shadow: 0 4px 12px {COLORS['shadow']};
}}

.timeline-item.active .timeline-dot {{
    background: linear-gradient(135deg, {COLORS['gradient_start']}, {COLORS['gradient_end']});
    border-color: {COLORS['primary']};
    transform: scale(1.5);
    box-shadow: 0 0 20px {COLORS['shadow']}, 0 0 40px rgba(31, 65, 53, 0.3);
}}

.timeline-label {{
    font-size: 0.8rem;
    color: {COLORS['text_muted']};
    white-space: nowrap;
    transition: all 0.3s ease;
    font-weight: 500;
}}

.timeline-item:hover .timeline-label {{
    color: {COLORS['text_secondary']};
}}

.timeline-item.active .timeline-label {{
    color: {COLORS['primary']};
    font-weight: 600;
    font-size: 0.9rem;
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
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05) !important;
}}

.nav-button:hover {{
    background: {COLORS['primary']} !important;
    color: white !important;
    border-color: {COLORS['primary']} !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px {COLORS['shadow']} !important;
}}

/* Carousel nav buttons: perfect circle, fixed size */
.carousel-nav-btn {{
    width: 56px !important;
    height: 56px !important;
    min-width: 56px !important;
    max-width: 56px !important;
    min-height: 56px !important;
    max-height: 56px !important;
    border-radius: 50% !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    color: {COLORS['text_primary']} !important;
    font-size: 1.25rem !important;
    cursor: pointer !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 4px 16px rgba(0,0,0,0.08) !important;
    padding: 0 !important;
    margin: 0 !important;
    background: {COLORS['surface']} !important;
    border: 2px solid {COLORS['border']} !important;
    flex-shrink: 0 !important;
    flex-grow: 0 !important;
    overflow: hidden !important;
}}

.carousel-nav-btn:hover {{
    background: {COLORS['primary']} !important;
    color: white !important;
    transform: scale(1.06) !important;
    border-color: {COLORS['primary_light']} !important;
}}

.stats-container {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 1.5rem;
    margin: 2.5rem 0 3rem 0;
}}

.stat-card {{
    background: {COLORS['surface']};
    border: 2px solid {COLORS['border']};
    border-radius: 24px;
    padding: 2rem 1.5rem;
    text-align: center;
    transition: all 0.3s ease;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}}

.stat-card:hover {{
    transform: translateY(-4px);
    border-color: {COLORS['primary_light']};
    box-shadow: 0 8px 24px {COLORS['shadow']};
}}

.stat-value {{
    font-family: 'Playfair Display', serif;
    font-size: 2.75rem;
    font-weight: 700;
    color: {COLORS['primary']};
    margin-bottom: 0.5rem;
}}

.stat-label {{
    color: {COLORS['text_secondary']};
    font-size: 0.95rem;
    font-weight: 500;
}}

/* Chat container with rounded edges */
.chat-container {{
    background: {COLORS['surface']};
    border: 2px solid {COLORS['border']};
    border-radius: 24px;
    padding: 2.5rem;
    margin-top: 3rem;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
}}

.chat-header {{
    font-family: 'Playfair Display', serif;
    font-size: 1.8rem;
    color: {COLORS['text_primary']};
    margin-bottom: 1.5rem;
    display: flex;
    align-items: center;
    gap: 1rem;
}}

/* Fixed wavebot logo proportions */
.chat-header .wavebot-logo {{
    width: 48px;
    height: 48px;
    border-radius: 12px;
    flex-shrink: 0;
    object-fit: contain;
    padding: 4px;
    background: white;
    border: 1px solid {COLORS['border']};
}}

.chat-header .agent-name {{
    font-weight: 700;
    color: {COLORS['primary']};
}}

/* Chatbot component styling with rounded edges */
.gradio-chatbot {{
    border-radius: 20px !important;
    border: 2px solid {COLORS['border']} !important;
    background: {COLORS['surface']} !important;
    overflow: hidden !important;
}}

.gradio-chatbot .message {{
    border-radius: 16px !important;
}}

/* Chat input area styling with rounded edges */
.chat-input-container {{
    background: {COLORS['surface']} !important;
    border-radius: 16px !important;
    border: 2px solid {COLORS['border']} !important;
    padding: 0.5rem !important;
    margin-top: 1rem !important;
}}

button.primary {{
    background: linear-gradient(135deg, {COLORS['gradient_start']}, {COLORS['gradient_end']}) !important;
    border: none !important;
    color: white !important;
}}

button.primary:hover {{
    box-shadow: 0 6px 20px {COLORS['shadow']} !important;
    transform: translateY(-1px) !important;
}}

.gr-button {{
    border-radius: 12px !important;
    font-weight: 500 !important;
    transition: all 0.3s ease !important;
}}

.gr-input, .gr-textbox {{
    background: {COLORS['surface']} !important;
    border: 2px solid {COLORS['border']} !important;
    border-radius: 12px !important;
    color: {COLORS['text_primary']} !important;
    transition: all 0.3s ease !important;
}}

.gr-input:focus, .gr-textbox:focus {{
    border-color: {COLORS['primary']} !important;
    box-shadow: 0 0 0 3px rgba(31, 65, 53, 0.1) !important;
}}

/* Footer styling */
.footer {{
    text-align: center;
    margin-top: 4rem;
    padding: 2.5rem;
    border-top: 2px solid {COLORS['border']};
    background: {COLORS['surface']};
    border-radius: 24px;
}}

/* Send button styling */
#send-btn {{
    height: 48px !important;
    min-height: 48px !important;
    border-radius: 12px !important;
    padding: 0 14px !important;
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
    margin-left: 0.5rem !important;
    background: linear-gradient(135deg, {COLORS['gradient_start']}, {COLORS['gradient_end']}) !important;
    color: white !important;
    border: none !important;
    box-shadow: 0 6px 20px {COLORS['shadow']} !important;
}}

/* Improved spacing */
.gradio-container > * {{
    animation: fadeIn 0.6s ease-in-out;
}}

@keyframes fadeIn {{
    from {{
        opacity: 0;
        transform: translateY(10px);
    }}
    to {{
        opacity: 1;
        transform: translateY(0);
    }}
}}


/* Better card shadows on hover */
.card::after {{
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    border-radius: 24px;
    background: linear-gradient(135deg, transparent, rgba(31, 65, 53, 0.03));
    opacity: 0;
    transition: opacity 0.3s ease;
    pointer-events: none;
}}

.card:hover::after {{
    opacity: 1;
}}

/* Skill card specific styling */
.skills-card-content {{
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
    gap: 1rem;
    width: 100%;
}}

.skill-item {{
    background: rgba(31, 65, 53, 0.05);
    border-radius: 12px;
    padding: 0.75rem 1rem;
    color: {COLORS['text_primary']};
    font-size: 0.9rem;
    transition: all 0.3s ease;
}}

.skill-item:hover {{
    background: rgba(31, 65, 53, 0.1);
    transform: translateY(-2px);
}}

/* Education card specific styling */
.card-location {{
    color: {COLORS['text_muted']};
    font-size: 0.9rem;
    font-style: italic;
    margin-top: 0.25rem;
}}

/* Responsive adjustments */
@media (max-width: 768px) {{
    .premium-header {{
        padding: 2rem 1.5rem;
    }}
    
    .premium-header h1 {{
        font-size: 2.2rem;
    }}
    
    .social-links {{
        flex-direction: column;
        gap: 0.75rem;
    }}
    
    .carousel-wrapper {{
        flex-direction: column;
        gap: 1rem;
    }}
    
    .carousel-nav-btn {{
        margin: 0 auto;
    }}
    
    .card {{
        padding: 1.5rem;
        min-height: auto;
    }}
    
    .card-header {{
        flex-direction: column;
        align-items: center;
        text-align: center;
        gap: 1rem;
    }}
    
    .stats-container {{
        grid-template-columns: 1fr;
    }}
    
    .timeline {{
        gap: 1.5rem;
        justify-content: flex-start;
        padding-left: 1rem;
        padding-right: 1rem;
    }}
    
    .timeline-item {{
        min-width: 40px;
    }}
    
    .timeline-label {{
        font-size: 0.7rem;
    }}
    
    .nav-button {{
        padding: 0.75rem 1rem !important;
        font-size: 0.9rem !important;
    }}
    
    .chat-header {{
        font-size: 1.5rem;
    }}
}}

/* Skills card styling */
.category-title {{
    font-family: 'Playfair Display', serif;
    font-size: 1.5rem;
    font-weight: 600;
    color: {COLORS['primary']};
    margin-bottom: 1.25rem;
    display: flex;
    align-items: center;
    gap: 0.75rem;
}}

.category-icon {{
    font-size: 1.75rem;
}}

.skills-list {{
    list-style: none;
    padding: 0;
    margin: 0;
}}

.skills-list li {{
    position: relative;
    padding-left: 1.5rem;
    margin-bottom: 0.75rem;
    color: {COLORS['text_secondary']};
    line-height: 1.6;
}}

.skills-list li::before {{
    content: '•';
    position: absolute;
    left: 0;
    color: {COLORS['primary']};
    font-weight: bold;
}}

"""


def embed_image_base64(rel_path: str) -> Optional[str]:
    """
    Convert a local image file into a base64-embedded data URI string.

    Args:
        rel_path (str): Relative path to the image from repo root

    Returns:
        Optional[str]: Base64 data URI string or None if file not found
    """
    abs_path = os.path.join(os.path.dirname(__file__), rel_path)
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


# SmolAgent tools for portfolio interaction
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
        if "location" in edu:
            output += f"  Location: {edu['location']}\n"
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
        output += "Excellent Match: Strong alignment with requirements\n"
    elif matches["strength"] > 8:
        output += "Good Match: Relevant experience and skills\n"
    elif matches["strength"] > 3:
        output += "Partial Match: Some relevant experience\n"
    else:
        output += "Learning Opportunity: Fast learner ready to acquire new skills\n"

    return output


# Initialize agent based on environment with improved fallback system
if USE_HF_MODEL:
    # SmolAgent with HuggingFace (FREE) - with fallback
    hf_token = os.getenv("HF_TOKEN")
    working_model = FREE_HF_MODELS[0]

    if working_model:
        print(f"Using HuggingFace model: {working_model}")
        model = InferenceClientModel(
            model_id=working_model,
            temperature=0.7,
            token=hf_token,
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
    else:
        print("No working HF models found, falling back to LiteLLM")
        agent = None
        USE_HF_MODEL = False

elif USE_SMOLAGENT_WITH_LITELLM:
    # SmolAgent with LiteLLM backend (PAID but with tools)
    model = LiteLLMModel(
        model_id=os.getenv("LITELLM_MODEL", "gpt-4o-mini"),
        api_key=os.getenv("OPENAI_API_KEY"),
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
else:
    # Pure LiteLLM without tools (PAID but faster)
    agent = None


def chat_with_agent(message: str, history: List) -> Tuple[str, List]:
    """
    Process chat message using SmolAgent or LiteLLM with improved error handling

    Args:
        message: User's message
        history: Chat history

    Returns:
        Tuple of (empty string for input, updated history)
    """
    try:
        if USE_HF_MODEL and agent:
            # Use SmolAgent with HF model
            result = agent.run(message)
            response = (
                result.get("output", str(result))
                if isinstance(result, dict)
                else str(result)
            )
        elif USE_SMOLAGENT_WITH_LITELLM and agent:
            # Use SmolAgent with LiteLLM backend
            result = agent.run(message)
            response = (
                result.get("output", str(result))
                if isinstance(result, dict)
                else str(result)
            )
        else:
            # Use pure LiteLLM without tools
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
                max_tokens=500,
            )

            response = llm_response.choices[0].message.content

        history.append((message, response))
        return "", history

    except Exception as e:
        error_msg = f"I encountered an error: {str(e)}. Please try again."
        history.append((message, error_msg))
        return "", history


def generate_card_html(item: Dict, category: str) -> str:
    """
    Generate HTML for a portfolio item card with improved logo handling.

    Args:
        item (Dict): Portfolio item data
        category (str): Category type (experiences, skills, certifications, education)

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
        # Fallback emoji or icon
        logo_html = f'<div style="font-size: 2.2rem;">{icon or "📌"}</div>'

    # Generate tech badges with logos and clickable links
    tech_badges_html = []
    for tech in techs[:6]:
        tech_name = tech if isinstance(tech, str) else str(tech)
        tech_base = (
            tech_name.lower()
            .replace(" ", "_")
            .replace("-", "_")
            .replace("/", "_")
            .replace(".", "_")
        )

        # Try multiple possible paths for tech logos
        logo_data = None
        logo_paths = [
            f"logos/technologies/{tech_base}.png",
            f"logos/technologies/{tech_base}.svg",
            f"logos/{tech_base}.png",
            f"logos/{tech_base}.svg",
        ]

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
    tech_badges = (
        f'<div class="tech-badges-container">{"".join(tech_badges_html)}</div>'
        if tech_badges_html
        else ""
    )

    # Build title section with improved layout
    if category == "certifications" and name:
        title_section = f"""
            <div style="flex: 1;">
                <div class="card-subtitle">{subtitle}</div>
                <div class="card-title" style="margin-top: 0.5rem;">{name}</div>
            </div>
        """
    elif category == "education":
        title_section = f"""
            <div style="flex: 1;">
                <div class="card-title">{title}</div>
                {f'<div class="card-subtitle">{subtitle}</div>' if subtitle else ''}
                {f'<div class="card-location">{location}</div>' if location else ''}
            </div>
        """
    else:
        title_section = f"""
            <div style="flex: 1;">
                <div class="card-title">{title}</div>
                {f'<div class="card-subtitle">{subtitle}</div>' if subtitle else ''}
            </div>
        """

    # Build meta information
    meta_html = ""
    if duration:
        meta_html += f'<div class="card-meta">📅 {duration}</div>'
    if impact:
        meta_html += f'<div class="card-meta">🎯 {impact}</div>'
    if achievement:
        meta_html += f'<div class="card-meta">🏅 {achievement}</div>'

    # Return final card HTML
    return f"""
    <div class="card">
        <div class="card-header">
            <div class="card-logo">{logo_html}</div>
            {title_section}
        </div>
        <div class="card-content">{description}</div>
        {meta_html}
        {tech_badges}
    </div>
    """


def generate_skills_card_html(skill_category: Dict) -> str:
    """
    Generate HTML specifically for skills cards

    Args:
        skill_category (Dict): Skills category data

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


def create_interface():
    """
    Create the main Gradio interface with fixed timeline functionality and improved chat styling

    Returns:
        gr.Blocks: Configured Gradio interface
    """

    with gr.Blocks(
        css=CUSTOM_CSS,
        theme=gr.themes.Soft(
            primary_hue=gr.themes.colors.emerald,
            secondary_hue=gr.themes.colors.stone,
            neutral_hue=gr.themes.colors.slate,
            font=[gr.themes.GoogleFont("Inter"), "system-ui", "sans-serif"],
        ),
        title="Clément Peponnet - Portfolio GenAI & Agentic",
    ) as app:

        # State variables for carousel navigation
        category_state = gr.State("experiences")

        # Get the most recent experience for initial display
        experiences = PORTFOLIO.get("experiences", [])
        if experiences:
            sorted_experiences = sorted(
                experiences,
                key=lambda x: x.get("date", x.get("period", "0000")),
                reverse=True,
            )
            most_recent_exp = sorted_experiences[0]
            initial_index = experiences.index(most_recent_exp)
        else:
            initial_index = 0

        index_state = gr.State(initial_index)

        # Header with social links
        gr.HTML(
            f"""
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
        )

        # Stats section
        gr.HTML(
            f"""
        <div class="stats-container">
            <div class="stat-card">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">🚀</div>
                <div class="stat-value">{len(PORTFOLIO['experiences'])}</div>
                <div class="stat-label">Projets GenAI majeurs</div>
            </div>
            <div class="stat-card">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">🏆</div>
                <div class="stat-value">{len(PORTFOLIO['certifications'])}</div>
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
        )

        # Navigation tabs
        with gr.Row():
            exp_btn = gr.Button("🚀 Expériences", elem_classes="nav-button")
            cert_btn = gr.Button("🏆 Certifications", elem_classes="nav-button")
            skills_btn = gr.Button("💡 Expertise & Skills", elem_classes="nav-button")
            edu_btn = gr.Button("🎓 Études", elem_classes="nav-button")

        # Carousel display with proper alignment
        gr.HTML('<div style="margin: 3rem 0 1rem 0;"></div>')  # Spacer

        # Carousel wrapper with improved layout
        with gr.Row(elem_classes="carousel-wrapper"):
            prev_btn = gr.Button("◀", elem_classes="carousel-nav-btn", scale=1)
            with gr.Column(scale=6, elem_classes="carousel-container"):
                # Display the most recent experience initially
                initial_experience = (
                    experiences[initial_index]
                    if experiences
                    else PORTFOLIO["experiences"][0]
                )
                carousel_html = gr.HTML(
                    generate_card_html(initial_experience, "experiences")
                )
            next_btn = gr.Button("▶", elem_classes="carousel-nav-btn", scale=1)

        # Timeline HTML display - Fixed implementation
        timeline_html = gr.HTML()

        # Navigation functions with improved error handling and fixed timeline
        def update_category(category: str):
            """Update the displayed category and show the most recent item"""
            items = PORTFOLIO.get(category, [])
            if items:
                sorted_items = sorted(
                    items,
                    key=lambda x: x.get("date", x.get("year", x.get("period", "0000"))),
                    reverse=True,
                )
                most_recent_item = sorted_items[0]
                most_recent_index = items.index(most_recent_item)

                card = generate_card_html(most_recent_item, category)

                # Generate timeline HTML with fixed JavaScript
                sorted_for_timeline = sorted(
                    enumerate(items),
                    key=lambda x: x[1].get(
                        "date", x[1].get("year", x[1].get("period", "0000"))
                    ),
                )

                timeline_items_html = []
                for idx, (original_index, item) in enumerate(sorted_for_timeline):
                    date = item.get("date", item.get("year", item.get("period", "")))
                    active_class = (
                        "active" if original_index == most_recent_index else ""
                    )

                    # Fixed timeline click handler with proper Gradio integration
                    timeline_items_html.append(
                        f"""
                    <div class="timeline-item {active_class}" 
                         onclick="document.querySelector('[data-timeline-index=\"{original_index}\"]').click()">
                        <div class="timeline-dot"></div>
                        <div class="timeline-label">{date}</div>
                    </div>
                    """
                    )

                timeline = f'<div class="timeline">{"".join(timeline_items_html)}</div>'

                return card, timeline, category, most_recent_index
            return carousel_html.value, timeline_html.value, category, 0

        def navigate_carousel(direction: int, category: str, current_index: int):
            """Navigate through carousel items"""
            items = PORTFOLIO.get(category, [])
            if not items:
                return carousel_html.value, timeline_html.value, current_index

            new_index = (current_index + direction) % len(items)
            card = generate_card_html(items[new_index], category)

            # Update timeline with proper active state
            sorted_for_timeline = sorted(
                enumerate(items),
                key=lambda x: x[1].get(
                    "date", x[1].get("year", x[1].get("period", "0000"))
                ),
            )

            timeline_items_html = []
            for idx, (original_index, item) in enumerate(sorted_for_timeline):
                date = item.get("date", item.get("year", item.get("period", "")))
                active_class = "active" if original_index == new_index else ""

                timeline_items_html.append(
                    f"""
                <div class="timeline-item {active_class}" 
                     onclick="document.querySelector('[data-timeline-index=\"{original_index}\"]').click()">
                    <div class="timeline-dot"></div>
                    <div class="timeline-label">{date}</div>
                </div>
                """
                )

            timeline = f'<div class="timeline">{"".join(timeline_items_html)}</div>'

            return card, timeline, new_index

        def jump_to_index(target_index: int, category: str):
            """Jump to specific index from timeline click"""
            items = PORTFOLIO.get(category, [])
            if not items or target_index >= len(items):
                return carousel_html.value, timeline_html.value, index_state.value

            card = generate_card_html(items[target_index], category)

            # Update timeline with proper active state
            sorted_for_timeline = sorted(
                enumerate(items),
                key=lambda x: x[1].get(
                    "date", x[1].get("year", x[1].get("period", "0000"))
                ),
            )

            timeline_items_html = []
            for idx, (original_index, item) in enumerate(sorted_for_timeline):
                date = item.get("date", item.get("year", item.get("period", "")))
                active_class = "active" if original_index == target_index else ""

                timeline_items_html.append(
                    f"""
                <div class="timeline-item {active_class}" 
                     onclick="document.querySelector('[data-timeline-index=\"{original_index}\"]').click()">
                    <div class="timeline-dot"></div>
                    <div class="timeline-label">{date}</div>
                </div>
                """
                )

            timeline = f'<div class="timeline">{"".join(timeline_items_html)}</div>'

            return card, timeline, target_index

        # Create hidden buttons for timeline navigation - Fixed approach
        timeline_buttons = []
        max_items = max(
            len(PORTFOLIO.get("experiences", [])),
            len(PORTFOLIO.get("skills", [])),
            len(PORTFOLIO.get("certifications", [])),
            len(PORTFOLIO.get("education", [])),
        )

        with gr.Column(visible=False):
            for i in range(max_items):
                btn = gr.Button(f"Timeline {i}", elem_classes="timeline-btn")
                btn.elem_id = f"timeline-btn-{i}"
                # Add data attribute for proper selection
                btn.elem_attributes = {"data-timeline-index": str(i)}
                timeline_buttons.append(btn)

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

        # Connect timeline buttons with proper handlers
        for i, btn in enumerate(timeline_buttons):
            btn.click(
                lambda idx=i: jump_to_index(idx, category_state.value),
                inputs=[category_state],
                outputs=[carousel_html, timeline_html, index_state],
            )

        # Initialize timeline display properly
        def init_timeline():
            items = PORTFOLIO.get("experiences", [])
            sorted_items = sorted(
                enumerate(items),
                key=lambda x: x[1].get(
                    "date", x[1].get("year", x[1].get("period", "0000"))
                ),
            )

            timeline_items_html = []
            for idx, (original_index, item) in enumerate(sorted_items):
                date = item.get("date", item.get("year", item.get("period", "")))
                active_class = "active" if original_index == initial_index else ""

                timeline_items_html.append(
                    f"""
                <div class="timeline-item {active_class}" 
                     onclick="document.querySelector('[data-timeline-index=\"{original_index}\"]').click()">
                    <div class="timeline-dot"></div>
                    <div class="timeline-label">{date}</div>
                </div>
                """
                )

            return f'<div class="timeline">{"".join(timeline_items_html)}</div>'

        # Set initial timeline
        timeline_html.value = init_timeline()

        # Add instruction for timeline navigation
        gr.HTML(
            f"""
        <p style="text-align: center; color: {COLORS['text_muted']}; font-size: 0.85rem; margin-top: 1rem;">
            💡 Cliquez sur les points de la timeline ou utilisez les flèches ◀ ▶ pour naviguer
        </p>
        """
        )

        # Chat interface with improved styling and rounded components
        wavebot_logo = embed_image_base64("logos/technologies/wavebot.png")
        wavebot_img = (
            f'<img src="{wavebot_logo}" class="wavebot-logo" alt="WaveBot" />'
            if wavebot_logo
            else "🤖"
        )

        gr.HTML(
            f"""
        <div style="margin-top: 4rem;"></div>
        <div class="chat-header">
            {wavebot_img}
            <span><span class="agent-name">PeponeAgent</span> - Un agent IA spécialisé sur mon profil</span>
        </div>
        <p style="color: {COLORS['text_secondary']}; margin-bottom: 1.5rem; font-size: 0.95rem;">
            Posez-lui vos questions sur mon profil, mes expériences GenAI & Agentic, mes compétences techniques ou demandez-lui une analyse de correspondance avec vos besoins.
        </p>
        """
        )

        # Create chatbot with proper avatar and improved styling
        chatbot_avatar = os.path.join(logos_path, "technologies", "wavebot.png")

        # Wrap chatbot in a container for better styling control
        with gr.Column(elem_classes="chat-container"):
            chatbot = gr.Chatbot(
                height=400,
                label="",
                avatar_images=(None, chatbot_avatar),
                bubble_full_width=False,
                show_label=False,
                elem_classes="gradio-chatbot",  # Custom class for styling
            )

            # Input area with improved styling
            with gr.Row(elem_classes="chat-input-container"):
                msg = gr.Textbox(
                    placeholder="Ex: Quels projets multi-agents as-tu réalisés ?",
                    label="",
                    scale=10,
                    lines=1,
                    show_label=False,
                    container=False,
                    elem_id="msg-input",
                )

                send_btn = gr.Button(
                    "➤",
                    variant="primary",
                    scale=1,
                    size="md",
                    elem_id="send-btn",
                )

        gr.Examples(
            examples=[
                "En quoi Clément serait adapté pour un post de tech lead GenAI ?",
                "Quelle expérience Clément a-t-il avec le MCP ?",
                "Quelles technologies GenAI maîtrise Clément ?",
            ],
            inputs=msg,
            label="Questions suggérées",
        )

        # Chat functionality
        msg.submit(chat_with_agent, [msg, chatbot], [msg, chatbot])
        send_btn.click(chat_with_agent, [msg, chatbot], [msg, chatbot])

        # Footer with model information
        if USE_HF_MODEL and agent:
            model_info = f"SmolAgent + {working_model} (HuggingFace)"
        elif USE_SMOLAGENT_WITH_LITELLM:
            model_info = (
                f"SmolAgent + {os.getenv('LITELLM_MODEL', 'GPT-4o-mini')} (LiteLLM)"
            )
        else:
            model_info = f"{os.getenv('LITELLM_MODEL', 'GPT-4o-mini')} (LiteLLM)"

        gr.HTML(
            f"""
        <div class="footer">
            <p style="color: {COLORS['text_primary']}; font-size: 1rem; font-weight: 500; margin-bottom: 0.5rem;">
                © 2025 Clément Peponnet - Portfolio GenAI & Agentic
            </p>
            <p style="color: {COLORS['text_secondary']}; font-size: 0.875rem;">
                Built with Gradio & {model_info}
            </p>
        </div>
        """
        )

    return app


# Launch application
if __name__ == "__main__":
    app = create_interface()
    app.launch(server_name="0.0.0.0", server_port=7860, debug=True, show_error=True)
