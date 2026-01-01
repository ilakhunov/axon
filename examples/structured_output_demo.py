import os
import sys

# Add project root to path for local run
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from axon import Agent
from pydantic import BaseModel, Field

class EmailExtraction(BaseModel):
    """Structured response for email extraction."""
    email: str = Field(description="The extracted email address")
    confidence: float = Field(description="Confidence score 0-1", ge=0, le=1)
    domain: str = Field(description="Email domain (e.g., gmail.com)")

def main():
    print("🧠 Testing Structured Outputs...")
    
    agent = Agent("EmailBot", system="You are an email extraction assistant.")
    
    # Check for API Key
    if not os.environ.get("OPENAI_API_KEY"):
        print("\n❌ Error: OPENAI_API_KEY not found.")
        return

    # Test 1: Extract email with structured output
    text = "Contact me at john.doe@example.com for more information."
    print(f"\n📝 Input: '{text}'")
    print(f"🎯 Requesting structured output: {EmailExtraction.__name__}\n")
    
    result = agent.ask(
        f"Extract the email from this text: {text}",
        response_model=EmailExtraction
    )
    
    print(f"\n✅ Result type: {type(result)}")
    print(f"📧 Email: {result.email}")
    print(f"📊 Confidence: {result.confidence}")
    print(f"🌐 Domain: {result.domain}")
    
    # Test 2: Complex extraction
    print("\n" + "="*50)
    
    class Person(BaseModel):
        """Person information."""
        name: str
        email: str
        phone: str | None = None
    
    text2 = "My name is Alice Smith, reach me at alice@company.com or call 555-1234"
    print(f"\n📝 Input: '{text2}'")
    print(f"🎯 Requesting structured output: {Person.__name__}\n")
    
    person = agent.ask(
        f"Extract person info from: {text2}",
        response_model=Person
    )
    
    print(f"\n✅ Result:")
    print(f"👤 Name: {person.name}")
    print(f"📧 Email: {person.email}")
    print(f"📞 Phone: {person.phone}")

if __name__ == "__main__":
    main()
