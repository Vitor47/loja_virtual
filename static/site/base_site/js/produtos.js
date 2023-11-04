$(document).ready(function () {
    document.getElementById("select-filter").style.display = 'none';
    document.getElementById("select-order").style.display = 'none';
});

function expandFilterCategory() {
    document.getElementById("select-filter").style.display = 'block';
    document.getElementById("select-order").style.display = 'none';
}

function expandFilterOrder() {
    document.getElementById("select-filter").style.display = 'none';
    document.getElementById("select-order").style.display = 'block';
}

function SelectCategoria() {
    var slugCategoria = $("#categoria_slug").val();
    window.location.href = "/produtos?categoria_slug=" + slugCategoria;
}

function SelectPreco() {
    var stringPreco = $("#valor").val();
    window.location.href = "/produtos?valor=" + stringPreco;
}