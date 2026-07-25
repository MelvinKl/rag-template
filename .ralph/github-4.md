# Task: Improve MCp Interface

Task Number: 4
Branch: ai/issue-4-improve-mcp-interface

## Required Task

Improve the MCP Interface.
It should Not generate the answer to the question, but only Return the sources and applicable snippets from the database.

## Steps

- [x] 1. Identify the MCP server methods that need to be modified to return only sources and snippets.
  - Acceptance Criteria:
    - The methods `chat_simple` and `chat_with_history` in `rag_mcp_server.py` are identified as needing modification.
    - The expected behavior is defined: return only the citations (list of objects with content and metadata) for `chat_simple` and only the citations for `chat_with_history` (removing answer and finish_reason).

- [ ] 2. Verify that `chat_simple` in `services/mcp-server/src/rag_mcp_server.py` already returns only citations.
  - Acceptance Criteria:
    - Confirmed: The method at line 54 already returns `list[dict]` of simplified citations (each with `content` and `metadata` keys) and does not return `response.answer`.
    - Update `chat_simple_returns` in `services/mcp-server/src/settings/mcp_settings.py` (line 49) from `"The answer from the RAG system as plain text."` to accurately describe the list-of-citations return type (see Step 4).

- [ ] 3. Verify that `chat_with_history` in `services/mcp-server/src/rag_mcp_server.py` already returns only citations.
  - Acceptance Criteria:
    - Confirmed: The method at line 69 already returns `list[dict]` of simplified citations and does not return answer or finish_reason.
    - Update `chat_with_history_returns` in `services/mcp-server/src/settings/mcp_settings.py` (lines 71-78) from the old description (listing answer, finish_reason, citations) to accurately describe the list-of-citations return type (see Step 4).

- [ ] 4. Update `MCPSettings` fields in `services/mcp-server/src/settings/mcp_settings.py` to match actual return values.
  - Acceptance Criteria:
    - `chat_simple_returns` (line 49): Change from `"The answer from the RAG system as plain text."` to a description of the list of citation dicts (each with `content` and `metadata` keys).
    - `chat_with_history_returns` (lines 71-78): Change from the multi-line description mentioning answer/finish_reason/citations to a description matching the list-of-citation-dicts return type.
    - `chat_simple_description` (lines 42-47): Update `"get back the answer as plain text"` to reflect that citations are returned, not the answer directly.
    - `chat_with_history_description` (lines 59-65): Update `"get structured response"` to reflect that only citations are returned.

- [ ] 5. Update tests in `services/mcp-server/tests/docstring_system_test.py` to verify the new settings values.
  - Acceptance Criteria:
    - Update the `test_mcp_settings_defaults` test (line 198) which asserts `chat_simple_returns` default is `"The answer from the RAG system as plain text."` — change expected value to the new description.
    - Update the `test_mcp_settings_defaults` test which asserts `chat_with_history_returns` default matches the old multi-line description — change expected value to the new description.
    - Update any integration tests in `test_integration_*` methods (lines 230-363) that render docstrings with the old return descriptions.
    - No new unit tests for `RagMcpServer` methods are needed at this time since the method behavior (returning only citations) is already correct and unchanged.

- [ ] 6. Run `make test` from `services/mcp-server/` and confirm it succeeds.
  - Acceptance Criteria:
    - Run: `make test` in `services/mcp-server/` directory (which executes `poetry run python -m pytest tests`).
    - The command exits with a zero status code, indicating all tests pass.