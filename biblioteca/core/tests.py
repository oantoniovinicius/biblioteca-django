from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from core.models import Colecao
from rest_framework.authtoken.models import Token


class ColecaoTestCase(APITestCase):
    def setUp(self):
        # Criando dois usuários (um colecionador e outro não)
        self.colecionador = User.objects.create_user(username='colecionador', password='senha123')
        self.outro_usuario = User.objects.create_user(username='outro_usuario', password='senha123')
        
        # Criando um token para autenticação
        self.colecionador_token = Token.objects.create(user=self.colecionador)
        self.outro_usuario_token = Token.objects.create(user=self.outro_usuario)

        # Criando uma coleção associada ao colecionador
        self.colecao = Colecao.objects.create(nome='Minha Coleção', colecionador=self.colecionador)

    def test_criar_colecao_usuario_autenticado(self):
        """
        Teste que verifica a criação de uma nova coleção por um usuário autenticado.
        """
        url = '/colecoes/'  # URL da view de criação de coleção
        data = {'nome': 'Nova Coleção', 'descricao': 'Uma descrição válida'}
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.colecionador_token.key)
        
        response = self.client.post(url, data, format='json')
        
        # Verifica se a coleção foi criada com sucesso
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Colecao.objects.count(), 2)  # Verifica que a quantidade de coleções aumentou
        self.assertEqual(Colecao.objects.last().colecionador, self.colecionador)  # Verifica se o colecionador está correto

    def test_criar_colecao_usuario_nao_autenticado(self):
        """
        Teste que verifica que um usuário não autenticado não pode criar uma coleção.
        """
        url = '/colecoes/'
        data = {'nome': 'Nova Coleção'}
        
        response = self.client.post(url, data, format='json')
        
        # Verifica se o status é 401 (não autorizado)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Colecao.objects.count(), 1)  # Verifica que nenhuma nova coleção foi criada

    def test_permissao_editar_colecao(self):
        """
        Teste que verifica que apenas o colecionador pode editar a coleção.
        """
        url = f'/colecoes/{self.colecao.id}/'  # URL da coleção criada
        
        # Tentando editar com o colecionador
        data = {'nome': 'Coleção Atualizada'}
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.colecionador_token.key)
        response = self.client.put(url, data, format='json')
        
        # Verifica se a edição foi bem-sucedida
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.colecao.refresh_from_db()  # Atualiza a instância da coleção
        self.assertEqual(self.colecao.nome, 'Coleção Atualizada')

        # Tentando editar com outro usuário
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.outro_usuario_token.key)
        response = self.client.put(url, data, format='json')
        
        # Verifica se a edição falhou
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.colecao.refresh_from_db()  # Atualiza a instância da coleção
        self.assertNotEqual(self.colecao.nome, 'Coleção Atualizada')  # O nome da coleção não deve ter mudado

    def test_permissao_deletar_colecao(self):
        """
        Teste que verifica que apenas o colecionador pode deletar sua coleção.
        """
        url = f'/colecoes/{self.colecao.id}/'
        
        # Tentando deletar com o colecionador
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.colecionador_token.key)
        response = self.client.delete(url)
        
        # Verifica se a deleção foi bem-sucedida
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Colecao.objects.count(), 0)  # Verifica se a coleção foi removida

        # Criando uma nova coleção para testar
        self.colecao = Colecao.objects.create(nome='Minha Nova Coleção', colecionador=self.colecionador)
        
        # Tentando deletar com outro usuário
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.outro_usuario_token.key)
        response = self.client.delete(url)
        
        # Verifica se a deleção falhou
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Colecao.objects.count(), 1)  # A coleção não deve ser removida

    def test_listagem_colecao_usuario_autenticado(self):
        """
        Teste que verifica se coleções podem ser listadas para usuários autenticados.
        """
        url = '/colecoes/'
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.colecionador_token.key)
        
        response = self.client.get(url)
        
        # Verifica se a coleção aparece na listagem
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Apenas uma coleção deve ser retornada
        self.assertEqual(response.data[0]['nome'], 'Minha Coleção')

    def test_listagem_colecao_usuario_nao_autenticado(self):
        """
        Teste que verifica que usuários não autenticados não podem listar coleções.
        """
        url = '/colecoes/'
        
        response = self.client.get(url)
        
        # Verifica se o status é 401 (não autorizado)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
