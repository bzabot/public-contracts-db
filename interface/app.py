import datetime
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
from flask import render_template, Flask, request
import db
import locale
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8') 
APP = Flask(__name__)

queries = {
    "index": 
    '''
        SELECT count(*) as n_contratos, sum(precoContratual) as valor_total
        FROM contratos;
    ''',
    "p1":
    '''
        SELECT tipo
        FROM TiposContratos
        ORDER BY tipo;
    ''',
    "p2":
    '''
        SELECT pais, tipo, SUM(precoContratual) AS total
        FROM Contratos 
        NATURAL JOIN LocaisDeExecucao
        NATURAL JOIN Municipios
        NATURAL JOIN Distritos
        NATURAL JOIN Paises
        NATURAL JOIN ClassificacaoContratos
        NATURAL JOIN TiposContratos
        GROUP BY pais, tipo
        ORDER BY total DESC;
    ''',
    "p3":
    '''
        SELECT entidade AS adjudicante, MAX(precoContratual) AS valor_maximo
        FROM Contratos
        JOIN Entidades ON idAdjudicante = idEntidade;
    ''',
    "p4":
    '''
        SELECT nif, entidade
        FROM Contratos 
        NATURAL JOIN LocaisDeExecucao
        NATURAL JOIN Municipios
        NATURAL JOIN Distritos
        NATURAL JOIN Paises
        NATURAL JOIN Adjudicatarios
        NATURAL JOIN Entidades
        WHERE prazoExecucao < 365
        GROUP BY idEntidade;
    ''',
    "p5":
    '''
        SELECT entidade
        FROM Entidades
        NATURAL JOIN Adjudicatarios
        WHERE entidade LIKE "M%";
    ''',
    "p6":
    '''
        SELECT COUNT(idcontrato) as quantidade, procedimento as tipo_procedimento
        FROM contratos
        NATURAL JOIN tiposProcedimentos 
        GROUP BY idProcedimento
        ORDER BY quantidade DESC;
    ''',
    "p7":
    '''
        SELECT entidade, COUNT(idContrato) AS num_contratos
        FROM Contratos
        NATURAL JOIN Adjudicatarios 
        NATURAL JOIN Entidades  
        GROUP BY idEntidade
        ORDER BY num_contratos DESC
        LIMIT 1;
    ''',
    "p8":
    '''
        SELECT distrito, COUNT(idContrato) AS total
        FROM Contratos
        NATURAL JOIN AcordoQuadroContratos
        NATURAL JOIN LocaisDeExecucao
        NATURAL JOIN Municipios
        NATURAL JOIN Distritos
        WHERE dataPublicacao > '2024-01-10'
        AND  dataPublicacao < '2024-01-14'
        AND distrito IS NOT NULL
        GROUP BY distrito
        ORDER BY total DESC;
    ''',
    "p9":
    '''
        WITH municipiosCentra AS (
            SELECT idMunicipio
            FROM Contratos
            NATURAL JOIN LocaisDeExecucao
            NATURAL JOIN Municipios
            WHERE procedimentoCentralizado = "Sim"
            GROUP BY idMunicipio
        )
        SELECT municipio 
        FROM Municipios
        WHERE idMunicipio NOT IN municipiosCentra
        AND municipio IS NOT NULL
        ORDER BY municipio;
    ''',
    "p10":
    '''
        WITH Adjudicantes5Cont AS (
            SELECT idAdjudicante
            FROM Contratos
            JOIN Entidades ON idAdjudicante = idEntidade
            GROUP BY idAdjudicante
            HAVING COUNT(idContrato) <= 5
        ) 
        SELECT nif, entidade AS designacao, objetoContrato
        FROM Contratos
        JOIN Entidades ON idAdjudicante = idEntidade
        WHERE idAdjudicante IN Adjudicantes5Cont
        ORDER BY entidade;
    ''',
    "p11":
    '''
        WITH MaiorValorPorPais AS (
            SELECT 
                idContrato,
                precoContratual,
                idPais,
                pais AS nomePais
            FROM Contratos
            NATURAL JOIN LocaisDeExecucao
            NATURAL JOIN Municipios
            NATURAL JOIN Distritos
            NATURAL JOIN Paises
            WHERE precoContratual IS NOT NULL
            GROUP BY idPais
            HAVING precoContratual = MAX(precoContratual)
        )

        SELECT 
            MVPC.idContrato,
            CP.codigoCPV,
            MVPC.nomePais,
            MVPC.precoContratual AS valorContrato
        FROM MaiorValorPorPais MVPC
        NATURAL JOIN CPVContratos CP
        ORDER BY valorContrato DESC, CP.codigoCPV ASC;
    ''',
    "p12":
    '''
        SELECT 
            TC.tipo AS tipoContrato,
            M.municipio,
            COUNT(C.idContrato) AS quantidadeContratos,
            DATE(C.dataCelebracaoContrato) AS dia
        FROM Contratos C
        JOIN LocaisDeExecucao L ON C.idContrato = L.idContrato
        JOIN Municipios M ON L.idMunicipio = M.idMunicipio
        JOIN TiposContratos TC ON C.idProcedimento = TC.idTipoContrato
        WHERE DATE(C.dataCelebracaoContrato) = '2024-01-15'
        GROUP BY TC.tipo, M.municipio, dia
        ORDER BY TC.tipo, M.municipio;
    ''',
    "p13":
    '''
        WITH MediaPorTipoProcedimentoDistrito AS (
            SELECT 
                D.distrito,
                TP.procedimento AS tipoProcedimento,
                ROUND(AVG(C.precoContratual), 2) AS mediaValor
            FROM Contratos C
            JOIN LocaisDeExecucao L ON C.idContrato = L.idContrato
            JOIN Municipios M ON L.idMunicipio = M.idMunicipio
            JOIN Distritos D ON M.idDistrito = D.idDistrito
            JOIN TiposProcedimentos TP ON C.idProcedimento = TP.idProcedimento
            WHERE C.precoContratual IS NOT NULL
            AND D.distrito IS NOT NULL
            GROUP BY D.distrito, TP.procedimento
        )
        SELECT * 
        FROM MediaPorTipoProcedimentoDistrito
        ORDER BY distrito, tipoProcedimento;
    '''
}

