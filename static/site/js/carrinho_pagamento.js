$(document).ready(function () {
    document.querySelector('#home-icon').classList.replace('box-selected', 'box-footer');
    document.querySelector('#carrinho').classList.replace('box-footer', 'box-selected');
})

// Cria a função que recupera a lista do localStorage parseando a string
function getProdutos() {
    if (localStorage.getItem('produtos')) {
        return JSON.parse(localStorage.getItem('produtos'));
    }
    return [];
}

function fazerCheckout() {
    const produtos = getProdutos();
    const produtosquery = produtos.map((produto) => ({ id: produto.id, qtd: produto.qtd }));

    $.ajax({
        url: "/pagamento-carrinho/",
        type: "POST",
        data: { 'produtos': JSON.stringify(produtosquery) },
        success: function (response) {
            if (response.msg) {
                if (response.msg.length > 0) {
                    swal({
                        title: "Opps!",
                        text: response.msg,
                        icon: "error",
                        button: "OK",
                    });
                }
            }
            else if (response) {
                $.each(response, function (index, response) {
                    montaTable(response.produtos);
                });
            }
        },
        error: function (response) {
            swal({
                title: "Opps!",
                text: "Algum erro inesperado tente novamente.",
                icon: "error",
                button: "OK",
            });
        }
    });
}


// monta item por item do array
function itemTable(produto) {
    return `
        <tr class="list-group-item">
            <td class="col-carrinho" data-label="Imagem"><img class="img-thumbnail" src="/media/${produto.imagem_pricipal}"></td>
            <td class="col-carrinho" data-label="Produto">${produto.nome}</td>
            <td class="col-carrinho" data-label="Quantidade">${produto.qtd}</td>
            <td class="col-carrinho" data-label="Valor da unidade">R\$ ${produto.valor}</td>
            <td class="col-carrinho" data-label="Valor final">R\$ ${(Number(produto.valor) * Number(produto.qtd)).toFixed(2)}</td>
        </tr>
    `;
}

// gif de reload table
function reloadGif() {
    return $('#loading').show();
}

//monta a tabela com os itens salvos em localStorage
function montaTable(produto) {
    reloadGif();

    $('#table-carrinho-compra').html('');
    getProdutos().slice(0, 10).forEach((produto) => {
        $('#table-carrinho-compra').append(itemTable(produto));
    });

    $('#loading').hide();
}

window.onload = fazerCheckout();

//gera QR CODE para pagamento
function GerarQrCode() {
    const produtos = getProdutos();
    const produtosquery = produtos.map((produto) => ({ id: produto.id, qtd: produto.qtd }));

    $.ajax({
        url: "/gerar-pagamento/",
        type: "POST",
        data: { 'produtos': JSON.stringify(produtosquery) },
        success: function (response) {
            if (response.msg) {
                if (response.msg.length > 0) {
                    swal({
                        title: "Opps!",
                        text: response.msg,
                        icon: "error",
                        button: "OK",
                    });
                }
            }
            else if (response) {
                $('#table-pagamento').html('');
                $('#btn-pagamento').html('');
                $('#column-img-pix').html(
                    `
                        <p>Informações importantes, após pagamento efetuado a loja imediatamente enviara a encomenda via correios, ou conforme escolhido na opção de entrega.</p>
                        <p>Leia o QR CODE abaixo para realizar o pagamento!</p>
                        <img src="${response.img}">
                    `
                )
            }
        },
        error: function (response) {
            swal({
                title: "Opps!",
                text: "Algum erro inesperado tente novamente.",
                icon: "error",
                button: "OK",
            });
        }
    });
}