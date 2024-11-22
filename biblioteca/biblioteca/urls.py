"""
URL configuration for biblioteca project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from core import views
from rest_framework.authtoken.views import obtain_auth_token
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls),

    # URLs para o modelo Livro
    path('livros/', views.LivroList.as_view(), name='livros-list'),  # Atualizado para a CBV LivroList
    path('livros/<int:pk>/', views.LivroDetail.as_view(), name='livro-detail'),  # Atualizado para a CBV LivroDetail
    path('livros/create/', views.LivroList.as_view(), name='livro-create'),  # Adiciona a rota para criar livro

    # URLs para o modelo Categoria
    path('categorias/', views.CategoriaList.as_view(), name='categorias-list'),  # Nova rota para a CBV CategoriaList
    path('categorias/<int:pk>/', views.CategoriaDetail.as_view(), name='categoria-detail'),  # Nova rota para a CBV CategoriaDetail

    # URLs para o modelo Autor
    path('autores/', views.AutorList.as_view(), name='autores-list'),  # Nova rota para a CBV AutorList
    path('autores/<int:pk>/', views.AutorDetail.as_view(), name='autor-detail'),  # Nova rota para a CBV AutorDetail
    
    # URLs para o modelo Colecao
    path('colecoes/', views.ColecaoListCreate.as_view(), name='colecao-list-create'),
    path('colecoes/<int:pk>/', views.ColecaoDetail.as_view(), name='colecao-detail'),

    path('api/token/', obtain_auth_token, name='api_token_auth'),  # Endpoint para obter token

    # Endpoints de schema e documentação
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]
