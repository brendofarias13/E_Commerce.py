from flask import Flask, render_template, request, redirect, url_for
from E_Commerce import SistemaEcommerce, Produto, Pedido, Cliente

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        nome = request.form['nome']
        preco = float(request.form['preco'])
        descricao = request.form['descricao']
        quantidade = int(request.form['quantidade'])
        imagem = request.form['imagem']  # Adicionar o campo de imagem

        novo_produto = Produto(nome, preco, descricao, quantidade, imagem)
        sistema = SistemaEcommerce()
        sistema.adicionar_produto(novo_produto)
        sistema.fechar_conexao()
        return redirect(url_for('index'))
    return render_template('add_product.html')


@app.route('/delete_product', methods=['GET', 'POST'])
def delete_product():
    if request.method == 'POST':
        id_produto = int(request.form['id_produto'])
        sistema = SistemaEcommerce()
        sistema.excluir_produto(id_produto)
        sistema.fechar_conexao()
        return redirect(url_for('index'))
    return render_template('delete_product.html')


@app.route('/place_order', methods=['GET', 'POST'])
def place_order():
    if request.method == 'POST':
        nome_cliente = request.form['nome_cliente']
        contato_cliente = request.form['contato_cliente']
        endereco_cliente = request.form['endereco_cliente']
        produto_id = int(request.form['produto_id'])

        novo_cliente = Cliente(nome_cliente, contato_cliente, endereco_cliente)
        sistema = SistemaEcommerce()
        cliente_id = sistema.adicionar_cliente(novo_cliente)
        if cliente_id is not None:
            novo_pedido = Pedido(cliente_id, produto_id)
            sistema.adicionar_pedido(novo_pedido)
        sistema.fechar_conexao()
        return redirect(url_for('index'))

    sistema = SistemaEcommerce()
    produtos = sistema.listar_produtos_disponiveis()
    sistema.fechar_conexao()
    return render_template('place_order.html', produtos=produtos)


@app.route('/view_orders')
def view_orders():
    sistema = SistemaEcommerce()
    pedidos = sistema.listar_pedidos()
    sistema.fechar_conexao()
    return render_template('view_orders.html', pedidos=pedidos)


@app.route('/view_products')
def view_products():
    sistema = SistemaEcommerce()
    query = "SELECT id, nome, preco, descricao, quantidade, imagem FROM produtos"
    sistema.cursor.execute(query)
    produtos = sistema.cursor.fetchall()
    sistema.fechar_conexao()
    return render_template('view_products.html', produtos=produtos)


if __name__ == '__main__':
    app.run(debug=True)
