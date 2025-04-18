# Pysesuite 🐍

> Utilize o Python para automatizar o Se Suite!

Para facilitar a utilização da api do Se Suite, essa biblioteca traz algumas funções e classes que irão facilitar na hora da automação de processos.

## Instalação

Para instalar o o projeto, utilize o comando:

```shell
pip install git+https://gitlab.coop.sicredi.in/central_nne/coop0806/uipath/python/sesuite
```

Ou se estiver utilizando o `uv`:

```shell
uv add git+https://gitlab.coop.sicredi.in/central_nne/coop0806/uipath/python/sesuite
```

## Exemplo de uso

Aqui está um exemplo de como podemos desenvolver um script:

```python
import os

from pysesuite import Entity, Sesuite

AUTH = os.environ.get("AUTH", "Token de Autorização do Sesuite")


def main() -> None:
    data = [
        Entity("iptconta", "999999"),
        Entity("iptnaoexiste", "99999999999"),
        Entity("dtasolicitacao", "2024-09-11"),
        Entity("iptiniciador", "Pedro Henrique Souza Meinen"),
    ]

    with Sesuite(AUTH) as se:
        detalhes, identificador = se.new_workflow_edit_data(
            process_id="prc_0806_teste",
            workflow_title="Teste de API",
            entity_id="tab0806teste",
            entity_list=data,
        )

    if identificador:
        print(f"Processo {identificador} criado: {detalhes}")
    else:
        print(f"Não foi possível criar o processo: {detalhes}")


if __name__ == "__main__":
    main()
```

## Configuração para Desenvolvimento

Esse projeto utiliza a ferramenta [uv](https://docs.astral.sh/uv/) para gerenciamento de dependências.

Após clonar o projeto, para instalar todas as dependências, crie um novo ambiente virtual com:

```shell
uv sync
```

## Contributing

1. Faça o _fork_ do projeto no [GitLab](<https://gitlab.coop.sicredi.in/central_nne/coop0806/uipath/python/sesuite>)
2. Crie uma _branch_ para sua modificação (`git checkout -b feature/fooBar`)
3. Faça o _commit_ (`git commit -am 'Add some fooBar'`)
4. _Push_ (`git push origin feature/fooBar`)
5. Crie um novo _Merge Request_
