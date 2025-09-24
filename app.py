from flask import Flask, request, render_template
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime
import pytz
import os
from dotenv import load_dotenv

# ----------------- Configura variáveis de ambiente -----------------
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")  # URL do banco

app = Flask(__name__)

def get_connection():
    return psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)

@app.route("/aceite", methods=["GET", "POST"])
def aceite():
    token = request.args.get("token")
    if not token:
        return "Token não fornecido."

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, nome, email, status, html_contrato FROM aceite WHERE token = %s", (token,))
    row = cur.fetchone()

    if not row:
        conn.close()
        return "Token inválido ou expirado."

    user_id = row["id"]
    nome = row["nome"]
    email = row["email"]
    status = row["status"]
    contrato_html = row["html_contrato"] or "<p>Contrato não disponível.</p>"

    # Fuso horário de Brasília
    brasilia_tz = pytz.timezone('America/Sao_Paulo')
    hora_agora_brasilia = datetime.now(brasilia_tz)

    # Atualiza status para 'aceito' se o usuário enviar POST
    if request.method == "POST" and status != "aceito":
        ip = request.headers.get('X-Forwarded-For', request.remote_addr).split(',')[0].strip()
        hora_agora_utc = hora_agora_brasilia.astimezone(pytz.utc)

        cur.execute(
            "UPDATE aceite SET status = 'aceito', data_hora = %s, ip = %s WHERE id = %s",
            (hora_agora_utc, ip, user_id)
        )
        conn.commit()
        status = "aceito"

    conn.close()

    # Renderiza o template 'aceite.html'
    return render_template(
        "aceite.html",
        nome=nome,
        email=email,
        status=status,
        contrato_html=contrato_html,
        hora_agora=hora_agora_brasilia.strftime("%d/%m/%Y %H:%M:%S")
    )