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


# Premium GenAI Portfolio - Clément Peponnet

A premium portfolio showcasing GenAI and Agentic AI expertise with an elegant dark green, cream, and gray design inspired by luxury materials. Built with Gradio and powered by SmolAgent.

## ✨ Features

### 🎨 Premium Design
- **Luxury Color Palette**: Premium dark green (#1f4135), cream, and light gray
- **Brushed Metal Background**: Elegant diagonal brushed metal texture on light background
- **Elegant Typography**: Playfair Display for headers, Inter for body
- **Smooth Animations**: Refined transitions and micro-interactions
- **Apple-Inspired UX**: Clean, spacious, and sophisticated interface

### 🚀 Interactive Components
- **Wide Carousel Cards**: Expanded cards (900px) for better content visibility
- **Compact Navigation**: Small circular arrows (48px) with hover effects
- **Chronological Timeline**: Sorted by date with clickable dots to jump between items
- **Timeline Visual**: Line passes through dots showing progression
- **Smart Navigation**: Category tabs for quick switching
- **Responsive Cards**: Detailed information with smooth hover effects
- **Icon Indicators**: Visual icons on stat cards for better scannability

### 🤖 AI-Powered Chat
- **SmolAgent Integration**: Intelligent agent with custom tools
- **Robot Avatar**: Custom SVG robot icon for assistant
- **Optimized UI**: White text on green background for messages, circular send button
- **Dual LLM Support**: Choose between free HuggingFace or paid OpenAI/Claude
- **Custom Tools**:
  - `list_clement_experiences` - Filter experiences by technology, client, or sector
  - `list_clement_skills` - Get skills by category
  - `list_clement_certifications` - View all certifications
  - `list_clement_education` - Educational background
  - `analyze_profile_match` - Match profile against job requirements

### 🔗 Social Integration
- LinkedIn profile with custom icon
- GitHub profile with custom icon
- Clean, professional footer

## 📁 Project Structure

```
genai-portfolio/
├── app.py                  # Main application with both LLM options
├── portfolio_data.yaml     # All portfolio content (easy to update)
├── requirements.txt        # Python dependencies
├── .env                   # Environment configuration (create from .env.example)
├── .env.example           # Template for environment variables
├── README.md              # This file
└── DEPLOYMENT.md          # Deployment guide
```

## 🚀 Quick Start

### 1. Local Development

```bash
# Clone repository
git clone <your-repo>
cd genai-portfolio

# Install dependencies
pip install -r requirements.txt

# Configure environment (choose one option)
cp .env.example .env

# Option A: FREE - Use Hugging Face (recommended for testing)
echo "USE_HF_MODEL=true" >> .env
echo "HF_TOKEN=hf_your_token" >> .env

# Option B: PAID - Use OpenAI
echo "USE_HF_MODEL=false" >> .env
echo "OPENAI_API_KEY=sk-proj-your-key" >> .env

# Run application
python app.py
```

### 2. Hugging Face Spaces Deployment

1. **Create Space**: https://huggingface.co/new-space
   - SDK: Gradio
   - Hardware: CPU basic (free)

2. **Upload files**: `app.py`, `portfolio_data.yaml`, `requirements.txt`

3. **Configure secrets** (Settings → Variables and secrets):
   ```
   USE_HF_MODEL=true
   HF_TOKEN=hf_your_token_here
   ```

4. **Deploy**: Space builds automatically

## 🎨 Color Palette

```css
Primary: #1f4135        /* Premium dark green */
Primary Light: #2d5949  /* Lighter premium green */
Secondary: #F5F5DC      /* Cream/Beige */
Accent: #7fa890         /* Sage green accent */
Background: #f8f9fa     /* Light gray background */
Surface: #ffffff        /* White surface */
Text: #1a1a1a          /* Dark gray text */
Border: #dee2e6        /* Light border */
```

The design uses a sophisticated light theme with premium dark green accents, creating a professional and luxurious appearance perfect for showcasing GenAI expertise.

## 🔧 Configuration Options

### LLM Backend Selection

The app supports two LLM backends via the `USE_HF_MODEL` environment variable:

#### Option 1: Hugging Face (FREE)
```bash
USE_HF_MODEL=true
HF_TOKEN=hf_your_token
```
- ✅ Free to use
- ✅ SmolAgent with tool calling
- ✅ Qwen2.5-Coder-32B-Instruct model
- ⚠️ May be slower on CPU

#### Option 2: LiteLLM (PAID)
```bash
USE_HF_MODEL=false
OPENAI_API_KEY=sk-proj-your-key
LITELLM_MODEL=gpt-4o-mini
```
- ✅ Faster responses
- ✅ Better quality
- ✅ Multiple providers (OpenAI, Claude, Azure)
- ⚠️ Requires API credits

### Supported LLM Providers (via LiteLLM)

- **OpenAI**: `gpt-4o-mini`, `gpt-4o`, `gpt-4-turbo`
- **Anthropic**: `claude-3-5-sonnet-20241022`, `claude-3-opus-20240229`
- **Azure OpenAI**: `azure/your-deployment-name`
- **100+ other providers**: See [LiteLLM docs](https://docs.litellm.ai/docs/providers)

## 📝 Updating Your Portfolio

All content is managed in `portfolio_data.yaml`. Simply edit this file to update your portfolio:

### Add New Experience

```yaml
experiences:
  - id: exp_new
    title: "New Project Title"
    client: "Client Name"
    duration: "3 months"
    date: "2025-03"
    period: "2025-03"
    icon: "🚀"  # Use emoji or provide PNG logo
    description: >
      Detailed description of the project...
    technologies:
      - Technology 1
      - Technology 2
    impact: "Key business impact"
    sector: "Industry sector"
```

### Add New Skill Category

```yaml
skills:
  - category: "New Category"
    icon: "💡"
    skills:
      - Skill 1
      - Skill 2
      - Skill 3
```

### Add Certification

```yaml
certifications:
  - id: cert_new
    name: "Certification Name"
    issuer: "Issuing Organization"
    year: "2025"
    date: "2025"
    icon: "🏆"
    description: "Brief description"
```

## 🎯 SmolAgent Tools

The AI assistant uses custom tools to query your portfolio:

### Available Tools

1. **`list_clement_experiences`**
   ```python
   # Filter experiences by technology, client, or sector
   "Show me projects using MCP"
   "What work has been done for Wavestone?"
   ```

2. **`list_clement_skills`**
   ```python
   # Get skills by category
   "What are the GenAI skills?"
   "Show me web development expertise"
   ```

3. **`list_clement_certifications`**
   ```python
   # List all certifications
   "What certifications does Clément have?"
   ```

4. **`list_clement_education`**
   ```python
   # Get educational background
   "Tell me about the education"
   ```

5. **`analyze_profile_match`**
   ```python
   # Analyze match with job requirements
   "Analyze match for: Senior GenAI Engineer with Azure and multi-agent experience"
   ```

## 🐛 Troubleshooting

### Chat Not Working

**Issue**: Chat returns errors or doesn't respond

**Solutions**:
1. Check your API key/token is correctly set
2. Verify `USE_HF_MODEL` matches your configuration
3. Check Space logs for specific errors
4. Try switching between HF and LiteLLM backends

### Carousel Navigation Issues

**Issue**: Cards don't update when clicking buttons

**Solutions**:
1. Verify `portfolio_data.yaml` is properly formatted
2. Check browser console for JavaScript errors
3. Clear browser cache and reload

### Timeline Not Clickable

**Issue**: Timeline dots don't respond to clicks

**Note**: Currently timeline is visual-only. Use Previous/Next buttons or category tabs for navigation. Timeline shows current position.

### Styling Issues

**Issue**: Colors or layout look wrong

**Solutions**:
1. Hard refresh browser (Ctrl+F5)
2. Check if custom CSS loaded (view page source)
3. Verify Gradio version >= 4.0.0

## 🎨 Customization

### Change Color Palette

Edit the `COLORS` dictionary in `app.py`:

```python
COLORS = {
    'primary': '#1f4135',        # Your primary color
    'secondary': '#F5F5DC',      # Your secondary color  
    'background': '#f8f9fa',     # Background color
    # ... other colors
}
```

### Modify Background Texture

Edit the `CUSTOM_CSS` background pattern in `app.py`:

```css
background: 
    repeating-linear-gradient(90deg, #f8f9fa, #f8f9fa 2px, rgba(222, 226, 230, 0.3) 2px, rgba(222, 226, 230, 0.3) 3px),
    repeating-linear-gradient(0deg, #f8f9fa, #f8f9fa 2px, rgba(222, 226, 230, 0.2) 2px, rgba(222, 226, 230, 0.2) 3px),
    linear-gradient(180deg, #f8f9fa 0%, #f0f2f5 100%);
background-size: 80px 80px, 80px 80px, 100% 100%;
```

### Add Client Logos

To use PNG logos instead of emojis:

1. Add logo files to a `/logos` folder
2. Update `icon` in `portfolio_data.yaml`:
   ```yaml
   icon: "logos/wavestone.png"
   ```
3. Modify `generate_card_html()` to handle image paths

## 📊 Performance Tips

### For Free Tier (CPU)
- Use `USE_HF_MODEL=true` (HuggingFace)
- Keep conversations short
- Limit max_tokens in agent configuration

### For Better Performance
- Upgrade to CPU upgrade ($0.03/hour)
- Use GPU for faster inference
- Use LiteLLM with GPT-4o-mini

## 🔒 Security

- ✅ Never commit `.env` file
- ✅ Use Spaces secrets for sensitive data
- ✅ Validate YAML input when updating portfolio
- ✅ Keep dependencies updated
- ✅ Review Space logs regularly

## 🌐 Adding Custom Domain

1. Purchase domain (Namecheap, GoDaddy, etc.)
2. Add CNAME record:
   ```
   Type: CNAME
   Name: portfolio
   Value: username-genai-portfolio.hf.space
   ```
3. Wait for DNS propagation (up to 48h)

## 📈 Analytics

Enable Gradio analytics in `app.py`:

```python
app.launch(
    analytics_enabled=True,
    show_api=False
)
```

Monitor in Space → Analytics tab

## 🤝 Contributing

To contribute improvements:

1. Fork the repository
2. Create feature branch
3. Test changes locally
4. Submit pull request

## 📞 Support

- **LinkedIn**: [Clément Peponnet](https://www.linkedin.com/in/clément-peponnet-b26906194)
- **GitHub**: [@clementpep](https://github.com/clementpep)
- **Issues**: Open an issue on GitHub

## 📄 License

This project is private and proprietary. All rights reserved.

---

**Built with ❤️ using Gradio, SmolAgent, and Hugging Face Spaces**