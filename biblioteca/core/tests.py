from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from core.models import Colecao, Livro, Categoria, Autor


class ColecaoTests(APITestCase):
    def setUp(self):
        # Criação de usuários
        self.user = User.objects.create_user(username='colecionador1', password='senha123')
        self.other_user = User.objects.create_user(username='colecionador2', password='senha456')

        # Geração de tokens
        self.user_token = Token.objects.create(user=self.user)
        self.other_user_token = Token.objects.create(user=self.other_user)

        # Configuração inicial dos modelos
        self.categoria = Categoria.objects.create(nome='Ficção Científica')
        self.autor = Autor.objects.create(nome='Isaac Asimov')

        self.livro1 = Livro.objects.create(
            titulo='Fundação', autor=self.autor, categoria=self.categoria, publicado_em='1951-01-01'
        )

        self.colecao = Colecao.objects.create(
            nome='Coleção de Isaac Asimov', descricao='Livros do autor', colecionador=self.user
        )
        self.colecao.livros.set([self.livro1])

    def autenticar_como_user(self):
        """Autentica como colecionador1."""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_token.key)

    def autenticar_como_other_user(self):
        """Autentica como colecionador2."""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.other_user_token.key)

    def test_criacao_de_colecao(self):
        self.autenticar_como_user()
        data = {'nome': 'Nova Coleção', 'descricao': 'Descrição', 'livros': [self.livro1.id]}
        response = self.client.post('/colecoes/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_permissao_edicao_colecao(self):
        self.autenticar_como_other_user()
        data = {'nome': 'Coleção Editada'}
        response = self.client.patch(f'/colecoes/{self.colecao.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_permissao_delecao_colecao(self):
        self.autenticar_como_other_user()
        response = self.client.delete(f'/colecoes/{self.colecao.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_listagem_de_colecoes(self):
        self.autenticar_como_user()
        response = self.client.get('/colecoes/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
