import pytest

from src.dominio.validacao.cpf import CPF


# Testa se um CPF válido é aceito
def test_cpf_valido():

    cpf = CPF(
        "24489006047"
    )

    assert str(cpf) == "24489006047"


# Testa se um CPF válido informado com máscara é aceito
def test_cpf_valido_com_mascara():

    cpf = CPF(
        "244.890.060-47"
    )

    assert str(cpf) == "24489006047"


# Testa se um CPF com dígitos verificadores inválidos é rejeitado
def test_cpf_invalido():

    with pytest.raises(ValueError):

        CPF(
            "24487706047"
        )


# Um CPF tem que possuir 11 dígitos
def test_cpf_com_quantidade_incorreta_de_digitos():

    with pytest.raises(ValueError):

        CPF(
            "123456789"
        )


# Letras não são permitidas no CPF.
def test_cpf_com_letras():

    with pytest.raises(ValueError):

        CPF(
            "03895992ABC"
        )

# Rejeita cpf formado apenas por dígitos repetidos
def test_cpf_com_digitos_repetidos():

    with pytest.raises(ValueError):

        CPF(
            "11111111111"
        )