class WorkflowError(Exception):
    """Ocorreu algum erro com a componente de Workflow."""


class FormError(Exception):
    """Ocorreu algum erro com a componente de Formulário."""


class SessionError(Exception):
    """A sessão HTTP não foi iniciada."""
