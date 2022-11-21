// Cria a função que recupera a lista do localStorage parseando a string
function getProdutos() {
    if (localStorage.getItem('produtos')) {
        return JSON.parse(localStorage.getItem('produtos'));
    }
    return [];
}

// adicona produtos ao carrinho
function adicionarProduto(produto) {
    var novaLista = getProdutos()
    novaLista.push(produto);

    localStorage.setItem('produtos', JSON.stringify(novaLista));
    montaCarrinho();
}

// manipula valor
function manipulaValor(valor, qtd) {
    return Number(valor.toString().replace(",", ".") * qtd).toFixed(2);
}

// funcao para adicionar produtos nos produtos e salvar em localStorage
function AddCarrinho(id, nome, imagem, qtd, valor) {
    event.preventDefault();

    adicionarProduto({ id, nome, imagem, qtd, valor: manipulaValor(valor, qtd) });

    swal({
        title: "SUCESSO!",
        text: "Produto adicionado ao carrinho com sucesso!",
        icon: "success",
        button: "OK",
    })

        .then((willSucess) => {
            if (willSucess) {
                ConteudoCarrinho();
                montaCarrinho();
            }
        });
}

function itemCarrinho(produto) {
    return `
        <div class="row">
            <div class="col-md-4">
                <div id="image-carrinho" style="background-image: url(/media/${produto.imagem}">
                    <span id="qtd-carrinho" class="quantidade-item-carrinho">${produto.qtd}</span>
                </div>
            </div>
            <div class="col-md-8">
                <div style="margin-top: 12px;">
                    <span style="font-size: 12px; color: var(--main-color); margin-right: 12px;" id="valor-carrinho">R\$ ${produto.valor}</span>
                    <span style="font-size: 12px; color: darkgrey;" id="nome-carrinho">${produto.nome}</span>
                </div>
            </div>
            <button class="remove-item-carrinho" type="button" onclick="deleteItemCarrinho(${produto.id})">X</button>
        </div>
    `;
}

function montaCarrinho() {
    $('#itens-carrinho').html('');
    getProdutos().slice(0, 3).forEach((produto) => {
        $('#itens-carrinho').append(itemCarrinho(produto));
    });
}

window.onload = ConteudoCarrinho();
function ConteudoCarrinho() {
        $("#conteudo-carrinho").html(`
            <div class="container-carrinho">
                <p>Meu carrinho </p>
                <div id="itens-carrinho"></div>
                <a class="btn btn-carrinho" href="/carrinho/"> Meu carrinho </a>
                <button class="btn btn-clear" type="button" onclick="clearCarrinho()"> Limpar carrinho </button>
            </div>
        `);
        montaCarrinho();
        $("#total-carrinho").html(getProdutos().length);
};

function deleteItemCarrinho(id) {
    swal({
        title: "OPS!",
        text: "Você realmente deseja remover este item do carrinho?",
        icon: "warning",
        buttons: true,
    })

        .then((willSucess) => {
            if (willSucess) {
                let products = getProdutos()
                const index = products.findIndex(produto => produto.id === parseInt(id));
                if (index > -1) {
                    products.splice(index, 1);
                    localStorage.setItem('produtos', JSON.stringify(products));
                }
                ConteudoCarrinho();
                montaCarrinho();
            }
        });
}

function clearCarrinho() {
    swal({
        title: "OPS!",
        text: "Você realmente deseja apagar todo o carrinho?",
        icon: "warning",
        buttons: true,
    })

        .then((willSucess) => {
            if (willSucess) {
                localStorage.clear();
                ConteudoCarrinho();
                montaCarrinho();
            }
        });
}