import sqlite3
from openpyxl import load_workbook
#import re


def sanitize_text_input(input):
    if (not(input)):
        return False

    # Verificar se o valor é uma string
    if isinstance(input, str):
        # Remove extra spaces at the beginning and end
        sanitized = input.strip()

        # Replace multiple spaces with a single space
        sanitized = ' '.join(sanitized.split())
        return sanitized
    
    return input

def check_existence(cur, table, column, value):
    value = sanitize_text_input(value)
    query = f"SELECT * FROM {table} WHERE {column} = ?"
    cur.execute(query, (value,))
    return cur.fetchone()

def check_existence_two_values(cur, table, column1, column2, value1, value2):
    value1 = sanitize_text_input(value1)
    value2 = sanitize_text_input(value2)

    query = f"SELECT * FROM {table} WHERE {column1} = ? AND {column2} = ? "
    cur.execute(query, (value1, value2))
    return cur.fetchone()

def table_one_value(cur, table, column, value):
    if not table.isidentifier() or not column.isidentifier():
        raise ValueError("Nomes de tabela ou coluna inválidos")
    
    value = sanitize_text_input(value)
    found_row = check_existence(cur, table, column, value)

    if(found_row): return found_row[0] #retorna o id
    elif(value):
        return insert_one_value(cur, table, column, value)

def insert_one_value(cur, table, column, value):
    query = f"""
            INSERT INTO {table} ({column}) 
            VALUES (?);
        """
    cur.execute(query, (value,))
    return cur.lastrowid

def table_two_values(cur, table, column1, column2, values, check_function = check_existence):

    if not table.isidentifier() or not column1.isidentifier() or not column2.isidentifier():
        raise ValueError("Nomes de tabela ou coluna inválidos")
    
    values = [sanitize_text_input(values[0]), sanitize_text_input(values[1])]
    if (check_function == check_existence):
        found_row = check_function(cur, table, column1, values[0])
    else:
        found_row = check_function(cur, table, column1, column2, values[0], values[1])

    if(found_row): return found_row[0] 
    elif(values[0] and values[1]):
        return insert_two_values(cur, table, column1, column2, values[0], values[1])
    
def insert_two_values(cur, table, column1, column2, value1, value2):
    query = f"""
        INSERT INTO {table} ({column1}, {column2}) 
        VALUES (?, ?);
    """
    cur.execute(query, (value1, value2))
    return cur.lastrowid

def table_local(cur, value):
    places = value.split("|")
    place = [p.split(",") for p in places]
    municipios = []
    paises = []
    for p in place:
        pais_id = table_one_value(cur, "paises", "nome", p[0])

        if(len(p) == 1): # se só informar o pais 
            if pais_id not in paises:
                paises.append(pais_id)
        
        if(len(p) == 3):
            distrito_id = table_two_values(cur, "distritos", "nome", "pais", [p[1], pais_id])
            municipio_id = table_two_values(cur, "municipios", "nome", "distrito", [p[2], distrito_id])
            if municipio_id not in municipios:
                municipios.append(municipio_id)
        #else:
            # TODO AJEITAR ESSA PARTE
            # found_row = check_existence(cur, "municipios", "nome", value)
            # print(p)
            # if(not found_row): 
            #     print(f"Municipio {p[1]} não tem distrito vinculado ")
            #     return None  
    return [municipios, paises]

def table_contrato(cur, values, ids):
        for key, value in values.items():
            values[key] = sanitize_text_input(value)
        found_row = check_existence(cur, "Contratos", "idContrato", values["idcontrato"])

        if (found_row): return found_row[0]
        
        query = f"""
            INSERT INTO contratos (idContrato, objetoContrato, dataPublicacao, dataCelebracaoContrato , precoContratual, procedimentoCentralizado, prazoExecucao, idProcedimento, idAdjudicante) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
        """

        cur.execute(query, (values["idcontrato"], values["objectoContrato"], values["dataPublicacao"], values["dataCelebracaoContrato"], values["precoContratual"], values["ProcedimentoCentralizado"], values["prazoExecucao"], ids["idProcedimento"], ids["idAdjudicante"][0]))
        return cur.lastrowid


def handle_entidades(list_values, i):
    """Manipula entradas para o caso especial de 'entidades'."""
    if i != len(list_values) - 1 and len(list_values[i + 1].split(" - ", 1)) == 1:
        combined_value = list_values[i] + "|" + list_values[i + 1]
        return combined_value.split(" - ", 1), True
    return list_values[i].split(" - ", 1), False


