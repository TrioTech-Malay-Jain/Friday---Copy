# FRIDAY AI: Dummy Google plugin package init
"""
Testing Google plugin package for FRIDAY AI conversation logging system
"""

from .llm import LLM, create_google_llm

__all__ = ["LLM", "create_google_llm"]
