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
            <td class="col-carrinho" data-label="Imagem"><img class="img-thumbnail" src="/media/${produto.imagem}"></td>
            <td class="col-carrinho" data-label="Produto">${produto.nome}</td>
            <td class="col-carrinho" data-label="Quantidade">
                <div class="display-count-carrinho">
                    <input type="text" class="form-count" name="calculator_${produto.id}" id="calculator_${produto.id}" value="${produto.qtd}">

                    <div class="display-count-button" role="group" aria-label="plus-minus">
                        <button type="button" onClick="Calculator(${parseInt(produto.qtd) + 1}, ${produto.id})" class="btn-count" data-dir="up" id="up">
                            +
                        </button>
                        <button type="button" onClick="Calculator(${parseInt(produto.qtd) - 1}, ${produto.id})" class="btn-count" data-dir="dwn" id="dwn">
                            -
                        </button>
                    </div>
                </div>
            </td>
            <td class="col-carrinho" data-label="Valor da unidade">R\$ ${produto.valor}</td>
            <td class="col-carrinho" data-label="Valor final">R\$ ${produto.valor * produto.qtd}</td>
        </tr>
    `;
}

function reloadGif() {
    return $('#loading').show();
}

// percorre o array montando os itens
window.onload = montaTable();
function montaTable() {
    reloadGif();

    $('#table-carrinho').html('');
    getProdutos().slice(0, 10).forEach((produto) => {
        $('#table-carrinho').append(itemTable(produto));
    });

    $('#loading').hide();
}

function Calculator(qtd, id) {
    editItemCarrinho(qtd, id);
}

$(document).on('click', '.display-count-carrinho button', function () {
    var btn = $(this),
        oldValue = btn.closest('.display-count-carrinho').find('input').val().trim(),
        newVal = 0;
    if (btn.attr('data-dir') == 'up') {
        newVal = parseInt(oldValue) + 1;
    } else {
        if (oldValue > 1) {
            newVal = parseInt(oldValue) - 1;
        } else {
            newVal = 0;
        }
    }
    btn.closest('.display-count-carrinho').find('input').val(newVal);
});

function formataQtdValor(valor, qtd_produto, qtd){
    if (qtd == 0){
        return valor
    }
    else if(qtd_produto <= qtd) {
        return valor * qtd
    }else{
        return valor / qtd
    }
}

function editItemCarrinho(qtd, id) {
    let products = getProdutos().filter(produto => produto.id !== id);

    products.forEach(function(produto) {
        produto.id = id,
        produto.nome = produto.nome,
        produto.imagem = produto.imagem,
        produto.qtd = qtd,
        produto.valor = formataQtdValor(produto.valor, produto.qtd, qtd)
      });

    localStorage.setItem('produtos', JSON.stringify(products));
    montaTable();
}