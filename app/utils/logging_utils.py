import logging

def setup_logging():
    """Configures basic logging for the application."""
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')