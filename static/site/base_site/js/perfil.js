$(document).ready(function () {
    document.querySelector('#home-icon').classList.replace('box-selected', 'box-footer');
    document.querySelector('#conta-icon').classList.replace('box-footer', 'box-selected');
})

$(document).ready(function () {
    $('#expandir-menu').css('display', 'none');
    $('#expandir-menu-password').css('display', 'none');
    $('#icon-perfil-up').css('display', 'none');
    $('#icon-perfil-up-password').css('display', 'none');
})

function ExpandirMenu() {
    if ($("#expandir-menu").is(":hidden")) {
        $('#expandir-menu').css('display', 'block');
        $('#icon-perfil-down').css('display', 'none');
        $('#icon-perfil-up').css('display', 'block');
    } else {
        $('#expandir-menu').css('display', 'none');
        $('#icon-perfil-down').css('display', 'block');
        $('#icon-perfil-up').css('display', 'none');
    }
}

function ExpandirMenuPassword() {
    if ($("#expandir-menu-password").is(":hidden")) {
        $('#expandir-menu-password').css('display', 'block');
        $('#icon-perfil-down-password').css('display', 'none');
        $('#icon-perfil-up-password').css('display', 'block');
    } else {
        $('#expandir-menu-password').css('display', 'none');
        $('#icon-perfil-down-password').css('display', 'block');
        $('#icon-perfil-up-password').css('display', 'none');
    }
}

function openPopup(popup) {
	$(popup).show().attr("aria-hidden", "false");
	$("#closePopup").focus();
}

function closePopup(popup) {
	$(popup).hide().attr("aria-hidden", "true");
	$("#openMyPopup").focus();
}

function editAvatarPerfil(image, csrf_token) {
    $.ajax({
        url: "/perfil-site/",
        type: "POST",
        dataType: "json",
        data: {
            image: image,
        },
        headers: {
            "X-Requested-With": "XMLHttpRequest",
            "X-CSRFToken": csrf_token,
        },
        success: (data) => {
            swal({
                title: "Sucesso!",
                text: "Avatar alterado com sucesso.",
                icon: "success",
                button: "OK",
            })
            .then((willSucess) => {
                if (willSucess) {
                    location.reload();
                }
            });
        },
        error: (error) => {
            swal({
                title: "Opps!",
                text: "Algum erro inesperado tentar novamente!",
                icon: "error",
                button: "OK",
            });
        }
    });
}

$(document).ready(function () {
    $('#telefone').mask('(00) 00000-0000');
    $('#data_nascimento').mask('00/00/0000');
});

$('#cpf_cnpj').mask('000.000.000-00', {
    onKeyPress: function (cpfcnpj, e, field, options) {
        const masks = ['000.000.000-000', '00.000.000/0000-00'];
        const mask = (cpfcnpj.length > 14) ? masks[1] : masks[0];
        $('#cpf_cnpj').mask(mask, options);
    }
});

$(document).ready(function () {
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

function verificaForcaSenha() {
    var numeros = /([0-9])/;
    var alfabeto = /([a-zA-Z])/;
    var chEspeciais = /([~,!,@,#,$,%,^,&,*,-,_,+,=,?,>,<])/;

    if ($('#new_password').val().length < 6) {
        $('#password-status').html("<span style='color:red'>Fraco, insira no mínimo 6 caracteres</span>");
    } else {
        if ($('#new_password').val().match(numeros) && $('#new_password').val().match(alfabeto) && $('#new_password').val().match(chEspeciais)) {
            $('#password-status').html("<span style='color:green'><b>Forte</b></span>");
        } else {
            $('#password-status').html("<span style='color:orange'>Médio, insira um caracter especial</span>");
        }
    }
}