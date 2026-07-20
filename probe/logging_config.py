import logging

def setup_logging(level=logging.WARNING):
    """
    Configure root logging. Safe to call more than once per process -
    logging.basicConfig() is a no-op if handlers are already configured.
    """
    logging.basicConfig(level=level, format="%(levelname)s:%(name)s:%(message)s")
