from rag_core_api.main import app as perfect_rag_app, register_dependency_container  # noqa: F401







from container import UseCaseContainer








register_dependency_container(UseCaseContainer())
