import logging
from livekit.agents import function_tool,RunContext
import requests
from langchain_community.tools import DuckDuckGoSearchRun
import json
import os
import sys
import time
from datetime import datetime

# Lead utilities (inline to avoid import issues)
LEADS_DIR = os.path.join(os.getcwd(), "leads")
os.makedirs(LEADS_DIR, exist_ok=True)

def save_lead(lead: dict) -> str:
    """Save lead as JSON file. Returns the saved file path."""
    ts = time.strftime("%Y%m%d_%H%M%S")
    filename = f"lead_{ts}.json"
    path = os.path.join(LEADS_DIR, filename)
    
    lead_data = {
        "timestamp": datetime.now().isoformat(),
        "source": "Friday AI Assistant",
        "status": "new",
        **lead
    }
    
    with open(path, "w", encoding="utf-8") as f:
        json.dump(lead_data, f, indent=2, ensure_ascii=False)
    
    logging.info(f"FRIDAY AI: Lead saved to {path}")
    return path

def is_valid_lead(lead: dict) -> bool:
    """Validate if lead has required fields."""
    required = ["name", "email", "company", "interest"]
    return all(lead.get(field) for field in required)

def validate_email(email: str) -> bool:
    """Basic email validation."""
    return "@" in email and "." in email.split("@")[-1]

# Path to triotech content
TRIOTECH_FILE = os.path.join(os.path.dirname(__file__), "data", "triotech_content.json")

