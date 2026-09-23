import asyncio

from fastmcp import Client
from ollama import AsyncClient as OllamaClient

client = Client("http://localhost:8000/mcp")
OLLAMA_MODEL = "qwen3"

ollama = OllamaClient()

def mcp_tools_to_ollama_format(mcp_tools):
    return [
        {
            "type": "function",
            "function": {
                "name": t.name,
                "description": t.description or "",
                "parameters": t.input_schema,
            },
        }
        for t in mcp_tools
    ]

async def ask(prompt: str):
    async with client:
        tools = mcp_tools_to_ollama_format(await client.list_tools())
        messages = [{"role": "user", "content": prompt}]
    
        response = await ollama.chat(model=OLLAMA_MODEL, messages=messages, tools=tools)
        messages.append(response.message)

        if response.message.tool_calls:
            for call in response.message.tool_calls:
                result = await client.call_tool(call.function.name, call.function.arguments)
                messages.append({
                    "role": "tool",
                    "tool_name": call.function.name,
                    "content": str(result),
                })

            final = await ollama.chat(model=OLLAMA_MODEL, messages=messages)
            print(final.message.content)
        else:
            print(response.message.content)

asyncio.run(ask("What are my classes?"))