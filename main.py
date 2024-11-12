import os
import shutil
import requests
import xml.etree.ElementTree as ET
from datetime import datetime
from api import api
from time import sleep


class XML:
    def __init__(self):
        self.filiais = {
            '33890542000136': '1',
            '33890542000217': '2',
            '33890542000306': '3',
            '33890542000560': '4',
            '33890542000640': '5',
            '33890542000721': '6',
            '33890542000802': '7',
            '33890542000993': '11',
            '33890542001108': '12',
            '33890542001027': '13',
        }

    def localizar(self, xml, caminho, atributo=None):
        self.tree = ET.parse(xml)
        self.root = self.tree.getroot()
        ns = {'nfe': 'http://www.portalfiscal.inf.br/nfe'}
        elemento = self.root.find(caminho, namespaces=ns)
        if elemento is not None:
            if atributo:
                return elemento.attrib.get(atributo)
            else:
                return elemento.text
        return None

    def consultar_cnpj(self, cnpj):
        url = f"https://brasilapi.com.br/api/cnpj/v1/{cnpj}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            return "Erro na consulta"

    def coletar_dados_nfe(self, xml):
        ## Dados Emitente
        self.cnpj_emitente = self.localizar(xml, './/nfe:emit/nfe:CNPJ')
        self.ie_emitente = self.localizar(xml, './/nfe:emit/nfe:IE')
        self.nome_emitente = self.localizar(xml, './/nfe:emit/nfe:xNome')
        self.uf_emitente = self.localizar(xml, './/nfe:emit/nfe:enderEmit/nfe:UF')
        self.municipio_emitente = self.localizar(xml, './/nfe:emit/nfe:enderEmit/nfe:xMun')
        self.cod_municipio_emitente = self.localizar(xml, './/nfe:emit/nfe:enderEmit/nfe:cMun')

        ## Dados Destinatário
        self.cnpj_destinatario = self.localizar(xml, './/nfe:dest/nfe:CNPJ')

        ## Seta a filial
        self.filial = self.filiais.get(self.cnpj_destinatario, 'Filial não encontrada')
        self.cnpj_emitente = f"{self.cnpj_emitente[:2]}.{self.cnpj_emitente[2:5]}.{self.cnpj_emitente[5:8]}/{self.cnpj_emitente[8:12]}-{self.cnpj_emitente[12:14]}"

        ## Cod fornecedor
        resultado = api('GET', f"SELECT CODCLIFOR FROM RODCLI WHERE CODCGC = '{self.cnpj_emitente}'")
        if resultado:
            self.cod_forn = resultado[0]['CODCLIFOR']
        else:
            self.cod_forn = None
        
        self.produtos = []
        self.valor_total_desconto = 0.0
        for produto in self.root.findall('.//nfe:det', namespaces={'nfe': 'http://www.portalfiscal.inf.br/nfe'}):
            vDesc = produto.find('.//nfe:vDesc', namespaces={'nfe': 'http://www.portalfiscal.inf.br/nfe'})
            valor_desc = float(vDesc.text) if vDesc is not None else 0.00
            self.valor_total_desconto += valor_desc
            self.produto = {
                'codigo': produto.find('.//nfe:cProd', namespaces={'nfe': 'http://www.portalfiscal.inf.br/nfe'}).text,
                'descricao': produto.find('.//nfe:xProd', namespaces={'nfe': 'http://www.portalfiscal.inf.br/nfe'}).text,
                'quantidade': produto.find('.//nfe:qCom', namespaces={'nfe': 'http://www.portalfiscal.inf.br/nfe'}).text,
                'unidade': produto.find('.//nfe:uCom', namespaces={'nfe': 'http://www.portalfiscal.inf.br/nfe'}).text,
                'valor_unitario': produto.find('.//nfe:vUnCom', namespaces={'nfe': 'http://www.portalfiscal.inf.br/nfe'}).text,
                'valor_total': produto.find('.//nfe:vProd', namespaces={'nfe': 'http://www.portalfiscal.inf.br/nfe'}).text,
                'valor_desc': valor_desc
            }
            self.produtos.append(self.produto)

        ## Observação
        self.observacao = self.localizar(xml, './/nfe:infAdic/nfe:infCpl')

        self.numero_nfe = self.localizar(xml, './/nfe:ide/nfe:nNF')

        self.chave_nfe = self.localizar(xml, './/nfe:infNFe', 'Id')
        if self.chave_nfe:
            self.chave_nfe = self.chave_nfe.replace('NFe', '')
        else:
            self.chave_nfe = None
        self.serie_nfe = self.localizar(xml, './/nfe:ide/nfe:serie')
        self.data_emissao = self.localizar(xml, './/nfe:ide/nfe:dhEmi')
        # se a data de emissao for diferente de 03:00 (horário de Brasília), converte para o horário de Brasília
        if self.data_emissao[-6:] != '-03:00':
            data = datetime.strptime(self.data_emissao, '%Y-%m-%dT%H:%M:%S-%H:%M')
            data = data.replace(hour=3)
            self.data_emissao = data.strftime('%Y-%m-%dT%H:%M:%S-03:00')
        self.valor_nfe = self.localizar(xml, './/nfe:total/nfe:ICMSTot/nfe:vNF')

        dados_nfe = {
            "NF-e": {
                "Filial": self.filial,
                "Número": self.numero_nfe,
                "Série": self.serie_nfe,
                "Chave": self.chave_nfe,
                "Data de Emissão": self.data_emissao,
                "Valor Total": f'{self.valor_nfe}',
                "Referencia": f'{self.observacao[:200]}'
            },
            "Emitente": {
                "CNPJ": self.cnpj_emitente,
                "IE": self.ie_emitente,
                "Nome": self.nome_emitente,
                "UF": self.uf_emitente,
                "Município": self.municipio_emitente,
                "Cód. Município": self.cod_municipio_emitente,
                "Cód. Fornecedor": f'{self.cod_forn}' if self.cod_forn else 'Fornecedor não encontrado'
            },
            "Destinatário": {
                "CNPJ": self.cnpj_destinatario,
            },
            "Produtos": self.produtos,
        }
        return dados_nfe


