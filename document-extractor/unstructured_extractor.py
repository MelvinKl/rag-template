"""Module for the GeneralExtractor class."""

from pathlib import Path
from enum import StrEnum
from typing import Any, Optional

from langchain_unstructured import UnstructuredLoader
from unstructured_client import UnstructuredClient
from unstructured_client.models import shared


from extractor_api_lib.document_parser.information_extractor import InformationExtractor
from extractor_api_lib.file_services.file_service import FileService
from extractor_api_lib.impl.types.file_type import FileType
from extractor_api_lib.models.dataclasses.information_piece import InformationPiece
from extractor_api_lib.impl.types.content_type import ContentType
from extractor_api_lib.impl.utils.utils import hash_datetime


class AdditionalFileType(StrEnum):
    EPUB = "EPUB"

class UnstructuredExtractor(InformationExtractor):

    def __init__(self, file_service: FileService):
        """
        Initialize the GeneralExtractor.

        Parameters
        ----------
        file_service : FileService
            An instance of FileService to handle file operations.
        available_extractors : list of InformationExtractor
            A list of available information extractors to be used by the GeneralExtractor.
        """
        super().__init__(file_service=file_service)

        self._unstructured_client = UnstructuredClient(server_url="http://unstructured:8000")

    @property
    def compatible_file_types(self) -> list[FileType]:
        """
        List of compatible file types for the document parser.

        Returns
        -------
        list[FileType]
            A list containing the compatible file types. By default, it returns a list with FileType.NONE.
        """
        return [FileType.PDF, AdditionalFileType.EPUB]

    def extract_content(self, file_path: Path) -> list[InformationPiece]:
        """
        Extract content from given file.

        Parameters
        ----------
        file_path : Path
            Path to the file the information should be extracted from.

        Returns
        -------
        list[InformationPiece]
            The extracted information.
        """
        unstructured = UnstructuredLoader(
                    client=self._unstructured_client,
                    #chunking_strategy=shared.ChunkingStrategy.BY_TITLE,
                    file_path=file_path,
                    partition_via_api=True,
                    #strategy=shared.Strategy.OCR_ONLY,
                    languages=["deu", "eng"],
                    #pdf_infer_table_structure=True,
                )
        extracted_content = unstructured.load()
        return [self._create_information_piece(file_path.name, x.page_content, ContentType.TEXT, x.metadata) for x in extracted_content]
    
    def _create_information_piece(
        self,
        document_name: str,
        content: str,
        content_type: ContentType,
        additional_meta: Optional[dict[str, Any]] = None,
    ) -> InformationPiece:
        metadata = {
            "document": document_name,
            "id": hash_datetime(),
            "related": [],
        }
        if additional_meta:
            metadata.update(additional_meta)
        return InformationPiece(
            type=content_type,
            metadata=metadata,
            page_content=content,
        )