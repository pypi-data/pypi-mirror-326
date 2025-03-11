import asyncio

from mcp.server.models import InitializationOptions
import mcp.types as types
from mcp.server import NotificationOptions, Server
from pydantic import AnyUrl
import mcp.server.stdio

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("biz-mcp-server")
# Store notes as a simple key-value dict to demonstrate state management
notes: dict[str, str] = {}


@mcp.resource(uri="note://internal/notes/{name}", name="Note", description="A note resource", mime_type="text/plain")
def get_notes(name: str) -> str|None:
    """
    List available note resources.
    Each note is exposed as a resource with a custom note:// URI scheme.
    """
    return notes.get(name)

@mcp.resource(uri="note://internal/notes/", name="Notes", description="A list of note resources", mime_type="text/plain")
def get_notes() -> list[str]:
    """
    List available note resources.
    """
    return list(notes.keys())



@mcp.tool(name="add_note", description="Add a new note to the server.")
def add_note(name: str, content: str) -> None:
    """
    Add a new note to the server.
    """
    notes[name] = content


async def main():
    # Run the server using stdin/stdout streams
    await mcp.run_stdio_async();