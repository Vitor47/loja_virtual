$('.show_confirm').click(function (event) {
    var form = $(this).closest("form");
    var name = $(this).data("name");
    event.preventDefault();
    swal({
        title: "Atenção!",
        text: "Você deseja realmente excluir este usuário?",
        icon: "warning",
        buttons: true,
        dangerMode: true,
    })
        .then((willDelete) => {
            if (willDelete) {
                form.submit();
            }
            else {
                swal("Usuário não deletado!");
            }
        });
});

function verificaForcaSenha() {
    var numeros = /([0-9])/;
    var alfabeto = /([a-zA-Z])/;
    var chEspeciais = /([~,!,@,#,$,%,^,&,*,-,_,+,=,?,>,<])/;

    if ($('#senha_user').val().length < 6) {
        $('#password-status').html("<span style='color:red'>Fraco, insira no mínimo 6 caracteres</span>");
    } else {
        if ($('#senha_user').val().match(numeros) && $('#senha_user').val().match(alfabeto) && $('#senha_user').val().match(chEspeciais)) {
            $('#password-status').html("<span style='color:green'><b>Forte</b></span>");
        } else {
            $('#password-status').html("<span style='color:orange'>Médio, insira um caracter especial</span>");
        }
    }
}