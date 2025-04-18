"""Os diferentes atributos que podemos passar para o Web Service do Sesuite."""

from dataclasses import dataclass

from .render import render


@dataclass(slots=True, frozen=True, repr=False)
class Entity:
    """
    Campo a ser passado para o Web Service do Sesuite.

    Attributes
    ----------
    id : str
        identificador do Campo.
    value: str
        valor do Campo.

    """

    id: str
    value: str

    def __str__(self) -> str:
        return render("attributes/entity.xml", id=self.id, value=self.value)


@dataclass(slots=True, frozen=True, repr=False)
class Relationship:
    """
    Relacionamento a ser passado para o Web Service do Sesuite.

    Attributes
    ----------
    relationship_id : str
        Identificador do relacionamento.
    field_id: str
        Identificador do campo do relacionamentos.
    field_value: str
        Valor do campo do relacionamento.

    """

    relationship_id: str
    field_id: str
    field_value: str

    def __str__(self) -> str:
        return render(
            "attributes/relationship.xml",
            relationship_id=self.relationship_id,
            field_id=self.field_id,
            field_value=self.field_value,
        )


@dataclass(slots=True, frozen=True, repr=False)
class TableField:
    """
    Campo da tabela do formulário.

    Attributes
    ----------
    id : str
        Identificador do campo.
    value : str
        Valor do campo.

    """

    id: str
    value: str

    def __str__(self) -> str:
        return render("attributes/tablefield.xml", id=self.id, value=self.value)
