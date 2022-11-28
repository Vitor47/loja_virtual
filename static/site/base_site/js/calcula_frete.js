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
                success: function (data) {
                    console.log(data);
                    if (data) {
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
                            $.each(data, function (index, data) {
                                html += '<p style="margin-top: 12px;"> Valor do frete: R$ ' + data['Valor'] + ', prazo de entrega: ' + data['PrazoEntrega'] + ' dias, entrega domiciliar: ' + data['EntregaDomiciliar'] + ' </p>';
                            });
                        }
                        $("#result-fret").html(html);
                    } else {
                        html += '<p style="margin-top: 12px;">Não possuei cobrança de frete para este cep.</p>';
                        $("#result-fret").html(html);
                    }

                    $('#img-reload').css('display', 'none');
                },
                error: function (data) {
                    swal({
                        title: "Opps!",
                        text: data.msg,
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