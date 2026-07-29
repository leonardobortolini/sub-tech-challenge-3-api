from fastapi import (
    APIRouter,
    Depends
)

from sqlalchemy.orm import Session


from src.infraestrutura.database.conexao import (
    obter_sessao
)

from src.infraestrutura.database.venda_repositorio import (
    VendaRepositorioPostgres
)


from src.aplicacao.casos_de_uso.atualizar_pagamento import (
    AtualizarPagamento
)


from src.aplicacao.schemas.venda_schema import (
    PagamentoWebhookRequest
)


from src.aplicacao.casos_de_uso.listar_pagamentos import (
    ListarPagamentos
)


router = APIRouter(
    prefix="/pagamentos",
    tags=["Pagamentos"]
)


# Endpoint atualizacao pagamento
@router.post("/webhook")
def webhook_pagamento(
    request: PagamentoWebhookRequest,
    sessao: Session = Depends(obter_sessao)
):

    repositorio = VendaRepositorioPostgres(
        sessao
    )


    caso_de_uso = AtualizarPagamento(
        repositorio
    )


    return caso_de_uso.executar(
        codigo_pagamento=request.codigo_pagamento,
        status=request.status
    )

# Endpoint listar pagamentos
@router.get("")
def listar_pagamentos(
    status: str,
    sessao: Session = Depends(obter_sessao)
):

    repositorio = VendaRepositorioPostgres(
        sessao
    )


    caso_de_uso = ListarPagamentos(
        repositorio
    )


    return caso_de_uso.executar(
        status=status
    )