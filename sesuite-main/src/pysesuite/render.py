from pathlib import Path

import jinja2

TEMPLATES_FOLDER = Path(__file__).parent.resolve() / "templates"


def render(template_name: str, **kwargs: object) -> str:
    """
    Renderiza o template especificado e passa dados para o mesmo.

    Parameters
    ----------
    template_name : str
        O nome do template.
    **kwargs
        Argumentos extras para serem passados ao template.

    Returns
    -------
    str
        A representação em XML renderizada.

    """
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(TEMPLATES_FOLDER),
        autoescape=jinja2.select_autoescape(),
    )

    template = env.get_template(template_name).render(**kwargs)

    return str(template)
