import os
import anthropic
from tono import Agent
from tono.models.anthropic import CompletionClient
from tono.tools import http_request, write_to_file

anthropic_client = anthropic.Anthropic(
    api_key=os.environ.get("ANTHROPIC_API_KEY"),
)
client = CompletionClient(client=anthropic_client)

# agent creation
agent = Agent(
    name="claude-agent",
    client=client,
    tools=[write_to_file, http_request],
    context=[
        {
            "role": "assistant",
            "content": "You are a helpful assistant that can visit websites by making http requests and write text to files. Use the supplied tools to complete the objective.",
        }
    ],
)

# run the agent
agent.start(
    objective="Check what is trending by visiting a popular news website, and write a summary of the top 10 news articles to a markdown file."
)
