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

// monta item por item do array
function itemTable(produto) {
    return `
        <tr class="list-group-item">
            <td class="col-carrinho" data-label="Imagem"><img class="img-thumbnail" src="/media/${produto.imagem_pricipal}"></td>
            <td class="col-carrinho" data-label="Produto">${produto.nome}</td>
            <td class="col-carrinho" data-label="Quantidade">
                <div class="display-count-carrinho">
                    <div class="text-count">${produto.qtd} </div>
                    <div class="display-count-button" role="group" aria-label="plus-minus">
                        <button type="button" onClick="aumentaQuantidade('${produto.id}')" class="btn-count" data-dir="up" id="up">
                            +
                        </button>
                        <button type="button" onClick="diminuiQuantidade('${produto.id}')" class="btn-count" data-dir="dwn" id="dwn">
                            -
                        </button>
                    </div>
                </div>
            </td>
            <td class="col-carrinho" data-label="Valor da unidade">R\$ ${produto.valor}</td>
            <td class="col-carrinho" data-label="Valor final">R\$ ${(Number(produto.valor) * Number(produto.qtd)).toFixed(2)}</td>
            <td class="col-carrinho" data-label="Quantidade"><button class="btn btn-danger" type="button" onclick="deletarItem(${produto.id})"><i class="fa fa-trash"></i></td>
        </tr>
    `;
}

function reloadGif() {
    return $('#loading').show();
}

function OrderBy(pessoas) {

}


function montaTable() {
    reloadGif();
    $('#table-carrinho').html('');

    produtos = getProdutos().sort(function (a, b) {
        if (a.id < b.id) {
            return -1;
        } else {
            return true;
        }
    });

    produtos.slice(0, 10).forEach((produto) => {
        $('#table-carrinho').append(itemTable(produto));
    });

    $('#loading').hide();
}

function aumentaQuantidade(id) {
    atualizaQtdProduto(id, 'aumenta')
}

function diminuiQuantidade(id) {
    atualizaQtdProduto(id, 'diminui')
}

function atualizaQtdProduto(id, opcao) {
    const produto = getProdutos().filter(produto => Number(produto.id) === Number(id))[0];
    if (opcao === 'diminui' && (produto.qtd - 1) < 1) {
        return;
    }
    const novoProduto = { ...produto, qtd: opcao === 'aumenta' ? Number(produto.qtd) + 1 : Number(produto.qtd) - 1 };

    const products = getProdutos().filter(produto => Number(produto.id) !== Number(id));
    products.push(novoProduto);

    localStorage.setItem('produtos', JSON.stringify(products));
    montaTable();
    ConteudoCarrinho();
}

function deletarItem(id) {
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
                montaTable();
            }
        });
}

// percorre o array montando os itens
window.onload = montaTable();