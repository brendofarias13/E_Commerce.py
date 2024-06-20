const BASE_URL = 'http://localhost:5000/api'; // Atualize com o endereço do seu servidor Flask

function adicionarProduto() {
    const produto = {
        nome: "Camisa",
        preco: 30.00,
        descricao: "camisa de algodão",
        quantidade: 9
    };

    fetch(`${BASE_URL}/adicionar_produto`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(produto),
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message); // Exibe a mensagem de sucesso ou erro retornada pelo servidor
    })
    .catch(error => {
        console.error('Erro:', error);
    });
}

function excluirProduto() {
    const idProduto = prompt("Digite o ID do produto a ser excluído:");
    if (idProduto) {
        fetch(`${BASE_URL}/excluir_produto/${idProduto}`, {
            method: 'DELETE',
        })
        .then(response => response.json())
        .then(data => {
            alert(data.message); // Exibe a mensagem de sucesso ou erro retornada pelo servidor
        })
        .catch(error => {
            console.error('Erro:', error);
        });
    }
}

function fazerPedido() {
    const nomeCliente = prompt("Digite o nome do cliente:");
    const contatoCliente = prompt("Digite o contato do cliente:");
    const enderecoCliente = prompt("Digite o endereço do cliente:");

    // Primeiro, adicionamos o cliente
    const cliente = {
        nome: nomeCliente,
        contato: contatoCliente,
        endereco: enderecoCliente
    };

    fetch(`${BASE_URL}/adicionar_cliente`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(cliente),
    })
    .then(response => response.json())
    .then(data => {
        const clienteId = data.cliente_id;
        if (clienteId) {
            // Após adicionar o cliente, fazemos o pedido
            listarProdutos(); // Implemente a lógica para listar os produtos disponíveis
            const idProduto = prompt("Digite o ID do produto desejado:");
            if (idProduto) {
                const pedido = {
                    cliente_id: clienteId,
                    produto_id: parseInt(idProduto)
                };

                fetch(`${BASE_URL}/adicionar_pedido`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(pedido),
                })
                .then(response => response.json())
                .then(data => {
                    alert(data.message); // Exibe a mensagem de sucesso ou erro retornada pelo servidor
                })
                .catch(error => {
                    console.error('Erro:', error);
                });
            }
        }
    })
    .catch(error => {
        console.error('Erro:', error);
    });
}

function excluirPedido() {
    const idPedido = prompt("Digite o ID do pedido a ser excluído:");
    if (idPedido) {
        fetch(`${BASE_URL}/excluir_pedido/${idPedido}`, {
            method: 'DELETE',
        })
        .then(response => response.json())
        .then(data => {
            alert(data.message); // Exibe a mensagem de sucesso ou erro retornada pelo servidor
        })
        .catch(error => {
            console.error('Erro:', error);
        });
    }
}

function listarProdutos() {
    fetch(`${BASE_URL}/listar_produtos`)
    .then(response => response.json())
    .then(produtos => {
        // Aqui você pode manipular os dados dos produtos, por exemplo, exibir em uma lista na interface
        console.log(produtos); // Exemplo de como você pode lidar com os produtos retornados
    })
    .catch(error => {
        console.error('Erro:', error);
    });
}

function listarPedidos() {
    fetch(`${BASE_URL}/listar_pedidos`)
    .then(response => response.json())
    .then(pedidos => {
        // Aqui você pode manipular os dados dos pedidos, por exemplo, exibir em uma lista na interface
        console.log(pedidos); // Exemplo de como você pode lidar com os pedidos retornados
    })
    .catch(error => {
        console.error('Erro:', error);
    });
}
