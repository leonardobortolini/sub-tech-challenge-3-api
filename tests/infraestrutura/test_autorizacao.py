import pytest
from fastapi import HTTPException

from src.infraestrutura.autenticacao.autorizacao import (
    exigir_role
)


# Testa se um usuário que possui a role necessária consegue acessar o recurso
def test_usuario_com_role_permitida():

    # Simula um usuário autenticado com a role cliente
    usuario = {
        "realm_access": {
            "roles": ["cliente"]
        }
    }

    # A execução não deve gerar nenhuma exceção quando a role é permitida
    exigir_role(
        usuario,
        "cliente"
    )


# Testa se um usuário sem a role necessária recebe erro de acesso negado
def test_usuario_com_role_nao_permitida():

    # Simula um usuário que possui apenas a role cliente"
    usuario = {
        "realm_access": {
            "roles": ["cliente"]
        }
    }

    # A tentativa de acesso como admin deve ser rejeitada
    with pytest.raises(HTTPException) as erro:

        exigir_role(
            usuario,
            "admin"
        )

    assert erro.value.status_code == 403


# Testa se um usuário que não possui nenhuma role recebe acesso negado
def test_usuario_sem_roles():

    # Simula um usuário autenticado sem nenhuma role atribuída
    usuario = {
        "realm_access": {
            "roles": []
        }
    }

    with pytest.raises(HTTPException) as erro:

        exigir_role(
            usuario,
            "admin"
        )

    assert erro.value.status_code == 403


# Testa o comportamento quando as informações de roles não estão presentes
def test_usuario_sem_realm_access():

    # Simula um usuário sem a estrutura realm_access retornada pelo Keycloak
    usuario = {}

    with pytest.raises(HTTPException) as erro:

        exigir_role(
            usuario,
            "admin"
        )

    assert erro.value.status_code == 403


# Testa se o usuário pode acessar o recurso quando possui uma das várias roles permitidas.
def test_usuario_com_uma_das_roles_permitidas():

    # Simula um usuário que possui a role cliente
    usuario = {
        "realm_access": {
            "roles": ["cliente"]
        }
    }

    # O acesso deve ser permitido porque cliente é uma das roles aceitas
    exigir_role(
        usuario,
        "admin",
        "cliente"
    )


# Testa se um usuário com múltiplas roles pode acessar um recurso que exige apenas uma delas
def test_usuario_com_multiplas_roles():

    # Simula um usuário que possui as roles cliente e admin
    usuario = {
        "realm_access": {
            "roles": ["cliente", "admin"]
        }
    }

    # O acesso deve ser permitido porque o usuário possui a role admin
    exigir_role(
        usuario,
        "admin"
    )