def processar_xmls(diretorio, pasta_lancadas, pasta_erros, update_progress=None, update_text=None):  
    if not os.path.exists(pasta_lancadas):
        os.makedirs(pasta_lancadas)

    if not os.path.exists(pasta_erros):
        os.makedirs(pasta_erros)

    arquivos = [f for f in os.listdir(diretorio) if f.endswith('.xml')]
    total_arquivos = len(arquivos)

    for i, arquivo in enumerate(arquivos):
        if update_progress:
            update_progress(i + 1, total_arquivos)

        if arquivo.endswith('.xml'):
            try:
                classe = XML()
                dados_nfe = classe.coletar_dados_nfe(os.path.join(diretorio, arquivo))
                
                codforn = dados_nfe["Emitente"]["Cód. Fornecedor"]
                serie = dados_nfe["NF-e"]["Série"]
                numdoc = dados_nfe["NF-e"]["Número"]
                codfil = dados_nfe["NF-e"]["Filial"]
                vlrdoc = dados_nfe["NF-e"]["Valor Total"]
                vlrliq = dados_nfe["NF-e"]["Valor Total"]
                chavenf = dados_nfe["NF-e"]["Chave"]
                dataemi = dados_nfe["NF-e"]["Data de Emissão"]
                ref = dados_nfe['NF-e']["Referencia"]

                
                produtos_diesel = ['DIESEL', 'S10', 'S-10', 'OLEO COMBUSTÍVEL', 'DIESEL S10', 'DIESEL S-10', "COMBUSTIVEL DIESEL", "DIESEL S10", "ORIGINAL DIESEL S10"]
                produtos_arla = ["ARLA", 'ARLA 32', 'ARLA32', 'REDUX', "ARLA 32 GRANEL LT"]
                produtos_gasolina = ["GASOLINA", "GASOLINA COMUM"]

                produtos_rodopar = {
                    'DIESEL': ['4', '15103', '15104', '15105'],
                    'ARLA': ['1231', '15106', '15107', '15108'],
                    'GASOLINA': ['1215', '15109', '15110', '15111']
                }

                # Verifica se a nota já foi lançada
                consulta_existente = api('GET', f"SELECT COUNT(*) AS QUANTIDADE FROM ESTENT WHERE CODCLIFOR = {codforn} AND SERIE = '{serie}' AND NUMDOC = '{numdoc}' AND CODFIL = {codfil}")
                try:
                    if consulta_existente[0]['QUANTIDADE'] > 0:
                        erro_msg = f"Impossível importar nota fiscal, já foi lançada. Arquivo: {arquivo}\n"
                        print(erro_msg)
                        shutil.move(os.path.join(diretorio, arquivo), os.path.join(pasta_erros, arquivo))
                        if update_text:
                            update_text(erro_msg)
                        continue
                except Exception as e:
                    erro_msg = f"Erro ao verificar se a nota fiscal já foi lançada. Arquivo: {arquivo}\n"
                    print(erro_msg)
                    shutil.move(os.path.join(diretorio, arquivo), os.path.join(pasta_erros, arquivo))
                    if update_text:
                        update_text(erro_msg)
                    continue
                # Insere a nota fiscal
                sleep(0.25)
                try:
                    # verifica se os produtos da nota são diesel, arla ou gasolina
                    for produto in dados_nfe["Produtos"]:
                        if any(desc in produto['descricao'].upper() for desc in produtos_diesel):
                            break
                        elif any(desc in produto['descricao'].upper() for desc in produtos_arla):
                            break
                        elif any(desc in produto['descricao'].upper() for desc in produtos_gasolina):
                            break
                    else:
                        erro_msg = f"Impossível importar nota fiscal, nenhum produto de diesel, arla ou gasolina encontrado. Arquivo: {arquivo}\n"
                        print(erro_msg)
                        shutil.move(os.path.join(diretorio, arquivo), os.path.join(pasta_erros, arquivo))
                        if update_text:
                            update_text(erro_msg)
                        continue
                    query_nf = (
                        f"EXEC SP_InsertNF @CODCLIFOR = {codforn}, @SERIE = '{serie}', "
                        f"@NUMDOC = '{numdoc}', @CODFIL = {codfil}, @REFERE = '{ref}', "
                        f"@VLRDOC = {vlrdoc}, @VLRLIQ = {vlrliq}, @NFE_ID = '{chavenf}', "
                        f"@DATEMI = '{dataemi}'"
                    )
                    print(f"Executando consulta NF: {query_nf}")
                    api('POST', query_nf)
                except Exception as e:
                    erro_msg = f"Erro ao importar Nota Fiscal para o arquivo {arquivo}: {e}"
                    print(erro_msg)
                    shutil.move(os.path.join(diretorio, arquivo), os.path.join(pasta_erros, arquivo))
                    if update_text:
                        update_text(erro_msg)
                    continue


                produtos_diesel = ['DIESEL', 'S10', 'S-10', 'OLEO COMBUSTÍVEL', 'DIESEL S10', 'DIESEL S-10', "COMBUSTIVEL;DIESEL", "DIESEL S10;"]
                produtos_arla = ["ARLA", 'ARLA 32', 'ARLA32', 'REDUX']
                produtos_gasolina = ["GASOLINA", "GASOLINA COMUM"]

                produtos_rodopar = {
                    'DIESEL': ['4', '15103', '15104', '15105'],
                    'ARLA': ['1231', '15106', '15107', '15108'],
                    'GASOLINA': ['1215', '15109', '15110', '15111']
                }

                if "JBS" in dados_nfe["Emitente"]["Nome"].upper():
                    texto_nota = f"Nota: {dados_nfe['NF-e']['Série']}/{dados_nfe['NF-e']['Número']} - Lançada com sucesso! - Empresa JBS, não será processada para contas a pagar.\n"
                    if update_text:
                        update_text(texto_nota)
                else:
                    texto_nota = f"Nota: {dados_nfe['NF-e']['Série']}/{dados_nfe['NF-e']['Número']} - Lançada com sucesso!\n"
                    if update_text:
                        update_text(texto_nota)

                codigos_utilizados = set()

                for produto in dados_nfe["Produtos"]:
                    codprod = produto['codigo']
                    qtdent = float(produto['quantidade'])
                    vlruni = float(produto['valor_unitario'])
                    vlrdes = produto['valor_desc']

                    codprod_insert = codprod  # Código do produto a ser inserido

                    if any(desc in produto['descricao'].upper() for desc in produtos_diesel):
                        lista_codigos = produtos_rodopar['DIESEL']
                    elif any(desc in produto['descricao'].upper() for desc in produtos_arla):
                        lista_codigos = produtos_rodopar['ARLA']
                    elif any(desc in produto['descricao'].upper() for desc in produtos_gasolina):
                        lista_codigos = produtos_rodopar['GASOLINA']
                    else:
                        lista_codigos = []

                    for codigo in lista_codigos:
                        if codigo not in codigos_utilizados:
                            codprod_insert = codigo
                            codigos_utilizados.add(codigo)
                            break
                    sleep(0.25)

                    try:
                        query_prod = (
                            f"EXEC SP_InsertProdNF @CODPROD = '{codprod_insert}', "
                            f"@QTDENT = {qtdent}, @VLRUNI = {vlruni}, @PRDCMR = {vlrdes}, "
                            f"@CHAVE_NFE = '{chavenf}'"
                        )
                        print(f"Executando consulta Produto: {query_prod}\n")
                        api('POST', query_prod)
                    except Exception as e:
                        erro_msg = f"Erro ao importar produtos para o arquivo {arquivo}: {e}"
                        print(erro_msg)
                        shutil.move(os.path.join(diretorio, arquivo), os.path.join(pasta_erros, arquivo))
                        if update_text:
                            update_text(erro_msg)
                        continue
                    sleep(0.25)
                    try:
                        query_loc = (
                            f"EXEC SP_InsertLoc @CODPROD = '{codprod_insert}', @QUANTI = {qtdent},"
                            f"@NUMDOC = {numdoc}, @CODCLIFOR = {codforn}, @SERIE = {serie}"
                        )
                        print(f"Executando consulta Localização: {query_loc}\n")
                        api('POST', query_loc)
                    except Exception as e:
                        erro_msg = f"Erro ao importar localização do produto para o arquivo {arquivo}: {e}"
                        print(erro_msg)
                        shutil.move(os.path.join(diretorio, arquivo), os.path.join(pasta_erros, arquivo))
                        if update_text:
                            update_text(erro_msg)
                        continue
                    sleep(0.25)
                    try:
                        query_fiscal = (
                            f"EXEC SP_InsertFis @CODPROD = '{codprod_insert}', "
                            f"@NUMDOC = {numdoc}, @CODCLIFOR = {codforn}, @SERIE = {serie}, @QUANTI = {qtdent}, @VLROUT = {vlruni * qtdent}, @VLRCON = {vlruni * qtdent}"
                        )
                        print(f"Executando consulta Fiscal: {query_fiscal}\n")
                        api('POST', query_fiscal)
                    except Exception as e:
                        erro_msg = f"Erro ao importar o fiscal do produto para o arquivo {arquivo}: {e}"
                        print(erro_msg)
                        shutil.move(os.path.join(diretorio, arquivo), os.path.join(pasta_erros, arquivo))
                        if update_text:
                            update_text(erro_msg)
                        continue
                sleep(0.25)
                try:
                    # Primeiro, recupere a razão social da nota fiscal
                    razao_social = dados_nfe["Emitente"]["Nome"]

                    # Verifique se a razão social contém "JBS"
                    if "JBS" in razao_social.upper():
                        print(f"Nota fiscal da empresa '{razao_social}' não será processada para contas a pagar.")
                    else:
                        # Executa a consulta de contas a pagar apenas se a razão social não contiver "JBS"
                        query_contpag = (
                            f"EXEC SP_InsertPG @NUMDOC = '{numdoc}', "
                            f"@SERSUB = {serie}, @CODCLIFOR = {codforn}, @CODFIL = {codfil}, @VLRDOC = {vlrliq} "
                        )
                        print(f"Executando consulta Pagamento: {query_contpag}\n")
                        api('POST', query_contpag)
    
                except Exception as e:
                    erro_msg = f"Erro ao Importar informações para o contas a pagar para o arquivo {arquivo}: {e}"
                    print(erro_msg)
                    shutil.move(os.path.join(diretorio, arquivo), os.path.join(pasta_erros, arquivo))
                    if update_text:
                        update_text(erro_msg)
                    continue
                sleep(0.25)
                # executa a proc de classificacao
                try:
                    # Primeiro, recupere a razão social da nota fiscal
                    razao_social = dados_nfe["Emitente"]["Nome"]

                    # Verifique se a razão social contém "JBS"
                    if "JBS" in razao_social.upper():
                        print(f"Nota fiscal da empresa '{razao_social}' não será processada para contas a pagar.")
                    else:
                        query_class = ( f"EXEC SP_InsertClass @NUMDOC = '{numdoc}', "
                                        f"@SERSUB = {serie}, @CODCLIFOR = {codforn}, @VLRDOC = {vlrdoc} "
                                        )
                        print(f"Executando consulta Classificação: {query_class}\n")
                        api('POST', query_class)
                except Exception as e:
                    erro_msg = f"Erro ao Importar informações para a classificação para o arquivo {arquivo}: {e}"
                    print(erro_msg)
                    shutil.move(os.path.join(diretorio, arquivo), os.path.join(pasta_erros, arquivo))
                    if update_text:
                        update_text(erro_msg)
                    continue
                
                shutil.move(os.path.join(diretorio, arquivo), os.path.join(pasta_lancadas, arquivo))
                print(f"Arquivo movido para: {pasta_lancadas}")

            except Exception as e:
                erro_msg = f"Erro ao processar o arquivo {arquivo}: {e}"
                print(erro_msg)
                if update_text:
                    update_text(erro_msg)
                shutil.move(os.path.join(diretorio, arquivo), os.path.join(pasta_erros, arquivo))
