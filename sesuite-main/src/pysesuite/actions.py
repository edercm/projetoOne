"""As diferentes ações SOAP que o Web Service do Sesuite aceita."""

from enum import StrEnum


class SOAPAction(StrEnum):
    """Tipo de ação a ser realizada pelo Web Service do Sesuite."""

    execute_activity = "executeActivity"
    execute_system_activity = "executeSystemActivity"
    new_workflow_edit_data = "newWorkflowEditData"
    get_table_record = "getTableRecord"
    new_attachment = "newAttachment"
    cancel_workflow = "cancelWorkflow"
    new_child_entity_record = "newChildEntityRecord"
