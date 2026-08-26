"""Module for testing the MCP server chat methods."""

import pytest
from unittest.mock import AsyncMock, MagicMock

from src.rag_mcp_server import RagMcpServer
from src.settings.mcp_settings import MCPSettings
from rag_backend_client.openapi_client.models.chat_response import ChatResponse
from rag_backend_client.openapi_client.models.information_piece import InformationPiece
from rag_backend_client.openapi_client.models.key_value_pair import KeyValuePair
from rag_backend_client.openapi_client.models.content_type import ContentType
from fastmcp import FastMCP


# Fixtures
@pytest.fixture
def settings():
    """Create a default MCPSettings instance."""
    return MCPSettings()


@pytest.fixture
def mock_api_client():
    """Create a mock RAG API client."""
    return AsyncMock()


@pytest.fixture
def mock_mcp_server():
    """Create a mock MCP server."""
    return MagicMock(spec=FastMCP)


@pytest.fixture
def rag_mcp_server(mock_api_client, mock_mcp_server, settings):
    """Create a RagMcpServer instance with mocked dependencies."""
    return RagMcpServer(api_client=mock_api_client, mcp_server=mock_mcp_server, settings=settings)


@pytest.fixture
def sample_citations():
    """Create sample citation data for testing."""
    return [
        InformationPiece(
            page_content="Sample content 1",
            metadata=[
                KeyValuePair(key="source", value="doc1.txt"),
                KeyValuePair(key="page", value="1"),
            ],
            type=ContentType.TEXT,
        ),
        InformationPiece(
            page_content="Sample content 2",
            metadata=[
                KeyValuePair(key="source", value="doc2.txt"),
                KeyValuePair(key="page", value="2"),
            ],
            type=ContentType.TEXT,
        ),
    ]


@pytest.fixture
def sample_chat_response(sample_citations):
    """Create a sample chat response with citations and answer."""
    response = MagicMock(spec=ChatResponse)
    response.citations = sample_citations
    response.answer = "This is the answer that should not be returned"
    response.finish_reason = "stop"
    return response


# Tests for chat_simple method
@pytest.mark.asyncio
async def test_chat_simple_returns_only_citations(rag_mcp_server, mock_api_client, sample_chat_response):
    """Test that chat_simple returns only citations without the answer."""
    # Setup
    rag_mcp_server._handle_chat = AsyncMock(return_value=sample_chat_response)

    # Execute
    result = await rag_mcp_server.chat_simple(session_id="test_session", message="test message")

    # Verify that skip_answer_generation was set to True
    call_args = rag_mcp_server._handle_chat.call_args
    assert call_args is not None
    chat_request = call_args[0][1]  # Second argument is chat_request
    assert chat_request.skip_answer_generation is True

    # Verify
    assert isinstance(result, list)
    assert len(result) == 2
    assert result[0]["content"] == "Sample content 1"
    assert result[0]["metadata"] == {"source": "doc1.txt", "page": "1"}
    assert result[1]["content"] == "Sample content 2"
    assert result[1]["metadata"] == {"source": "doc2.txt", "page": "2"}

    # Verify that the answer is not included in the result
    for item in result:
        assert "answer" not in item


@pytest.mark.asyncio
async def test_chat_with_history_returns_only_citations(rag_mcp_server, mock_api_client, sample_chat_response):
    """Test that chat_with_history returns only citations without the answer."""
    # Setup
    rag_mcp_server._handle_chat = AsyncMock(return_value=sample_chat_response)

    # Execute
    result = await rag_mcp_server.chat_with_history(
        session_id="test_session",
        message="test message",
        history=[{"role": "user", "message": "previous message"}],
    )

    # Verify that skip_answer_generation was set to True
    call_args = rag_mcp_server._handle_chat.call_args
    assert call_args is not None
    chat_request = call_args[0][1]  # Second argument is chat_request
    assert chat_request.skip_answer_generation is True

    # Verify
    assert isinstance(result, list)
    assert len(result) == 2
    assert result[0]["content"] == "Sample content 1"
    assert result[0]["metadata"] == {"source": "doc1.txt", "page": "1"}
    assert result[1]["content"] == "Sample content 2"
    assert result[1]["metadata"] == {"source": "doc2.txt", "page": "2"}

    # Verify that the answer is not included in the result
    for item in result:
        assert "answer" not in item


@pytest.mark.asyncio
async def test_chat_simple_handles_empty_citations(rag_mcp_server, mock_api_client):
    """Test that chat_simple handles empty citations correctly."""
    # Setup
    empty_response = MagicMock(spec=ChatResponse)
    empty_response.citations = []
    empty_response.answer = "This answer should not be returned"
    empty_response.finish_reason = "stop"
    rag_mcp_server._handle_chat = AsyncMock(return_value=empty_response)

    # Execute
    result = await rag_mcp_server.chat_simple(session_id="test_session", message="test message")

    # Verify that skip_answer_generation was set to True
    call_args = rag_mcp_server._handle_chat.call_args
    assert call_args is not None
    chat_request = call_args[0][1]  # Second argument is chat_request
    assert chat_request.skip_answer_generation is True

    # Verify
    assert isinstance(result, list)
    assert len(result) == 0


@pytest.mark.asyncio
async def test_chat_with_history_handles_empty_citations(rag_mcp_server, mock_api_client):
    """Test that chat_with_history handles empty citations correctly."""
    # Setup
    empty_response = MagicMock(spec=ChatResponse)
    empty_response.citations = []
    empty_response.answer = "This answer should not be returned"
    empty_response.finish_reason = "stop"
    rag_mcp_server._handle_chat = AsyncMock(return_value=empty_response)

    # Execute
    result = await rag_mcp_server.chat_with_history(session_id="test_session", message="test message", history=[])

    # Verify that skip_answer_generation was set to True
    call_args = rag_mcp_server._handle_chat.call_args
    assert call_args is not None
    chat_request = call_args[0][1]  # Second argument is chat_request
    assert chat_request.skip_answer_generation is True

    # Verify
    assert isinstance(result, list)
    assert len(result) == 0
