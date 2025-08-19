#!/usr/bin/env python3
"""
FRIDAY AI: Test Script for Triotech Sales Assistant
This script tests the new Triotech knowledge base and lead generation functionality.
"""

import asyncio
import os
import sys
import json

# Add current directory to path
sys.path.append(os.path.dirname(__file__))

# Import tools for testing
from tools import triotech_info, create_lead

async def test_triotech_knowledge():
    """Test the Triotech knowledge base tool"""
    
    print("FRIDAY AI: Testing Triotech Knowledge Base")
    print("=" * 50)
    
    test_queries = [
        "Tell me about Justtawk",
        "What is Convoze?",
        "List all products",
        "Do you support Hindi and English?",
        "What is your pricing model?",
        "Why choose Triotech?",
        "Random query that should not match"
    ]
    
    for query in test_queries:
        print(f"\nQuery: {query}")
        try:
            result = await triotech_info(query)
            print(f"Result: {result}")
        except Exception as e:
            print(f"Error: {e}")
    
    print("\n" + "=" * 50)

async def test_lead_creation():
    """Test the lead creation functionality"""
    
    print("FRIDAY AI: Testing Lead Creation")
    print("=" * 50)
    
    # Test valid lead
    print("\nTest 1: Valid Lead")
    try:
        result = await create_lead(
            name="Rajesh Kumar",
            email="rajesh@techcorp.com",
            company="Tech Corp India",
            interest="AI Voice Bot",
            phone="9876543210",
            job_title="CTO",
            budget="50k-100k",
            timeline="Q1 2025"
        )
        print(f"Result: {result}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test invalid email
    print("\nTest 2: Invalid Email")
    try:
        result = await create_lead(
            name="John Doe",
            email="invalid-email",
            company="Test Company",
            interest="AI Solutions"
        )
        print(f"Result: {result}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test missing required fields
    print("\nTest 3: Missing Required Fields")
    try:
        result = await create_lead(
            name="Jane Smith",
            email="jane@company.com",
            company="",  # Missing company
            interest="AI Chat Bot"
        )
        print(f"Result: {result}")
    except Exception as e:
        print(f"Error: {e}")
    
    print("\n" + "=" * 50)

def test_lead_files():
    """Check if lead files were created"""
    
    print("FRIDAY AI: Checking Lead Files")
    print("=" * 50)
    
    leads_dir = "leads"
    if os.path.exists(leads_dir):
        files = os.listdir(leads_dir)
        print(f"Lead files found: {len(files)}")
        
        for file in files:
            if file.endswith('.json'):
                file_path = os.path.join(leads_dir, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        lead_data = json.load(f)
                    print(f"\nFile: {file}")
                    print(f"Name: {lead_data.get('name', 'N/A')}")
                    print(f"Email: {lead_data.get('email', 'N/A')}")
                    print(f"Company: {lead_data.get('company', 'N/A')}")
                    print(f"Interest: {lead_data.get('interest', 'N/A')}")
                    print(f"Timestamp: {lead_data.get('timestamp', 'N/A')}")
                except Exception as e:
                    print(f"Error reading {file}: {e}")
    else:
        print("Leads directory not found")
    
    print("\n" + "=" * 50)

async def main():
    """Run all tests"""
    
    print("FRIDAY AI: Triotech Sales Assistant Test Suite")
    print("=" * 60)
    
    # Test knowledge base
    await test_triotech_knowledge()
    
    # Test lead creation
    await test_lead_creation()
    
    # Check lead files
    test_lead_files()
    
    print("FRIDAY AI: All tests completed!")

if __name__ == "__main__":
    asyncio.run(main())
