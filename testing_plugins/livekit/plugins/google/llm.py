# FRIDAY AI: Dummy Google LLM Plugin for Testing
# This is a minimal implementation for testing the conversation logging system

import json
import os
from datetime import datetime
import config  # Import our config module


class LLM:
    """Dummy Google LLM class for testing conversation logging"""
    
    def __init__(self, model="gemini-1.5-flash"):
        self.model = model
        print(f"FRIDAY AI: Dummy Google LLM initialized with model: {model}")
    
    def _log_user_message(self, user_input, input_type="voice"):
        """
        FRIDAY AI: Log user message to conversation JSON
        
        Args:
            user_input (str): The user's input message
            input_type (str): Type of input - 'voice' or 'text'
        """
        try:
            # Get the conversation log file path from config
            log_file_path = config.get_conversation_log_path()
            
            # Create log entry
            log_entry = {
                "timestamp": datetime.now().isoformat(),
                "role": "user",
                "content": user_input,
                "input_type": input_type
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
                
            print(f"FRIDAY AI: User message logged - Type: {input_type}, Content: {user_input[:50]}...")
            
        except Exception as e:
            print(f"FRIDAY AI: Error logging user message: {e}")
    
    async def agenerate(self, prompt, **kwargs):
        """Dummy generate function that logs user input"""
        # FRIDAY AI: Log the user input (prompt)
        self._log_user_message(prompt, "voice")  # Assuming voice input for testing
        
        # Return a dummy response
        dummy_response = "यह एक परीक्षण उत्तर है। (This is a test response.)"
        print(f"FRIDAY AI: Dummy LLM generated response: {dummy_response}")
        return dummy_response
    
    def generate(self, prompt, **kwargs):
        """Dummy generate function (sync version)"""
        # FRIDAY AI: Log the user input (prompt)
        self._log_user_message(prompt, "text")  # Assuming text input for sync
        
        # Return a dummy response
        dummy_response = "यह एक परीक्षण उत्तर है। (This is a test response.)"
        print(f"FRIDAY AI: Dummy LLM generated response: {dummy_response}")
        return dummy_response


# Mock functions for compatibility
def create_google_llm(**kwargs):
    """Create a dummy Google LLM instance"""
    return LLM(**kwargs)


if __name__ == "__main__":
    # Test the dummy LLM
    llm = LLM()
    test_prompt = "नमस्ते, आप कैसे हैं?"
    response = llm.generate(test_prompt)
    print(f"Test complete - Input: {test_prompt}, Output: {response}")
