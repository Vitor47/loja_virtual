function AddCarrinho(id, produto, imagem, qtd, valor, posicao) {
    event.preventDefault();
    valor = valor.toString().replace(",", ".");
    valor = Number(valor * qtd).toFixed(2)
    valor = valor.toString().replace(".", ",");
    localStorage.setItem("id" + posicao, id);
    localStorage.setItem("produto" + posicao, produto);
    localStorage.setItem("imagem" + posicao, imagem);
    localStorage.setItem("qtd" + posicao, qtd);
    localStorage.setItem("valor" + posicao, valor);

    swal({
        title: "SUCESSO!",
        text: "Produto adicionado ao carrinho com sucesso!",
        icon: "success",
        button: "OK",
    })
    
    .then((willSucess) => {
        if (willSucess) {
            location.reload();
        }
    });
}

function deleteItemCarrinho(i){
    swal({
        title: "OPS!",
        text: "Você realmente deseja remover este item do carrinho?",
        icon: "warning",
        buttons: true,
    })

    .then((willSucess) => {
        if (willSucess) {
            localStorage.removeItem("id" + i);
            localStorage.removeItem("imagem" + i)
            localStorage.removeItem("qtd" + i) + " x ";
            localStorage.removeItem("produto" + i);
            localStorage.removeItem("valor" + i);
            location.reload();
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
            for (i = 1; i <= 4; i++) // verifica até 3 produtos registrados na localStorage
            {
                var prod = localStorage.getItem("produto" + i + ""); // verifica se há produto nesta posição. 
                if (prod != null) {
                    localStorage.clear();
                    location.reload();
                }
            }
        }
    });
}

var count = 0; // variável que retorna o total dos produtos que estão na LocalStorage.
var i = 0;     // variável que irá percorrer as posições
var valor = 0; // variável que irá receber o preço do produto convertido em Float.

for (i = 1; i <= 4; i++) // verifica até 3 produtos registrados na localStorage
{
    var prod = localStorage.getItem("produto" + i + ""); // verifica se há produto nesta posição. 
    if (prod != null) {
        // exibe os dados da lista dentro da div itens
        id = localStorage.getItem("id" + i);
        quantidade = localStorage.getItem("qtd" + i) + " x ";
        produto = localStorage.getItem("produto" + i);
        valor = "R$: " + localStorage.getItem("valor" + i);

        document.getElementById("itens-carrinho").innerHTML += '<div class="row">'
            + '<input type="hidden" value="' + id + '">'
            + '<div class="col-md-4"> '
            + '<div id="image-carrinho" style="background-image: url(' + '/media/' + localStorage.getItem("imagem" + i) + ');">'
            + '<span id="qtd-carrinho" class="quantidade-item-carrinho">' + quantidade + '</span>'
            + '</div>'
            + '</div>'
            + '<div class="col-md-8">'
            + '<div style="margin-top: 12px;"><span style="font-size: 12px; color: green; margin-right: 12px;" id="valor-carrinho">' + valor + '</span> <span style="font-size: 12px; color: darkgrey;" id="nome-carrinho">' + produto + '</span></div>'
            + '</div>'
            + '<button class="remove-item-carrinho" type="button" onclick="deleteItemCarrinho('+ i +')">X</button>'
            + '</div>';
        count++;
    }
}
document.getElementById("total-carrinho").innerHTML = count;  