import React, { useState, useEffect, useRef } from 'react';
import { ChevronLeft, ChevronRight, Send, Bot, User, Calendar, Award, Briefcase, BookOpen, X, Github, Linkedin, Code } from 'lucide-react';

/**
 * Main Portfolio Application Component with SmolAgent Integration
 * Showcases GenAI & Agentic experiences with interactive carousel, timeline and AI chatbot
 */
const Portfolio = () => {
  const [activeCategory, setActiveCategory] = useState('experiences');
  const [activeCardIndex, setActiveCardIndex] = useState(0);
  const [flippedCards, setFlippedCards] = useState(new Set());
  const [chatMessages, setChatMessages] = useState([
    { role: 'assistant', content: 'Bonjour! Je suis votre assistant IA spécialisé dans le profil de Clément. Posez-moi des questions sur ses expériences GenAI, ses compétences en agents, ou ses certifications!' }
  ]);
  const [inputMessage, setInputMessage] = useState('');
  const [isChatOpen, setIsChatOpen] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const carouselRef = useRef(null);
  const timelineRef = useRef(null);
  const chatEndRef = useRef(null);

  // Portfolio data from your documents
  const portfolioData = {
    experiences: [
      {
        id: 'exp1',
        title: 'MVP GenAI Traduction',
        client: 'Wavestone',
        duration: '13 mois',
        date: '2024-12',
        shortDesc: 'Tech lead traducteur GenAI avec Mistral Large',
        fullDesc: "Tech lead d'une équipe de 5 développeurs sur un traducteur GenAI basé sur Mistral Large via Azure AI Foundry. Développement d'une web app fullstack (ReactJS + Flask) avec architecture modulaire multi-LLMs. Présentation du MVP à l'Ex-Com et déploiement chez un grand compte du luxe.",
        logo: '🌊',
        techs: ['Azure AI Foundry', 'Mistral Large', 'ReactJS', 'Flask', 'Docker'],
        sector: 'Digital Transformation'
      },
      {
        id: 'exp2',
        title: 'Système Multi-Agents SentinelOne',
        client: 'Hugging Face x Gradio',
        duration: 'Hackathon',
        date: '2024-11',
        shortDesc: '2e prix - Analyse de risques climatiques',
        fullDesc: "2e prix au Hackathon HF x Gradio catégorie 'AI Agents' parmi 600+ projets. Conception d'un système multi-agents (SmolAgent + LiteLLM) pour l'analyse en continu de risques climatiques à partir de données open source.",
        logo: '🤗',
        techs: ['SmolAgent', 'LiteLLM', 'Gradio', 'FastMCP', 'NASA FIRMS'],
        sector: 'Climate Tech'
      },
      {
        id: 'exp3',
        title: 'Serveurs MCP',
        client: 'Client Transport Confidentiel',
        duration: '4 mois',
        date: '2024-09',
        shortDesc: 'Tech lead 3 serveurs MCP connectés à LibreChat',
        fullDesc: 'Développement de 3 serveurs MCP: Bing Search (recherche web sécurisée), Microsoft Graph (M365), Python Interpreter (exécution autonome). Déploiement sur Azure Kubernetes (AKS).',
        logo: '🚂',
        techs: ['MCP', 'LibreChat', 'Azure AKS', 'Microsoft Graph', 'Python'],
        sector: 'Transport'
      },
      {
        id: 'exp4',
        title: 'Workflow Multi-Agents Dataiku',
        client: 'ALSTOM',
        duration: '4 mois',
        date: '2024-06',
        shortDesc: 'Pipeline 12 agents, 80K+ validations/an',
        fullDesc: 'Conception et pilotage d\'un pipeline multi-agents (12 agents) sur Dataiku LLM Mesh pour automatiser la validation de 80,000+ Purchase Requisitions annuelles. Allègement équivalent 50 ETP. Projet vitrine COMEX.',
        logo: '🤖',
        techs: ['Dataiku LLM Mesh', 'Multi-Agent', 'GenAI', 'Automation'],
        sector: 'Transport'
      },
      {
        id: 'exp5',
        title: 'Server MCP PowerPoint',
        client: 'Wavestone',
        duration: '4 mois',
        date: '2024-05',
        shortDesc: 'Produit GenAI interne génération slides',
        fullDesc: 'Tech lead équipe 5 consultants pour produit GenAI interne de génération automatisée PowerPoint. Déployé sur Azure avec CI/CD et MCP Shield. Disponible pour 6000+ collaborateurs.',
        logo: '📊',
        techs: ['MCP', 'Docker', 'Azure', 'Copilot Studio', 'MCPOps'],
        sector: 'Produit Interne'
      },
      {
        id: 'exp6',
        title: 'PoC GenAI Enquêtes Satisfaction',
        client: 'Wavestone',
        duration: '6 mois',
        date: '2024-03',
        shortDesc: 'Chatbot RAG analyse enquêtes satisfaction',
        fullDesc: 'Définition besoins métier et développement chatbot RAG. Création base vectorielle (LlamaIndex BERT), comparaison retrievers SPARSE/DENSE, application Streamlit avec GPT4-32k.',
        logo: '💬',
        techs: ['LlamaIndex', 'GPT4', 'Streamlit', 'Azure OpenAI', 'BERT'],
        sector: 'Analytics'
      }
    ],
    skills: [
      {
        id: 'skill1',
        title: 'Agents & MCP',
        date: '2025',
        shortDesc: 'Expert frameworks agents et protocole MCP',
        fullDesc: 'Azure AI Agents, Hugging Face SmolAgent, FastMCP, Gradio, MCP Shield, Dataiku LLM Mesh',
        logo: '🤖',
        techs: ['Azure AI Agents', 'SmolAgent', 'FastMCP', 'MCP Shield'],
      },
      {
        id: 'skill2',
        title: 'Frameworks GenAI',
        date: '2025',
        shortDesc: 'Maîtrise des services et outils GenAI majeurs',
        fullDesc: 'Azure AI Foundry, Azure AI Search, Ollama, LlamaIndex, LangChain, LangGraph, n8n, Copilot Studio',
        logo: '🧠',
        techs: ['Azure AI', 'LangChain', 'LlamaIndex', 'Copilot Studio'],
      },
      {
        id: 'skill3',
        title: 'Développement Web',
        date: '2025',
        shortDesc: 'Expertise fullstack',
        fullDesc: 'Backend: FastAPI, Django, Flask, Streamlit. Frontend: React. Infrastructure: Docker, Azure (AKS, ACR, App Service)',
        logo: '💻',
        techs: ['React', 'FastAPI', 'Docker', 'Azure'],
      },
      {
        id: 'skill4',
        title: 'Data & ML',
        date: '2025',
        shortDesc: 'Machine Learning et Deep Learning',
        fullDesc: 'Python (pandas, scikit-learn, keras, tensorflow, pyTorch), Régression, SVM, Random Forest, CNN, Transfer Learning',
        logo: '📈',
        techs: ['Python', 'TensorFlow', 'PyTorch', 'Scikit-learn'],
      }
    ],
    certifications: [
      {
        id: 'cert1',
        title: 'Azure AI Engineer Associate',
        date: '2024',
        shortDesc: 'Certification Microsoft Azure AI',
        fullDesc: 'Ingénieur IA Azure certifié avec expertise en conception et implémentation de solutions IA utilisant les services Azure AI.',
        logo: '☁️',
        techs: ['Azure', 'AI', 'Cloud'],
      },
      {
        id: 'cert2',
        title: 'Dataiku GenAI Practitioner',
        date: '2024',
        shortDesc: 'Spécialisation GenAI sur plateforme Dataiku',
        fullDesc: 'Praticien certifié dans l\'implémentation de solutions GenAI utilisant Dataiku, incluant LLM Mesh et systèmes multi-agents.',
        logo: '📊',
        techs: ['Dataiku', 'GenAI', 'LLM'],
      },
      {
        id: 'cert3',
        title: 'Hugging Face MCP Course',
        date: '2025',
        shortDesc: 'Expertise Model Context Protocol',
        fullDesc: 'Formation avancée sur l\'implémentation du Model Context Protocol (MCP) et les bonnes pratiques Hugging Face.',
        logo: '🤗',
        techs: ['MCP', 'Hugging Face', 'Agents'],
      }
    ],
    education: [
      {
        id: 'edu1',
        title: 'Arts & Métiers ParisTech',
        date: '2020',
        shortDesc: 'Diplôme ingénieur - Classé 38/120',
        fullDesc: 'Diplômé avec médaille d\'argent, classé 38e sur 120 étudiants. Spécialisation en ingénierie et technologie.',
        logo: '🎓',
        techs: ['Ingénierie', 'Technologie'],
      },
      {
        id: 'edu2',
        title: 'ETS Montréal',
        date: '2019',
        shortDesc: 'Spécialisation Data Science',
        fullDesc: 'Spécialisation en Data Science avec focus sur les techniques de Machine Learning et Deep Learning.',
        logo: '🍁',
        techs: ['ML', 'Deep Learning', 'Data Science'],
      },
      {
        id: 'edu3',
        title: 'Prépa PT* Jules Ferry',
        date: '2017',
        shortDesc: 'Classes préparatoires à Versailles',
        fullDesc: 'Classes préparatoires intensives aux grandes écoles d\'ingénieurs françaises.',
        logo: '📚',
        techs: ['Mathématiques', 'Physique'],
      }
    ]
  };

  const currentData = portfolioData[activeCategory] || [];

  /**
   * Navigate to next card in carousel
   */
  const nextCard = () => {
    setActiveCardIndex((prev) => (prev + 1) % currentData.length);
  };

  /**
   * Navigate to previous card in carousel
   */
  const prevCard = () => {
    setActiveCardIndex((prev) => (prev - 1 + currentData.length) % currentData.length);
  };

  /**
   * Toggle card flip state for detailed view
   */
  const toggleCardFlip = (cardId) => {
    setFlippedCards(prev => {
      const newSet = new Set(prev);
      if (newSet.has(cardId)) {
        newSet.delete(cardId);
      } else {
        newSet.add(cardId);
      }
      return newSet;
    });
  };

  /**
   * Handle timeline click to navigate to specific card
   */
  const handleTimelineClick = (index) => {
    setActiveCardIndex(index);
  };

  /**
   * Send message to SmolAgent backend
   */
  const sendMessage = async () => {
    if (!inputMessage.trim() || isLoading) return;

    const userMessage = { role: 'user', content: inputMessage };
    setChatMessages(prev => [...prev, userMessage]);
    setInputMessage('');
    setIsLoading(true);

    try {
      // Call SmolAgent backend endpoint
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          message: inputMessage,
          history: chatMessages
        })
      });

      if (!response.ok) throw new Error('Network response was not ok');
      
      const data = await response.json();
      
      setChatMessages(prev => [...prev, {
        role: 'assistant',
        content: data.response
      }]);
    } catch (error) {
      console.error('Chat error:', error);
      setChatMessages(prev => [...prev, {
        role: 'assistant',
        content: 'Désolé, j\'ai rencontré une erreur. Veuillez réessayer.'
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  // Update timeline position when carousel changes
  useEffect(() => {
    if (timelineRef.current && currentData.length > 0) {
      const timelineWidth = timelineRef.current.offsetWidth;
      const itemWidth = timelineWidth / currentData.length;
      const scrollPosition = activeCardIndex * itemWidth - (timelineWidth / 2) + (itemWidth / 2);
      timelineRef.current.scrollTo({
        left: scrollPosition,
        behavior: 'smooth'
      });
    }
  }, [activeCardIndex, currentData]);

  // Auto-scroll chat to bottom
  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [chatMessages]);

  // Reset active index when category changes
  useEffect(() => {
    setActiveCardIndex(0);
    setFlippedCards(new Set());
  }, [activeCategory]);

  // Inline styles using CSS-in-JS
  const styles = {
    container: {
      minHeight: '100vh',
      background: 'linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f172a 100%)',
      color: 'white',
      fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", sans-serif'
    },
    header: {
      position: 'fixed',
      top: 0,
      left: 0,
      right: 0,
      background: 'rgba(15, 23, 42, 0.8)',
      backdropFilter: 'blur(12px)',
      zIndex: 50,
      borderBottom: '1px solid rgba(100, 116, 139, 0.3)'
    },
    gradientText: {
      background: 'linear-gradient(to right, #60a5fa, #a78bfa)',
      WebkitBackgroundClip: 'text',
      WebkitTextFillColor: 'transparent',
      backgroundClip: 'text'
    },
    navButton: (isActive) => ({
      display: 'flex',
      alignItems: 'center',
      gap: '8px',
      padding: '12px 24px',
      borderRadius: '12px',
      transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
      transform: 'translateY(0)',
      background: isActive 
        ? 'linear-gradient(135deg, #3b82f6, #8b5cf6)' 
        : 'rgba(71, 85, 105, 0.5)',
      boxShadow: isActive ? '0 10px 25px rgba(59, 130, 246, 0.5)' : 'none',
      border: 'none',
      color: 'white',
      fontSize: '16px',
      fontWeight: '500',
      cursor: 'pointer'
    }),
    card: {
      position: 'absolute',
      width: '320px',
      height: '400px',
      transformStyle: 'preserve-3d',
      transition: 'transform 0.7s cubic-bezier(0.4, 0, 0.2, 1)',
      cursor: 'pointer'
    },
    cardFace: {
      position: 'absolute',
      width: '100%',
      height: '100%',
      borderRadius: '20px',
      padding: '24px',
      boxShadow: '0 20px 50px rgba(0, 0, 0, 0.3)',
      backfaceVisibility: 'hidden',
      display: 'flex',
      flexDirection: 'column',
      border: '1px solid rgba(100, 116, 139, 0.2)'
    },
    cardFront: {
      background: 'linear-gradient(135deg, rgba(71, 85, 105, 0.9), rgba(51, 65, 85, 0.9))',
    },
    cardBack: {
      background: 'linear-gradient(135deg, rgba(139, 92, 246, 0.9), rgba(59, 130, 246, 0.9))',
      transform: 'rotateY(180deg)'
    },
    techBadge: {
      padding: '4px 8px',
      background: 'rgba(15, 23, 42, 0.5)',
      borderRadius: '6px',
      fontSize: '11px',
      whiteSpace: 'nowrap'
    },
    timelineDot: (isActive) => ({
      width: '16px',
      height: '16px',
      borderRadius: '50%',
      transition: 'all 0.3s',
      background: isActive 
        ? 'linear-gradient(to right, #3b82f6, #8b5cf6)'
        : '#64748b',
      transform: isActive ? 'scale(1.5)' : 'scale(1)',
      cursor: 'pointer'
    }),
    chatContainer: {
      position: 'fixed',
      bottom: '16px',
      right: '16px',
      zIndex: 40
    },
    chatBox: {
      position: 'absolute',
      bottom: '64px',
      right: '0',
      width: '384px',
      height: '500px',
      background: 'rgba(30, 41, 59, 0.95)',
      backdropFilter: 'blur(12px)',
      borderRadius: '16px',
      boxShadow: '0 20px 50px rgba(0, 0, 0, 0.5)',
      border: '1px solid rgba(100, 116, 139, 0.3)',
      display: 'flex',
      flexDirection: 'column',
      overflow: 'hidden'
    },
    messageUser: {
      maxWidth: '70%',
      padding: '12px',
      borderRadius: '12px',
      background: '#3b82f6',
      alignSelf: 'flex-end',
      marginBottom: '8px'
    },
    messageAssistant: {
      maxWidth: '70%',
      padding: '12px',
      borderRadius: '12px',
      background: 'rgba(71, 85, 105, 0.5)',
      alignSelf: 'flex-start',
      marginBottom: '8px'
    }
  };

  return (
    <div style={styles.container}>
      {/* Header */}
      <header style={styles.header}>
        <div style={{ maxWidth: '1280px', margin: '0 auto', padding: '16px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <h1 style={{ fontSize: '24px', fontWeight: 'bold', ...styles.gradientText }}>
            Clément - Portfolio GenAI & Agentic
          </h1>
          <div style={{ display: 'flex', gap: '16px', alignItems: 'center' }}>
            <a href="https://github.com/clement-portfolio" target="_blank" rel="noopener noreferrer" 
               style={{ color: 'white', transition: 'color 0.3s' }}
               onMouseOver={e => e.target.style.color = '#60a5fa'}
               onMouseOut={e => e.target.style.color = 'white'}>
              <Github size={20} />
            </a>
            <a href="https://linkedin.com/in/clement" target="_blank" rel="noopener noreferrer"
               style={{ color: 'white', transition: 'color 0.3s' }}
               onMouseOver={e => e.target.style.color = '#60a5fa'}
               onMouseOut={e => e.target.style.color = 'white'}>
              <Linkedin size={20} />
            </a>
            <Code size={20} />
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main style={{ maxWidth: '1280px', margin: '0 auto', padding: '96px 16px 32px' }}>
        {/* Mini Pitch */}
        <section style={{ textAlign: 'center', marginBottom: '48px' }}>
          <h2 style={{ fontSize: '36px', fontWeight: 'bold', marginBottom: '16px', ...styles.gradientText }}>
            Convaincu par le potentiel de la GenAI et de l'Agentic AI
          </h2>
          <p style={{ fontSize: '18px', color: '#cbd5e1', maxWidth: '768px', margin: '0 auto' }}>
            J'accompagne mes clients sur toutes les étapes de vie de leurs projets, 
            de l'idéation à l'industrialisation, pour maximiser leur impact métier.
          </p>
        </section>

        {/* Navigation Buttons */}
        <div style={{ display: 'flex', flexWrap: 'wrap', justifyContent: 'center', gap: '16px', marginBottom: '48px' }}>
          {[
            { key: 'experiences', label: 'Expériences', icon: Briefcase },
            { key: 'skills', label: 'Expertise & Skills', icon: Award },
            { key: 'certifications', label: 'Certifications', icon: Award },
            { key: 'education', label: 'Études', icon: BookOpen }
          ].map(({ key, label, icon: Icon }) => (
            <button
              key={key}
              onClick={() => setActiveCategory(key)}
              style={styles.navButton(activeCategory === key)}
              onMouseEnter={e => {
                if (activeCategory !== key) {
                  e.currentTarget.style.transform = 'translateY(-2px)';
                  e.currentTarget.style.background = 'rgba(71, 85, 105, 0.7)';
                }
              }}
              onMouseLeave={e => {
                if (activeCategory !== key) {
                  e.currentTarget.style.transform = 'translateY(0)';
                  e.currentTarget.style.background = 'rgba(71, 85, 105, 0.5)';
                }
              }}
            >
              <Icon size={20} />
              <span>{label}</span>
            </button>
          ))}
        </div>

        {/* Carousel */}
        <section style={{ position: 'relative', marginBottom: '48px', minHeight: '450px' }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '16px' }}>
            <button 
              onClick={prevCard}
              style={{
                padding: '12px',
                background: 'rgba(71, 85, 105, 0.5)',
                borderRadius: '50%',
                border: 'none',
                color: 'white',
                cursor: 'pointer',
                transition: 'background 0.3s'
              }}
              onMouseEnter={e => e.currentTarget.style.background = 'rgba(71, 85, 105, 0.7)'}
              onMouseLeave={e => e.currentTarget.style.background = 'rgba(71, 85, 105, 0.5)'}
            >
              <ChevronLeft size={24} />
            </button>
            
            <div style={{ position: 'relative', width: '100%', maxWidth: '400px', height: '400px', perspective: '1000px' }}>
              {currentData.map((item, index) => {
                const isActive = index === activeCardIndex;
                const isFlipped = flippedCards.has(item.id);
                
                return (
                  <div
                    key={item.id}
                    style={{
                      ...styles.card,
                      opacity: isActive ? 1 : 0,
                      pointerEvents: isActive ? 'auto' : 'none',
                      transform: isFlipped ? 'rotateY(180deg)' : 'rotateY(0deg)',
                      left: '50%',
                      top: '50%',
                      marginLeft: '-160px',
                      marginTop: '-200px'
                    }}
                    onClick={() => toggleCardFlip(item.id)}
                  >
                    {/* Front of card */}
                    <div style={{ ...styles.cardFace, ...styles.cardFront }}>
                      <div style={{ fontSize: '48px', textAlign: 'center', marginBottom: '16px' }}>{item.logo}</div>
                      <h3 style={{ fontSize: '20px', fontWeight: 'bold', marginBottom: '8px', textAlign: 'center' }}>{item.title}</h3>
                      {item.client && (
                        <p style={{ color: '#60a5fa', textAlign: 'center', marginBottom: '8px' }}>{item.client}</p>
                      )}
                      <p style={{ color: '#cbd5e1', textAlign: 'center', flex: 1, fontSize: '14px' }}>{item.shortDesc}</p>
                      {item.duration && (
                        <p style={{ fontSize: '12px', color: '#94a3b8', textAlign: 'center', marginBottom: '16px' }}>
                          <Calendar style={{ display: 'inline', width: '16px', height: '16px', marginRight: '4px' }} />
                          {item.duration}
                        </p>
                      )}
                      <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px', justifyContent: 'center' }}>
                        {item.techs.slice(0, 3).map((tech, i) => (
                          <span key={i} style={styles.techBadge}>
                            {tech}
                          </span>
                        ))}
                      </div>
                    </div>

                    {/* Back of card */}
                    <div style={{ ...styles.cardFace, ...styles.cardBack }}>
                      <h3 style={{ fontSize: '20px', fontWeight: 'bold', marginBottom: '16px' }}>{item.title}</h3>
                      <p style={{ fontSize: '14px', flex: 1, overflow: 'auto', lineHeight: '1.6' }}>{item.fullDesc}</p>
                      <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px', marginTop: '16px' }}>
                        {item.techs.map((tech, i) => (
                          <span key={i} style={{ ...styles.techBadge, background: 'rgba(15, 23, 42, 0.3)' }}>
                            {tech}
                          </span>
                        ))}
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>

            <button 
              onClick={nextCard}
              style={{
                padding: '12px',
                background: 'rgba(71, 85, 105, 0.5)',
                borderRadius: '50%',
                border: 'none',
                color: 'white',
                cursor: 'pointer',
                transition: 'background 0.3s'
              }}
              onMouseEnter={e => e.currentTarget.style.background = 'rgba(71, 85, 105, 0.7)'}
              onMouseLeave={e => e.currentTarget.style.background = 'rgba(71, 85, 105, 0.5)'}
            >
              <ChevronRight size={24} />
            </button>
          </div>
        </section>

        {/* Timeline */}
        <section style={{ marginBottom: '48px' }}>
          <div 
            ref={timelineRef}
            style={{ 
              position: 'relative',
              overflowX: 'auto',
              scrollbarWidth: 'none',
              msOverflowStyle: 'none',
              WebkitScrollbar: { display: 'none' }
            }}
          >
            <div style={{ display: 'flex', justifyContent: 'center', minWidth: 'max-content', padding: '16px 0' }}>
              <div style={{ position: 'relative', display: 'flex', alignItems: 'center' }}>
                <div style={{ position: 'absolute', height: '2px', background: '#475569', width: '100%' }}></div>
                {currentData.map((item, index) => (
                  <button
                    key={item.id}
                    onClick={() => handleTimelineClick(index)}
                    style={{ 
                      position: 'relative', 
                      margin: '0 32px',
                      background: 'transparent',
                      border: 'none',
                      cursor: 'pointer'
                    }}
                  >
                    <div style={styles.timelineDot(index === activeCardIndex)}></div>
                    <span style={{ 
                      position: 'absolute', 
                      top: '24px', 
                      left: '50%',
                      transform: 'translateX(-50%)',
                      fontSize: '12px',
                      whiteSpace: 'nowrap',
                      color: index === activeCardIndex ? '#60a5fa' : '#94a3b8'
                    }}>
                      {item.date}
                    </span>
                  </button>
                ))}
              </div>
            </div>
          </div>
        </section>

        {/* Chatbot */}
        <div style={styles.chatContainer}>
          <button
            onClick={() => setIsChatOpen(!isChatOpen)}
            style={{
              padding: '16px',
              background: 'linear-gradient(135deg, #3b82f6, #8b5cf6)',
              borderRadius: '50%',
              boxShadow: '0 10px 25px rgba(59, 130, 246, 0.5)',
              border: 'none',
              color: 'white',
              cursor: 'pointer',
              transition: 'transform 0.3s'
            }}
            onMouseEnter={e => e.currentTarget.style.transform = 'scale(1.1)'}
            onMouseLeave={e => e.currentTarget.style.transform = 'scale(1)'}
          >
            {isChatOpen ? <X size={24} /> : <Bot size={24} />}
          </button>
          
          {isChatOpen && (
            <div style={styles.chatBox}>
              <div style={{ 
                padding: '16px', 
                borderBottom: '1px solid rgba(100, 116, 139, 0.3)',
                background: 'rgba(15, 23, 42, 0.5)'
              }}>
                <h3 style={{ fontWeight: '600', fontSize: '16px' }}>Assistant IA - SmolAgent</h3>
                <p style={{ fontSize: '12px', color: '#94a3b8' }}>Powered by Qwen2.5-Coder-32B</p>
              </div>
              
              <div style={{ 
                flex: 1, 
                overflowY: 'auto', 
                padding: '16px',
                display: 'flex',
                flexDirection: 'column'
              }}>
                {chatMessages.map((msg, index) => (
                  <div key={index} style={msg.role === 'user' ? styles.messageUser : styles.messageAssistant}>
                    <div style={{ display: 'flex', alignItems: 'flex-start', gap: '8px' }}>
                      {msg.role === 'assistant' ? <Bot size={16} /> : <User size={16} />}
                      <p style={{ fontSize: '14px', margin: 0 }}>{msg.content}</p>
                    </div>
                  </div>
                ))}
                {isLoading && (
                  <div style={styles.messageAssistant}>
                    <div style={{ display: 'flex', gap: '4px' }}>
                      <span style={{ animation: 'pulse 1.5s infinite' }}>.</span>
                      <span style={{ animation: 'pulse 1.5s infinite 0.2s' }}>.</span>
                      <span style={{ animation: 'pulse 1.5s infinite 0.4s' }}>.</span>
                    </div>
                  </div>
                )}
                <div ref={chatEndRef} />
              </div>
              
              <div style={{ 
                padding: '16px', 
                borderTop: '1px solid rgba(100, 116, 139, 0.3)',
                background: 'rgba(15, 23, 42, 0.5)'
              }}>
                <div style={{ display: 'flex', gap: '8px' }}>
                  <input
                    type="text"
                    value={inputMessage}
                    onChange={(e) => setInputMessage(e.target.value)}
                    onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
                    placeholder="Posez une question sur mon profil..."
                    disabled={isLoading}
                    style={{
                      flex: 1,
                      padding: '8px 12px',
                      background: 'rgba(71, 85, 105, 0.3)',
                      borderRadius: '8px',
                      border: '1px solid rgba(100, 116, 139, 0.3)',
                      color: 'white',
                      fontSize: '14px',
                      outline: 'none'
                    }}
                  />
                  <button
                    onClick={sendMessage}
                    disabled={isLoading}
                    style={{
                      padding: '8px 12px',
                      background: isLoading ? 'rgba(71, 85, 105, 0.5)' : 'linear-gradient(135deg, #3b82f6, #8b5cf6)',
                      borderRadius: '8px',
                      border: 'none',
                      color: 'white',
                      cursor: isLoading ? 'not-allowed' : 'pointer',
                      transition: 'transform 0.2s'
                    }}
                    onMouseEnter={e => !isLoading && (e.currentTarget.style.transform = 'scale(1.05)')}
                    onMouseLeave={e => e.currentTarget.style.transform = 'scale(1)'}
                  >
                    <Send size={20} />
                  </button>
                </div>
              </div>
            </div>
          )}
        </div>
      </main>

      <style jsx>{`
        @keyframes pulse {
          0%, 60%, 100% {
            opacity: 0.3;
          }
          30% {
            opacity: 1;
          }
        }
      `}</style>
    </div>
  );
};

export default Portfolio;