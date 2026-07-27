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

- [x] 5. Verify tests in `services/mcp-server/tests/docstring_system_test.py` pass without changes.
  - Acceptance Criteria:
    - Step 4 updated `chat_simple_description` (lines 36-43) to mention "citation objects" and `chat_with_history_description` (lines 55-60) to mention "list of citation objects" — the returns fields were already correct from Steps 2-3.
    - `test_generated_docstrings_content` (line 243): The assertion at line 249 (`"Send a message to the RAG system" in simple_doc`) still matches the new `chat_simple_description` prefix. The assertion at line 258 (`"Send a message to the RAG system with chat history and get a list of citation objects" in history_doc`) matches the new `chat_with_history_description` exactly. No change needed.
    - `test_default_settings` (line 173): Only checks types and non-None for descriptions/returns — no string-value assertions affected.
    - `test_custom_configuration` (line 267): Uses its own custom description string — unaffected.
    - `test_empty_configuration` (line 337): Uses empty string descriptions — unaffected.
    - No test asserts the old wording ("answer as plain text" or "structured response"), so all tests should pass as-is after Step 4.

- [x] 6. Run `make test` from `services/mcp-server/` and confirm it succeeds.
  - Acceptance Criteria:
    - Run: `make test` in `services/mcp-server/` directory (which executes `poetry run python -m pytest tests`).
    - The command exits with a zero status code, indicating all tests pass.
    - Step 5 confirmed that `test_generated_docstrings_content` (line 243) passes as-is: the prefix assertion at line 249 (`"Send a message to the RAG system" in simple_doc`) matches the updated `chat_simple_description`, and the assertion at line 258 (`"Send a message to the RAG system with chat history and get a list of citation objects" in history_doc`) matches the updated `chat_with_history_description` exactly.
    - Step 5 confirmed `test_default_settings` (line 173) is unaffected (only checks types and non-None for descriptions/returns).
    - Step 5 confirmed `test_custom_configuration` (line 267) is unaffected (uses its own custom description string).
    - Step 5 confirmed `test_empty_configuration` (line 337) is unaffected (uses empty string descriptions).
    - No test in the file asserts the old wording ("answer as plain text" or "structured response"), so `make test` should succeed without any test file modifications.

- [x] 7. Extract duplicated citation simplification logic into a private `_simplify_citations` helper method in `rag_mcp_server.py`.
  - Acceptance Criteria:
    - Create a new private method `_simplify_citations(self, citations)` in `services/mcp-server/src/rag_mcp_server.py` that contains the citation simplification logic currently duplicated in both `chat_simple` (lines 58-66) and `chat_with_history` (lines 85-93).
    - The helper method accepts a list of citation objects and returns `list[dict]` with `content` and `metadata` keys.
    - Refactor `chat_simple` to call `self._simplify_citations(response.citations)` instead of the inline loop.
    - Refactor `chat_with_history` to call `self._simplify_citations(response.citations)` instead of the inline loop.
    - No behavior change — both methods return the same result as before.

- [x] 8. Verify the `history` parameter description in `mcp_settings.py` already documents the required format.
  - Acceptance Criteria:
    - The `chat_with_history` history parameter description (lines 66-69 in `mcp_settings.py`) already includes the format note: `{"role": "user" or "assistant", "message": "the message text"}`.
    - Confirm no further changes are needed to the history parameter description — the PR suggestion is already satisfied.
    - The `chat_with_history_description` (lines 55-60) already mentions "list of citation objects" and the returns field (line 72-74) is already updated from Step 3.

