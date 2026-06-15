class NotFoundError(Exception):
    """Recurso não encontrado."""

    pass


class BadRequestError(Exception):
    """Dados inválidos enviados pelo cliente"""

    pass


class UnauthorizedError(Exception):
    """Usuário não autenticado"""

    pass


class ForbiddenError(Exception):
    """Usuário autenticado sem permissão"""

    pass
