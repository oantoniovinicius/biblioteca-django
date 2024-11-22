from rest_framework import permissions

class IsColecionador(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        # Permite leitura para todos os usuários
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Permite edição/exclusão apenas para o colecionador da coleção
        return obj.colecionador == request.user