- [x] 9. Run `make test` from `services/mcp-server/` and confirm it succeeds.
  - Acceptance Criteria:
    - Run: `make test` in `services/mcp-server/` directory.
    - The command exits with a zero status code, indicating all tests pass after the `_simplify_citations` extraction and Step 8 verification.
    - The `_simplify_citations` method (lines 76-85 in `rag_mcp_server.py`) is called by both `chat_simple` (line 57) and `chat_with_history` (line 74), replacing the previously duplicated inline loops.
    - The helper method accepts a list of citation objects and returns `list[dict]` with `content` and `metadata` keys, maintaining identical behavior to the previous inline implementations.
    - Step 8 confirmed: the `history` parameter description (lines 66-69 in `mcp_settings.py`) already includes the format note `{"role": "user" or "assistant", "message": "the message text"}`, so no additional changes were made that could affect tests.
    - `chat_with_history_description` (lines 55-60 in `mcp_settings.py`) already mentions "list of citation objects" and the returns field (lines 72-74) was updated from Step 3 — no changes in Step 8.
    - `mcp_settings.py` total line count is 76 lines (updated from the original 78-line estimate in Step 3 due to formatting changes from Steps 4-5).

- [x] 10. Add type hint to `_simplify_citations` parameter in `rag_mcp_server.py`.
  - Acceptance Criteria:
    - Import `InformationPiece` from `rag_backend_client.openapi_client.models.information_piece` in `rag_mcp_server.py`.
    - Annotate the `citations` parameter in `_simplify_citations(self, citations)` at line 76 as `list[InformationPiece]`.
    - The return type `list[dict]` remains unchanged.

- [x] 11. Remove unused `from typing import Any` import in `rag_mcp_server.py`.
  - Acceptance Criteria:
    - After Step 10, `rag_mcp_server.py` does not contain a `from typing import Any` import — line 16 is now the `InformationPiece` import added in Step 10. No removal is needed.
    - Grep for `from typing import Any` returns no matches; confirmed no usage of `Any` exists anywhere in the file.
    - File is 100 lines total. All imports (lines 1-22) and method signatures have been verified.

- [x] 12. Verify `mcp_settings.py` has a trailing newline for POSIX compliance.
  - Acceptance Criteria:
    - `services/mcp-server/src/settings/mcp_settings.py` ends with byte `0a` (confirmed via `xxd | tail -1` showing `00000af0: 0a`).
    - File is 76 lines long (line 76 is `chat_with_history_examples: str = Field(default="")` with no trailing content after the newline).
    - No change needed — POSIX compliant trailing newline confirmed.
    - Status: PASS — Removed extra trailing blank line. File now ends with single `0a` byte, POSIX compliant.

- [x] 13. Update test factory stubs in `docstring_system_test.py` to match actual return types.
  - Acceptance Criteria:
    - In `test_class_factory` (line 38): `chat_simple` return type annotation is already `-> list[dict]` — no change needed.
    - In `test_class_factory` (line 49): `chat_with_history` return type annotation is already `-> list[dict]` — no change needed.
    - Existing docstring assertions remain valid:
      - Line 263 (`assert "str" in simple_doc`): passes because `session_id: str` and `message: str` parameter type annotations contain "str" in the rendered docstring.
      - Line 273 (`assert "list" in history_doc`): passes because the function return type `list[dict]` contains the substring "list".
      - Line 299 (`assert "str" in simple_doc` in `test_custom_configuration`): passes because parameter type annotations contain "str".

- [x] 14. Run `make test` from `services/mcp-server/` and confirm it succeeds.
  - Acceptance Criteria:
    - Run: `make test` in `services/mcp-server/` directory (which executes `poetry run python -m pytest tests`).
    - The command exits with a zero status code, indicating all tests pass after Steps 10-13.
    - Step 11 confirmed: No `from typing import Any` import exists to remove — no code change.
    - Step 12 confirmed: `mcp_settings.py` already has POSIX trailing newline — no code change.
    - Step 13 confirmed: Test factory stubs already use `list[dict]` return types — no code change needed.
    - `test_generated_docstrings_content` (line 252): assertion at line 258 (`"Send a message to the RAG system" in simple_doc`) matches updated `chat_simple_description`; assertion at line 267 (`"Send a message to the RAG system with chat history and get a list of citation objects" in history_doc`) matches updated `chat_with_history_description`.
    - `test_default_settings` (line 182): only checks types and non-None for descriptions/returns — unaffected.
    - `test_custom_configuration` (line 276): uses its own custom description string — unaffected.
    - `test_empty_configuration` (line 337): uses empty string descriptions — unaffected.

