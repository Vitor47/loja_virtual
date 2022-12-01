import urllib.request
import re
from xml.dom import minidom
import time
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
        if cpf_reverso[i - 1:i] != str(dv_calculado % 10):
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
        if cnpj_r[i - 1:i] != str(dv % 10):
            return False

    return True

class Correios(object):
    def __init__(self):
        self.status = 'OK'

    def _getDados(self, tags_name, dom):
        dados = {}

        for tag_name in tags_name:
            try:
                dados[tag_name] = dom.getElementsByTagName(tag_name)[0]
                dados[tag_name] = dados[tag_name].childNodes[0].data
            except:
                dados[tag_name] = ''
                
        return dados

    def frete(self, cod, GOCEP, HERECEP, peso, formato,
              comprimento, altura, largura, diametro, mao_propria='N',
              valor_declarado='0', aviso_recebimento='N',
              empresa='', senha='', toback='xml'):

        base_url = "http://ws.correios.com.br/calculador/CalcPrecoPrazo.aspx"

        fields = [
            ('nCdEmpresa', empresa),
            ('sDsSenha', senha),
            ('nCdServico', cod),
            ('sCepOrigem', HERECEP),
            ('sCepDestino', GOCEP),
            ('nVlPeso', peso),
            ('nCdFormato', formato),
            ('nVlComprimento', comprimento),
            ('nVlAltura', altura),
            ('nVlLargura', largura),
            ('nVlDiametro', diametro),
            ('sCdMaoPropria', mao_propria),
            ('nVlValorDeclarado', valor_declarado),
            ('sCdAvisoRecebimento', aviso_recebimento),
            ('StrRetorno', toback),
        ]

        url = base_url + "?" + urllib.parse.urlencode(fields)
        dom = minidom.parse(urllib.request.urlopen(url))

        tags_name = ('MsgErro',
                     'Erro',
                     'Codigo',
                     'Valor',
                     'PrazoEntrega',
                     'ValorMaoPropria',
                     'ValorValorDeclarado',
                     'EntregaDomiciliar',
                     'EntregaSabado',)

        return tags_name, dom

    '''def cep(self, numero):
        url = 'http://cep.republicavirtual.com.br/web_cep.php?formato=' \
              'xml&cep=%s' % str(numero)
        dom = minidom.parse(urllib.request.urlopen(url))

        tags_name = ('uf',
                     'cidade',
                     'bairro',
                     'tipo_logradouro',
                     'logradouro',)

        resultado = dom.getElementsByTagName('resultado')[0]
        resultado = int(resultado.childNodes[0].data)
        if resultado != 0:
            return self._getDados(tags_name, dom)
        else:
            return {}'''

    '''def encomenda(self, numero):
        # Usado como referencia o codigo do Guilherme Chapiewski
        # https://github.com/guilhermechapiewski/correios-api-py

        url = 'http://websro.correios.com.br/sro_bin/txect01$.QueryList?' \
              'P_ITEMCODE=&P_LINGUA=001&P_TESTE=&P_TIPO=001&P_COD_UNI=%s' % \
              str(numero)

        html = urllib.request.urlopen(url).read()
        table = re.search(r'<table.*</TABLE>', html, re.S).group(0)

        parsed = BeautifulSoup(table)
        dados = []

        for count, tr in enumerate(parsed.table):
            if count > 4 and str(tr).strip() != '':
                if re.match(r'\d{2}/\d{2}/\d{4} \d{2}:\d{2}',
                            tr.contents[0].string):

                    dados.append({
                        'data': str(tr.contents[0].string),
                        'local': str(tr.contents[1].string),
                        'status': str(tr.contents[2].font.string)
                    })

                else:
                    dados[len(dados) - 1]['detalhes'] = str(
                        tr.contents[0].string)

        return dados'''

class GeraPix():
    def __init__(self) -> None:
        self.status = "OK"

        '''
            nome	Sim	Nome do recebedor.
            cidade	Sim	Cidade do recebedor.
            valor	Não	Valor do QrCode. Exemplo: 1200.99
            saida	Sim	Use br para string e qr para imagem.
            tamanho	Não	Define a altura do QrCode em pixels.
            txid	Não	Define um identificador pro Pix.
            chave	Sim	Chave Pix cadastrada em qualquer PSP.

            Exemplos:
            - Telefone: +5531912345678
            - CPF ou CNPJ: 01234567890
            - E-mail: teste@pix.com.br
            - Aleatória: 2aa96c40-d85f-4b98-b29f-d158a1c45f7f

            Exemplo -> nome=Cecília%20Devêza&cidade=Ouro%20Preto&valor=10.00&saida=qr&chave=2aa96c40-d85f-4b98-b29f-d158a1c45f7f&txid=testeCecilia
        '''

    def envia_dados(self, valor):
        base_url = "https://gerarqrcodepix.com.br/api/v1?"

        fields = [
            ('nome', 'Vitor Miolo'),
            ('cidade', 'Santa Maria'),
            ('valor', valor),
            ('saida', 'qr'),
            ('chave', '04992940099'),
            ('txid', 'testeVitor'),  
        ]

        url = base_url + urllib.parse.urlencode(fields)
        return url
