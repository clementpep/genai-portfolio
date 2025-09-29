"""
Agent initialization and chat logic.

This module handles the initialization of the LLM agent (SmolAgent or LiteLLM)
and manages the chat functionality including easter egg detection.
"""

from typing import List, Tuple, Optional
import os

from config.settings import (
    USE_HF_MODEL,
    USE_SMOLAGENT_WITH_LITELLM,
    FREE_HF_MODELS,
    HF_TOKEN,
    LITELLM_MODEL,
    OPENAI_API_KEY,
    AGENT_MAX_STEPS,
    AGENT_VERBOSITY,
    EASTER_EGG_TERMS,
)
from tools.portfolio_tools import AVAILABLE_TOOLS, get_tools_description
from core.data_loader import portfolio_loader


class AgentManager:
    """
    Manages the LLM agent initialization and chat interactions.
    Handles both SmolAgent and LiteLLM backends, plus easter egg detection.
    """

    def __init__(self):
        self.agent = None
        self.working_model = None
        self.agent_type = None
        self._initialize_agent()

    def _initialize_agent(self):
        """Initialize the appropriate agent based on environment configuration."""

        if USE_HF_MODEL:
            self._initialize_smolagent_hf()
        elif USE_SMOLAGENT_WITH_LITELLM:
            self._initialize_smolagent_litellm()
        else:
            self._initialize_litellm()

    def _initialize_smolagent_hf(self):
        """Initialize SmolAgent with HuggingFace models (free tier)."""
        try:
            from smolagents import CodeAgent, InferenceClientModel

            self.working_model = FREE_HF_MODELS[0]

            if self.working_model:
                print(f"Using HuggingFace model: {self.working_model}")
                model = InferenceClientModel(
                    model_id=self.working_model,
                    temperature=0.7,
                    token=HF_TOKEN,
                )
                self.agent = CodeAgent(
                    model=model,
                    tools=AVAILABLE_TOOLS,
                    max_steps=AGENT_MAX_STEPS,
                    verbosity_level=AGENT_VERBOSITY,
                )
                self.agent_type = "smolagent_hf"
            else:
                print("No working HF models found, falling back to LiteLLM")
                self._initialize_litellm()

        except Exception as e:
            print(f"Error initializing SmolAgent HF: {e}")
            self._initialize_litellm()

    def _initialize_smolagent_litellm(self):
        """Initialize SmolAgent with LiteLLM backend (paid)."""
        try:
            from smolagents import CodeAgent, LiteLLMModel

            model = LiteLLMModel(
                model_id=LITELLM_MODEL,
                api_key=OPENAI_API_KEY,
            )
            self.agent = CodeAgent(
                model=model,
                tools=AVAILABLE_TOOLS,
                max_steps=AGENT_MAX_STEPS,
                verbosity_level=AGENT_VERBOSITY,
            )
            self.working_model = LITELLM_MODEL
            self.agent_type = "smolagent_litellm"
            print(f"Using SmolAgent with LiteLLM: {LITELLM_MODEL}")

        except Exception as e:
            print(f"Error initializing SmolAgent LiteLLM: {e}")
            self._initialize_litellm()

    def _initialize_litellm(self):
        """Initialize pure LiteLLM without agent tools (paid but faster)."""
        self.agent = None
        self.working_model = LITELLM_MODEL
        self.agent_type = "litellm"
        print(f"Using pure LiteLLM: {LITELLM_MODEL}")

    def _get_base_system_prompt(self) -> str:
        """
        Generate the base system prompt for the agent.
        Optimized for faster response times.

        Returns:
            str: Concise system prompt describing PeponeAgent's role
        """
        return """Tu es PeponeAgent, spécialisé dans le portfolio GenAI de Clément Peponnet.  

Expertises : GenAI, Agentic AI, MCP (Model Context Protocol), Azure AI  
Rôle : Tech Lead en systèmes multi-agents  

Si nécessaire, utilise tes outils pour répondre aux questions concernant :  
- Les expériences professionnelles et projets  
- Les compétences techniques et certifications  
- La formation et les réalisations  
- L’adéquation du profil avec des besoins ou offres d’emploi  

Sois concis, professionnel et utilise les outils uniquement quand c’est nécessaire, en ciblant spécifiquement ceux dont tu aurais besoin.
"""

    def _get_chill_system_prompt(self, term: str, gender: str) -> str:
        """
        Generate the chill mode system prompt when easter egg is triggered.

        Args:
            term: The easter egg term that was used
            gender: The grammatical gender for the term (ma/mon)

        Returns:
            str: Chill mode system prompt
        """
        return f"""Tu es PeponeAgent en mode coquinou !  

L’utilisateur vient de découvrir l’easter egg en disant « {term} » !  
Tu es maintenant de chasseur de soleil, sur l'autoroute du kiff, et dans un mood coquinou.  

Tu peux toujours utiliser tes outils pour répondre aux questions sur le profil de Clément,  
mais fais-le en mode chill !"""

    def _detect_easter_egg(self, message: str) -> Optional[Tuple[str, str, bool]]:
        """
        Detect if the message contains an easter egg term.

        Args:
            message: User's message

        Returns:
            Optional[Tuple[str, str, bool]]: (term, gender, is_special) if easter egg found, None otherwise
        """
        message_lower = message.lower()

        for term, config in EASTER_EGG_TERMS.items():
            if term in message_lower:
                return (term, config["gender"], config["special"])

        return None

    def _generate_easter_egg_response(
        self, term: str, gender: str, is_special: bool
    ) -> str:
        """
        Generate the initial easter egg response.

        Args:
            term: The easter egg term
            gender: Grammatical gender (ma/mon)
            is_special: Whether this is the special tchoupinoux case

        Returns:
            str: Easter egg greeting message
        """
        if is_special and term == "tchoupinoux":
            return (
                "Coucouuuuu mon tchoupinoux du B15 !!!! Comment il va mon superbe tchoup' masqué ?? "
                "J'espère que tu as récupéré ton sticker qui te reviens de droit telle une très bonne poupouille que tu es."
            )
        else:
            return f"Coucouuuuu {gender} {term} !!!! Comment ça va par ici ??"

    def _generate_notification_html(self) -> str:
        """
        Generate the HTML for easter egg notification display.

        Returns:
            str: HTML notification element
        """
        return """
        <div class="easter-egg-notification">
            🎉 <strong>Easter Egg trouvé !</strong> Tu as débloqué le plein potentiel de PeponeAgent! 🎉
        </div>
        """

    def chat(
        self, message: str, history: List[Tuple[str, str]]
    ) -> Tuple[str, List[Tuple[str, str]], str]:
        """
        Process a chat message and generate a response.

        Args:
            message: User's message
            history: Chat history as list of (user_msg, assistant_msg) tuples

        Returns:
            Tuple[str, List, str]: (empty string for input clear, updated history, notification HTML)
        """
        # Check for easter egg
        easter_egg = self._detect_easter_egg(message)
        notification_html = ""

        try:
            if easter_egg:
                term, gender, is_special = easter_egg

                # Generate easter egg greeting
                greeting = self._generate_easter_egg_response(term, gender, is_special)

                # Generate notification HTML for UI display
                notification_html = self._generate_notification_html()

                # Continue with the actual response in chill mode
                if self.agent and self.agent_type in [
                    "smolagent_hf",
                    "smolagent_litellm",
                ]:
                    # Use SmolAgent with chill mode
                    chill_prompt = self._get_chill_system_prompt(term, gender)
                    enriched_message = f"{chill_prompt}\n\nUser message: {message}"
                    result = self.agent.run(enriched_message)
                    response = (
                        result.get("output", str(result))
                        if isinstance(result, dict)
                        else str(result)
                    )
                    full_response = f"{greeting}\n\n{response}"
                else:
                    # Use LiteLLM with chill mode
                    from litellm import completion

                    chill_prompt = self._get_chill_system_prompt(term, gender)
                    messages = [{"role": "system", "content": chill_prompt}]

                    # Add history
                    for user_msg, assistant_msg in history:
                        messages.append({"role": "user", "content": user_msg})
                        messages.append({"role": "assistant", "content": assistant_msg})

                    # Add greeting and current message
                    messages.append({"role": "assistant", "content": greeting})
                    messages.append({"role": "user", "content": message})

                    llm_response = completion(
                        model=self.working_model,
                        messages=messages,
                        api_key=OPENAI_API_KEY,
                        max_tokens=500,
                    )

                    response = llm_response.choices[0].message.content
                    full_response = f"{greeting}\n\n{response}"

                # Add response to history
                history.append((message, full_response))

            else:
                # Normal chat flow
                if self.agent and self.agent_type in [
                    "smolagent_hf",
                    "smolagent_litellm",
                ]:
                    # Use SmolAgent with tools
                    result = self.agent.run(message)
                    response = (
                        result.get("output", str(result))
                        if isinstance(result, dict)
                        else str(result)
                    )
                else:
                    # Use pure LiteLLM
                    from litellm import completion

                    context = self._get_base_system_prompt()
                    messages = [{"role": "system", "content": context}]

                    # Add history
                    for user_msg, assistant_msg in history:
                        messages.append({"role": "user", "content": user_msg})
                        messages.append({"role": "assistant", "content": assistant_msg})

                    messages.append({"role": "user", "content": message})

                    llm_response = completion(
                        model=self.working_model,
                        messages=messages,
                        api_key=OPENAI_API_KEY,
                        max_tokens=500,
                    )

                    response = llm_response.choices[0].message.content

                history.append((message, response))

            return "", history, notification_html

        except Exception as e:
            error_msg = f"I encountered an error: {str(e)}. Please try again."
            history.append((message, error_msg))
            return "", history, notification_html

    def get_model_info(self) -> str:
        """
        Get information about the currently active model.

        Returns:
            str: Model information string for display
        """
        if self.agent_type == "smolagent_hf":
            return f"SmolAgent + {self.working_model} (HuggingFace)"
        elif self.agent_type == "smolagent_litellm":
            return f"SmolAgent + {self.working_model} (LiteLLM)"
        else:
            return f"{self.working_model} (LiteLLM)"


# Create global instance
agent_manager = AgentManager()
