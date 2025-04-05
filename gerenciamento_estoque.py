import mysql.connector
from datetime import datetime

class Estoque:
    def __init__(self, host, usuario, senha, banco):
        # Conectar ao banco de dados MySQL
        self.conexao = mysql.connector.connect(
            host=host,
            user=usuario,
            password=senha,
            database=banco
        )
        self.cursor = self.conexao.cursor()

    # Método para cadastrar um produto
    def cadastrar_produto(self, nome, quantidade, preco):
        query = "INSERT INTO produtos (nome, quantidade, preco) VALUES (%s, %s, %s)"
        valores = (nome, quantidade, preco)
        self.cursor.execute(query, valores)
        self.conexao.commit()
        print(f"Produto {nome} cadastrado com sucesso.")

    # Método para consultar todos os produtos
    def consultar_produtos(self):
        self.cursor.execute("SELECT * FROM produtos")
        produtos = self.cursor.fetchall()
        for produto in produtos:
            print(produto)

    # Método para atualizar um produto
    def atualizar_produto(self, id_produto, nome=None, quantidade=None, preco=None):
        query = "UPDATE produtos SET "
        valores = []

        if nome:
            query += "nome = %s, "
            valores.append(nome)
        if quantidade is not None:
            query += "quantidade = %s, "
            valores.append(quantidade)
        if preco is not None:
            query += "preco = %s, "
            valores.append(preco)

        query = query.rstrip(", ")  # Remove a vírgula extra no final
        query += " WHERE id = %s"
        valores.append(id_produto)

        self.cursor.execute(query, tuple(valores))
        self.conexao.commit()
        print(f"Produto {id_produto} atualizado com sucesso.")

    # Método para remover um produto
    def remover_produto(self, id_produto):
        query = "DELETE FROM produtos WHERE id = %s"
        self.cursor.execute(query, (id_produto,))
        self.conexao.commit()
        print(f"Produto {id_produto} removido com sucesso.")

    # Método para registrar uma venda e ajustar o estoque
    def registrar_venda(self, produto_id, quantidade_vendida):
        # Consultar a quantidade disponível no estoque
        self.cursor.execute("SELECT quantidade FROM produtos WHERE id = %s", (produto_id,))
        estoque_atual = self.cursor.fetchone()

        if estoque_atual:
            estoque_atual = estoque_atual[0]
            if estoque_atual >= quantidade_vendida:
                # Reduzir a quantidade do produto no estoque
                nova_quantidade = estoque_atual - quantidade_vendida
                self.cursor.execute(
                    "UPDATE produtos SET quantidade = %s WHERE id = %s", 
                    (nova_quantidade, produto_id)
                )
                
                # Registrar a venda na tabela vendas
                data_venda = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                self.cursor.execute(
                    "INSERT INTO vendas (produto_id, quantidade_vendida, data_venda) VALUES (%s, %s, %s)", 
                    (produto_id, quantidade_vendida, data_venda)
                )

                self.conexao.commit()
                print(f"Venda registrada com sucesso! Produto ID: {produto_id}, Quantidade: {quantidade_vendida}")
            else:
                print("Quantidade insuficiente no estoque para realizar a venda.")
        else:
            print(f"Produto ID {produto_id} não encontrado no estoque.")

    def fechar_conexao(self):
        self.cursor.close()
        self.conexao.close()


# Exemplo de uso da classe
estoque = Estoque("localhost", "root", "senha", "estoque_vendas")

# Cadastrar um produto
estoque.cadastrar_produto("Produto A", 100, 29.99)

# Consultar todos os produtos
estoque.consultar_produtos()

# Registrar uma venda (produto_id = 1, quantidade_vendida = 10)
estoque.registrar_venda(1, 10)

# Consultar os produtos após a venda
estoque.consultar_produtos()

# Fechar a conexão
estoque.fechar_conexao()
