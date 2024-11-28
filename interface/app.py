import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
from flask import render_template, Flask
import logging
import db

APP = Flask(__name__)

# Start page
@APP.route('/')
def index():
    contratos = db.execute('''
        SELECT C.objetoContrato, A1.designacao AS adjudicante, A2.designacao AS adjudicatario, C.precoContratual
        FROM contratos C
        JOIN( SELECT contrato, designacao FROM adjudicantes JOIN entidades on entidade = codigo) A1 on A1.contrato = C.idContrato
        JOIN( SELECT contrato, designacao FROM adjudicatarios JOIN entidades on entidade = codigo) A2 on A2.contrato = C.idContrato
        ;
    ''').fetchall()

    return render_template('index.html',contratos=contratos)




