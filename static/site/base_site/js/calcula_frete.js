function SelectCategoria() {
    var slugCategoria = $("#categoria_slug").val();
    window.location.href = "/produtos?categoria_slug=" + slugCategoria;
}

$(document).ready(function () {
    $('#calcula-frete').mask('00000-000');
});

function CalcularFrete(id, slug, csrf_token) {
    var html = '';
    var _cep = $("#calcula-frete").val();
    if (_cep != "") {
        if (_cep.length == 9) {
            $('#img-reload').css('display', 'block');
            $("#img-reload").html('<img style="max-width: 24%;" src="/static/images/reload-gif.gif" alt="gif">');

            $.ajax({
                url: "/detalhes-produto/" + slug,
                type: "POST",
                dataType: "json",
                data: {
                    id_produto: id,
                    cep: _cep,
                },
                headers: {
                    "X-Requested-With": "XMLHttpRequest",
                    "X-CSRFToken": csrf_token,
                },
                success: (data) => {
                    if (data) {
                        $.each(data, function (index, data) {
                            if(data['MsgErro'].length > 0){
                                html += '<p style="margin-top: 12px;"> '+ data['MsgErro'] +' </p>';
                            }else{
                                html += '<p style="margin-top: 12px;"> Valor do frete: R$ ' + data['Valor'] + ', prazo de entrega: ' + data['PrazoEntrega'] + ' dias, entrega domiciliar: ' + data['EntregaDomiciliar'] + ' </p>';
                            }
                        });

                        $("#result-fret").html(html);
                    } else {
                        html += '<p style="margin-top: 12px;">Não possuei cobrança de frete para este cep.</p>';
                        $("#result-fret").html(html);
                    }

                    $('#img-reload').css('display', 'none');
                },
                error: (error) => {
                    swal({
                        title: "Opps!",
                        text: "Algum erro inesperado tente novamente.",
                        icon: "error",
                        button: "OK",
                    });
                    $('#img-reload').css('display', 'none');
                }
            });
        }
    }
    else {
        swal({
            title: "Opps!",
            text: "Preencha o CEP.",
            icon: "error",
            button: "OK",
        });
    }
}