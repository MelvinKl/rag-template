"""
This is an example of how to replace a dependency in the dependency container of the rag-core-api library.
If you replace a dependency keep in mind that the dependency you are replacing should have:
1. the same name and
2. the same base class
as the dependency you are replacing it with.

Furthermore, if the dependency you are replacing has any dependencies from the dependency container,
they can be simply reused in the new dependency as shown in the example.
"""

from dependency_injector.providers import Singleton, List
from dependency_injector import containers

from extractor_api_lib.dependency_container import DependencyContainer
from extractor_api_lib.impl.document_parser.general_extractor import GeneralExtractor

from unstructured_extractor import UnstructuredExtractor


@containers.copy(DependencyContainer)
class UseCaseContainer(DependencyContainer):

    pdf_extractor = Singleton(UnstructuredExtractor, DependencyContainer.file_service)
    
    all_extractors = List(pdf_extractor, DependencyContainer.ms_docs_extractor, DependencyContainer.xml_extractor)

    general_extractor = Singleton(GeneralExtractor, DependencyContainer.file_service, all_extractors)    
