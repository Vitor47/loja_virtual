import urllib.request
from xml.dom import minidom
from itertools import cycle

TAMANHO_CPF = 11


def is_cpf_valido(cpf: str) -> bool:
    if len(cpf) != TAMANHO_CPF:
        return False

    if cpf in (c * TAMANHO_CPF for c in "1234567890"):
        return False

    cpf_reverso = cpf[::-1]
    for i in range(2, 0, -1):
        cpf_enumerado = enumerate(cpf_reverso[i:], start=2)
        dv_calculado = sum(map(lambda x: int(x[1]) * x[0], cpf_enumerado)) * 10 % 11
        if cpf_reverso[i - 1 : i] != str(dv_calculado % 10):
            return False

    return True


LENGTH_CNPJ = 14


def is_cnpj_valido(cnpj: str) -> bool:
    if len(cnpj) != LENGTH_CNPJ:
        return False

    if cnpj in (c * LENGTH_CNPJ for c in "1234567890"):
        return False

    cnpj_r = cnpj[::-1]
    for i in range(2, 0, -1):
        cnpj_enum = zip(cycle(range(2, 10)), cnpj_r[i:])
        dv = sum(map(lambda x: int(x[1]) * x[0], cnpj_enum)) * 10 % 11
        if cnpj_r[i - 1 : i] != str(dv % 10):
            return False

    return True


class Correios(object):
    def __init__(self):
        self.status = "OK"

    def _getDados(self, tags_name, dom):
        dados = {}

        for tag_name in tags_name:
            try:
                dados[tag_name] = dom.getElementsByTagName(tag_name)[0]
                dados[tag_name] = dados[tag_name].childNodes[0].data
            except:
                dados[tag_name] = ""

        return dados

    def frete(
        self,
        cod,
        GOCEP,
        HERECEP,
        peso,
        formato,
        comprimento,
        altura,
        largura,
        diametro,
        mao_propria="N",
        valor_declarado="0",
        aviso_recebimento="N",
        empresa="",
        senha="",
        toback="xml",
    ):
        base_url = "http://ws.correios.com.br/calculador/CalcPrecoPrazo.aspx"

        fields = [
            ("nCdEmpresa", empresa),
            ("sDsSenha", senha),
            ("nCdServico", cod),
            ("sCepOrigem", HERECEP),
            ("sCepDestino", GOCEP),
            ("nVlPeso", peso),
            ("nCdFormato", formato),
            ("nVlComprimento", comprimento),
            ("nVlAltura", altura),
            ("nVlLargura", largura),
            ("nVlDiametro", diametro),
            ("sCdMaoPropria", mao_propria),
            ("nVlValorDeclarado", valor_declarado),
            ("sCdAvisoRecebimento", aviso_recebimento),
            ("StrRetorno", toback),
        ]

        url = base_url + "?" + urllib.parse.urlencode(fields)
        dom = minidom.parse(urllib.request.urlopen(url))

        tags_name = (
            "MsgErro",
            "Erro",
            "Codigo",
            "Valor",
            "PrazoEntrega",
            "ValorMaoPropria",
            "ValorValorDeclarado",
            "EntregaDomiciliar",
            "EntregaSabado",
        )

        return tags_name, dom


class GeraPix:
    def __init__(self) -> None:
        self.status = "OK"

    def envia_dados(self, valor):
        base_url = "https://gerarqrcodepix.com.br/api/v1?"

        fields = [
            ("nome", ""),
            ("cidade", ""),
            ("valor", valor),
            ("saida", "qr"),
            ("chave", ""),
            ("txid", ""),
        ]

        url = base_url + urllib.parse.urlencode(fields)
        return url