def _load_triotech_data():
    """Load Triotech knowledge base data."""
    try:
        with open(TRIOTECH_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        logging.error(f"Error loading Triotech data: {e}")
        return {"products": [], "faqs": [], "differentiators": []}

@function_tool()
async def get_weather(city: str) -> str:
    """Get the current weather for a given city"""
    try:
        response = requests.get(f"https://wttr.in/{city}?format=3")
        if response.status_code == 200:
            logging.info(f"Weather for {city}: {response.text.strip()}")
            return response.text.strip()
        else:
            logging.error(f"Failed to get weather for {city}: {response.status_code}")
            return f"Failed to get weather for {city}: {response.status_code}"
    except Exception as e:
        logging.error(f"Error getting weather for {city}: {e}")
        return f"Error getting weather for {city}: {e}"
    
@function_tool()
async def search_web(query: str) -> str:
    """Search the web for information about a given query using DuckDuckGo Search"""
    try:
        results = DuckDuckGoSearchRun().run(tool_input=query)
        logging.info(f"Search results for '{query}': {results}")
        return results
    except Exception as e:
        logging.error(f"Error searching the web for '{query}': {e}")
        return f"An error occurred while searching the web for '{query}'."

@function_tool()
async def triotech_info(query: str) -> str:
    """
    Search Triotech knowledge base (products, FAQs, differentiators).
    Examples:
      - "Tell me about Justtawk"
      - "What CRMs do you support?"
      - "List all products"
      - "Why choose Triotech?"
    Returns a short Hindi (or English if query in English) answer string.
    """
    data = _load_triotech_data()
    query_lower = (query or "").lower()

    # Product lookup by name (exact substring match)
    for p in data.get("products", []):
        if p.get("name", "").lower() in query_lower:
            return f"{p['name']}: {p['desc']} (Target: {p['target']})"

    # FAQ lookup: match on words from the question text
    for faq in data.get("faqs", []):
        fq_lower = faq.get("q", "").lower()
        # simple heuristic: check if any significant word from faq question exists in query
        faq_words = [w for w in fq_lower.split() if len(w) > 3]
        if any(w in query_lower for w in faq_words):
            return f"Q: {faq['q']} → A: {faq['a']}"

    # Differentiators lookup
    if "why triotech" in query_lower or "differentiator" in query_lower or "why choose" in query_lower:
        return "Key Differentiators: " + ", ".join(data.get("differentiators", []))

    # List products
    if "list" in query_lower and "product" in query_lower:
        names = [p.get("name") for p in data.get("products", [])]
        return "Products: " + ", ".join(names) if names else "माफ़ करें, उत्पाद सूची उपलब्ध नहीं है।"

    # Fallback
    return "माफ़ करें, इस बारे में मुझे जानकारी नहीं मिली। क्या आप चाहेंगे कि मैं आपको हमारी सेल्स टीम से जोड़ दूँ?"

@function_tool()
async def create_lead(name: str, email: str, company: str, interest: str, phone: str = "", job_title: str = "", budget: str = "", timeline: str = "") -> str:
    """
    Create a new lead for Triotech sales team.
    Required: name, email, company, interest
    Optional: phone, job_title, budget, timeline
    
    Example: create_lead("John Doe", "john@company.com", "Tech Corp", "AI Voice Bot", "9876543210", "CTO", "50k-100k", "Q1 2025")
    """
    # Validate required fields
    if not all([name, email, company, interest]):
        return "कृपया सभी आवश्यक जानकारी प्रदान करें: नाम, ईमेल, कंपनी, और रुचि का विषय।"
    
    # Validate email
    if not validate_email(email):
        return "कृपया एक वैध ईमेल पता प्रदान करें।"
    
    # Create lead data
    lead_data = {
        "name": name.strip(),
        "email": email.strip().lower(),
        "company": company.strip(),
        "interest": interest.strip(),
        "phone": phone.strip() if phone else "",
        "job_title": job_title.strip() if job_title else "",
        "budget": budget.strip() if budget else "",
        "timeline": timeline.strip() if timeline else ""
    }
    
    # Validate lead
    if not is_valid_lead(lead_data):
        return "लीड डेटा में कुछ समस्या है। कृपया सभी आवश्यक फील्ड भरें।"
    
    try:
        # Save lead
        file_path = save_lead(lead_data)
        
        # Return success message
        return f"धन्यवाद {name}! आपकी जानकारी सुरक्षित कर ली गई है। हमारी सेल्स टीम जल्द ही {company} के लिए {interest} के बारे में आपसे संपर्क करेगी।"
        
    except Exception as e:
        logging.error(f"Error creating lead: {e}")
        return "माफ़ करें, लीड सेव करने में कुछ समस्या हुई है। कृपया दोबारा कोशिश करें।"

@function_tool()
async def detect_lead_intent(user_message: str) -> str:
    """
    Analyze user message to detect if they are introducing themselves or showing business interest.
    Returns guidance on how to respond for lead generation.
    
    Example: detect_lead_intent("I am John from Tech Corp")
    """
    message_lower = user_message.lower()
    
    # Check for self-introduction patterns
    intro_patterns = [
        "i am", "my name is", "this is", "i'm", 
        "from", "company", "business", "organization"
    ]
    
    # Check for business interest patterns
    interest_patterns = [
        "demo", "price", "cost", "quote", "proposal", 
        "solution", "service", "product", "help", "need"
    ]
    
    # Check for company indicators
    company_indicators = [
        "ltd", "limited", "corp", "corporation", "inc", "company",
        "pvt", "private", "llc", "solutions", "systems", "tech"
    ]
    
    has_intro = any(pattern in message_lower for pattern in intro_patterns)
    has_interest = any(pattern in message_lower for pattern in interest_patterns)
    has_company = any(indicator in message_lower for indicator in company_indicators)
    
    if has_intro and (has_company or has_interest):
        return "LEAD_OPPORTUNITY: User is introducing themselves from a company. Ask about their requirements and collect contact details."
    elif has_interest:
        return "INTEREST_DETECTED: User shows business interest. Ask qualifying questions and collect lead information."
    elif has_company:
        return "COMPANY_MENTIONED: User mentioned a company. Explore their needs and collect contact details."
    else:
        return "NO_LEAD_INTENT: Continue normal conversation."