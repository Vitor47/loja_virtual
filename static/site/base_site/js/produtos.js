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