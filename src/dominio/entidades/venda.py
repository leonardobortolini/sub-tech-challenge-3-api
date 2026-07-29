from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from src.dominio.enums.status import StatusPagamento

# Entidade que representa uma venda
@dataclass
class Venda:

    id: UUID

    veiculo_id: UUID

    cpf_comprador: str

    codigo_pagamento: str

    data_venda: datetime

    status_pagamento: StatusPagamento = StatusPagamento.PENDENTE


    def atualizar_pagamento(
        self,
        status: StatusPagamento
    ):

        self.status_pagamento = status