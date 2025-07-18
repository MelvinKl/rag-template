"""Module for the LangchainSummarizer class."""

import logging
import traceback
from typing import Optional

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_core.runnables import Runnable, RunnableConfig, ensure_config

from admin_api_lib.summarizer.summarizer import (
    Summarizer,
    SummarizerInput,
    SummarizerOutput,
)
from rag_core_lib.impl.langfuse_manager.langfuse_manager import LangfuseManager
from rag_core_lib.impl.utils.async_threadsafe_semaphore import AsyncThreadsafeSemaphore

logger = logging.getLogger(__name__)


class LangchainSummarizer(Summarizer):
    """Is responsible for summarizing input data.

    LangchainSummarizer is responsible for summarizing input data using the LangfuseManager,
    RecursiveCharacterTextSplitter, and AsyncThreadsafeSemaphore. It handles chunking of the input
    document and retries the summarization process if an error occurs.
    """

    def __init__(
        self,
        langfuse_manager: LangfuseManager,
        chunker: RecursiveCharacterTextSplitter,
        semaphore: AsyncThreadsafeSemaphore,
    ):
        self._chunker = chunker
        self._langfuse_manager = langfuse_manager
        self._semaphore = semaphore

    async def ainvoke(self, query: SummarizerInput, config: Optional[RunnableConfig] = None) -> SummarizerOutput:
        """
        Asynchronously invokes the summarization process on the given query.

        Parameters
        ----------
        query : SummarizerInput
            The input data to be summarized.
        config : Optional[RunnableConfig], optional
            Configuration options for the summarization process, by default None.

        Returns
        -------
        SummarizerOutput
            The summarized output.

        Raises
        ------
        Exception
            If the summary creation fails after the allowed number of tries.

        Notes
        -----
        This method handles chunking of the input document and retries the summarization
        process if an error occurs, up to the number of tries specified in the config.
        """
        assert query, "Query is empty: %s" % query  # noqa S101
        config = ensure_config(config)
        tries_remaining = config.get("configurable", {}).get("tries_remaining", 3)
        logger.debug("Tries remaining %d" % tries_remaining)

        if tries_remaining < 0:
            raise Exception("Summary creation failed.")
        document = Document(page_content=query)
        langchain_documents = self._chunker.split_documents([document])

        outputs = []
        for langchain_document in langchain_documents:
            async with self._semaphore:
                try:
                    result = await self._create_chain().ainvoke({"text": langchain_document.page_content}, config)
                    # Extract content from AIMessage if it's not already a string
                    content = result.content if hasattr(result, "content") else str(result)
                    outputs.append(content)
                except Exception as e:
                    logger.error("Error in summarizing langchain doc: %s %s", e, traceback.format_exc())
                    config["tries_remaining"] = tries_remaining - 1
                    result = await self._create_chain().ainvoke({"text": langchain_document.page_content}, config)
                    # Extract content from AIMessage if it's not already a string
                    content = result.content if hasattr(result, "content") else str(result)
                    outputs.append(content)

        if len(outputs) == 1:
            return outputs[0]
        summary = " ".join(outputs)
        logger.debug(
            "Reduced number of chars from %d to %d"
            % (len("".join([x.page_content for x in langchain_documents])), len(summary))
        )
        return await self.ainvoke(summary, config)

    def _create_chain(self) -> Runnable:
        return self._langfuse_manager.get_base_prompt(self.__class__.__name__) | self._langfuse_manager.get_base_llm(
            self.__class__.__name__
        )
