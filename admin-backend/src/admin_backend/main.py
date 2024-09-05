# coding: utf-8

"""
    rag

    The API is used for the communication between the frontend and the backend in the rag project.

    The version of the OpenAPI document: 1.0.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501
import logging.config
import yaml

from fastapi import FastAPI
from rag_core_lib.impl.settings.rag_class_types_settings import RAGClassTypeSettings

from admin_backend.apis.admin_api import router
from admin_backend.dependency_container import DependencyContainer


with open("/config/logging.yaml", "r") as stream:
    config = yaml.safe_load(stream)
logging.config.dictConfig(config)

app = FastAPI(
    title="admin backend",
    description="The API is used for the communication between services in the rag project.",
    version="1.0.0",
)
container = DependencyContainer()
container.class_selector_config.from_dict(RAGClassTypeSettings().model_dump())
app.container = container

app.include_router(router)
