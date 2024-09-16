import os
import shutil
import xml.etree.ElementTree as ET
from datetime import datetime
from api import api
from time import sleep

# Classe para manipulação de arquivos XML
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

# Função para localizar elementos em um arquivo XML
    def localizar(self, xml, caminho, atributo=None):
        self.tree = ET.parse(xml)
        self.root = self.tree.getroot()
        # Define o namespace
        ns = {'nfe': 'http://www.portalfiscal.inf.br/nfe'}
        elemento = self.root.find(caminho, namespaces=ns)
        # Verifica se o elemento foi encontrado
        if elemento is not None:
            if atributo:
                return elemento.attrib.get(atributo)
            else:
                return elemento.text
        return None

    # Função para coletar dados da nota fiscal
    def coletar_dados_nfe(self, xml):
        # Dados Emitente
        self.cnpj_emitente = self.localizar(xml, './/nfe:emit/nfe:CNPJ')
        self.ie_emitente = self.localizar(xml, './/nfe:emit/nfe:IE')
        self.nome_emitente = self.localizar(xml, './/nfe:emit/nfe:xNome')
        self.uf_emitente = self.localizar(xml, './/nfe:emit/nfe:enderEmit/nfe:UF')
        self.municipio_emitente = self.localizar(xml, './/nfe:emit/nfe:enderEmit/nfe:xMun')
        self.cod_municipio_emitente = self.localizar(xml, './/nfe:emit/nfe:enderEmit/nfe:cMun')

        # Dados Destinatário
        self.cnpj_destinatario = self.localizar(xml, './/nfe:dest/nfe:CNPJ')

        # Seta a filial
        self.filial = self.filiais.get(self.cnpj_destinatario, 'Filial não encontrada')
        # Formata o CNPJ do emitente
        self.cnpj_emitente = f"{self.cnpj_emitente[:2]}.{self.cnpj_emitente[2:5]}.{self.cnpj_emitente[5:8]}/{self.cnpj_emitente[8:12]}-{self.cnpj_emitente[12:14]}"

        # SELECIONA O CODIGO DO FORNECEDOR CADASTRADOS NO BANCO DE DADOS
        resultado = api('GET', f"SELECT CODCLIFOR FROM RODCLI WHERE CODCGC = '{self.cnpj_emitente}'")
        if resultado:
            # SE O FORNECEDOR FOR ENCONTRADO, RETORNA O CODIGO DO FORNECEDOR
            self.cod_forn = resultado[0]['CODCLIFOR']
            # SE O FORNECEDOR NÃO FOR ENCONTRADO, RETORNA NULO
        else:
            self.cod_forn = None
        
        # Produtos da Nota Fiscal
        self.produtos = []
        self.valor_total_desconto = 0.0
        # Percorre os produtos da nota fiscal
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
            # Adiciona o produto na lista de produtos
            self.produtos.append(self.produto)

        # Observação da Nota Fiscal
        self.observacao = self.localizar(xml, './/nfe:infAdic/nfe:infCpl')

        # NUMERO DA NOTA FISCAL
        self.numero_nfe = self.localizar(xml, './/nfe:ide/nfe:nNF')

        # CHAVE DA NOTA FISCAL
        self.chave_nfe = self.localizar(xml, './/nfe:infNFe', 'Id')
        # Formata a chave da nota fiscal
        if self.chave_nfe:
            self.chave_nfe = self.chave_nfe.replace('NFe', '')
        else:
            self.chave_nfe = None
        # SÉRIE DA NOTA FISCAL
        self.serie_nfe = self.localizar(xml, './/nfe:ide/nfe:serie')
        # DATA DE EMISSÃO DA NOTA FISCAL
        self.data_emissao = self.localizar(xml, './/nfe:ide/nfe:dhEmi')
        self.data_emissao = datetime.strptime(self.data_emissao, '%Y-%m-%dT%H:%M:%S-03:00').strftime('%Y-%m-%d %H:%M:%S')
        self.data_emissao = datetime.strptime(self.data_emissao, '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d')
        # VALOR TOTAL DA NOTA FISCAL
        self.valor_nfe = self.localizar(xml, './/nfe:total/nfe:ICMSTot/nfe:vNF')

        # Retorna os dados da nota fiscal
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

