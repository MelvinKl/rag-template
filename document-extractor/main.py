from extractor_api_lib.main import app as perfect_extractor_app, register_dependency_container  # noqa: F401

from container import UseCaseContainer


register_dependency_container(UseCaseContainer())