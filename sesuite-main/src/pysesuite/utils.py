from collections.abc import Generator
from pathlib import Path

import requests

from .attributes import Entity, Relationship, TableField
from .exceptions import FormError


def entity(**fields: str) -> Generator[Entity]:
    """
    Função para facilitar a criação de entidades do webservice.

    Parameters
    ----------
    **fields : str
        Keyword arguments de cada campo que deve ser preenchido.

    Yields
    ------
    Entity
        Representação de uma entidade do webservice.

    """
    for field_id, field_value in fields.items():
        yield Entity(field_id, field_value)


def relationship(
    relationship_id: str, **fields: str
) -> Generator[Relationship]:
    """
    Função para facilitar a criação de relacionamento do webservice.

    Parameters
    ----------
    relationship_id : str
        Identificador do relacionamento.
    **fields : str
        Keyword arguments de cada campo que deve ser preenchido.

    Yields
    ------
    Relationship
        Representação de um relacionamento do webservice.

    """
    for field_id, field_value in fields.items():
        yield Relationship(relationship_id, field_id, field_value)


def tablefield(**fields: str) -> Generator[TableField]:
    """
    Função para facilitar a criação de campos da tabela do webservice.

    Parameters
    ----------
    **fields : str
        Keyword arguments de cada campo que deve ser preenchido.

    Yields
    ------
    Entity
        Representação de um campo da tabela do webservice.

    """
    for field_id, field_value in fields.items():
        yield TableField(field_id, field_value)


def download(auth: str, file_hash: str, file_name: str) -> None:
    """
    Baixe o arquivo com o hash retornado pelo método ``get_table_record()``.

    Parameters
    ----------
    auth : str
        Token de autorização do usuário.
    file_hash : str
        Hash do arquivo
    file_name : str
        Nome que o arquivo deve ser salvo.

    Raises
    ------
    FormError
        Caso ocorra algum problema com a api.

    See Also
    --------
    Sesuite().get_table_record:
        Utilize esse método para obter o hash do arquivo.

    """
    with requests.Session() as session:
        session.headers = {"accept": "*/*", "Authorization": auth}
        response = session.get(
            f"https://sesuite.sicredi.com.br/apigateway/v1/file/{file_hash}"
        )

    if response.status_code != 200:
        error = "ocorreu um erro com o retorno do arquivo"
        raise FormError(error)

    download_dir = Path.cwd() / "downloads"
    download_dir.mkdir(exist_ok=True)

    file_path = download_dir / file_name
    file_path.touch(exist_ok=True)

    file_path.write_bytes(response.content)
