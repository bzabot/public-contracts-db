"""
This module sets up a Flask web application to interface with a database of contracts.
It defines various routes to execute SQL queries and render HTML templates with the results.

Modules:
    warnings: Provides a way to handle warnings in the code.
    flask: A micro web framework for Python.
    db: A custom module for database operations.
    locale: Provides internationalization services.

Functions:
    routing(page, qnt): Sets up a route for a given page and query quantity.
    search(): Handles the search functionality by contract ID.
    to_euro(value): A template filter to format numbers as Euro currency.
"""

import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
from flask import render_template, Flask, request
import db
import locale
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8') 
APP = Flask(__name__)

# SQL queries to be executed for different routes
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
    ''',
    "p14":
    '''
        WITH FundamentacaoPorDistrito AS (
            SELECT 
                d.distrito, 
                f.artigo,
                f.numero,
                f.alinea,
                f.referenciaLegislativa,
                (COALESCE(f.artigo, '') || ' ' || 
                COALESCE(f.numero, '') || ' ' || 
                COALESCE(f.alinea, '') || ' - ' || 
                COALESCE(f.referenciaLegislativa, '')) AS fundamentacao, 
                COUNT(*) as total
            FROM LocaisDeExecucao le
            NATURAL JOIN Municipios m
            NATURAL JOIN Distritos d
            NATURAL JOIN FundamentacaoContratos fc
            NATURAL JOIN Fundamentacoes f
            GROUP BY d.distrito, f.artigo, f.numero, f.alinea, f.referenciaLegislativa, fundamentacao
        ),
        MaxFundamentacao AS (
            SELECT 
                distrito, 
                MAX(total) as max_total
            FROM FundamentacaoPorDistrito
            GROUP BY distrito
        )
        SELECT 
            fpd.distrito, 
            fpd.artigo,
            fpd.numero,
            fpd.alinea,
            fpd.referenciaLegislativa,
            fpd.fundamentacao, 
            fpd.total
        FROM FundamentacaoPorDistrito fpd
        NATURAL JOIN MaxFundamentacao mf
        WHERE fpd.total = mf.max_total
        ORDER BY fpd.distrito;
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
        ORDER BY quantidadeContratos DESC, TC.tipo, M.municipio;
    ''',
    "p15":
    '''
        WITH MunicipiosSemContratosAltos AS (
            SELECT DISTINCT m.municipio, 
                MAX(c.precoContratual) AS valorMaisProximo
            FROM Municipios m
            NATURAL JOIN LocaisDeExecucao le
            NATURAL JOIN Contratos c
            WHERE m.idMunicipio NOT IN (
                SELECT DISTINCT m2.idMunicipio
                FROM Municipios m2
                NATURAL JOIN LocaisDeExecucao le2
                NATURAL JOIN Contratos c2
                WHERE c2.precoContratual > 1000000
            )
            AND m.municipio IS NOT NULL
            GROUP BY m.municipio
            HAVING MAX(c.precoContratual) IS NOT NULL
        )
        SELECT 
            municipio, 
            valorMaisProximo
        FROM MunicipiosSemContratosAltos
        ORDER BY municipio;
    '''
}

def routing(page, qnt):
    """
    Sets up a route for a given page and query quantity.

    Args:
        page (str): The name of the page.
        qnt (int): The number of query results to fetch (1 for single result, >1 for multiple results).
    """
    def route_func():
        if qnt == 1:
            contratos = db.execute(queries[page]).fetchone()
        else:
            contratos = db.execute(queries[page]).fetchall()
        return render_template(page + '.html', contratos=contratos)
    route_func.__name__ = page  # Ensure unique function name
    if(page == "index"):
        APP.route("/")(route_func)
    else:
        APP.route("/" + page)(route_func)

# INDEX PAGE
routing('index', 1)
# QUESTIONS
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
routing("p14", 2)  
routing("p15", 2)  

# Search by ID
@APP.route('/search')
def search():
    """
    Handles the search functionality by contract ID.

    Returns:
        str: The rendered template with search results or an error message.
    """
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

# FILTROS
@APP.template_filter('to_euro')
def to_euro(value):
    """
    A template filter to format numbers as Euro currency.

    Args:
        value (float): The number to format.

    Returns:
        str: The formatted currency string.
    """
    try:
        return locale.currency(value, symbol=True, grouping=True).replace('$', '€')
    except ValueError:
        return f"{value:.2f} €"







