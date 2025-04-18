"""
Submódulo para auxiliar na analise e manipulação de XML.

Classes
-------
Xml
    Uma classe que permite analisar e manipulação de XML.
"""

from __future__ import annotations

from xml.etree import ElementTree as ET


class Xml:
    """Manipulação de XML."""

    __slots__ = ("_element", "_namespaces", "_root")

    def __init__(self, data: str, component: str) -> None:
        """
        Manipulação de XML.

        Parameters
        ----------
        data : XML
            Os dados XML.
        component : str
            Qual o componente do sesuite será utilizado.

        """
        self._root = ET.fromstring(data)
        self._element = component
        self._namespaces = {component: f"urn:{component}"}

    def find_one(self, tag: str) -> str | None:
        """
        Retorna o valor da tag especificada.

        Parameters
        ----------
        tag : str
            Nome da tag de onde o valor vai ser extraído.

        Returns
        -------
        str
            Valor extraído da tag.
        None
            caso não seja encontrado nada, um valor nulo é retornado.

        """
        result = self._root.find(
            f".//{self._element}:{tag}", namespaces=self._namespaces
        )
        if result is None:
            return None

        return result.text

    def find_many(self, tag: str) -> list[str | None]:
        """
        Retorna uma representação em dicionario do XML.

        Parameters
        ----------
        tag : str
            Nome da tag de onde os valores vão ser extraído.

        Returns
        -------
        list of str or None
            Uma representação em lista dos valores encontrados.

        """
        return [
            v.text
            for v in self._root.findall(
                f".//{self._element}:{tag}", namespaces=self._namespaces
            )
        ]
