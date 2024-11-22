from rest_framework import permissions

class IsColecionadorOrReadOnly(permissions.BasePermission):
    """
    Permite apenas ao colecionador modificar os dados.
    Outros usuários podem visualizar.
    """
    def has_object_permission(self, request, view, obj):
        # Permite leitura para métodos seguros
        if request.method in permissions.SAFE_METHODS:
            return True
        # Permite modificação apenas ao colecionador
        return obj.colecionador == request.user