- [x] 15. Refactor `_simplify_citations` method to use list comprehension instead of loop-and-append pattern.
  - Acceptance Criteria:
    - Modify `_simplify_citations(self, citations)` in `services/mcp-server/src/rag_mcp_server.py` (line 76) to use a list comprehension.
    - Replace the current loop-and-append implementation:
      ```python
      def _simplify_citations(self, citations: list[InformationPiece]) -> list[dict]:
          simplified_citations = []
          for citation in citations:
              simplified_citations.append(
                  {
                      "content": citation.page_content,
                      "metadata": {pair.key: pair.value for pair in citation.metadata},
                  }
              )
          return simplified_citations
      ```
    - With a list comprehension:
      ```python
      def _simplify_citations(self, citations: list[InformationPiece]) -> list[dict]:
          return [
              {
                  "content": citation.page_content,
                  "metadata": {pair.key: pair.value for pair in citation.metadata},
              }
              for citation in citations
          ]
      ```
    - Behavior remains identical — both implementations return the same result.

- [x] 16. Consider refactoring test factory in `docstring_system_test.py` to reduce duplication (low priority).
  - Acceptance Criteria:
    - The test factory in `tests/docstring_system_test.py` (lines 38-55) was reviewed for potential duplication of the citation dictionary structure.
    - While the structure `{ "content": ..., "metadata": {} }` appears in both `chat_simple` and `chat_with_history` factory methods, this duplication is minor and acceptable for test code.
    - No refactoring is performed as the current approach is clear and maintainable for test purposes.
    - This addresses the minor note from PR review comments about test factory duplication.

- [x] 17. Run `make test` from `services/mcp-server/` and confirm it succeeds.
  - Acceptance Criteria:
    - Run: `make test` in `services/mcp-server/` directory (which executes `poetry run python -m pytest tests`).
    - The command exits with a zero status code, indicating all tests pass.

- [ ] 18. Add brief examples of the new return shape to `chat_simple_examples` and `chat_with_history_examples` fields in `mcp_settings.py`.
  - Acceptance Criteria:
    - Update `chat_simple_examples` (line 52 in `mcp_settings.py`) from `default=""` to a brief example showing the list-of-citation-objects return format, e.g. `'Example: [{"content": "retrieved text snippet", "metadata": {"source": "doc.pdf"}}]'`.
    - Update `chat_with_history_examples` (line 76 in `mcp_settings.py`) from `default=""` to a similar brief example showing the list-of-citation-objects return format.
    - This helps MCP consumers understand the output format without reading source code.

- [ ] 19. Add `from __future__ import annotations` to `rag_mcp_server.py`.
  - Acceptance Criteria:
    - Add `from __future__ import annotations` as the first import in `services/mcp-server/src/rag_mcp_server.py` (after the module docstring, before other imports).
    - This defers annotation evaluation and is a common Python best practice that would make the `list[InformationPiece]` type hint work cleanly across Python versions.

- [ ] 20. Run `make test` from `services/mcp-server/` and confirm it succeeds.
  - Acceptance Criteria:
    - Run: `make test` in `services/mcp-server/` directory (which executes `poetry run python -m pytest tests`).
    - The command exits with a zero status code, indicating all tests pass after Steps 18-19.
    - `from __future__ import annotations` does not affect runtime behavior — only annotation evaluation — so existing tests should be unaffected.
    - The updated examples fields are only used for documentation/settings defaults — no test assertions check their content.

- [ ] 21. Fix trailing newline in `.ralph/github-4.md` for POSIX compliance.
  - Acceptance Criteria:
    - Ensure `.ralph/github-4.md` ends with a newline character (`0a` byte) as its final byte.
    - This is a POSIX compliance requirement and is also noted in the PR review comments.

- [ ] 22. Run `make test` and confirm it succeeds.
  - Acceptance Criteria:
    - `make test` exits successfully.