# Função para processar arquivos XML
def processar_xmls(diretorio, pasta_lancadas, pasta_erros, update_progress=None, update_text=None):  
    # Verifica se os diretórios existem
    if not os.path.exists(pasta_lancadas):
        # Cria o diretório de notas fiscais lançadas
        os.makedirs(pasta_lancadas)

    # Verifica se os diretórios existem
    if not os.path.exists(pasta_erros):
        # Cria o diretório de erros
        os.makedirs(pasta_erros)

    # Lista os arquivos XML no diretório
    arquivos = [f for f in os.listdir(diretorio) if f.endswith('.xml')]
    total_arquivos = len(arquivos)

    # Percorre os arquivos XML
    for i, arquivo in enumerate(arquivos):
        # Atualiza a barra de progresso
        if update_progress:
            update_progress(i + 1, total_arquivos)

        # Verifica se o arquivo é um arquivo XML
        if arquivo.endswith('.xml'):
            try:
                # Coleta os dados da nota fiscal
                classe = XML()
                dados_nfe = classe.coletar_dados_nfe(os.path.join(diretorio, arquivo))
                
                # Dados da nota fiscal
                codforn = dados_nfe["Emitente"]["Cód. Fornecedor"]
                serie = dados_nfe["NF-e"]["Série"]
                numdoc = dados_nfe["NF-e"]["Número"]
                codfil = dados_nfe["NF-e"]["Filial"]
                vlrdoc = dados_nfe["NF-e"]["Valor Total"]
                vlrliq = dados_nfe["NF-e"]["Valor Total"]
                chavenf = dados_nfe["NF-e"]["Chave"]
                dataemi = dados_nfe["NF-e"]["Data de Emissão"]
                ref = dados_nfe['NF-e']["Referencia"]

                # Produtos da Nota Fiscal
                produtos_diesel = ['DIESEL', 'S10', 'S-10', 'OLEO COMBUSTÍVEL', 'DIESEL S10', 'DIESEL S-10', "COMBUSTIVEL;DIESEL", "DIESEL S10;"]
                produtos_arla = ["ARLA", 'ARLA 32', 'ARLA32', 'REDUX']
                produtos_gasolina = ["GASOLINA", "GASOLINA COMUM"]

                # Produtos do sistema
                produtos_sistema = {
                    'DIESEL': ['4', '15103', '15104', '15105'],
                    'ARLA': ['1231', '15106', '15107', '15108'],
                    'GASOLINA': ['1215', '15109', '15110', '15111']
                }

                # Verifica se a nota já foi lançada
                consulta_existente = api('GET', f"SELECT COUNT(*) AS QUANTIDADE FROM ESTENT WHERE CODCLIFOR = {codforn} AND SERIE = '{serie}' AND NUMDOC = '{numdoc}' AND CODFIL = {codfil}")
                try:
                    if consulta_existente[0]['QUANTIDADE'] > 0:
                        # Move o arquivo para a pasta de erros
                        erro_msg = f"Impossível importar nota fiscal, já foi lançada. Arquivo: {arquivo}\n"
                        print(erro_msg)
                        shutil.move(os.path.join(diretorio, arquivo), os.path.join(pasta_erros, arquivo))
                        # Atualiza o texto
                        if update_text:
                            update_text(erro_msg)
                        continue
                # Trata exceções
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
                    # validar para nao lançar notas que não possuem diesel, arla ou gasolina
                    if not any(desc in ref.upper() for desc in produtos_diesel) and not any(desc in ref.upper() for desc in produtos_arla) and not any(desc in ref.upper() for desc in produtos_gasolina):
                        erro_msg = f"Impossível importar nota fiscal, não possui produtos válidos. Arquivo: {arquivo}\n"
                        print(erro_msg)
                        shutil.move(os.path.join(diretorio, arquivo), os.path.join(pasta_erros, arquivo))
                        if update_text:
                            update_text(erro_msg)
                        # Pula para a próxima iteração
                        continue
                    
                    # Insere a nota fiscal
                    query_nf = (
                        f"EXEC SP_InsertNF @CODCLIFOR = {codforn}, @SERIE = '{serie}', "
                        f"@NUMDOC = '{numdoc}', @CODFIL = {codfil}, @REFERE = '{ref}', "
                        f"@VLRDOC = {vlrdoc}, @VLRLIQ = {vlrliq}, @NFE_ID = '{chavenf}', "
                        f"@DATEMI = '{dataemi}'"
                    )
                    # Executa a consulta
                    print(f"Executando consulta NF: {query_nf}")
                    api('POST', query_nf)
                except Exception as e:
                    # Move o arquivo para a pasta de erros
                    erro_msg = f"Erro ao importar Nota Fiscal para o arquivo {arquivo}: {e}"
                    print(erro_msg)
                    shutil.move(os.path.join(diretorio, arquivo), os.path.join(pasta_erros, arquivo))
                    if update_text:
                        update_text(erro_msg)
                    # Pula para a próxima iteração
                    continue
                
                # verificar se a nota é da empresa JBS, usa o código da tarefa diferente
                if "JBS" in dados_nfe["Emitente"]["Nome"].upper():
                    texto_nota = f"Nota: {dados_nfe['NF-e']['Série']}/{dados_nfe['NF-e']['Número']} - Lançada com sucesso! - Empresa JBS, não será processada para contas a pagar.\n"
                    if update_text:
                        update_text(texto_nota)
                # Se não for da empresa JBS, insere os produtos e as informações de contas a pagar
                else:
                    texto_nota = f"Nota: {dados_nfe['NF-e']['Série']}/{dados_nfe['NF-e']['Número']} - Lançada com sucesso!\n"
                    if update_text:
                        update_text(texto_nota)

                codigos_utilizados = set()

                for produto in dados_nfe["Produtos"]:
                    # Coleta os dados do produto
                    codprod = produto['codigo']
                    qtdent = float(produto['quantidade'])
                    vlruni = float(produto['valor_unitario'])
                    vlrdes = produto['valor_desc']

                    # Código do produto a ser inserido
                    codprod_insert = codprod  

                    # Verifica se o produto é diesel, arla ou gasolina
                    if any(desc in produto['descricao'].upper() for desc in produtos_diesel):
                        lista_codigos = produtos_sistema['DIESEL']
                    elif any(desc in produto['descricao'].upper() for desc in produtos_arla):
                        lista_codigos = produtos_sistema['ARLA']
                    elif any(desc in produto['descricao'].upper() for desc in produtos_gasolina):
                        lista_codigos = produtos_sistema['GASOLINA']
                    else:
                        lista_codigos = []

                    # Verifica se o produto possui um código válido
                    for codigo in lista_codigos:
                        if codigo not in codigos_utilizados:
                            codprod_insert = codigo
                            codigos_utilizados.add(codigo)
                            break
                    sleep(0.25)

                    try:
                        # Insere o produto na nota fiscal
                        query_prod = (
                            f"EXEC SP_InsertProdNF @CODPROD = '{codprod_insert}', "
                            f"@QTDENT = {qtdent}, @VLRUNI = {vlruni}, @PRDCMR = {vlrdes}, "
                            f"@CHAVE_NFE = '{chavenf}'"
                        )
                        # Executa a consulta
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
                        # Insere a localização do produto
                        query_loc = (
                            f"EXEC SP_InsertLoc @CODPROD = '{codprod_insert}', @QUANTI = {qtdent},"
                            f"@NUMDOC = {numdoc}, @CODCLIFOR = {codforn}, @SERIE = {serie}"
                        )
                        # Executa a consulta
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
                        # Insere o fiscal do produto
                        query_fiscal = (
                            f"EXEC SP_InsertFis @CODPROD = '{codprod_insert}', "
                            f"@NUMDOC = {numdoc}, @CODCLIFOR = {codforn}, @SERIE = {serie}, @QUANTI = {qtdent}, @VLROUT = {vlruni * qtdent}, @VLRCON = {vlruni * qtdent}"
                        )
                        # Executa a consulta
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
                        # Executa a consulta
                        print(f"Executando consulta Classificação: {query_class}\n")
                        api('POST', query_class)
                except Exception as e:
                    erro_msg = f"Erro ao Importar informações para a classificação para o arquivo {arquivo}: {e}"
                    print(erro_msg)
                    shutil.move(os.path.join(diretorio, arquivo), os.path.join(pasta_erros, arquivo))
                    if update_text:
                        update_text(erro_msg)
                    continue
                # Move o arquivo para a pasta de notas fiscais lançadas
                shutil.move(os.path.join(diretorio, arquivo), os.path.join(pasta_lancadas, arquivo))
                print(f"Arquivo movido para: {pasta_lancadas}")
            
            # Trata exceções
            except Exception as e:
                erro_msg = f"Erro ao processar o arquivo {arquivo}: {e}"
                print(erro_msg)
                if update_text:
                    update_text(erro_msg)
                shutil.move(os.path.join(diretorio, arquivo), os.path.join(pasta_erros, arquivo))
