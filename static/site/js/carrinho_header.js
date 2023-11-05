// Cria a função que recupera a lista do localStorage parseando a string
function getProdutos() {
    if (localStorage.getItem('produtos')) {
        return JSON.parse(localStorage.getItem('produtos'));
    }
    return [];
}

// adicona produtos ao carrinho
function adicionarProduto(data) {
    const products = getProdutos().filter(produto => Number(produto.id) === Number(data['id']));
    if (products.length === 0) {
        var novaLista = getProdutos();
        novaLista.push(data);

        localStorage.setItem('produtos', JSON.stringify(novaLista));
        ConteudoCarrinho()
        montaCarrinho();

        swal({
            title: "Sucesso!",
            text: "Produto adcionado ao carrinho com sucesso!",
            icon: "success",
            button: "OK",
        });

    } else {
        swal({
            title: "Opps!",
            text: "Este produto já existe no carrinho.",
            icon: "error",
            button: "OK",
        });
    }
}

// funcao para adicionar produtos nos produtos e salvar em localStorage
function AddCarrinho(id, qtd) {
    event.preventDefault();

    $("#comprar_" + id).addClass("m-progress");
    $.ajax({
        url: "/adiciona-carrinho/",
        type: "POST",
        dataType: "json",
        data: {
            id_produto: id,
            qtd: qtd,
        },
        headers: {
            "X-Requested-With": "XMLHttpRequest",
        },
        success: function (data) {
            if (data.msg) {
                if (data.msg.length > 0) {
                    swal({
                        title: "Opps!",
                        text: data.msg,
                        icon: "error",
                        button: "OK",
                    });
                }
            }
            else if (data) {
                adicionarProduto({ id: data['id'], nome: data['nome'], imagem_pricipal: data['imagem_principal'], qtd: Number(qtd), valor: data['valor'] });
            }
        },
        error: function (data) {
            swal({
                title: "Opps!",
                text: "Algum erro inesperado tente novamente.",
                icon: "error",
                button: "OK",
            });
        }
    });

    $("#comprar_" + id).removeClass("m-progress");
    ConteudoCarrinho();
    montaCarrinho();
}

function itemCarrinho(produto) {
    return `
        <div class="row">
            <div class="col-md-4">
                <div id="image-carrinho" style="background-image: url(/media/${produto.imagem_pricipal}">
                    <span id="qtd-carrinho" class="quantidade-item-carrinho">${produto.qtd}</span>
                </div>
            </div>
            <div class="col-md-8">
                <div style="margin-top: 12px;">
                    <span style="font-size: 12px; color: var(--main-color); margin-right: 12px;" id="valor-carrinho">R\$ ${parseInt(produto.valor * produto.qtd).toFixed(2)} </span>
                    <span style="font-size: 12px; color: darkgrey;" id="nome-carrinho">${produto.nome}</span>
                </div>
            </div>
            <button class="remove-item-carrinho" type="button" onclick="deleteItemCarrinho('${produto.id}')">X</button>
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
    $("#span-value").html(`
        <p class="value-carrinho-mobile">${getProdutos().length}</p>
    `)
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
                const products = getProdutos().filter(produto => Number(produto.id) !== Number(id));
                localStorage.setItem('produtos', JSON.stringify(products));
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
                location.reload();
            }
        });
}