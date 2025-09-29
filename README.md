---
title: Clément's GenAI Portfolio
emoji: 🎨
colorFrom: green
colorTo: gray
sdk: gradio
sdk_version: 5.47.2
app_file: app.py
pinned: false
---


# Portfolio GenAI & Agentic - Clément Peponnet

Premium GenAI Portfolio Application deployed on Hugging Face Spaces with Gradio.
Version 3.0 - Refactored modular architecture with easter egg feature.

## Project Structure

```
portfolio_app/
├── app.py                           # Main entry point
├── portfolio_data.yaml              # Portfolio data configuration
├── .env                             # Environment variables (not in repo)
├── requirements.txt                 # Python dependencies
│
├── config/
│   ├── __init__.py
│   ├── settings.py                  # Configuration and constants
│   └── css.py                       # CSS styling
│
├── core/
│   ├── __init__.py
│   ├── data_loader.py              # Portfolio data loading with caching
│   └── agent.py                    # Agent initialization and chat logic
│
├── tools/
│   ├── __init__.py
│   └── portfolio_tools.py          # SmolAgent tools for portfolio queries
│
├── ui/
│   ├── __init__.py
│   ├── components.py               # HTML component generation
│   └── interface.py                # Gradio interface construction
│
├── utils/
│   ├── __init__.py
│   └── helpers.py                  # Utility functions
│
└── logos/
    ├── clients/                    # Client logos
    ├── technologies/               # Technology logos
    ├── education/                  # Education institution logos
    └── textures/                   # Background textures
```

## Architecture Overview

### Configuration Layer (`config/`)
- **settings.py**: Centralized configuration for LLM models, paths, colors, and easter egg settings
- **css.py**: Complete CSS styling for the premium interface design

### Core Layer (`core/`)
- **data_loader.py**: Singleton pattern for loading and caching portfolio data from YAML
- **agent.py**: Manages LLM agent (SmolAgent or LiteLLM) with secret easter egg

### Tools Layer (`tools/`)
- **portfolio_tools.py**: SmolAgent tools for querying experiences, skills, certifications, education, and profile matching

### UI Layer (`ui/`)
- **components.py**: HTML generation for cards, headers, stats, footers
- **interface.py**: Gradio interface assembly with navigation, carousel, timeline, and chat

### Utilities (`utils/`)
- **helpers.py**: Image encoding, path resolution, and formatting utilities

## Key Features

### Agent Capabilities
- **SmolAgent with HuggingFace**: Free tier using Qwen or Zephyr models
- **SmolAgent with LiteLLM**: Paid tier with GPT-4o-mini and tool support
- **Pure LiteLLM**: Faster responses without tools (paid tier)
- **Optimized prompts**: Concise system prompts for faster response times

### Portfolio Tools
1. `list_clement_experiences()` - Filter by technology, client, or sector
2. `list_clement_skills()` - Get skills by category
3. `list_clement_certifications()` - List all certifications
4. `list_clement_education()` - Educational background

## Environment Variables

Create a `.env` file with:

```env
# LLM Configuration
USE_HF_MODEL=true                    # Use HuggingFace free models
USE_SMOLAGENT_WITH_LITELLM=false     # Use SmolAgent with LiteLLM
HF_TOKEN=your_hf_token               # HuggingFace API token
OPENAI_API_KEY=your_openai_key       # OpenAI API key
LITELLM_MODEL=gpt-4o-mini            # LiteLLM model name

```

## Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

The application will be available at `http://0.0.0.0:7860`

## Deployment on Hugging Face Spaces

1. Push the entire project structure to a Hugging Face Space
2. Set environment variables in Space settings
3. The app will automatically deploy with Gradio

## Development Guidelines

### Code Style
- English comments and documentation
- Type hints for function parameters and returns
- Docstrings for all functions and classes
- Minimal emoji usage (only where strictly necessary)

### Performance Optimization
- Cached portfolio data loading (singleton pattern)
- Concise system prompts for faster LLM responses
- Efficient HTML generation with reusable components
- Lazy imports for LLM libraries

### Adding New Features

**New Portfolio Tool:**
1. Add tool function in `tools/portfolio_tools.py`
2. Decorate with `@tool`
3. Add to `AVAILABLE_TOOLS` list

**New UI Component:**
1. Add generation function in `ui/components.py`
2. Import and use in `ui/interface.py`

**New Configuration:**
1. Add constant in `config/settings.py`
2. Import where needed

## 📞 Support

- **LinkedIn**: [Clément Peponnet](https://www.linkedin.com/in/clément-peponnet-b26906194)
- **GitHub**: [@clementpep](https://github.com/clementpep)
- **Issues**: Open an issue on GitHub

## License

© 2025 Clément Peponnet - All rights reserved

---

**Built with ❤️ using Gradio, SmolAgent, and Hugging Face Spaces**