import datetime
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
from flask import render_template, Flask, request
import db
import locale
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8') 

APP = Flask(__name__)

# Start page
@APP.route('/')
def index():
    contratos = db.execute('''
        SELECT count(*) as n_contratos, sum(precoContratual) as valor_total
        FROM contratos;
    ''').fetchone()

    return render_template('index.html',contratos=contratos)

@APP.route('/p1')
def p1():
    tipos = db.execute('''
        SELECT tipo
        FROM TiposContratos
        ORDER BY tipo;
    ''').fetchall()

    return render_template('questions/p1.html',tipos=tipos)

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


@APP.route('/search')
def search():
    id = request.args.get('id')
    if id:
        data = db.execute(''' 
            SELECT idContrato , objetoContrato, precoContratual
            FROM contratos 
            WHERE idContrato = ?''', [id]).fetchone()
    if data:
        return render_template('search_result.html', data=data)
    else:
        return "Id não encontrado."

# FILTROS
@APP.template_filter('to_euro')
def to_euro(value):
    try:
        return locale.currency(value, symbol=True, grouping=True).replace('$', '€')
    except ValueError:
        return f"{value:.2f} €"







