
"""


This is an example of how to replace a dependency in the dependency container of the rag-core-api library.


If you replace a dependency keep in mind that the dependency you are replacing should have:


1. the same name and


2. the same base class


as the dependency you are replacing it with.





Furthermore, if the dependency you are replacing has any dependencies from the dependency container,


they can be simply reused in the new dependency as shown in the example.


"""


from answer import CustomAnswerGenerationChain
from langchain_openai import ChatOpenAI


from dependency_injector.providers import Singleton


from dependency_injector import containers





from rag_core_api.dependency_container import DependencyContainer


from rag_core_lib.impl.langfuse_manager.langfuse_manager import LangfuseManager
from rag_core_lib.impl.llms.llm_factory import llm_provider





from chat_endpoint import UseCaseChat
from rephrase import CustomRephrasingChain



from dependency_injector import containers


from langchain_community.llms import Ollama
from dependency_injector.providers import (  # noqa: WOT001
    Selector,
    Singleton,
)




@containers.copy(DependencyContainer)
class UseCaseContainer(DependencyContainer):


    DependencyContainer.large_language_model.override(Singleton(llm_provider, DependencyContainer.stackit_vllm_settings, ChatOpenAI))

    DependencyContainer.answer_generation_chain.override( Singleton(
        CustomAnswerGenerationChain,
        langfuse_manager=DependencyContainer.langfuse_manager,
    ))

    DependencyContainer.rephrasing_chain.override(Singleton(
        CustomRephrasingChain,
        langfuse_manager=DependencyContainer.langfuse_manager,
    ))

    DependencyContainer.langfuse_manager.override( Singleton(
        LangfuseManager,
        langfuse=DependencyContainer.langfuse,
        managed_prompts={
            CustomAnswerGenerationChain.__name__: DependencyContainer.prompt,
            CustomRephrasingChain.__name__: DependencyContainer.rephrasing_prompt,
        },
        llm=DependencyContainer.large_language_model,
    )
    )
