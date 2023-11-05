$('.show_confirm').click(function (event) {
    var form = $(this).closest("form");
    var name = $(this).data("name");
    event.preventDefault();
    swal({
        title: "Atenção!",
        text: "Você deseja realmente excluir este grupo? Atenção se você deletar o grupo vai deletar todos os acessos adicionados a ele!",
        icon: "warning",
        buttons: true,
        dangerMode: true,
    })
        .then((willDelete) => {
            if (willDelete) {
                form.submit();
            }
            else {
                swal("Grupo não deletado!");
            }
        });
});