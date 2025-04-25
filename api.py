from flask import Flask, jsonify
from flask_cors import CORS
from apscheduler.schedulers.background import BackgroundScheduler
from weather_data import atualizar_dados

import sqlite3

app = Flask(__name__)
CORS(app)
DB_NAME = 'clima.db'

# Agendador
scheduler = BackgroundScheduler()

# Roda a cada 1 horas 
scheduler.add_job(func=atualizar_dados, trigger="interval", hours=1)

scheduler.start()

# Função para conectar ao banco e buscar dados
def query_db(query, args=(), one=False):
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(query, args)
    results = cur.fetchall()
    conn.close()
    return (results[0] if results else None) if one else results

# Endpoint 1 – Retorna TODAS as previsões
@app.route("/previsoes", methods=["GET"])
def todas_as_previsoes():
    rows = query_db("SELECT * FROM previsoes ORDER BY estado, data")
    dados = [dict(row) for row in rows]
    return jsonify(dados)

# Endpoint 2 – Retorna previsões de um estado específico
@app.route("/previsoes/<estado>", methods=["GET"])
def previsao_por_estado(estado):
    rows = query_db("SELECT * FROM previsoes WHERE estado = ? ORDER BY data", (estado,))
    if not rows:
        return jsonify({"erro": "Estado não encontrado"}), 404
    dados = [dict(row) for row in rows]
    return jsonify(dados)

if __name__ == "__main__":
    app.run(debug=True)
