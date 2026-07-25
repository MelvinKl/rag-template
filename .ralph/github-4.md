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

- [x] 2. Verify that `chat_simple` in `services/mcp-server/src/rag_mcp_server.py` already returns only citations.
  - Acceptance Criteria:
    - Confirmed: The method at line 54 already returns `list[dict]` of simplified citations (each with `content` and `metadata` keys) and does not return `response.answer`.
    - Update `chat_simple_returns` in `services/mcp-server/src/settings/mcp_settings.py` (line 49) from `"The answer from the RAG system as plain text."` to accurately describe the list-of-citations return type (see Step 4).

- [x] 3. Verify that `chat_with_history` in `services/mcp-server/src/rag_mcp_server.py` already returns only citations.
  - Acceptance Criteria:
    - Confirmed: The method at line 69 already returns `list[dict]` of simplified citations (each with `content` and `metadata` keys, same format as `chat_simple`) and does not return answer or finish_reason. The return type annotation is `list[dict]`.
    - Update `chat_with_history_returns` in `services/mcp-server/src/settings/mcp_settings.py` (lines 71-78) from the old multi-line description (`"Response containing:\n    - answer: The response text\n    - finish_reason: Why the response ended\n    - citations: List of source documents used (simplified)"`) to `"List of citation objects, each containing content and metadata."` to match the actual return type.

- [ ] 4. Update `MCPSettings` description fields in `services/mcp-server/src/settings/mcp_settings.py` to reflect that citations are returned.
  - Acceptance Criteria:
    - `chat_simple_returns` (line 49): Already updated to `"List of citation objects, each containing content and metadata."` in Step 2 — no change needed.
    - `chat_with_history_returns` (line 71-73): Already updated to `"List of citation objects, each containing content and metadata."` in Step 3 — no change needed.
    - `chat_simple_description` (lines 36-41): Update `"get back the answer as plain text"` (line 40) to reflect that citations (source snippets with metadata) are returned, not the answer directly.
    - `chat_with_history_description` (lines 54-59): Update `"get structured response"` (line 56) to reflect that only citations are returned, not a structured answer object.

- [ ] 5. Update tests in `services/mcp-server/tests/docstring_system_test.py` to verify the new settings values.
  - Acceptance Criteria:
    - `chat_simple_returns` (line 49) and `chat_with_history_returns` (lines 71-73) are already updated to `"List of citation objects, each containing content and metadata."` — no test changes needed for these.
    - No `test_mcp_settings_defaults` test exists that asserts specific string values for `chat_simple_returns` or `chat_with_history_returns` — the `test_default_settings` test (line 173) only checks types and non-None, so no update needed there.
    - The `test_class_factory` fixture (line 27) defines `chat_simple` returning `str` and `chat_with_history` returning `dict` — these are test-only signatures unrelated to the actual MCP server return types; no update needed.
    - `test_generated_docstrings_content` (line 243) asserts `"str" in simple_doc` (line 254) and `"dict" in history_doc` (line 264) based on the test class return type annotations; these remain valid for the test class.
    - No integration tests render the old return descriptions directly — the docstrings are generated from settings at runtime.
    - After Step 4 updates the description fields, the generated docstrings will reflect the new text automatically. Run tests to confirm nothing breaks.

- [ ] 6. Run `make test` from `services/mcp-server/` and confirm it succeeds.
  - Acceptance Criteria:
    - Run: `make test` in `services/mcp-server/` directory (which executes `poetry run python -m pytest tests`).
    - The command exits with a zero status code, indicating all tests pass.
    - Key tests to watch: `test_default_settings` (line 173), `test_generated_docstrings_content` (line 243), `test_custom_configuration` (line 267), and `test_empty_configuration` (line 337).
    - After Step 4 updates the description fields (not the returns fields which are already updated), re-run to confirm the docstring changes don't break any assertions.