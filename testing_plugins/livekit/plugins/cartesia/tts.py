# FRIDAY AI: Dummy Cartesia TTS Plugin for Testing
# This is a minimal implementation for testing the conversation logging system

import json
import os
from datetime import datetime
import asyncio
import config  # Import our config module


class TTS:
    """Dummy Cartesia TTS class for testing conversation logging"""
    
    def __init__(self, voice_id="hindi-voice", language="hi"):
        self.voice_id = voice_id
        self.language = language
        print(f"FRIDAY AI: Dummy Cartesia TTS initialized - Voice: {voice_id}, Language: {language}")
    
    def _log_tts_message(self, agent_response):
        """
        FRIDAY AI: Log agent response to conversation JSON
        
        Args:
            agent_response (str): The complete agent response
        """
        try:
            # Get the conversation log file path from config
            log_file_path = config.get_conversation_log_path()
            
            # Create log entry
            log_entry = {
                "timestamp": datetime.now().isoformat(),
                "role": "agent",
                "content": agent_response,
                "output_type": "voice"
            }
            
            # Read existing log or create new
            if os.path.exists(log_file_path):
                with open(log_file_path, 'r', encoding='utf-8') as f:
                    conversation_log = json.load(f)
            else:
                conversation_log = {"conversation": []}
            
            # Append new entry
            conversation_log["conversation"].append(log_entry)
            
            # Write back to file
            with open(log_file_path, 'w', encoding='utf-8') as f:
                json.dump(conversation_log, f, ensure_ascii=False, indent=2)
                
            print(f"FRIDAY AI: Agent response logged - Content: {agent_response[:50]}...")
            
        except Exception as e:
            print(f"FRIDAY AI: Error logging agent response: {e}")
    
    async def asynthesize(self, text, **kwargs):
        """Dummy async synthesize function that logs agent response"""
        # FRIDAY AI: Log the complete agent response
        self._log_tts_message(text)
        
        # Simulate audio generation delay
        await asyncio.sleep(0.1)
        
        # Return dummy audio data
        dummy_audio = b"dummy_audio_data_for_testing"
        print(f"FRIDAY AI: Dummy TTS synthesized audio for: {text[:50]}...")
        return dummy_audio
    
    def synthesize(self, text, **kwargs):
        """Dummy sync synthesize function"""
        # FRIDAY AI: Log the complete agent response
        self._log_tts_message(text)
        
        # Return dummy audio data
        dummy_audio = b"dummy_audio_data_for_testing"
        print(f"FRIDAY AI: Dummy TTS synthesized audio for: {text[:50]}...")
        return dummy_audio
    
    async def synthesize_streaming(self, text_stream, **kwargs):
        """Dummy streaming synthesis"""
        collected_text = ""
        
        # Collect all text chunks
        async for chunk in text_stream:
            collected_text += chunk
            yield b"dummy_audio_chunk"
        
        # FRIDAY AI: Log the complete agent response after collecting all chunks
        if collected_text.strip():
            self._log_tts_message(collected_text)


class TTSVoice:
    """Dummy TTS Voice class"""
    
    def __init__(self, voice_id="hindi-voice", name="Hindi Voice"):
        self.voice_id = voice_id
        self.name = name


# Mock functions for compatibility
def create_cartesia_tts(**kwargs):
    """Create a dummy Cartesia TTS instance"""
    return TTS(**kwargs)


def get_voices():
    """Return dummy voice list"""
    return [
        TTSVoice("hindi-voice", "Hindi Voice"),
        TTSVoice("english-voice", "English Voice")
    ]


if __name__ == "__main__":
    # Test the dummy TTS
    async def test_tts():
        tts = TTS()
        test_text = "नमस्ते, यह एक परीक्षण संदेश है।"
        audio = await tts.asynthesize(test_text)
        print(f"Test complete - Input: {test_text}, Audio length: {len(audio)} bytes")
    
    # Run the test
    asyncio.run(test_tts())
