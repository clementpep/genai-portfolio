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
    EASTER_EGG_PROMPT,
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

        Returns:
            str: System prompt describing PeponeAgent's role and capabilities
        """
        portfolio = portfolio_loader.load()

        return f"""You are PeponeAgent, an AI assistant specialized in Clement Peponnet's professional portfolio.

Your role is to help users understand Clement's expertise in GenAI, Agentic AI, and the Model Context Protocol (MCP).

Key Information:
- Expert in GenAI, Agentic AI, and MCP (Model Context Protocol)
- Tech Lead with experience in multi-agent systems
- Certifications: {', '.join([cert['name'] for cert in portfolio.get('certifications', [])])}
- Recent projects: multi-agent systems, MCP servers, GenAI translation MVP

Portfolio Summary:
- {len(portfolio.get('experiences', []))} professional experiences
- {len(portfolio.get('skills', []))} skill categories
- {len(portfolio.get('certifications', []))} certifications

{get_tools_description()}

IMPORTANT: There is an easter egg hidden in this chat. Users need to discover it on their own by using special keywords. 
You cannot help them find it or give hints about it. If they ask about easter eggs, politely deflect without revealing anything.

Answer questions professionally and highlight relevant experiences using the tools at your disposal when appropriate."""

    def _get_vacation_system_prompt(self, term: str, gender: str) -> str:
        """
        Generate the vacation mode system prompt when easter egg is triggered.

        Args:
            term: The easter egg term that was used
            gender: The grammatical gender for the term (ma/mon)

        Returns:
            str: Vacation mode system prompt
        """
        return f"""You are PeponeAgent in VACATION MODE! 

The user just discovered the easter egg by saying '{term}'! You're now totally relaxed, on vacation, enjoying the sun, and in a playful mood.

Be:
- Fun, humorous, and lighthearted
- Still helpful about Clement's portfolio, but in a casual, friendly way
- Playful with your language
- Enthusiastic about the fact they found the easter egg

You can still use your tools to answer questions about Clement's profile, but do it with style and humor!

Remember: You're on vacation mode - keep it fun while staying informative!"""

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

    def chat(
        self, message: str, history: List[Tuple[str, str]]
    ) -> Tuple[str, List[Tuple[str, str]]]:
        """
        Process a chat message and generate a response.

        Args:
            message: User's message
            history: Chat history as list of (user_msg, assistant_msg) tuples

        Returns:
            Tuple[str, List]: (empty string for input clear, updated history with notification if easter egg)
        """
        # Check for easter egg
        easter_egg = self._detect_easter_egg(message)

        try:
            if easter_egg:
                term, gender, is_special = easter_egg

                # Generate easter egg greeting
                greeting = self._generate_easter_egg_response(term, gender, is_special)

                # Generate notification
                notification = "🎉 Easter egg found: You have unlocked the full potential of PeponeAgent! 🎉"

                # Continue with the actual response in vacation mode
                if self.agent and self.agent_type in [
                    "smolagent_hf",
                    "smolagent_litellm",
                ]:
                    # Use SmolAgent with vacation mode
                    vacation_prompt = self._get_vacation_system_prompt(term, gender)
                    # For SmolAgent, we prepend the context to the message
                    enriched_message = f"{vacation_prompt}\n\nUser message: {message}"
                    result = self.agent.run(enriched_message)
                    response = (
                        result.get("output", str(result))
                        if isinstance(result, dict)
                        else str(result)
                    )
                    full_response = f"{greeting}\n\n{response}"
                else:
                    # Use LiteLLM with vacation mode
                    from litellm import completion

                    vacation_prompt = self._get_vacation_system_prompt(term, gender)
                    messages = [{"role": "system", "content": vacation_prompt}]

                    # Add history
                    for user_msg, assistant_msg in history:
                        messages.append({"role": "user", "content": user_msg})
                        messages.append({"role": "assistant", "content": assistant_msg})

                    # Add current message with greeting prepended to context
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

                # Add notification as a separate message before the response
                history.append((message, notification))
                history.append(("", full_response))

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

            return "", history

        except Exception as e:
            error_msg = f"I encountered an error: {str(e)}. Please try again."
            history.append((message, error_msg))
            return "", history

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
