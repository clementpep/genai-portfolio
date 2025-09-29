"""
CSS styling for the portfolio application.

This module contains all custom CSS styles for the Gradio interface,
including premium design elements, card layouts, chat components, and responsive design.
"""

from .settings import COLORS


def get_custom_css() -> str:
    """
    Generate the custom CSS for the application.

    Returns:
        str: Complete CSS stylesheet as a string
    """
    return f"""
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

.gradio-chatbot {{
    border-radius: 20px !important;
    border: 2px solid {COLORS['border']} !important;
    background: {COLORS['surface']} !important;
    overflow: hidden !important;
}}

.gradio-chatbot .message {{
    border-radius: 16px !important;
}}

.chat-input-container {{
    background: {COLORS['surface']} !important;
    border-radius: 16px !important;
    border: 2px solid {COLORS['border']} !important;
    padding: 0.5rem !important;
    margin-top: 1rem !important;
}}

.easter-egg-notification {{
    background: linear-gradient(135deg, #FFD700, #FFA500);
    color: #1f4135;
    padding: 1.25rem 2rem;
    border-radius: 16px;
    text-align: center;
    font-weight: 600;
    font-size: 1.05rem;
    margin: 1.5rem 0;
    box-shadow: 0 4px 20px rgba(255, 215, 0, 0.4);
    animation: slideInBounce 0.6s ease-out;
    border: 2px solid rgba(255, 165, 0, 0.3);
}}

.easter-egg-container {{
    min-height: 0;
    transition: all 0.3s ease;
}}

@keyframes slideInBounce {{
    0% {{
        opacity: 0;
        transform: translateY(-30px) scale(0.9);
    }}
    60% {{
        opacity: 1;
        transform: translateY(5px) scale(1.02);
    }}
    100% {{
        opacity: 1;
        transform: translateY(0) scale(1);
    }}
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

.footer {{
    text-align: center;
    margin-top: 4rem;
    padding: 2.5rem;
    border-top: 2px solid {COLORS['border']};
    background: {COLORS['surface']};
    border-radius: 24px;
}}

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

.card-location {{
    color: {COLORS['text_muted']};
    font-size: 0.9rem;
    font-style: italic;
    margin-top: 0.25rem;
}}

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
"""
