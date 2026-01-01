import logging
from rich.console import Console
from rich.logging import RichHandler

def get_logger(name: str = "axon") -> logging.Logger:
    logging.basicConfig(
        level="INFO",
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(rich_tracebacks=True, markup=True)]
    )
    return logging.getLogger(name)

# Global console for direct printing if needed
console = Console()