def get_ids_for_multiple_values(cur, data, table_type, table, column1, column2=None, checkFunction=check_existence):
    list_values = data.split("|")
    ids = []
    skip_next = False
    for i in range(len(list_values)):
        if(table_type == table_one_value):
            contrato_id = table_one_value(cur, table, column1, list_values[i])
        elif (table_type == table_two_values and (not skip_next)):
            if (table == "CPVs"):
                value = list_values[i].split(" - ", 1)
            elif (table == "Entidades"):
                value, skip_next = handle_entidades(list_values, i)

            if (len(value) != 2): 
                print("Valor inválido ou incompleto")
                continue
            contrato_id = table_two_values(cur,table, column1, column2, value, checkFunction)

        ids.append(contrato_id)
    return ids

def associate_values_with_contract(cur, table, column1, column2, idcontrato, idlist):
    for id in idlist:
        table_two_values(cur,table, column1, column2, [idcontrato, id], check_existence_two_values)



def new_contract(cur, row_data):
    contrato_values_id = {}

    # tabelas simples
    contrato_values_id["codigoCPV"] = get_ids_for_multiple_values(cur, row_data["cpv"], table_two_values, "CPVs", "codigoCPV", "descricao")
    # TODO - Provavelmente vai ter que criar algo separado
    #contrato_values_id["idAcordoQuadro"] =  get_ids_for_multiple_values(cur, row_data["DescrAcordoQuadro"], table_two_values, "DescrAcordoQuadro", "identificador", "descricao")
    contrato_values_id["idProcedimento"] = table_one_value(cur, "TiposProcedimentos", "tipo", row_data["tipoprocedimento"])
    contrato_values_id["idTipoContrato"] = get_ids_for_multiple_values(cur, row_data["tipoContrato"], table_one_value, "TiposContratos", "tipo")
    #contrato_values_id["fundamentacao_id"] = table_one_value(cur, "fundamentacoes", "fundamentacao", row_data["fundamentacao"])
    # [contrato_values_id["municipios_id"], contrato_values_id["paises_id"]] = table_local(cur, row_data["localExecucao"])
    contrato_values_id["idAdjudicante"] = get_ids_for_multiple_values(cur, row_data["adjudicante"], table_two_values, "Entidades", "nif", "designacao", check_existence_two_values)
    if ( row_data["adjudicatarios"]): 
        idAdjudicatarios=get_ids_for_multiple_values(cur, row_data["adjudicatarios"], table_two_values, "Entidades", "nif", "designacao", check_existence_two_values)
    else : 
        idAdjudicatarios = None

    # criando contrato
    values_contrato = {"idcontrato": row_data["idcontrato"], "objectoContrato": row_data["objectoContrato"], "dataPublicacao": row_data["dataPublicacao"], "dataCelebracaoContrato": row_data["dataCelebracaoContrato"], "precoContratual": row_data["precoContratual"], "ProcedimentoCentralizado": row_data["ProcedimentoCentralizado"], "prazoExecucao": row_data["prazoExecucao"]}
    idContrato = table_contrato(cur, values_contrato, contrato_values_id)

    # Tabelas com duas chaves primarias
    associate_values_with_contract(cur, "CPVContratos", "idContrato", "codigoCPV", idContrato, contrato_values_id["codigoCPV"])
    associate_values_with_contract(cur, "ClassificacaoContratos", "idContrato", "idTipoContrato", idContrato, contrato_values_id["idTipoContrato"])
    if(idAdjudicatarios): associate_values_with_contract(cur, "Adjudicatarios", "idContrato", "idEntidade", idContrato, idAdjudicatarios) 
    # TODO
    #if contrato_values_id["LocaisDeExecucao"]: associate_values_with_contract(cur, "LocaisDeExecucao", "idContrato", "idMunicipio", idContrato, contrato_values_id["idMunicipio"])




def add_dataset(sheet):
    con = sqlite3.connect('../contratos_publicos.db')
    cur = con.cursor()

    headers = [cell.value for cell in sheet[1]] 

    # Itera sobre as linhas da planilha, começando na segunda linha, pois a primeira é o cabeçalho
    for row in sheet.iter_rows(min_row=2, values_only=True):
        row_data = dict(zip(headers, row))     
        # TODO Melhor fazer a checagem da existencia do contrato do lado de fora pq ai não adiciona o que já foi adicionado, já que garantidamente tudo que ta no contrato esta na bd
        new_contract(cur, row_data)

    con.commit()
    print("Adicionado na BD")
    con.close()

# Carregue o arquivo Excel
workbook = load_workbook(filename='../dataset/ContratosPublicos2024.xlsx')

# Selecione a planilha ativa
sheet = workbook.active

add_dataset(sheet)