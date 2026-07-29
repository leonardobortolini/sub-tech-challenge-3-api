class CPF:

    def __init__(
        self,
        numero: str
    ):

        cpf = (
            numero
            .replace(".", "")
            .replace("-", "")
        )


        if not self._validar(
            cpf
        ):

            raise ValueError(
                "CPF invalido"
            )


        self.numero = cpf


    def _validar(
        self,
        cpf: str
    ):

        # Precisa possuir 11 numeros
        if len(cpf) != 11:
            return False


        # Verifica se possui somente numeros
        if not cpf.isdigit():
            return False


        # Evita CPFs invalido
        if cpf == cpf[0] * 11:
            return False


        # Valida primeiro digito verificador
        soma = sum(
            int(cpf[i]) * (10 - i)
            for i in range(9)
        )


        primeiro_digito = (
            soma * 10
        ) % 11


        if primeiro_digito == 10:
            primeiro_digito = 0


        if primeiro_digito != int(cpf[9]):
            return False


        # Valida segundo digito verificador
        soma = sum(
            int(cpf[i]) * (11 - i)
            for i in range(10)
        )


        segundo_digito = (
            soma * 10
        ) % 11


        if segundo_digito == 10:
            segundo_digito = 0


        return segundo_digito == int(
            cpf[10]
        )


    def __str__(
        self
    ):

        return self.numero