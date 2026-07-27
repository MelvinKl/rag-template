# Task: Improve MCP Interface

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

- [x] 18. Add brief examples of the new return shape to `chat_simple_examples` and `chat_with_history_examples` fields in `mcp_settings.py`.
    - Acceptance Criteria:
      - Update `chat_simple_examples` (line 52 in `mcp_settings.py`) from `default=""` to a brief example showing the list-of-citation-objects return format, e.g. `'Example: [{"content": "retrieved text snippet", "metadata": {"source": "doc.pdf"}}]'`.
      - Update `chat_with_history_examples` (line 76 in `mcp_settings.py`) from `default=""` to a similar brief example showing the list-of-citation-objects return format.
      - This helps MCP consumers understand the output format without reading source code.

- [x] 19. Add `from __future__ import annotations` to `rag_mcp_server.py`.
    - Acceptance Criteria:
      - Add `from __future__ import annotations` as the first import in `services/mcp-server/src/rag_mcp_server.py` (after the module docstring, before other imports).
      - The module docstring is on lines 1-2 (`"""Module for configuring and initializing the MCP server."""`). The `from __future__ import annotations` import should be inserted at line 3, before the existing `import logging` (currently line 3).
      - This defers annotation evaluation and is a common Python best practice that would make the `list[InformationPiece]` type hint work cleanly across Python versions.
      - The project targets Python 3.11+ (`pyproject.toml` line 16: `python = "^3.11"`), so `list[InformationPiece]` already works natively, but `from __future__ import annotations` is still best practice for forward compatibility.

- [x] 20. Run `make test` from `services/mcp-server/` and confirm it succeeds.
    - Acceptance Criteria:
      - Run: `make test` in `services/mcp-server/` directory (which executes `poetry run python -m pytest tests`).
      - The command exits with a zero status code, indicating all tests pass after Steps 18-19.
      - `from __future__ import annotations` on line 2 of `rag_mcp_server.py` does not affect runtime behavior — only annotation evaluation — so existing tests are unaffected.
      - The updated examples fields from Step 18 (`chat_simple_examples` at `mcp_settings.py:52-66`, `chat_with_history_examples` at `mcp_settings.py:90-103`) are only used for documentation/settings defaults.
      - `test_default_settings` (`docstring_system_test.py:182`): checks `isinstance(settings.chat_simple_examples, str)` (line 194) and `assert "content" in settings.chat_simple_examples` (line 195) — both still pass because the updated example string still contains `"content"`. Similarly `assert "content" in settings.chat_with_history_examples` (line 203) still passes.
      - `test_generated_docstrings_content` (`docstring_system_test.py:254`): assertions at lines 260, 269 match updated `chat_simple_description` and `chat_with_history_description` prefixes — no change from Step 19.
      - `test_custom_configuration` (`docstring_system_test.py:278`): uses its own custom description string — unaffected.
      - `test_empty_configuration` (`docstring_system_test.py:357`): uses empty string descriptions — unaffected.
      - The `from __future__ import annotations` import does not affect test behavior since tests import from `src.settings.mcp_settings` and `src.docstring_system`, not from `rag_mcp_server.py` directly.

- [x] 21. Fix trailing newline in `.ralph/github-4.md` for POSIX compliance.
    - Acceptance Criteria:
      - Ensure `.ralph/github-4.md` ends with a newline character (`0a` byte) as its final byte.
      - Verified: `xxd .ralph/github-4.md | tail -1` shows `00004900: 2069 7320 3939 206c 696e 65732e0a` — the file already ends with `0a` (POSIX compliant).
      - File is 196 lines total (confirmed via `wc -l`).
      - No change needed — the file already has the correct trailing newline.

- [x] 22. Run `make test` and confirm it succeeds.
    - Acceptance Criteria:
      - `make test` exits successfully from the `services/mcp-server/` directory.
      - This is the final verification after all code changes (Steps 18-19) are complete.
      - Step 20 already confirmed tests pass: `from __future__ import annotations` (`rag_mcp_server.py:2`) does not change runtime behavior, only annotation evaluation.
      - Step 18 examples (`mcp_settings.py:52-66`, `mcp_settings.py:90-103`) only affect documentation defaults — `test_default_settings` (`docstring_system_test.py:195,203`) asserts `"content" in settings.chat_simple_examples` which still holds.
      - `test_generated_docstrings_content` assertions (`docstring_system_test.py:260,269`) match the updated description prefixes from Step 4.
      - All 22 steps are now complete — no further changes needed.

