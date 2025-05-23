import requests
import sqlite3

API_KEY = 'SUA_CHAVE_WEATHERAPI'
BASE_URL = 'http://api.weatherapi.com/v1/forecast.json'

estados = ["Acre","Alagoas","Amapa","Amazonas","Bahia","Ceará","Distrito Federal","Espírito Santo","Goiás","Maranhão",
"Mato Grosso","Mato Grosso do Sul","Minas Gerais","Pará","Paraíba","Paraná","Pernambuco","Piauí","Rio de Janeiro",
"Rio Grande do Norte","Rio Grande do Sul","Rondônia","Roraima","Santa Catarina","São Paulo","Sergipe","Tocantins",
]

# Extrai dados da API Weather API
def extrair_dados(estado):
    parametros = {
        'key': API_KEY,
        'q': estado,
        'days': 4,
        'lang': 'pt'
    }
    resposta = requests.get(BASE_URL, params=parametros)
    return resposta.json()

# Cria array com apenas os dados necessarios
def transformar_dados(json, estado):
    previsoes = []
    for dia in json['forecast']['forecastday']:
        previsoes.append({
            'estado': estado,
            'data': dia['date'],
            'temperatura_maxima': dia['day']['maxtemp_c'],
            'temperatura_minima': dia['day']['mintemp_c'],
            'condicao': dia['day']['condition']['text'],
            'img': dia['day']['condition']['icon']
        })
    return previsoes

#cria a tabela previsoes no banco
def criar_tabela():
    conn = sqlite3.connect("clima.db")
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS previsoes (
            estado TEXT,
            data TEXT,
            temperatura_maxima REAL,
            temperatura_minima REAL,
            condicao TEXT,
            img TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Carrega os dados na tabela previsoes
def carregar_dados(previsoes):
    conn = sqlite3.connect("clima.db")
    c = conn.cursor()
    for p in previsoes:
        c.execute('''
            INSERT INTO previsoes (estado, data, temperatura_maxima, temperatura_minima, condicao, img)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (p['estado'], p['data'], p['temperatura_maxima'], p['temperatura_minima'], p['condicao'], p['img']))
    conn.commit()
    conn.close()

# Deleta dados antigos e inseri novos obtidos pela API
def atualizar_dados():
    criar_tabela()
    conn = sqlite3.connect("clima.db")
    c = conn.cursor()
    c.execute("DELETE FROM previsoes")
    conn.commit()
    conn.close()

    for estado in estados:
        try:
            json = extrair_dados(estado)
            previsoes = transformar_dados(json, estado)
            carregar_dados(previsoes)
            print(estado, 'carregado')
        except Exception as e:
            print(f"Erro no estado {estado}: {e}")


if __name__ == "__main__":
    atualizar_dados()