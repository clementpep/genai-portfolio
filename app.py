"""
Premium GenAI Portfolio Application
Deployed on Hugging Face Spaces with Gradio
Enhanced with dark green/cream/gray premium design
Version: 3.0 - Refactored modular architecture with easter egg feature

Main entry point for the portfolio application.
"""

from ui.interface import create_interface
from config.settings import SERVER_NAME, SERVER_PORT, DEBUG_MODE, SHOW_ERROR


def main():
    """
    Main application entry point.
    Creates the Gradio interface and launches the server.
    """
    print("Initializing Clément Peponnet's Portfolio Application...")
    print("Version 3.0 - Modular Architecture")

    # Create the interface
    app = create_interface()

    # Launch the application
    print(f"Launching server on {SERVER_NAME}:{SERVER_PORT}")
    app.launch(
        server_name=SERVER_NAME,
        server_port=SERVER_PORT,
        debug=DEBUG_MODE,
        show_error=SHOW_ERROR,
    )


if __name__ == "__main__":
    main()
