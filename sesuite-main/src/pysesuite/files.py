import base64
from pathlib import Path


def base_64(filepath: Path) -> str:
    """
    Converte arquivos para base64.

    Parameters
    ----------
    filepath : str
        Caminho do arquivo.

    Returns
    -------
    str
        string em base64 do conteúdo do arquivo.

    """
    with filepath.open("rb") as f:
        content = f.read()
        content_encoded = base64.encodebytes(content).decode("ascii")

    return repr(content_encoded)
