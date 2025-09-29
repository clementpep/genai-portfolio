"""
Configuration settings and constants for the portfolio application.

This module contains all configuration variables, color schemes, technology links,
and environment-dependent settings.
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Application paths
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
LOGOS_PATH = os.path.join(BASE_DIR, "logos")
PORTFOLIO_DATA_PATH = os.path.join(BASE_DIR, "portfolio_data.yaml")

# LLM Configuration
USE_HF_MODEL = os.getenv("USE_HF_MODEL", "true").lower() == "true"
USE_SMOLAGENT_WITH_LITELLM = (
    os.getenv("USE_SMOLAGENT_WITH_LITELLM", "false").lower() == "true"
)
HF_TOKEN = os.getenv("HF_TOKEN")
LITELLM_MODEL = os.getenv("LITELLM_MODEL", "gpt-4o-mini")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Free HuggingFace models to try in order of preference
FREE_HF_MODELS = [
    "Qwen/Qwen2.5-Coder-32B-Instruct",
    "HuggingFaceH4/zephyr-7b-beta",
]

# Agent configuration
AGENT_MAX_STEPS = 6
AGENT_VERBOSITY = 0

# Easter egg configuration
EASTER_EGG_TERMS = {
    "poupouille": {"gender": "ma", "special": False},
    "tchoupinoux": {"gender": "mon", "special": True},
    "péchailloux": {"gender": "mon", "special": False},
    "péchaille": {"gender": "ma", "special": False},
    "chayoux": {"gender": "mon", "special": False},
    "chnawax": {"gender": "mon", "special": False},
}

EASTER_EGG_PROMPT = os.getenv(
    "EASTER_EGG_MODE_PROMPT",
    """You are PeponeAgent on vacation mode! You're relaxed, funny, and enjoying the sun.
Be playful, humorous, and lighthearted in your responses while still being helpful.
Use casual language and feel free to joke around.
Remember: the user found an easter egg, so celebrate that with them!""",
)

# Technology links for clickable logos
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
    "primary": "#1f4135",
    "primary_light": "#2d5949",
    "secondary": "#F5F5DC",
    "accent": "#7fa890",
    "background": "#f8f9fa",
    "surface": "#ffffff",
    "surface_elevated": "#ffffff",
    "text_primary": "#1a1a1a",
    "text_secondary": "#6c757d",
    "text_muted": "#adb5bd",
    "gradient_start": "#1f4135",
    "gradient_end": "#2d5949",
    "border": "#dee2e6",
    "shadow": "rgba(31, 65, 53, 0.1)",
}

# Server configuration
SERVER_NAME = "0.0.0.0"
SERVER_PORT = 7860
DEBUG_MODE = True
SHOW_ERROR = True
