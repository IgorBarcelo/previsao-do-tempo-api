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

# Roda a cada 1 hora 
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

# Endpoint 1 – Retorna TODAS as previsões/ por <estato> & por <data>
from flask import request

@app.route("/previsoes", methods=["GET"])
def buscar_previsoes():
    estado = request.args.get("estado")
    data = request.args.get("data")

    query = "SELECT * FROM previsoes"
    params = []

    if estado and data:
        query += " WHERE estado = ? AND data = ?"
        params = [estado, data]
    elif estado:
        query += " WHERE estado = ?"
        params = [estado]
    elif data:
        query += " WHERE data = ?"
        params = [data]

    query += " ORDER BY estado, data"

    rows = query_db(query, params)
    dados = [dict(row) for row in rows]
    return jsonify(dados)

# Endpoint 2 - deleta uma previsão se receber <estado> & <data>
@app.route("/previsoes", methods=["DELETE"])
def deletar_previsao():
    estado = request.args.get("estado")
    data = request.args.get("data")

    if not estado or not data:
        return jsonify({"erro": "Informe o estado e a data para exclusão"}), 400

    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("DELETE FROM previsoes WHERE estado = ? AND data = ?", (estado, data))
    conn.commit()
    deletados = cur.rowcount
    conn.close()

    if deletados == 0:
        return jsonify({"mensagem": "Nenhum registro encontrado para exclusão"}), 404
    return jsonify({"mensagem": f"{deletados} registro(s) excluído(s) com sucesso"}), 200

if __name__ == "__main__":
    app.run(debug=True)
