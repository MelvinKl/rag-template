# Task: MCP-server should not create summary

Task Number: 2
Branch: ai/issue-2-mcp-server-should-not-create-s

## Required Task

The mcp server should not create a summary/answer the question.
It should only provide the sources/citations required for doing so. The answering step in the rag should be skipped for the mcp-server.
Answering the question will be done by the mcp-client and is something that will increase answering time, as well as cost without benefit and might actually create a worse answer.

## Steps

- [x] 1. Analyze the MCP server implementation to identify where answers are generated.
  - Acceptance Criteria:
    - Identify that `chat_simple` and `chat_with_history` methods in `/root/git/managed/rag-template/services/mcp-server/src/rag_mcp_server.py` return answers from the RAG backend.
    - Determine that these methods need to be modified to skip answer generation and only return sources/citations.

- [x] 2. Modify the `chat_simple` method to return only citations instead of the answer.
  - Acceptance Criteria:
    - Change the return value of `chat_simple` to return only citations/sources from the response.
    - Remove the return of `response.answer` and instead return structured citation data.

- [x] 3. Modify the `chat_with_history` method to return only citations instead of the answer.
  - Acceptance Criteria:
    - Change the return value of `chat_with_history` to return only citations/sources from the response.
    - Remove the return of `response.answer` and instead return structured citation data without the answer field.
    - Maintain the existing citations simplification logic.

- [x] 4. Investigate the RAG backend API to determine if answer generation can be skipped.
  - Acceptance Criteria:
    - Examine the ChatRequest model to see if there's a parameter to skip answer generation.
    - Analyze the chat graph flow in the RAG backend to understand where answer generation occurs.
    - Determine if modifying the API to support citation-only responses is feasible.

- [x] 5. Verify RAG backend API answer generation skip is functional.
  - Acceptance Criteria:
    - Confirm `skip_answer_generation` parameter in ChatRequest model works correctly
    - Verify the DefaultChatGraph properly handles the parameter by running only retrieval nodes (language detection, rephrasing, and retrieval) and bypassing the answer generation node
    - Test that the API returns proper citations in ChatResponse when skip_answer_generation is True

- [x] 6. Confirm MCP server is properly using skip_answer_generation parameter.
  - Acceptance Criteria:
    - Verify `chat_simple` method passes `skip_answer_generation=True` to ChatRequest (already implemented at line 57)
    - Verify `chat_with_history` method passes `skip_answer_generation=True` to ChatRequest (already implemented at line 92)
    - Confirm both methods return simplified citations without answer generation by verifying ChatResponse has answer field empty/null when skip_answer_generation=True
    - Verify the citation simplification logic properly extracts page_content and metadata from InformationPiece objects
    - Validate that DefaultChatGraph in RAG backend skips answer generation node when skip_answer_generation=True parameter is received

- [x] 7. Create or update tests to verify that the MCP server returns only citations without generating answers
  - Acceptance Criteria:
    - Tests verify that `chat_simple` and `chat_with_history` return citation data without answers by asserting answer field is empty/null in ChatResponse (both methods pass skip_answer_generation=True at lines 57 and 92).
    - Tests confirm that RAG backend skips answer generation node when `skip_answer_generation=True` is passed, reducing latency and cost (DefaultChatGraph in RAG backend properly handles this parameter).
    - Tests validate that the citation data is properly formatted with page_content and metadata extracted from InformationPiece objects by the citation simplification logic.
    - Tests mock or use real ChatRequest/ChatResponse with skip_answer_generation=True to verify end-to-end behavior matches implementation in rag_mcp_server.py.

- [x] 8. Verify REST API endpoint properly handles citation-only responses.
  - Acceptance Criteria:
    - Confirm the `/chat` REST API endpoint in the RAG backend correctly processes the `skip_answer_generation` parameter from ChatRequest (DefaultChatGraph confirmed to handle this parameter in Step 5, validated by tests in Step 7).
    - Verify that when `skip_answer_generation=True`, the endpoint returns a ChatResponse with citations populated and answer field empty/null (confirmed in Step 5 and validated through end-to-end tests in Step 7 that ChatResponse properly contains empty/null answer when skip_answer_generation=True).
    - Test the endpoint with both `skip_answer_generation=True` (as used by MCP server at lines 57 and 92 with verified tests from Step 7) and `False` to confirm behavior difference: True skips answer_generation node for performance, False runs full pipeline.
    - Verify performance improvement by measuring that skip_answer_generation=True only runs language_detection, rephrasing, and retrieval nodes, eliminating answer generation overhead (confirmed in Step 7 tests that validate reduced node execution when flag is enabled).

- [x] 9. Run `make test` and confirm it succeeds.
  - Acceptance Criteria:
    - `make test` exits successfully with all tests passing.
    - All MCP server tests pass, including verified tests for `chat_simple` and `chat_with_history` methods (lines 57 and 92) that assert answer field is empty/null in ChatResponse when returning citations via skip_answer_generation=True parameter (tests created/verified in Step 7).
    - All RAG backend tests pass, confirming skip_answer_generation parameter functionality and DefaultChatGraph citation-only response logic work correctly across the API (behavior validated through end-to-end testing in Step 7 and REST API endpoint verification in Step 8).
    - REST API endpoint tests confirm `/chat` endpoint properly handles `skip_answer_generation=True` by returning ChatResponse with citations populated and answer field empty/null, as verified in Step 8 testing with both `skip_answer_generation=True` and `False` parameter values.
    - Performance validation tests confirm skip_answer_generation=True only executes language_detection, rephrasing, and retrieval nodes, eliminating answer generation overhead as verified in Step 8.
    - Tests validate that InformationPiece objects are properly converted to citation format with page_content and metadata extraction in the citation simplification logic (confirmed by citation data validation in Step 7 tests).