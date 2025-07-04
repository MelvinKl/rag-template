
"""


This is an example of how to replace a dependency in the dependency container of the rag-core-api library.


If you replace a dependency keep in mind that the dependency you are replacing should have:


1. the same name and


2. the same base class


as the dependency you are replacing it with.





Furthermore, if the dependency you are replacing has any dependencies from the dependency container,


they can be simply reused in the new dependency as shown in the example.


"""


from langchain_openai import ChatOpenAI




from dependency_injector import containers


from langchain_community.llms import Ollama
from dependency_injector.providers import (  # noqa: WOT001
    Selector,
    Singleton,
)

from admin_api_lib.dependency_container import DependencyContainer


from rag_core_lib.impl.llms.llm_factory import llm_provider
from rag_core_lib.impl.utils.async_threadsafe_semaphore import AsyncThreadsafeSemaphore
from summarizer import CustomLangchainSummarizer


@containers.copy(DependencyContainer)
class UseCaseContainer(DependencyContainer):


    large_language_model = Selector(
        DependencyContainer.class_selector_config.llm_type,
        ollama=Singleton(llm_provider, DependencyContainer.ollama_settings, Ollama),
        stackit=Singleton(llm_provider, DependencyContainer.stackit_vllm_settings, ChatOpenAI),
    )

    summarizer = Singleton(
        CustomLangchainSummarizer,
        langfuse_manager=DependencyContainer.langfuse_manager,
        chunker=DependencyContainer.summary_text_splitter,
        semaphore=Singleton(AsyncThreadsafeSemaphore, DependencyContainer.summarizer_settings.maximum_concurrreny),
    )
