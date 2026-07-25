# Task: Improve MCp Interface

Task Number: 4
Branch: ai/issue-4-improve-mcp-interface

## Required Task

Improve the MCP Interface.
It should Not generate the answer to the question, but only Return the sources and applicable snippets from the database.

## Steps

- [ ] 1. Identify the MCP server methods that need to be modified to return only sources and snippets.
  - Acceptance Criteria:
    - The methods `chat_simple` and `chat_with_history` in `rag_mcp_server.py` are identified as needing modification.
    - The expected behavior is defined: return only the citations (list of objects with content and metadata) for `chat_simple` and only the citations for `chat_with_history` (removing answer and finish_reason).

- [ ] 2. Modify the `chat_simple` method to return only the citations.
  - Acceptance Criteria:
    - The method no longer returns `response.answer` but instead returns a list of citation dictionaries (each with content and metadata).
    - The docstring (via the docstring system) is updated to reflect the new return type.

- [ ] 3. Modify the `chat_with_history` method to return only the citations.
  - Acceptance Criteria:
    - The method no longer returns the answer and finish_reason, but only the list of citation dictionaries.
    - The docstring is updated accordingly.

- [ ] 4. Update the MCPSettings to reflect the new return values for the documentation.
  - Acceptance Criteria:
    - The `chat_simple_returns` field in `MCPSettings` is updated to describe the new return value (list of citations with content and metadata).
    - The `chat_with_history_returns` field is updated to describe that only the list of citations is returned.

- [ ] 5. Update tests to verify the new behavior.
  - Acceptance Criteria:
    - Existing tests are updated to expect the new return format.
    - New tests are added if necessary to verify that the answer and finish_reason are not returned.

- [ ] 6. Run `make test` and confirm it succeeds.
  - Acceptance Criteria:
    - The command `make test` exits with a zero status code, indicating all tests pass.