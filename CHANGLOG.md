# Changelog

All notable changes to this portfolio project will be documented in this file.

## [2.0.0] - 2025-01-XX

### 🎨 Design Refresh - Premium Light Theme

#### Added
- New premium color palette with dark green (#1f4135), cream, and light gray
- Stone-textured background with subtle crosshatch pattern
- Enhanced visual hierarchy with improved spacing
- Icon indicators on stat cards for better scannability
- Smooth fade-in animations on page load
- Helper script `update_portfolio.py` for easy content management
- `DESIGN.md` comprehensive design system documentation
- `LOGOS.md` guide for adding client and technology logos

#### Changed
- **Complete color system overhaul** from dark theme to premium light theme
- Background from dark gray to light gray (#f8f9fa) with texture
- Primary color from #2D5016 to #1f4135 (premium dark green)
- Text colors inverted for light theme (dark text on light background)
- Carousel navigation: arrows now properly aligned with cards
- Timeline: improved visual alignment and centering
- Cards: increased padding and improved shadow depth
- Buttons: enhanced hover states with subtle lift effect
- Typography: improved contrast ratios for better readability
- Header: enhanced gradient with white text
- Footer: cleaner design with rounded corners
- Social links: improved hover effects with color transitions

#### Fixed
- Carousel navigation buttons alignment issue
- Timeline dots not properly centered with connecting line
- Navigation responsiveness on smaller screens
- Hover states inconsistency across components
- Spacing irregularities throughout the interface
- Card border visibility on light backgrounds

#### Improved
- Overall ergonomics with better visual flow
- Touch target sizes for mobile (minimum 56px)
- Transition smoothness across all interactive elements
- Accessibility with improved color contrast ratios
- Scrollbar styling for consistency
- Chat interface visual clarity

### 🤖 Chatbot Enhancements

#### Added
- Helper text above chat interface
- Better placeholder text with examples
- Improved example questions

#### Changed
- Chatbot container styling for better integration
- Message bubble styling for clarity
- Avatar positioning and sizing

## [1.0.0] - 2025-01-XX

### 🚀 Initial Release

#### Added
- Premium portfolio application with Gradio
- Dual LLM support: HuggingFace (SmolAgent) and LiteLLM
- Interactive carousel for experiences, skills, certifications, education
- SmolAgent with 5 custom tools:
  - `list_clement_experiences`
  - `list_clement_skills`
  - `list_clement_certifications`
  - `list_clement_education`
- Timeline navigation system
- Social media integration (LinkedIn, GitHub)
- Statistics dashboard
- YAML-based content management
- Comprehensive documentation (README, DEPLOYMENT)
- Environment-based configuration (.env)

#### Features
- Responsive design
- Smooth animations
- Category-based navigation
- AI-powered chatbot
- Professional color scheme
- Clean typography

---

## Version Numbering

This project follows [Semantic Versioning](https://semver.org/):
- **Major version** (X.0.0): Breaking changes or complete redesigns
- **Minor version** (0.X.0): New features, non-breaking changes
- **Patch version** (0.0.X): Bug fixes, minor improvements

## Contributing

To contribute to this project:
1. Create a feature branch
2. Make your changes
3. Update this CHANGELOG.md
4. Submit a pull request

## Maintenance Notes

### Adding New Features
1. Document in README.md
2. Add entry to CHANGELOG.md under [Unreleased]
3. Update version number when releasing

### Design Changes
1. Update DESIGN.md with new patterns/colors
2. Document reasoning for changes
3. Ensure consistency across all components

### Bug Fixes
1. Reference issue number (if applicable)
2. Describe the problem and solution
3. Test on all supported browsers

---

**Project Repository**: https://github.com/clementpep/genai-portfolio  
**Live Demo**: https://huggingface.co/spaces/[username]/genai-portfolio
