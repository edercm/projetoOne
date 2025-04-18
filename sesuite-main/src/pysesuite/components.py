"""Os diferentes componentes que o Web Service do Sesuite recebe."""

from enum import StrEnum

_components = {"wf": "workflow", "fm": "form"}


class Components(StrEnum):
    """
    Componente a ser utilizado pelo Web Service do Sesuite.

    Properties
    ----------
    url
        A url do componente
    """

    Workflow = "wf"
    Form = "fm"

    @property
    def url(self) -> str:
        """A url do componente especificado."""
        return f"https://sesuite.sicredi.com.br/apigateway/se/ws/{self}_ws.php"

    @property
    def name(self) -> str:
        """Nome do componente."""
        return _components[self]
