# Usa uma imagem leve do Python
FROM python:3.11-slim

# Define diretório de trabalho
WORKDIR /app

# Instala dependências do sistema necessárias para compilar psycopg2
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copia arquivos de dependências se existir (requirements.txt)
COPY requirements.txt .

# Instala pacotes Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do código
COPY . .

# Expõe a porta que o Flask vai rodar
EXPOSE 5000

# Usa Gunicorn como servidor WSGI (melhor para produção)
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