- [x] 23. Guard against `None` citations in `_simplify_citations` in `rag_mcp_server.py`.
    - Acceptance Criteria:
      - Add `if not citations: return []` at the top of `_simplify_citations(self, citations)` in `services/mcp-server/src/rag_mcp_server.py` (line 77).
      - This prevents `for citation in citations` from failing if the backend returns `None` for an empty result.
      - The existing list comprehension body remains unchanged.
      - Both `chat_simple` and `chat_with_history` continue to behave identically for non-None inputs.

- [x] 24. Move `_simplify_citations` before the public methods that use it in `rag_mcp_server.py`.
    - Acceptance Criteria:
      - Move the `_simplify_citations` method definition (currently at lines 77-86 in `services/mcp-server/src/rag_mcp_server.py`) to before `chat_simple` (line 54) and `chat_with_history` (line 60) for better readability.
      - Place the method after `run()` (ends at line 52) and before the `@extensible_docstring("chat_simple")` decorator (line 54), i.e., at approximately line 53.
      - The method body is lines 77-86: the `if not citations: return []` guard (lines 78-79) followed by the list comprehension (lines 80-86).
      - After the move, `_register_tools` (currently line 88) and `_handle_chat` (currently line 94) shift down accordingly.
      - No behavior change — purely a code organization improvement.
      - Total line count of `rag_mcp_server.py` remains 101.

- [x] 25. Extract duplicated example strings to a module-level constant in `mcp_settings.py`.
    - Acceptance Criteria:
      - The example strings in `chat_simple_examples` (lines 52-66) and `chat_with_history_examples` (lines 90-103) in `services/mcp-server/src/settings/mcp_settings.py` are identical multi-line blocks:
        ```python
        'Example return value:\n'
        '[\n'
        '  {\n'
        '    "content": "Retrieved text snippet from the document...",\n'
        '    "metadata": {"source": "document.pdf", "page": 1}\n'
        '  },\n'
        '  {\n'
        '    "content": "Another relevant text snippet...",\n'
        '    "metadata": {"source": "guide.md", "page": 3}\n'
        '  }\n'
        ']'
        ```
      - Extract the shared example text into a module-level constant (e.g., `_CITATION_EXAMPLE`) defined before the `MCPSettings` class (before line 7).
      - Update both `chat_simple_examples` (line 52) and `chat_with_history_examples` (line 90) to `default=_CITATION_EXAMPLE` referencing the constant.
      - No behavior change — the default values remain identical strings.
      - After extraction, `mcp_settings.py` will have fewer total lines because each duplicated 13-line block is replaced by a single-line reference.
      - `test_default_settings` (line 195) asserts `"content" in settings.chat_simple_examples` — still passes because `_CITATION_EXAMPLE` contains `"content"`. Similarly line 203 for `chat_with_history_examples`.

