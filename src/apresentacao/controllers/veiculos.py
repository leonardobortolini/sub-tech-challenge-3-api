from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session


from src.infraestrutura.database.conexao import (
    obter_sessao
)

from src.infraestrutura.database.veiculo_repositorio import (
    VeiculoRepositorioPostgres
)


from src.aplicacao.schemas.veiculo_schema import (
    CriarVeiculoRequest,
    VeiculoVendidoResponse
)


from src.aplicacao.casos_de_uso.cadastrar_veiculo import (
    CadastrarVeiculo
)

from src.aplicacao.casos_de_uso.editar_veiculo import (
    EditarVeiculo
)

from src.aplicacao.casos_de_uso.listar_veiculos import (
    ListarVeiculos
)

from src.infraestrutura.database.venda_repositorio import (
    VendaRepositorioPostgres
)

from src.aplicacao.casos_de_uso.vender_veiculo import (
    VenderVeiculo
)

from src.aplicacao.schemas.venda_schema import (
    VendaRequest
)

from src.dominio.excecoes.excecoes import (
    VeiculoNaoEncontrado,
    VeiculoJaVendido
)

from src.infraestrutura.autenticacao.dependencias import (
    obter_usuario_autenticado
)

from src.infraestrutura.autenticacao.autorizacao import exigir_role

router = APIRouter(
    prefix="/veiculos",
    tags=["Veiculos"]
)


# Endpoint cadastro de veiculos
@router.post("")
def cadastrar(
    request: CriarVeiculoRequest,
    usuario: dict = Depends(obter_usuario_autenticado),
    sessao: Session = Depends(obter_sessao)
):


    exigir_role(
        usuario,
        "admin"
    )


    repositorio = VeiculoRepositorioPostgres(
        sessao
    )


    caso_de_uso = CadastrarVeiculo(
        repositorio
    )


    veiculo = caso_de_uso.executar(
        marca=request.marca,
        modelo=request.modelo,
        ano=request.ano,
        cor=request.cor,
        preco=request.preco
    )


    return veiculo


# Endpoint editar veiculos
@router.put("/{id}")
def editar(
    id: str,
    request: CriarVeiculoRequest,
    usuario: dict = Depends(obter_usuario_autenticado),
    sessao: Session = Depends(obter_sessao)
):


    exigir_role(
        usuario,
        "admin"
    )


    repositorio = VeiculoRepositorioPostgres(
        sessao
    )


    caso_de_uso = EditarVeiculo(
        repositorio
    )


    veiculo = caso_de_uso.executar(
        id=id,
        marca=request.marca,
        modelo=request.modelo,
        ano=request.ano,
        cor=request.cor,
        preco=request.preco
    )


    return veiculo


# Endpoint listar veiculos disponiveis
@router.get("/disponiveis")
def listar_disponiveis(
    usuario: dict = Depends(obter_usuario_autenticado),
    sessao: Session = Depends(obter_sessao)
):

    repositorio = VeiculoRepositorioPostgres(
        sessao
    )


    caso_de_uso = ListarVeiculos(
        repositorio
    )


    return caso_de_uso.disponiveis()


# Endpoint lista veiculos vendidos
@router.get(
    "/vendidos",
    response_model=list[VeiculoVendidoResponse]
)
def listar_vendidos(
    usuario: dict = Depends(obter_usuario_autenticado),
    sessao: Session = Depends(obter_sessao)
):

    exigir_role(
        usuario,
        "admin"
    )

    repositorio = VeiculoRepositorioPostgres(
        sessao
    )


    caso_de_uso = ListarVeiculos(
        repositorio
    )


    return caso_de_uso.vendidos()


# Endpoint venda de veiculo
@router.post("/{id}/vender")
def vender(
    id: str,
    request: VendaRequest,
    usuario: dict = Depends(obter_usuario_autenticado),
    sessao: Session = Depends(obter_sessao)
):

    exigir_role(
        usuario,
        "cliente"
    )


    try:

        veiculo_repo = VeiculoRepositorioPostgres(
            sessao
        )


        venda_repo = VendaRepositorioPostgres(
            sessao
        )


        caso_de_uso = VenderVeiculo(
            veiculo_repo,
            venda_repo
        )


        return caso_de_uso.executar(
            veiculo_id=id,
            keycloak_user_id=usuario["sub"],
            cpf_comprador=request.cpf_comprador,
            data_venda=request.data_venda
        )
    
    # Trata veiculo nao encontrado
    except VeiculoNaoEncontrado as erro:

        raise HTTPException(
            status_code=404,
            detail=str(erro)
        )

    # Trata tentativa de vender veiculo ja vendido
    except VeiculoJaVendido as erro:

        raise HTTPException(
            status_code=400,
            detail=str(erro)
        )

    # Trata erros de validacao
    except ValueError as erro:

        raise HTTPException(
            status_code=400,
            detail=str(erro)
        )