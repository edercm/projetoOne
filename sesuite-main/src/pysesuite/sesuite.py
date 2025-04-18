"""Uma interface que permite a integração com o Sesuite."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

import requests
from typing_extensions import Self
from urllib3 import disable_warnings
from urllib3.exceptions import InsecureRequestWarning

from .actions import SOAPAction
from .components import Components
from .exceptions import FormError, SessionError, WorkflowError
from .files import base_64
from .parsing import get_dict, get_one
from .render import render

if TYPE_CHECKING:
    import types
    from collections.abc import Iterable
    from pathlib import Path

    from .attributes import Entity as Entity
    from .attributes import Relationship as Relationship
    from .attributes import TableField as TableField

disable_warnings(InsecureRequestWarning)


@dataclass(slots=True, repr=False)
class Sesuite:
    """A principal interface para a integração com o sesuite."""

    _auth: str
    _session: requests.Session | None = field(default=None)

    def __enter__(self) -> Self:
        self._session = requests.Session()
        return self

    def __exit__(
        self,
        _type: type[BaseException] | None,
        value: BaseException | None,
        traceback: types.TracebackType | None,
    ) -> None:
        self.close()

    def close(self) -> None:
        if self._session:
            self._session.close()

    def _call_api(
        self, component: Components, soap_action: SOAPAction, body: str
    ) -> str:
        """
        Chama a Web Service do Sesuite com os parâmetros necessários.

        Parameters
        ----------
        component : Components
            Componente do SeSuite que será utilizado.
        soap_action : SOAPAction
            Ação que o Web Service está chamando.
        body : str
            Corpo XML da requisição.

        Returns
        -------
        str
            Dados da requisição da API.

        Raises
        ------
        WorkflowError
            Se ocorre um erro com a requisição.
        SessionError
            Se não foi iniciado a sessão http.

        """
        headers = {
            "Authorization": self._auth,
            "Content-Type": "text/xml; charset=utf-8",
            "SOAPAction": f"urn:{component}#{soap_action}",
        }

        if not self._session:
            error = "Não foi iniciado a sessão HTTP"
            raise SessionError(error)

        response = self._session.post(
            component.url, data=body, headers=headers, verify=False
        )

        data = response.content.decode("utf-8")

        if response.status_code != 200:
            error = f"Ocorreu um erro com a requisição: {data}"
            raise WorkflowError(error)

        return data

    def execute_activity(
        self, *, workflow_id: str, activity_id: str, action_sequence: int
    ) -> str | None:
        """
        Executa a atividade especificada.

        Parameters
        ----------
        workflow_id : str
            Identificador do instancia do processo.
        activity_id : str
            Identificador da atividade.
        action_sequence : int
            Numero da sequencia da ação.

        Returns
        -------
        str or None
            Detalhes da execução.

        Raises
        ------
        WorkflowError
            Erro caso tenha ocorrido algum problema com a execução do Sesuite.

        """
        body = render(
            "actions/execute_activity.xml",
            workflow_id=workflow_id,
            activity_id=activity_id,
            action_sequence=action_sequence,
        )

        response = self._call_api(
            Components.Workflow, SOAPAction.execute_activity, body
        )

        status = get_one(response, Components.Workflow, "Status")
        detail = get_one(response, Components.Workflow, "Detail")

        if status == "FAILURE":
            raise WorkflowError(detail)

        return detail

    def execute_system_activity(
        self, *, workflow_id: str, activity_id: str, activity_order: str
    ) -> str | None:
        """
        Executa a atividades de sistema especificada.

        Parameters
        ----------
        workflow_id : str
            Identificador da instancia do processo.
        activity_id : str
            Identificador da atividade habilitada.
        activity_order : str
            Valor da ordem da atividade.

        Returns
        -------
        str or None
            Detalhes da execução.

        Raises
        ------
        WorkflowError
            Erro caso tenha ocorrido algum problema com a execução do Sesuite.

        """
        body = render(
            "actions/execute_system_activity.xml",
            workflow_id=workflow_id,
            activity_id=activity_id,
            activity_order=activity_order,
        )

        response = self._call_api(
            Components.Workflow, SOAPAction.execute_system_activity, body
        )

        status = get_one(response, Components.Workflow, "Status")
        detail = get_one(response, Components.Workflow, "Detail")

        if status == "FAILURE":
            raise WorkflowError(detail)

        return detail

    def new_workflow_edit_data(
        self,
        user_id: str | None = None,
        *,
        process_id: str,
        workflow_title: str,
        entity_id: str = "",
        entity_list: Iterable[Entity] | None = None,
        relationship_list: Iterable[Relationship] | None = None,
    ) -> tuple[str | None, str | None]:
        """
        Cria novo processo e preenche os dados especificados.

        Parameters
        ----------
        user_id : UserId, optional
            Matricula do usuário.
        process_id : str
            Identificador do processo.
        workflow_title : str
            Titulo da instancia do processo.
        entity_id : str, optional
            Identificador da tabela.
        entity_list : Iterable of Entity, optional
            Lista de informações dos campos da tabela.
        relationship_list : Iterable of Relationship, optional
            Lista de informações dos relacionamentos.

        Returns
        -------
        tuple of str or None
            status e detalhes da execução e o identificador na instancia.

        Raises
        ------
        WorkflowError
            Erro caso tenha ocorrido algum problema com a execução do Sesuite.

        """
        body = render(
            "actions/new_workflow_edit_data.xml",
            process_id=process_id,
            workflow_title=workflow_title,
            user_id=user_id,
            entity_id=entity_id,
            entity_list=entity_list,
            relationship_list=relationship_list,
        )

        response = self._call_api(
            Components.Workflow, SOAPAction.new_workflow_edit_data, body
        )

        status = get_one(response, Components.Workflow, "Status")
        detail = get_one(response, Components.Workflow, "Detail")
        record_id = get_one(response, Components.Workflow, "RecordID")

        if status == "FAILURE":
            raise WorkflowError(detail)

        return detail, record_id

    def new_attachment(
        self,
        user_id: str | None = None,
        *,
        workflow_id: str,
        activity_id: str,
        file_path: Path,
    ) -> tuple[str | None, str | None]:
        """
        Adiciona um novo anexo a uma atividade do processo.

        Parameters
        ----------
        user_id : UserId
            Matricula do usuário.
        workflow_id : str
            Identificador da instancia do processo.
        activity_id : str
            Identificador da atividade do processo.
        file_path : Path
            Caminho do arquivo

        Returns
        -------
        tuple of str or None
            status da execução, detalhes da execução e identificador do anexos.

        Raises
        ------
        WorkflowError
            Erro caso tenha ocorrido algum problema com a execução do Sesuite.

        """
        body = render(
            "actions/new_attachment.xml",
            user_id=user_id,
            workflow_id=workflow_id,
            activity_id=activity_id,
            file_path=file_path,
            content=base_64(file_path),
        )

        response = self._call_api(
            Components.Workflow, SOAPAction.new_attachment, body
        )

        status = get_one(response, Components.Workflow, "Status")
        detail = get_one(response, Components.Workflow, "Detail")
        record_id = get_one(response, Components.Workflow, "RecordID")

        if status == "FAILURE":
            raise WorkflowError(detail)

        return detail, record_id

    def get_table_record(
        self,
        *,
        table_id: str,
        table_field_list: Iterable[TableField],
        pagination: int = 1,
    ) -> tuple[str | None, dict[str | None, str | None]]:
        """
        Retorna os valores da tabela filtrados.

        Parameter
        ---------
        table_id : str
            Identificador da tabela.
        table_field_list : list of TableField
            Lista de campos que serão usados para filtrar a tabela.
        pagination : int, by default 1
            Paginação da resposta.

        Returns
        -------
        tuple of str or None and dict of str or None and str or None
            status e detalhes da execução e dicionario das informações da tabela

        Raises
        ------
        FormError
            Erro caso tenha ocorrido algum problema com a execução do Sesuite.

        """
        body = render(
            "actions/get_table_record.xml",
            table_id=table_id,
            pagination=pagination,
            table_field_list=table_field_list,
        )

        response = self._call_api(
            Components.Form, SOAPAction.get_table_record, body
        )

        status = get_one(response, Components.Workflow, "Status")
        detail = get_one(response, Components.Workflow, "Detail")
        records = get_dict(
            response, Components.Form, "TableFieldID", "TableFieldValues"
        )

        if status == "FAILURE":
            raise FormError(detail)

        return detail, records

    def cancel_workflow(
        self, user_id: str | None, *, workflow_id: int | str, explanation: str
    ) -> str | None:
        """
        Cancele uma instancia de um processos.

        Parameters
        ----------
        user_id : UserId
            Matricula do usuário.
        workflow_id : int | str
            Identificador da instancia do processo.
        explanation : str
            Motivo do cancelamento do processo.

        Returns
        -------
        tuple of str or None
            Status da execução e os detalhes da execução.

        Raises
        ------
        WorkflowError
            Erro caso tenha ocorrido algum problema com a execução do Sesuite.

        """
        body = render(
            "actions/cancel_workflow.xml",
            workflow_id=workflow_id,
            explanation=explanation,
            user_id=user_id,
        )

        response = self._call_api(
            Components.Workflow, SOAPAction.cancel_workflow, body
        )

        status = get_one(response, Components.Workflow, "Status")
        detail = get_one(response, Components.Workflow, "Detail")

        if status == "FAILURE":
            raise WorkflowError(detail)

        return detail

    def new_child_entity_record(
        self,
        *,
        workflow_id: str,
        entity_id: str,
        entity_attribute: Iterable[Entity],
        relationship_id: str,
        relationship_attribute: Iterable[Relationship],
    ) -> str | None:
        """
        Adicione novas linhas nas grids do fomulário.

        Parameters
        ----------
        workflow_id : str
            Identificador da instancia.
        entity_id : str
            Identificador da tabela principal.
        entity_attribute : Iterable[Entity]
            Os atributos a serem adicionados na tabela principal.
        relationship_id : str
            Identificador do relacionamento da grid.
        relationship_attribute : Iterable[Relationship]
            Os atributos a serem adicionados na grid.

        Returns
        -------
        str or None
            Detalhes do retorno da api.

        Raises
        ------
        WorkflowError
            Erro caso tenha ocorrido algum problema com a execução do Sesuite.

        """
        body = render(
            "actions/cancel_workflow.xml",
            workflow_id=workflow_id,
            entity_id=entity_id,
            entity_attribute=entity_attribute,
            relationship_id=relationship_id,
            relationship_attribute=relationship_attribute,
        )

        response = self._call_api(
            Components.Workflow, SOAPAction.new_child_entity_record, body
        )

        status = get_one(response, Components.Workflow, "Status")
        detail = get_one(response, Components.Workflow, "Detail")

        if status == "FAILURE":
            raise WorkflowError(detail)

        return detail
