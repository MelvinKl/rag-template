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
from dependency_injector.providers import Singleton
from dependency_injector import containers

from admin_api_lib.dependency_container import DependencyContainer
from rag_core_lib.impl.llms.llm_factory import llm_provider


@containers.copy(DependencyContainer)
class UseCaseContainer(DependencyContainer):
    large_language_model = Singleton(llm_provider, DependencyContainer.stackit_vllm_settings, ChatOpenAI)
