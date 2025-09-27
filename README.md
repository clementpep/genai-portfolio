# Clément's GenAI Portfolio - Hugging Face Space

Portfolio showcasing GenAI and Agentic AI expertise, built with Gradio and deployed on Hugging Face Spaces.

## Features

- **Interactive Carousel**: Navigate through experiences, skills, certifications, and education
- **Timeline Navigation**: Visual timeline with clickable dots for quick navigation
- **AI Chatbot**: Powered by LiteLLM with GPT-4o-mini for intelligent portfolio queries
- **Easy Updates**: All content managed through a single YAML configuration file
- **Responsive Layout**: Optimized for all screen sizes

## Project Structure

```
genai-portfolio/
├── app.py                  # Main Gradio application
├── portfolio_data.yaml     # Portfolio content (experiences, skills, etc.)
├── requirements.txt        # Python dependencies
├── README.md               # This file
└── .env                    # Environment variables (API keys)
```

## Setup Instructions

### Local Development

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd genai-portfoli
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   Create a `.env` file:
   ```bash
   # Required for LiteLLM chatbot
   OPENAI_API_KEY=your_openai_api_key_here
   
   # Or use Azure OpenAI
   AZURE_API_KEY=your_azure_key
   AZURE_API_BASE=https://your-resource.openai.azure.com/
   AZURE_API_VERSION=2024-02-15-preview
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Open in browser**
   Navigate to `http://localhost:7860`

### Hugging Face Space Deployment

1. **Create a new Space**
   - Go to https://huggingface.co/spaces
   - Click "Create new Space"
   - Choose "Gradio" as the SDK
   - Select your preferred hardware (CPU is sufficient)

2. **Upload files**
   - Upload `app.py`, `portfolio_data.yaml`, and `requirements.txt`
   - The Space will automatically detect and run the Gradio app

3. **Configure secrets**
   - Go to Space Settings > Variables and secrets
   - Add your API key as a secret:
     - Name: `OPENAI_API_KEY`
     - Value: Your OpenAI API key

4. **Deploy**
   - The Space will automatically build and deploy
   - Your portfolio will be live at `https://huggingface.co/spaces/<username>/<space-name>`

## Updating Your Portfolio

All portfolio content is managed in `portfolio_data.yaml`. Simply edit this file to update your portfolio.

### Adding a New Experience

```yaml
experiences:
  - id: exp_new
    title: "New Project Title"
    client: "Client Name"
    duration: "3 months"
    date: "2025-01"
    period: "2025-01"
    icon: "🚀"
    description: >
      Detailed description of the project, your role, 
      and key achievements.
    technologies:
      - Technology 1
      - Technology 2
      - Technology 3
    impact: "Key business impact or result"
    sector: "Industry sector"
```

### Adding a New Skill Category

```yaml
skills:
  - category: "New Skill Category"
    icon: "💡"
    skills:
      - Skill 1
      - Skill 2
      - Skill 3
```

### Adding a Certification

```yaml
certifications:
  - id: cert_new
    name: "Certification Name"
    issuer: "Issuing Organization"
    year: "2025"
    date: "2025"
    icon: "🏆"
    description: "Brief description of the certification."
```

### Adding Education

```yaml
education:
  - id: edu_new
    school: "University Name"
    degree: "Degree Title"
    year: "2025"
    date: "2025"
    icon: "🎓"
    achievement: "Honors, rankings, or special achievements"
    description: "Description of the program and specialization."
```

## Customization

### Colors and Theme

Edit the `COLORS` dictionary in `app.py`:

```python
COLORS = {
    'primary': '#007AFF',        # Primary accent color
    'secondary': '#5856D6',      # Secondary accent color
    'background': '#000000',     # Main background
    'surface': '#1C1C1E',        # Card background
    # ... other colors
}
```

### Chatbot Model

To use a different LLM model, modify the `chat_with_ai` function:

```python
# Use Claude instead of GPT-4o-mini
response = completion(
    model="claude-3-5-sonnet-20241022",  # or any other model
    messages=messages,
    temperature=0.7,
    max_tokens=500
)
```

**Supported models** (via LiteLLM):
- OpenAI: `gpt-4o-mini`, `gpt-4o`, `gpt-4-turbo`
- Anthropic: `claude-3-5-sonnet-20241022`, `claude-3-opus-20240229`
- Azure OpenAI: `azure/your-deployment-name`
- And 100+ other providers

### Alternative: Using SmolAgent

To use SmolAgent instead of LiteLLM:

1. Update `requirements.txt`:
   ```
   smolagents
   huggingface_hub
   ```

2. Replace the chat function in `app.py`:
   ```python
   from smolagents import CodeAgent, InferenceClientModel
   
   model = InferenceClientModel(model_id="Qwen/Qwen2.5-Coder-32B-Instruct")
   agent = CodeAgent(model=model, tools=[...])
   
   def chat_with_ai(message, history):
       result = agent.run(message)
       return str(result)
   ```

## Design Philosophy

This portfolio follows Apple's design principles:

- **Simplicity**: Clean, uncluttered interface
- **Clarity**: Clear visual hierarchy and typography
- **Depth**: Layered design with shadows and gradients
- **Consistency**: Unified color scheme and spacing
- **Animation**: Smooth, purposeful transitions

## Troubleshooting

### Chat not working
- Verify your API key is correctly set in environment variables
- Check the Space logs for error messages
- Ensure your API key has sufficient credits

### Carousel not displaying correctly
- Clear browser cache
- Check that `portfolio_data.yaml` is properly formatted
- Verify all required fields are present in each item

### Timeline not updating
- Ensure JavaScript is enabled in your browser
- Check browser console for errors
- Verify the timeline items have valid dates

## Performance Optimization

For better performance on Hugging Face Spaces:

1. **Use CPU hardware**: The application is optimized for CPU inference
2. **Limit chat history**: Truncate old messages to reduce token usage
3. **Optimize images**: Use compressed images for better loading times
4. **Cache responses**: Implement caching for repeated queries

## Contributing

To contribute to this project:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is private and proprietary. All rights reserved.

## Support

For questions or issues:
- Open an issue on GitHub
- Contact via LinkedIn
- Email: clement.peponnet@gmail.com

---

**Built with ❤️ using Gradio, LiteLLM, and Hugging Face Spaces**
