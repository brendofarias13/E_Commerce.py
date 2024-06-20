import mysql.connector  # Importa o módulo mysql.connector para conectar e interagir com o banco de dados MySQL


class Cliente:
    def __init__(self, nome, contato, endereco):
        self.nome = nome  # Atribui o nome do cliente ao atributo nome
        self.contato = contato  # Atribui o contato do cliente ao atributo contato
        self.endereco = endereco  # Atribui o endereço do cliente ao atributo endereco


class Produto:
    def __init__(self, nome, preco, descricao, quantidade, imagem):
        self.nome = nome  # Atribui o nome do produto ao atributo nome
        self.preco = preco  # Atribui o preço do produto ao atributo preco
        self.descricao = descricao  # Atribui a descrição do produto ao atributo descricao
        self.quantidade = quantidade  # Atribui a quantidade do produto ao atributo quantidade
        self.imagem = imagem


class Pedido:
    def __init__(self, cliente_id, produto_id):
        self.cliente_id = cliente_id  # Atribui o ID do cliente ao atributo cliente_id
        self.produto_id = produto_id  # Atribui o ID do produto ao atributo produto_id


class SistemaEcommerce:
    def __init__(self):
        self.conexao = mysql.connector.connect(  # Estabelece a conexão com o banco de dados MySQL
            host="localhost",
            user="root",
            password="he182555@",
            database="ecommerce_db"
        )
        self.cursor = self.conexao.cursor()  # Cria um cursor para executar comandos SQL no banco de dados

    def adicionar_produto(self, produto):
        try:
            # Verifica se o produto já existe pelo nome
            sql_verifica = "SELECT id FROM produtos WHERE nome = %s"  # Consulta SQL para verificar se o produto já existe
            self.cursor.execute(sql_verifica, (produto.nome,))  # Executa a consulta SQL com o nome do produto
            resultado = self.cursor.fetchone()  # Recupera o resultado da consulta

            if resultado:
                print(f"Produto '{produto.nome}' já existe no sistema.")  # Mensagem se o produto já existe
                return

            # Insere o produto se não existir
            sql = (
                "INSERT INTO produtos (nome, preco, descricao, quantidade, imagem) "  # Comando SQL para inserir um novo produto
                "VALUES (%s, %s, %s, %s, %s)"
            )
            valores = (produto.nome, produto.preco, produto.descricao, produto.quantidade, produto.imagem)  # Valores para a inserção
            self.cursor.execute(sql, valores)  # Executa o comando SQL de inserção
            self.conexao.commit()  # Confirma a transação no banco de dados
            print(f"Produto '{produto.nome}' adicionado com sucesso.")  # Mensagem de sucesso ao adicionar o produto
        except mysql.connector.Error as err:
            print(f"Erro ao adicionar produto: {err}")  # Mensagem de erro se ocorrer algum problema durante a inserção

    def excluir_produto(self, produto_id):
        try:
            # Exclui o produto
            sql = "DELETE FROM produtos WHERE id = %s"  # Comando SQL para excluir um produto pelo ID
            self.cursor.execute(sql, (produto_id,))  # Executa o comando SQL de exclusão com o ID do produto
            self.conexao.commit()  # Confirma a transação no banco de dados
            print(f'Produto com ID {produto_id} excluído com sucesso.')  # Mensagem de sucesso ao excluir o produto
        except mysql.connector.Error as err:
            print(f"Erro ao excluir produto: {err}")  # Mensagem de erro se ocorrer algum problema durante a exclusão

    def adicionar_cliente(self, cliente):
        try:
            # Insere o cliente
            sql = (
                "INSERT INTO clientes (nome, contato, endereco) "  # Comando SQL para inserir um novo cliente
                "VALUES (%s, %s, %s)"
            )
            valores = (cliente.nome, cliente.contato, cliente.endereco)  # Valores para a inserção
            self.cursor.execute(sql, valores)  # Executa o comando SQL de inserção
            self.conexao.commit()  # Confirma a transação no banco de dados
            return self.cursor.lastrowid  # Retorna o ID do cliente inserido
        except mysql.connector.Error as err:
            print(f"Erro ao adicionar cliente: {err}")  # Mensagem de erro se ocorrer algum problema durante a inserção
            return None  # Retorna None se ocorrer um erro

    def adicionar_pedido(self, pedido):
        try:
            # Verifica se o pedido já existe
            sql_verifica = "SELECT * FROM pedidos WHERE cliente_id = %s AND produto_id = %s"  # Consulta SQL para verificar se o pedido já existe
            self.cursor.execute(sql_verifica, (pedido.cliente_id, pedido.produto_id))  # Executa a consulta SQL com o ID do cliente e do produto
            if self.cursor.fetchone():  # Verifica se algum resultado foi retornado pela consulta
                print('Pedido duplicado não é permitido.')  # Mensagem se o pedido já existe
                return

            # Verifica se o produto está em estoque
            sql_verifica_quantidade = "SELECT quantidade FROM produtos WHERE id = %s"  # Consulta SQL para verificar a quantidade de um produto pelo ID
            self.cursor.execute(sql_verifica_quantidade, (pedido.produto_id,))  # Executa a consulta SQL com o ID do produto
            quantidade = self.cursor.fetchone()[0]  # Obtém a quantidade disponível do produto
            if quantidade <= 0:  # Verifica se a quantidade disponível é menor ou igual a zero
                print('Produto fora de estoque.')  # Mensagem se o produto estiver fora de estoque
                return

            # Insere o pedido se tudo estiver ok
            sql_insere_pedido = "INSERT INTO pedidos (cliente_id, produto_id) VALUES (%s, %s)"  # Comando SQL para inserir um novo pedido
            valores_pedido = (pedido.cliente_id, pedido.produto_id)  # Valores para a inserção
            self.cursor.execute(sql_insere_pedido, valores_pedido)  # Executa o comando SQL de inserção
            sql_atualiza_quantidade = (  # Comando SQL para atualizar a quantidade do produto no estoque após o pedido
                "UPDATE produtos SET quantidade = quantidade - 1 WHERE id = %s"
            )
            self.cursor.execute(sql_atualiza_quantidade, (pedido.produto_id,))  # Executa o comando SQL de atualização
            self.conexao.commit()  # Confirma a transação no banco de dados
            print('Pedido adicionado com sucesso.')  # Mensagem de sucesso ao adicionar o pedido
        except mysql.connector.Error as err:
            print(f"Erro ao adicionar pedido: {err}")  # Mensagem de erro se ocorrer algum problema durante a inserção

    def excluir_pedido(self, pedido_id):
        try:
            # Obtém o ID do produto do pedido
            sql_produto_id = "SELECT produto_id FROM pedidos WHERE id = %s"  # Consulta SQL para obter o ID do produto de um pedido pelo ID do pedido
            self.cursor.execute(sql_produto_id, (pedido_id,))  # Executa a consulta SQL com o ID do pedido
            produto_id = self.cursor.fetchone()[0]  # Obtém o ID do produto associado ao pedido

            # Exclui o pedido
            sql_exclui_pedido = "DELETE FROM pedidos WHERE id = %s"  # Comando SQL para excluir um pedido pelo ID
            self.cursor.execute(sql_exclui_pedido, (pedido_id,))  # Executa o comando SQL de exclusão com o ID do pedido

            # Atualiza a quantidade do produto no estoque
            sql_atualiza_quantidade = (
                "UPDATE produtos SET quantidade = quantidade + 1 WHERE id = %s"  # Comando SQL para aumentar a quantidade do produto no estoque
            )
            self.cursor.execute(sql_atualiza_quantidade, (produto_id,))  # Executa o comando SQL de atualização com o ID do produto
            self.conexao.commit()  # Confirma a transação no banco de dados
            print('Pedido excluído com sucesso.')  # Mensagem de sucesso ao excluir o pedido
        except mysql.connector.Error as err:
            print(f"Erro ao excluir pedido: {err}")  # Mensagem de erro se ocorrer algum problema durante a exclusão

    def listar_produtos(self, somente_disponiveis=False):
        try:
            if somente_disponiveis:
                self.cursor.execute(
                    "SELECT id, nome, preco, descricao, quantidade "  # Consulta SQL para selecionar produtos com quantidade maior que zero
                    "FROM produtos WHERE quantidade > 0"
                )
            else:
                self.cursor.execute(
                    "SELECT id, nome, preco, descricao, quantidade FROM produtos"  # Consulta SQL para selecionar todos os produtos
                )

            produtos = self.cursor.fetchall()  # Obtém todos os resultados da consulta
            for produto in produtos:
                estoque = "Sim" if produto[4] > 0 else "Não"  #
                print(
                    f"ID: {produto[0]}, Nome: {produto[1]}, Preço: {produto[2]}, "  # Imprime os detalhes do produto
                    f"Descrição: {produto[3]}, Quantidade: {produto[4]}, Em Estoque: {estoque}"  # Imprime se o produto está em estoque ou não
                )
        except mysql.connector.Error as err:
            print(f"Erro ao listar produtos: {err}")  # Mensagem de erro se ocorrer algum problema durante a listagem

    def listar_pedidos(self):
        try:
            self.cursor.execute(
                "SELECT pedidos.id, clientes.nome, produtos.nome FROM pedidos "  # Consulta SQL para selecionar pedidos
                "JOIN clientes ON pedidos.cliente_id = clientes.id "  # Junta a tabela de pedidos com a de clientes
                "JOIN produtos ON pedidos.produto_id = produtos.id"  # Junta a tabela de pedidos com a de produtos
            )
            pedidos = self.cursor.fetchall()  # Obtém todos os resultados da consulta
            for pedido in pedidos:
                print(f"Pedido ID: {pedido[0]}, Cliente: {pedido[1]}, Produto: {pedido[2]}")  # Imprime os detalhes do pedido
        except mysql.connector.Error as err:
            print(f"Erro ao listar pedidos: {err}")  # Mensagem de erro se ocorrer algum problema durante a listagem

    def fechar_conexao(self):
        self.cursor.close()  # Fecha o cursor
        self.conexao.close()  # Fecha a conexão com o banco de dados


