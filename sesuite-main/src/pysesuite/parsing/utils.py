from __future__ import annotations

from typing import TYPE_CHECKING

from .xml_parser import Xml

if TYPE_CHECKING:
    from ..components import Components


def _lists_to_dict(
    lista_chaves: list[str | None], lista_valores: list[str | None]
) -> dict[str | None, str | None]:
    """
    Junta uma lista de chaves com uma lista de valores em um dicionario.

    Parameters
    ----------
    lista_chaves : list of FieldID
        Lista que irá se tornar as chaves do dicionario.
    lista_valores : list of FieldValue
        Lista que irá se tornar os valores do dicionario.

    Returns
    -------
    dictionary of FieldID and FieldID
        Dicionario com os valores da lista.

    """
    return dict(
        zip(
            [chave.lower() if chave else chave for chave in lista_chaves[1:-3]],
            lista_valores[1:-3],
            strict=False,
        )
    )


def get_one(data: str, component: Components, tag: str) -> str | None:
    """
    Obtém o valor de uma tag especifica do XML.

    Parameters
    ----------
    data : str
        Os dados em XML a serem analisados.
    component : str
        Qual o nome do componente que deve ser analisado.
    tag : str
        Qual a tag que deve ser procurada.

    Returns
    -------
    str
        O valor encontrado
    None
        Caso o valor não seja encontrado.

    See Also
    --------
    get_many():
        Obtém vários valores e retorna uma lista.
    get_dict():
        Obtém vários valores e retorna um dicionario.

    """
    return Xml(data, component.name).find_one(tag)


def get_many(data: str, component: Components, tag: str) -> list[str | None]:
    """
    Obtém vários valore de uma tag e retorna um lista com os valores.

    Parameters
    ----------
    data : str
        Os dados em XML a serem analisados.
    component : str
        Qual o nome do componente que deve ser analisado.
    tag : str
        Qual a tag que deve ser procurada.

    Returns
    -------
    list of str
        Os vários valores encontrados.
    None
        Caso o valor não seja encontrado

    See Also
    --------
    get_one():
        Obtém apenas um valor.
    get_dict():
        Obtém vários valores e retorna um dicionario.

    """
    return Xml(data, component.name).find_many(tag)


def get_dict(
    data: str, component: Components, key_tag: str, value_tag: str
) -> dict[str | None, str | None]:
    """
    Obtém vários valore de uma tag e retorna um dicionario com os valores.

    Parameters
    ----------
    data : str
        Os dados em XML a serem analisados.
    component : str
        Qual o nome do componente que deve ser analisado.
    key_tag : str
        Qual a tag que os valores serão as chaves do dicionario.
    value_tag : str
        Qual a tag que os valores serão os valores do dicionario.

    Returns
    -------
    dictionary of str and str or None
        Representação em dicionario dos valores encontrados.

    See Also
    --------
    get_one():
        Obtém apenas um valor.
    get_many():
        Obtém vários valores e retorna uma lista.

    """
    value = Xml(data, component.name)

    keys = value.find_many(key_tag)
    values = value.find_many(value_tag)

    return _lists_to_dict(keys, values)
