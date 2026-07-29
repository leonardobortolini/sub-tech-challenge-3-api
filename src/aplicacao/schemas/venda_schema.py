from pydantic import BaseModel
from datetime import datetime

# Dados pra criar venda
class VendaRequest(BaseModel):

    cpf_comprador: str
    data_venda: datetime

# Dados webhook pagamento
class PagamentoWebhookRequest(BaseModel):

    codigo_pagamento: str
    status: str
