from rest_framework import generics
from django_filters import rest_framework as filters
from .models import Categoria, Autor, Livro
from .serializers import CategoriaSerializer, AutorSerializer, LivroSerializer

# Views para o modelo Categoria
class CategoriaList(generics.ListCreateAPIView):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    name = "categoria-list"
    # Ordenação disponível pelo nome da categoria
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
    # Ordenação disponível pelo nome do autor
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
    # Adicionar o atributo de ordenação
    ordering_fields = ['titulo', 'autor__nome', 'categoria__nome', 'publicado_em']  # Campos disponíveis para ordenação
    ordering = ['titulo']  # Ordem padrão (opcional)

class LivroDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Livro.objects.all()
    serializer_class = LivroSerializer
    name = "livro-detail"
