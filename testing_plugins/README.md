# FRIDAY AI: Testing Environment for Conversation Logging

This directory contains dummy plugin implementations for testing the FRIDAY AI conversation logging system without modifying actual LiveKit plugin files.

## Directory Structure

```
testing_plugins/
├── __init__.py
└── livekit/
    ├── __init__.py
    └── plugins/
        ├── __init__.py
        ├── google/
        │   ├── __init__.py
        │   └── llm.py          # Dummy Google LLM with logging
        └── cartesia/
            ├── __init__.py
            └── tts.py          # Dummy Cartesia TTS with logging
```

## Purpose

- **Safe Testing**: Test conversation logging without touching actual installed LiveKit plugins
- **Development**: Develop and debug logging functions in isolation
- **Validation**: Verify the hybrid logging approach works correctly
- **Documentation**: Demonstrate logging implementation with working examples

## Features

### Dummy Google LLM (`testing_plugins/livekit/plugins/google/llm.py`)

- **Class**: `LLM` - Minimal Google LLM implementation
- **Logging Function**: `_log_user_message(user_input, input_type="voice")`
- **Methods**:
  - `agenerate()` - Async generation with user input logging
  - `generate()` - Sync generation with user input logging
- **Functionality**: Logs user input to JSON conversation file

### Dummy Cartesia TTS (`testing_plugins/livekit/plugins/cartesia/tts.py`)

- **Class**: `TTS` - Minimal Cartesia TTS implementation
- **Logging Function**: `_log_tts_message(agent_response)`
- **Methods**:
  - `asynthesize()` - Async synthesis with agent response logging
  - `synthesize()` - Sync synthesis with agent response logging
  - `synthesize_streaming()` - Streaming synthesis with complete response logging
- **Functionality**: Logs complete agent responses to JSON conversation file

## Usage

### Running Tests

1. **Interactive Test Script**:
   ```bash
   python test_dummy_plugins.py
   ```
   
   Choose from:
   - Full async test
   - Sync only test  
   - Both tests

2. **Direct Import Testing**:
   ```python
   import sys
   import os
   
   # Add testing plugins to path
   sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'testing_plugins'))
   
   # Import dummy plugins
   from livekit.plugins.google.llm import LLM as GoogleLLM
   from livekit.plugins.cartesia.tts import TTS as CartesiaTTS
   
   # Use like normal plugins
   llm = GoogleLLM()
   tts = CartesiaTTS()
   ```

### Expected Output

The dummy plugins will:

1. **Initialize**: Display startup messages with "FRIDAY AI:" prefix
2. **Log Messages**: Show logging activity for each user input and agent response
3. **Generate Responses**: Return dummy Hindi responses for testing
4. **Create JSON**: Build conversation log in `conversations/` directory

### Sample Conversation Log

```json
{
  "conversation": [
    {
      "timestamp": "2024-08-18T14:30:00.123456",
      "role": "user",
      "content": "नमस्ते, आप कैसे हैं?",
      "input_type": "voice"
    },
    {
      "timestamp": "2024-08-18T14:30:01.234567",
      "role": "agent", 
      "content": "यह एक परीक्षण उत्तर है। (This is a test response.)",
      "output_type": "voice"
    }
  ]
}
```

## Integration with Main Project

### Import Pattern

To use these dummy plugins in your main agent code:

```python
# For testing (add this at the top of your script)
if TESTING_MODE:
    import sys
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'testing_plugins'))

# Import works the same for both dummy and real plugins
from livekit.plugins.google import LLM
from livekit.plugins.cartesia import TTS
```

### Configuration

The dummy plugins use the same `config.py` module:

- **Log Path**: `config.get_conversation_log_path()`
- **Setup**: `config.setup_conversation_log()`
- **JSON Format**: Same structure as production logging

## Advantages

1. **No Risk**: Never modifies actual installed plugin files
2. **Fast Testing**: Immediate feedback without plugin installation
3. **Debugging**: Easy to add debug prints and test modifications
4. **Isolation**: Test logging logic without LiveKit dependencies
5. **Documentation**: Clear examples of how logging should work

## Limitations

1. **No Real Audio**: Returns dummy audio data instead of actual synthesis
2. **No Real LLM**: Returns fixed responses instead of AI generation
3. **No Network**: No actual API calls to Google or Cartesia services
4. **Simplified**: Basic implementations without full plugin functionality

## Migration to Production

When ready for production:

1. **Test First**: Verify logging works with dummy plugins
2. **Use Docker**: Apply modifications using Docker deployment scripts
3. **Backup**: Ensure backup files in `backup_plugin_modifications/` are current
4. **Verify**: Use Docker verification scripts to confirm modifications applied correctly

## Troubleshooting

### Import Errors

If imports fail:
```python
# Add debugging
import sys
print("Python path:", sys.path)
print("Testing plugins directory exists:", os.path.exists('testing_plugins'))
```

### Logging Issues

If logging doesn't work:
1. Check `config.py` is in the project root
2. Verify `conversations/` directory permissions
3. Ensure JSON file is writable

### Module Not Found

If modules aren't found:
```bash
# Check directory structure
tree testing_plugins
# or
dir /s testing_plugins
```

## Next Steps

1. **Test Thoroughly**: Run all test scenarios with dummy plugins
2. **Validate Output**: Verify conversation logs are correctly formatted
3. **Docker Deploy**: Use Docker scripts for production deployment
4. **Monitor Logs**: Check conversation logs in production environment

---

**Note**: This testing environment is specifically designed for the FRIDAY AI hybrid conversation logging system. All dummy implementations include the same logging functions that will be used in production, ensuring testing accuracy.