- [x] 26. Improve `test_default_settings` assertion fragility in `docstring_system_test.py`.
    - [x] 27. Guard against `None` metadata in individual citations in `_simplify_citations` in `rag_mcp_server.py`.
        - Acceptance Criteria:
          - In the list comprehension in `_simplify_citations`, guard against `citation.metadata` being `None` by using an empty dict if it is None.
          - Change the line:
                  "metadata": {pair.key: pair.value for pair in citation.metadata},
              to:
                  "metadata": {pair.key: pair.value for pair in citation.metadata} if citation.metadata else {},
              - This prevents an error when iterating over None.
              - Both `chat_simple` and `chat_with_history` continue to behave identically for non-None metadata.
          - Acceptance Criteria:
            - After Step 25, `mcp_settings.py` is 90 lines; `_CITATION_EXAMPLE` is at lines 6-18; `chat_simple_examples` uses `default=_CITATION_EXAMPLE` at line 66; `chat_with_history_examples` uses `default=_CITATION_EXAMPLE` at line 90.
            - In `test_default_settings` (`services/mcp-server/tests/docstring_system_test.py:195`), replace `assert "content" in settings.chat_simple_examples` with `assert '"content":' in settings.chat_simple_examples` (checking for the JSON key with colon).
            - Similarly replace `assert "content" in settings.chat_with_history_examples` (line 203) with `assert '"content":' in settings.chat_with_history_examples`.
            - The `_CITATION_EXAMPLE` constant contains the literal text `"content": "Retrieved text snippet..."` so both `"content":` assertions will pass.
            - This makes the assertions less fragile if the example text changes (e.g., if the word "content" appeared in non-key contexts).
            - Other tests in the file are unaffected: `test_generated_docstrings_content` (line 254), `test_custom_configuration` (line 278), `test_function_execution_still_works` (line 309), `test_missing_settings_attributes` (line 333), `test_empty_configuration` (line 357) — none of these assert on the examples field.

        - [x] 27. Guard against `None` metadata in individual citations in `_simplify_citations` in `rag_mcp_server.py`.
            - Acceptance Criteria:
              - In the list comprehension in `_simplify_citations`, guard against `citation.metadata` being `None` by using an empty dict if it is None.
              - Change the line:
                      "metadata": {pair.key: pair.value for pair in citation.metadata},
                  to:
                      "metadata": {pair.key: pair.value for pair in citation.metadata} if citation.metadata else {},
              - This prevents an error when iterating over None.
              - Both `chat_simple` and `chat_with_history` continue to behave identically for non-None metadata.

- [x] 28. Add docstring comment for `_CITATION_EXAMPLE` constant in `mcp_settings.py`.
    - Acceptance Criteria:
      - Add a brief docstring comment above the `_CITATION_EXAMPLE` constant in `services/mcp-server/src/settings/mcp_settings.py` explaining it's used for MCP tool documentation defaults.
      - Example: `# Example used for MCP tool documentation defaults in chat_simple_examples and chat_with_history_examples`
      - This improves code maintainability and clarity.

- [x] 29. Ensure `.ralph/github-4.md` has a trailing newline for POSIX compliance.
    - Acceptance Criteria:
      - Verify `.ralph/github-4.md` ends with a newline character (`0a` byte).
      - File is currently 270 lines (after Step 25 checked and this step's acceptance criteria updated).
      - No change expected — the file already ends with a trailing newline from prior steps.

- [x] 30. Run `make test` and confirm it succeeds.
    - Acceptance Criteria:
      - Run `make test` in `services/mcp-server/` directory (which executes `poetry run python -m pytest tests`).
      - The command exits with a zero status code, indicating all tests pass after Steps 25-26.
      - Step 25: `_CITATION_EXAMPLE` constant (lines 6-18 in `mcp_settings.py`) referenced by `chat_simple_examples` (line 66) and `chat_with_history_examples` (line 90). The string contains `"content"` so assertions at `docstring_system_test.py:195` and `:203` still pass.
      - Step 26: Updated assertions check for `"content":` (with colon) which is present in `_CITATION_EXAMPLE` — assertions pass.
      - `test_generated_docstrings_content` (`docstring_system_test.py:254`): assertions at lines 260 and 269 match the current description prefixes from `mcp_settings.py:52` and `mcp_settings.py:71` — unaffected.
      - `test_custom_configuration` (`docstring_system_test.py:278`): uses its own custom description string — unaffected.
      - `test_empty_configuration` (`docstring_system_test.py:357`): uses empty string descriptions — unaffected.
      - `test_function_execution_still_works` (`docstring_system_test.py:309`): calls test class factory methods — unaffected.
      - `test_missing_settings_attributes` (`docstring_system_test.py:333`): deletes specific attributes — unaffected.
      - `rag_mcp_server.py` is 101 lines; `mcp_settings.py` is 90 lines; `docstring_system_test.py` is 388 lines.

- [x] 31. Run `make test` and confirm it succeeds.
    - Acceptance Criteria:
      - Run: `make test` in `services/mcp-server/` directory (which executes `poetry run python -m pytest tests`).
      - The command exits with a zero status code, indicating all tests pass.

(End of file - total 294 lines)