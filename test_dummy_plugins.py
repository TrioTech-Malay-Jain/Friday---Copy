#!/usr/bin/env python3
"""
FRIDAY AI: Test Script for Dummy Plugins
This script tests the conversation logging system using dummy plugins instead of actual LiveKit plugins.
"""

import sys
import os
import asyncio
import json

# Add testing_plugins to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'testing_plugins'))

# Import our config and dummy plugins
import config
from livekit.plugins.google.llm import LLM as GoogleLLM
from livekit.plugins.cartesia.tts import TTS as CartesiaTTS


async def test_conversation_logging():
    """Test the complete conversation logging workflow"""
    
    print("FRIDAY AI: Starting conversation logging test...")
    print("=" * 60)
    
    # Setup conversation log
    config.setup_conversation_log()
    print(f"Conversation log initialized at: {config.get_conversation_log_path()}")
    print()
    
    # Initialize dummy plugins
    print("Initializing dummy plugins...")
    llm = GoogleLLM(model="gemini-1.5-flash")
    tts = CartesiaTTS(voice_id="hindi-voice", language="hi")
    print()
    
    # Test conversation flow
    print("Testing conversation flow...")
    print("-" * 40)
    
    # Simulate user input
    user_message = "नमस्ते, आप कैसे हैं?"
    print(f"User Input: {user_message}")
    
    # Generate LLM response (this will log user input)
    agent_response = await llm.agenerate(user_message)
    print(f"Agent Response: {agent_response}")
    print()
    
    # Synthesize speech (this will log agent response)
    audio_data = await tts.asynthesize(agent_response)
    print(f"Audio synthesized: {len(audio_data)} bytes")
    print()
    
    # Test another round
    print("Testing second conversation turn...")
    print("-" * 40)
    
    user_message2 = "मुझे हिंदी में बात करना पसंद है।"
    print(f"User Input: {user_message2}")
    
    agent_response2 = llm.generate(user_message2)  # Test sync version
    print(f"Agent Response: {agent_response2}")
    
    audio_data2 = tts.synthesize(agent_response2)  # Test sync version
    print(f"Audio synthesized: {len(audio_data2)} bytes")
    print()
    
    # Display conversation log
    print("Conversation Log Contents:")
    print("=" * 60)
    
    log_file_path = config.get_conversation_log_path()
    if os.path.exists(log_file_path):
        with open(log_file_path, 'r', encoding='utf-8') as f:
            log_data = json.load(f)
        
        print(json.dumps(log_data, ensure_ascii=False, indent=2))
    else:
        print("No conversation log found!")
    
    print()
    print("FRIDAY AI: Test completed successfully!")


def test_sync_only():
    """Test synchronous functions only"""
    
    print("FRIDAY AI: Testing synchronous functions...")
    print("=" * 60)
    
    # Setup conversation log
    config.setup_conversation_log()
    
    # Initialize dummy plugins
    llm = GoogleLLM()
    tts = CartesiaTTS()
    
    # Test sync workflow
    user_input = "यह एक सिंक टेस्ट है।"
    print(f"User Input: {user_input}")
    
    response = llm.generate(user_input)
    print(f"LLM Response: {response}")
    
    audio = tts.synthesize(response)
    print(f"TTS Audio: {len(audio)} bytes")
    
    # Show log
    log_file_path = config.get_conversation_log_path()
    if os.path.exists(log_file_path):
        with open(log_file_path, 'r', encoding='utf-8') as f:
            log_data = json.load(f)
        print("\nConversation Log:")
        print(json.dumps(log_data, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    print("FRIDAY AI: Conversation Logging Test Suite")
    print("=" * 60)
    
    # Run sync test first (simpler)
    print("Running synchronous test...")
    test_sync_only()
    
    print("\n" + "=" * 60)
    print("Running asynchronous test...")
    asyncio.run(test_conversation_logging())
