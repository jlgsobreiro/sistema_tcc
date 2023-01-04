from flask import Flask, jsonify
import pyodbc
from flask_mongoengine import MongoEngine
from mongoengine import *

from models.clientes import Clientes
from models.cobrancas import Cobrancas
from models.objetivo_por_representante import ObjetivoPorRepresentante

app = Flask(__name__)

app.config['MONGODB_SETTINGS'] = {
    "db": "pwanswer",
}

db = MongoEngine(app)


@app.route('/')
def hello_world():
    Clientes().wipe_and_repopulate()
    return Clientes().create_table()


@app.route('/tabela_cobrancas')
def cobrancas_table():
    Cobrancas().wipe_and_repopulate()
    return Cobrancas().create_table()


@app.route('/objetivo_por_representante')
def objetivo_por_representante():
    ObjetivoPorRepresentante().wipe_and_repopulate()
    return ObjetivoPorRepresentante().create_table()


@app.route('/cobrancas')
def cobrancas():  # put application's code here
    Cobrancas().wipe_and_repopulate()
    return Cobrancas().create_table()


if __name__ == '__main__':
    app.run()
