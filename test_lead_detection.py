#!/usr/bin/env python3
"""
Test the enhanced lead detection functionality
"""

import asyncio
from tools import detect_lead_intent

async def test_lead_detection():
    """Test the lead intent detection"""
    
    print("Testing Lead Intent Detection")
    print("=" * 40)
    
    test_messages = [
        "I am anurag from techtalk india",
        "My name is John from Tech Corp",
        "We need AI solutions for our company",
        "Can you show me a demo?",
        "What is the pricing?",
        "Hello, how are you?",
        "I work at Microsoft India",
        "Our organization needs voice bots"
    ]
    
    for message in test_messages:
        result = await detect_lead_intent(message)
        print(f"Message: '{message}'")
        print(f"Detection: {result}")
        print("-" * 40)

if __name__ == "__main__":
    asyncio.run(test_lead_detection())