def routing(page, qnt):
    def route_func():
        if qnt == 1:
            contratos = db.execute(queries[page]).fetchone()
        else:
            contratos = db.execute(queries[page]).fetchall()
        print(f"Query results for {page}: {contratos}")  # Debugging statement
        return render_template(page + '.html', contratos=contratos)
    route_func.__name__ = page  # Ensure unique function name
    if(page == "index"):
        APP.route("/")(route_func)
    else:
        APP.route("/" + page)(route_func)

# INDEX PAGE
routing('index', 1)
routing("p1", 2)  
routing("p2", 2)  
routing("p3", 2)  
routing("p4", 2)  
routing("p5", 2)  
routing("p6", 2)  
routing("p7", 1)  
routing("p8", 2)  
routing("p9", 2)  
routing("p10", 2)  
routing("p11", 2)  
routing("p12", 2)  
routing("p13", 2)  


@APP.route('/search')
def search():
    id = request.args.get('id')
    if(len(id) != 8):
        return "Id inválido"
    search_value = request.args.get('search_value')
    if id:
        data = db.execute(''' 
            SELECT idContrato , objetoContrato, precoContratual
            FROM contratos 
            WHERE idContrato = ?''', [id]).fetchone()
    if data:
        return render_template('search_result.html', data=data, search_value=search_value)
    else:
        return "Id não encontrado."



@APP.route('/contratos')
def contratos():
    contratos = db.execute('''
    SELECT C.objetoContrato as objeto_contrato, A1.designacao AS adjudicante, A2.designacao AS adjudicatario, C.precoContratual as preco_contratual
    FROM contratos C
    JOIN( SELECT contrato, designacao FROM adjudicantes JOIN entidades on entidade = codigo) A1 on A1.contrato = C.idContrato
    JOIN( SELECT contrato, designacao FROM adjudicatarios JOIN entidades on entidade = codigo) A2 on A2.contrato = C.idContrato
    ORDER BY C.dataPublicacao;
    ''').fetchall()
    return render_template('listar_contratos.html', contratos=contratos)

@APP.route('/paises')
def paises():
    paises = db.execute(''' 
        SELECT P.nome AS pais,
            count(E.contrato) AS n_contratos,
            P.codigo as cod
        FROM paisDeExecucao E
            JOIN
            paises P ON E.pais = P.codigo
        GROUP BY P.codigo
        ORDER BY n_contratos DESC;
    ''').fetchall()
    return render_template('listar_paises.html', paises=paises)



@APP.route('/paises/<int:codigo>/')
def pais(codigo):
    
    pais = db.execute('''
        SELECT *
        FROM paises
        WHERE codigo = ?;
    ''', [codigo]).fetchone()
    contratos = db.execute("""
        SELECT A1.designacao as adjudicante, A2.designacao as adjudicatario, strftime('%d/%m/%Y', c.dataPublicacao) as dataPublicacao, C.prazoExecucao, C.precoContratual
        FROM paisDeExecucao E 
        JOIN contratos C on E.contrato = C.idContrato
        JOIN( SELECT contrato, designacao FROM adjudicantes JOIN entidades on entidade = codigo) A1 on A1.contrato = C.idContrato
        JOIN( SELECT contrato, designacao FROM adjudicatarios JOIN entidades on entidade = codigo) A2 on A2.contrato = C.idContrato
        WHERE pais = ?
        ORDER BY dataPublicacao;
""", [codigo]).fetchall()
    return render_template('pais.html', 
                            pais=pais,
                            contratos=contratos)


#### adjudicatarios ####
@APP.route('/adjudicatarios')
def adjudicatarios():
    adjudicatarios = db.execute(''' 
        SELECT E.designacao,
            sum(C.precoContratual) AS total,
            E.codigo as cod
        FROM contratos C
            JOIN
            adjudicatarios A ON C.idContrato = A.contrato
            JOIN
            entidades E ON A.entidade = E.codigo
        GROUP BY A.entidade
        ORDER BY total DESC;
    ''').fetchall()
    return render_template('listar_adjudicatarios.html', adjudicatarios=adjudicatarios)

@APP.route('/adjudicatarios/<int:codigo>/')
def adjudicatario(codigo):
    
    adjudicatario = db.execute('''
        SELECT *
        FROM entidades
        WHERE codigo = ?;
    ''', [codigo]).fetchone()
    contratos = db.execute("""
        SELECT C.objetoContrato,
            strftime('%d/%m/%Y', c.dataPublicacao) AS dataPublicacao,
            C.prazoExecucao,
            C.precoContratual
        FROM contratos C
            JOIN
            adjudicatarios A ON C.idContrato = A.contrato
        WHERE A.entidade = ?
        ORDER BY C.dataPublicacao;
""", [codigo]).fetchall()
    return render_template('adjudicatario.html', 
                            adjudicatario=adjudicatario,
                            contratos=contratos)




# FILTROS
@APP.template_filter('to_euro')
def to_euro(value):
    try:
        return locale.currency(value, symbol=True, grouping=True).replace('$', '€')
    except ValueError:
        return f"{value:.2f} €"







