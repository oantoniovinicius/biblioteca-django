from rest_framework import generics, permissions
from django_filters import rest_framework as filters
from .models import Categoria, Autor, Livro, Colecao
from .serializers import CategoriaSerializer, AutorSerializer, LivroSerializer, ColecaoSerializer

# Views para o modelo Categoria
class CategoriaList(generics.ListCreateAPIView):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    name = "categoria-list"
    ordering_fields = ['nome']

class CategoriaDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    name = "categoria-detail"

# Views para o modelo Autor
class AutorList(generics.ListCreateAPIView):
    queryset = Autor.objects.all()
    serializer_class = AutorSerializer
    name = "autor-list"
    ordering_fields = ['nome']

class AutorDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Autor.objects.all()
    serializer_class = AutorSerializer
    name = "autor-detail"

# Filtro para o modelo Livro
class LivroFilter(filters.FilterSet):
    titulo = filters.CharFilter(lookup_expr='icontains')  # Filtro para título (case insensitive)
    autor = filters.CharFilter(field_name='autor__nome', lookup_expr='icontains')  # Filtro pelo nome do autor
    categoria = filters.CharFilter(field_name='categoria__nome', lookup_expr='icontains')  # Filtro pelo nome da categoria

    class Meta:
        model = Livro
        fields = ['titulo', 'autor', 'categoria']

# Views para o modelo Livro
class LivroList(generics.ListCreateAPIView):
    queryset = Livro.objects.all()
    serializer_class = LivroSerializer
    filterset_class = LivroFilter
    ordering_fields = ['titulo', 'autor__nome', 'categoria__nome', 'publicado_em']
    ordering = ['titulo']

class LivroDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Livro.objects.all()
    serializer_class = LivroSerializer
    name = "livro-detail"

# Permissão personalizada para Colecao
class IsColecionadorOrReadOnly(permissions.BasePermission):
    """
    Permite apenas ao colecionador modificar os dados.
    Outros usuários podem apenas visualizar.
    """
    def has_object_permission(self, request, view, obj):
        # Permite leitura para qualquer método seguro (GET, HEAD ou OPTIONS)
        if request.method in permissions.SAFE_METHODS:
            return True
        # Permite modificações apenas para o colecionador da coleção
        return obj.colecionador == request.user

# View para listar e criar coleções
class ColecaoListCreate(generics.ListCreateAPIView):
    """
    Listagem e criação de coleções.
    Qualquer usuário pode listar as coleções.
    Apenas usuários autenticados podem criar coleções.
    """
    queryset = Colecao.objects.all()
    serializer_class = ColecaoSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        # Define o colecionador como o usuário autenticado
        serializer.save(colecionador=self.request.user)

# View para detalhar, editar e excluir coleções
class ColecaoDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Recuperação, edição e exclusão de uma coleção específica.
    Apenas o colecionador pode editar ou excluir.
    """
    queryset = Colecao.objects.all()
    serializer_class = ColecaoSerializer
    permission_classes = [IsColecionadorOrReadOnly]
