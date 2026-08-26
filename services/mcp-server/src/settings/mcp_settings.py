"""Module that contains settings for the MCP server."""

from pydantic import Field
from pydantic_settings import BaseSettings

_CITATION_EXAMPLE = (
    "Example return value:\n"
    "[\n"
    "  {\n"
    '    "content": "Retrieved text snippet from the document...",\n'
    '    "metadata": {"source": "document.pdf", "page": 1}\n'
    "  },\n"
    "  {\n"
    '    "content": "Another relevant text snippet...",\n'
    '    "metadata": {"source": "guide.md", "page": 3}\n'
    "  }\n"
    "]"
)


class MCPSettings(BaseSettings):
    """
    Settings for the mcp server.

    Attributes
    ----------
    host : str
        The address to bind to.
    port : int
        The port to bind to.
    name : str
        Name of the mcp server.
    tool_name : str
        Name of the mcp tool.
    tool_description : str
        Description of the mcp tool.
    """

    class Config:
        """Configuration for reading fields from the environment."""

        env_prefix = "MCP_"
        case_sensitive = False

    host: str = Field(default="0.0.0.0")
    port: int = Field(default=8000)
    name: str = Field(default="RAG MCP server")

    # Chat Simple Method Configuration
    chat_simple_description: str = Field(
        default=(
            "Send a message to the RAG system and get a list of citation objects.\n\n"
            "Each citation object contains the content of the retrieved text and its metadata.\n"
            "This is the simplest way to interact with the RAG system - just provide a message "
            "and get back the relevant citations."
        )
    )
    chat_simple_parameter_descriptions: dict[str, str] = Field(
        default_factory=lambda: {
            "session_id": "Unique identifier for the chat session.",
            "message": "The message/question to ask the RAG system.",
        }
    )
    chat_simple_returns: str = Field(default="List of citation objects, each containing content and metadata.")
    chat_simple_notes: str = Field(default="")
    chat_simple_examples: str = Field(default=_CITATION_EXAMPLE)

    # Chat With History Method Configuration
    chat_with_history_description: str = Field(
        default=(
            "Send a message to the RAG system with chat history and get a list of citation objects.\n\n"
            "This method allows you to maintain conversation context by providing previous "
            "messages. The response is a list of citation objects, each containing content and metadata."
        )
    )
    chat_with_history_parameter_descriptions: dict[str, str] = Field(
        default_factory=lambda: {
            "session_id": "Unique identifier for the chat session.",
            "message": "The current message/question to ask.",
            "history": (
                "Previous conversation history. Each item should be:\n"
                '    {"role": "user" or "assistant", "message": "the message text"}'
            ),
        }
    )
    chat_with_history_returns: str = Field(default="List of citation objects, each containing content and metadata.")
    chat_with_history_notes: str = Field(default="")
    chat_with_history_examples: str = Field(default=_CITATION_EXAMPLE)
