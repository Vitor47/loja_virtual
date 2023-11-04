$(document).ready(function () {
    function limpa_formulario_cep() {
        // Limpa valores do formulário de cep.
        $("#rua").val("");
        $("#bairro").val("");
        $("#cidade").val("");
        $("#uf").val("");
        $("#ibge").val("");
    }

    //Quando o campo cep perde o foco.
    $("#cep").blur(function () {

        //Nova variável "cep" somente com dígitos.
        var cep = $(this).val().replace(/\D/g, '');

        //Verifica se campo cep possui valor informado.
        if (cep != "") {

            //Expressão regular para validar o CEP.
            var validacep = /^[0-9]{8}$/;

            //Valida o formato do CEP.
            if (validacep.test(cep)) {

                //Preenche os campos com "..." enquanto consulta webservice.
                $("#rua").val("...");
                $("#bairro").val("...");
                $("#cidade").val("...");
                $("#uf").val("...");
                $("#ibge").val("...");

                //Consulta o webservice viacep.com.br/
                $.getJSON("https://viacep.com.br/ws/" + cep + "/json/?callback=?", function (dados) {

                    if (!("erro" in dados)) {
                        //Atualiza os campos com os valores da consulta.
                        $("#rua").val(dados.logradouro);
                        $("#bairro").val(dados.bairro);
                        $("#cidade").val(dados.localidade);
                        $("#uf").val(dados.uf);
                        $("#ibge").val(dados.ibge);
                    } //end if.
                    else {
                        //CEP pesquisado não foi encontrado.
                        limpa_formulario_cep();
                        swal({
                            title: "ERRO!",
                            text: "CEP não encontrado.",
                            icon: "error",
                            button: "OK",
                        })
                    }
                });
            } //end if.
            else {
                //cep é inválido.
                limpa_formulario_cep();
                swal({
                    title: "ERRO!",
                    text: "Formato de CEP inválido.",
                    icon: "error",
                    button: "OK",
                })
            }
        } //end if.
        else {
            //cep sem valor, limpa formulário.
            limpa_formulario_cep();
        }
    });
});

$(document).ready(function () {
    $('#telefone-create-conta').mask('(00) 00000-0000');
    $('#data-create-conta').mask('00/00/0000');
});

$('#cpfcnpj-create-conta').mask('000.000.000-00', {
    onKeyPress: function (cpfcnpj, e, field, options) {
        const masks = ['000.000.000-000', '00.000.000/0000-00'];
        const mask = (cpfcnpj.length > 14) ? masks[1] : masks[0];
        $('#cpfcnpj-create-conta').mask(mask, options);
    }
});

function verificaForcaSenha() {
    var numeros = /([0-9])/;
    var alfabeto = /([a-zA-Z])/;
    var chEspeciais = /([~,!,@,#,$,%,^,&,*,-,_,+,=,?,>,<])/;

    if ($('#senha-create-conta').val().length < 6) {
        $('#password-status').html("<span style='color:red'>Fraco, insira no mínimo 6 caracteres</span>");
    } else {
        if ($('#senha-create-conta').val().match(numeros) && $('#senha-create-conta').val().match(alfabeto) && $('#senha-create-conta').val().match(chEspeciais)) {
            $('#password-status').html("<span style='color:green'><b>Forte</b></span>");
        } else {
            $('#password-status').html("<span style='color:orange'>Médio, insira um caracter especial</span>");
        }
    }
}