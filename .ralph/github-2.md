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

- [ ] 7. Create or update tests to verify that the MCP server returns only citations without generating answers.
  - Acceptance Criteria:
    - Tests verify that `chat_simple` and `chat_with_history` return citation data without answers by asserting answer field is empty/null in ChatResponse.
    - Tests confirm that RAG backend skips answer generation node when `skip_answer_generation=True` is passed, reducing latency and cost.
    - Tests validate that the citation data is properly formatted with page_content and metadata from InformationPiece objects.
    - Tests mock or use real ChatRequest/ChatResponse with skip_answer_generation parameter to verify end-to-end behavior.

- [ ] 8. Verify REST API endpoint properly handles citation-only responses.
  - Acceptance Criteria:
    - Confirm the `/chat` REST API endpoint in the RAG backend correctly processes the `skip_answer_generation` parameter from ChatRequest (verified in Step 5 that DefaultChatGraph properly handles this)
    - Verify that when `skip_answer_generation=True`, the endpoint returns a ChatResponse with citations populated and answer field empty/null (confirmed in Step 5)
    - Test the endpoint with both `skip_answer_generation=True` and `False` to confirm proper behavior difference: True skips answer_generation node, False runs full pipeline
    - Verify performance improvement by measuring that skip_answer_generation=True only runs language_detection, rephrasing, and retrieval nodes

- [ ] 9. Run `make test` and confirm it succeeds.
  - Acceptance Criteria:
    - `make test` exits successfully with all tests passing.
    - All MCP server tests pass, including tests for `chat_simple` and `chat_with_history` returning citations without answers.
    - All RAG backend tests pass, confirming skip_answer_generation parameter works correctly across the API.