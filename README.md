# 🌤️ Previsão do Tempo - API + Frontend

Este projeto é uma aplicação web simples que consulta a **previsão do tempo para os 27 estados brasileiros** por meio da **WeatherAPI**, armazena os dados em um banco de dados **SQLite**, e exibe essas previsões em uma interface web desenvolvida com **Bootstrap**.

---

## 📸 Demonstração

![Demo](https://github.com/IgorBarcelo/previsao-do-tempo-api/blob/main/public/demo.png?raw=true)

## 🛠️ Tecnologias Utilizadas

- Python 3.11+
- Flask
- SQLite
- Requests
- APScheduler (agendamento de tarefas)
- HTML + Bootstrap (frontend)

---

## 🔧 Funcionalidades

### API (Flask)
- `GET /previsoes` — Lista todas as previsões do banco.
- `GET /previsoes/<estado>` — Retorna previsões de um estado específico.
- `GET /previsoes/<estado>/<data>` — Retorna a previsão de um estado em uma data específica.
- `DELETE /previsoes?estado=UF&data=YYYY-MM-DD` — Exclui uma previsão por estado e data.

### Agendamento
- A API busca automaticamente novas previsões a cada 1 hora e atualiza o banco de dados.

### Frontend
- Seleção de estado via dropdown.
- Exibição em tabela com:
  - Data formatada (ex: `25 sexta-feira`)
  - Temperaturas mínima e máxima
  - Condição do tempo e ícone
- Responsivo e intuitivo.

---

## 📦 Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/seuusuario/previsao-tempo.git
   cd previsao-tempo
   ```

2. Crie um ambiente virtual e ative:
   ```bash
   python -m venv venv
   source venv/bin/activate  # ou venv\Scripts\activate no Windows
   ```

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

4. Defina sua API key no arquivo `weather_data.py`:
   ```python
   API_KEY = 'SUA_CHAVE_WEATHERAPI'
   ```

5. Execute a API:
   ```bash
   python app.py
   ```

---

## 🗃️ Estrutura dos Arquivos

```
├── app.py                # API Flask + Agendador
├── weather_data.py       # Funções de ETL e consumo da API
├── clima.db              # Banco de dados SQLite (gerado automaticamente)
├── index.html            # Interface web com Bootstrap
└── README.md             # Este arquivo
```

---

## 🚀 Exemplo de Uso

### No navegador:
```
http://localhost:5500
```

### Com Insomnia / Postman:
- `GET http://localhost:5000/previsoes`
- `GET http://localhost:5000/previsoes/São Paulo`
- `DELETE http://localhost:5000/previsoes?estado=São Paulo&data=2025-04-25`

---

## Créditos
Desenvolvido por [Igor Barcelo](https://www.linkedin.com/in/igor-barcelo-631010216/)