def menu():
    sistema = SistemaEcommerce()  # Cria uma instância do sistema de e-commerce

    while True:
        print("\n1. Adicionar Produto")
        print("2. Excluir Produto")
        print("3. Fazer Pedido")
        print("4. Excluir Pedido")
        print("5. Listar Produtos")
        print("6. Listar Pedidos")
        print("7. Sair")
        escolha = input("Escolha uma opção: ")  # Solicita ao usuário que escolha uma opção do menu

        if escolha == "1":
            # Opção para adicionar produto
            print("\nInforme os detalhes do produto:")
            nome = input("Nome do produto: ")
            preco = float(input("Preço do produto: "))
            descricao = input("Descrição do produto: ")
            quantidade = int(input("Quantidade em estoque: "))

            novo_produto = Produto(nome, preco, descricao, quantidade)
            sistema.adicionar_produto(novo_produto)
            print(f"Produto '{nome}' adicionado com sucesso!")

        elif escolha == "2":
            id_produto = input("ID do Produto a ser excluído: ")  # Solicita o ID do produto a ser excluído
            sistema.excluir_produto(id_produto)  # Chama o método excluir_produto do sistema

        elif escolha == "3":
            nome_cliente = input("Nome do Cliente: ")  # Solicita o nome do cliente
            contato_cliente = input("Contato do Cliente: ")  # Solicita o contato do cliente
            endereco_cliente = input("Endereço do Cliente: ")  # Solicita o endereço do cliente
            cliente = Cliente(nome_cliente, contato_cliente, endereco_cliente)  # Cria um objeto Cliente
            cliente_id = sistema.adicionar_cliente(cliente)  # Adiciona o cliente ao sistema e obtém o ID do cliente

            if cliente_id is not None:
                sistema.listar_produtos()  # Lista os produtos disponíveis
                id_produto = input("ID do Produto desejado: ")  # Solicita o ID do produto desejado
                pedido = Pedido(cliente_id, id_produto)  # Cria um objeto Pedido
                sistema.adicionar_pedido(pedido)  # Adiciona o pedido ao sistema

        elif escolha == "4":
            id_pedido = input("ID do Pedido a ser excluído: ")  # Solicita o ID do pedido a ser excluído
            sistema.excluir_pedido(id_pedido)  # Chama o método excluir_pedido do sistema

        elif escolha == "5":
            sistema.listar_produtos(somente_disponiveis=True)  # Lista apenas os produtos disponíveis

        elif escolha == "6":
            sistema.listar_pedidos()  # Lista todos os pedidos

        elif escolha == "7":
            sistema.fechar_conexao()  # Fecha a conexão com o banco de dados e encerra o programa
            break  # Sai do loop while

        else:
            print("Opção inválida. Escolha novamente.")  # Mensagem se o usuário escolher uma opção inválida


menu()  # Inicia o programa chamando a função menu
