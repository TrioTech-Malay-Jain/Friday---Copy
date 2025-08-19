# FRIDAY AI: Dummy Cartesia plugin package init
"""
Testing Cartesia plugin package for FRIDAY AI conversation logging system
"""

from .tts import TTS, TTSVoice, create_cartesia_tts, get_voices

__all__ = ["TTS", "TTSVoice", "create_cartesia_tts", "get_voices"]
