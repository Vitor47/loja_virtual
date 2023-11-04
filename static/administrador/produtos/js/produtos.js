$(document).ready(function () {
    $("#valor_produto").maskMoney({
        prefix: "R$:",
        decimal: ',', // Separador do decimal
        thousands:'.',
        length: 6,
        allowZero: false, // Permite que o digito 0 seja o primeiro caractere
        showSymbol: false // Exibe/Oculta o símbolo
    });
});

$(document).ready(function () {
    $("#desconto_produto").maskMoney({
        prefix: "R$:",
        decimal: ',', // Separador do decimal
        thousands:'.',
        length: 6,
        allowZero: false, // Permite que o digito 0 seja o primeiro caractere
        showSymbol: false // Exibe/Oculta o símbolo
    });
});

function readUrl(input) {
    if (input.files && input.files[0]) {
        let reader = new FileReader();
        reader.onload = (e) => {
            let imgData = e.target.result;
            let imgName = input.files[0].name;
            input.setAttribute("data-title", imgName);
            console.log(e.target.result);
        }
        reader.readAsDataURL(input.files[0]);
    }

}

$('.show_confirm').click(function (event) {
    var form = $(this).closest("form");
    var name = $(this).data("name");
    event.preventDefault();
    swal({
        title: "Atenção!",
        text: "Você deseja realmente excluir este item?",
        icon: "warning",
        buttons: true,
        dangerMode: true,
    })
        .then((willDelete) => {
            if (willDelete) {
                form.submit();
            }
            else {
                swal("Item não deletado!");
            }
        });
});

function DeleteImage(_id) {
    var id = _id
    swal({
        title: "Atenção!",
        text: "Você deseja realmente excluir esta imagem?",
        icon: "warning",
        buttons: true,
        dangerMode: true,
    })
        .then((willDelete) => {
            if (willDelete) {
                location.href = "/admin/delete_image_produto/" + id;
            }
            else {
                swal("Imagem não deletada!");
            }
        });
}

