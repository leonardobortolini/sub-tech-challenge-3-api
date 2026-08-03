from fastapi import HTTPException


def exigir_role(
    usuario: dict,
    *roles_permitidas: str
):

    # Valida se o usuário possui uma das roles permitidas
    roles_usuario = usuario.get(
        "realm_access",
        {}
    ).get(
        "roles",
        []
    )

    if not any(
        role in roles_usuario
        for role in roles_permitidas
    ):
    
        # Bloqueia o acesso caso nenhuma role seja encontrada
        raise HTTPException(
            status_code=403,
            detail="Usuário não possui permissão."
        )