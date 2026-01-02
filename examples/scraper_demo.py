"""
Demo: Web scraping with Axon
"""
from axon import Agent
from axon_tools.scraper import scrape_url

agent = Agent("WebResearcher", system="You analyze web content.")

# Register scraping tool
agent.tool(scrape_url)

# Ask agent to scrape and summarize
result = agent.ask("Scrape https://example.com and summarize the main content")
print(result)
