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

- [x] 4. Update `MCPSettings` description fields in `services/mcp-server/src/settings/mcp_settings.py` to reflect that citations are returned.
  - Acceptance Criteria:
    - `chat_simple_returns` (line 49): Already updated to `"List of citation objects, each containing content and metadata."` in Step 2 — no change needed.
    - `chat_with_history_returns` (line 71-73): Already updated to `"List of citation objects, each containing content and metadata."` in Step 3 — no change needed.
    - `chat_simple_description` (lines 36-41): Update `"get back the answer as plain text"` (line 40) to reflect that citations (source snippets with metadata) are returned, not the answer directly.
    - `chat_with_history_description` (lines 54-59): Update `"get structured response"` (line 56) to reflect that only citations are returned, not a structured answer object.

- [ ] 5. Verify tests in `services/mcp-server/tests/docstring_system_test.py` pass without changes.
  - Acceptance Criteria:
    - Step 4 updated `chat_simple_description` (lines 36-43) to mention "citation objects" and `chat_with_history_description` (lines 55-60) to mention "list of citation objects" — the returns fields were already correct from Steps 2-3.
    - `test_generated_docstrings_content` (line 243): The assertion at line 249 (`"Send a message to the RAG system" in simple_doc`) still matches the new `chat_simple_description` prefix. The assertion at line 258 (`"Send a message to the RAG system with chat history and get a list of citation objects" in history_doc`) matches the new `chat_with_history_description` exactly. No change needed.
    - `test_default_settings` (line 173): Only checks types and non-None for descriptions/returns — no string-value assertions affected.
    - `test_custom_configuration` (line 267): Uses its own custom description string — unaffected.
    - `test_empty_configuration` (line 337): Uses empty string descriptions — unaffected.
    - No test asserts the old wording ("answer as plain text" or "structured response"), so all tests should pass as-is after Step 4.

- [ ] 6. Run `make test` from `services/mcp-server/` and confirm it succeeds.
  - Acceptance Criteria:
    - Run: `make test` in `services/mcp-server/` directory (which executes `poetry run python -m pytest tests`).
    - The command exits with a zero status code, indicating all tests pass.
    - Step 4 changed only the default values of `chat_simple_description` and `chat_with_history_description` in `mcp_settings.py` (lines 36-43, 55-60). No test file assertions match the old description strings, so no test changes are expected.
    - Key tests to verify: `test_generated_docstrings_content` (line 243) — the prefix assertions at lines 249 and 258 still match the updated descriptions; `test_default_settings` (line 173), `test_custom_configuration` (line 267), and `test_empty_configuration` (line 337) — all unaffected.