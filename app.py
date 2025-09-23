from flask import Flask, request, render_template
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime
import os

app = Flask(__name__)

# Pega a URL do banco de dados do Render (configurada nas variáveis de ambiente)
DATABASE_URL = os.getenv("DATABASE_URL")

def get_connection():
    return psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)

@app.route("/aceite", methods=["GET", "POST"])
def aceite():
    token = request.args.get("token")
    if not token:
        return "Token não fornecido."

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, nome, email, status, pdf_base64 FROM aceite WHERE token = %s", (token,))
    row = cur.fetchone()

    if not row:
        conn.close()
        return "Token inválido ou expirado."

    user_id = row["id"]
    nome = row["nome"]
    email = row["email"]
    status = row["status"]
    pdf_base64 = row["pdf_base64"]

    # Atualiza status para 'aceito' se o usuário enviar POST
    if request.method == "POST" and status != "aceito":
        ip = request.headers.get('X-Forwarded-For', request.remote_addr).split(',')[0].strip()
        cur.execute(
            "UPDATE aceite SET status = 'aceito', data_hora = %s, ip = %s WHERE id = %s",
            (datetime.now(), ip, user_id)
        )
        conn.commit()
        status = "aceito"

    conn.close()
    
    # Passa o PDF Base64 para o template
    return render_template(
        "aceite.html",
        nome=nome,
        email=email,
        status=status,
        pdf_base64=pdf_base64
    )
