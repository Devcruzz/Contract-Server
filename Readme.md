# 📑 Aplicação de Aceite de Contrato Digital

Este projeto automatiza o processo de **visualização e aceite de contratos digitais**. A aplicação permite que os usuários visualizem um contrato, aceitem os termos e gravem o aceite em um banco de dados **PostgreSQL**. O fluxo é simples: um usuário acessa um link com um **token único**, visualiza o contrato e o aceita, e o sistema registra o aceite com a data, hora e IP do usuário.

## 🚀 Funcionalidades  

- Exibição do contrato em **HTML** a partir de um modelo armazenado no banco de dados.
- Registro de aceite de contrato com **token único** para cada usuário.
- Armazenamento das informações no banco de dados **PostgreSQL**.
- Redirecionamento automático para página de agradecimento após aceite.
- Geração de timestamps e registro de IP para controle e rastreabilidade.
- Uso de **variáveis de ambiente** (`.env`) para proteger informações sensíveis.

## 🛠️ Tecnologias Utilizadas  

- **Python 3.x**
- [Flask](https://flask.palletsprojects.com/) → Framework para construção da aplicação web
- [psycopg2](https://www.psycopg.org/) → Biblioteca para interação com PostgreSQL
- [python-dotenv](https://pypi.org/project/python-dotenv/) → Gerenciamento de variáveis de ambiente
- [pytz](https://pypi.org/project/pytz/) → Manipulação de fusos horários
- **HTML5** → Formatação e exibição do contrato e das páginas de interação

## 📂 Estrutura de Pastas

```
📦 projeto
├── 📂 templates
│ ├── aceite.html # Template para exibir o contrato e aceitar
│ ├── obrigado.html # Template de agradecimento após aceite
├── .env # Variáveis de ambiente (ignorado no git)
├── appy.py # Código principal (backend)
├── requirements.txt # Dependências do projeto
└── README.md # Este arquivo
```


## ⚙️ Configuração

### 1️⃣ Pré-requisitos
- [Python 3.x](https://www.python.org/)
- Banco de dados **PostgreSQL**

### 2️⃣ Instalar dependências

Para instalar as dependências do projeto, execute o comando:

```bash
pip install -r requirements.txt
```

## 3️⃣ Configurar variáveis de ambiente (`.env`)

Crie um arquivo `.env` na raiz do projeto e defina a variável de ambiente `DATABASE_URL` com a URL de conexão do banco de dados:

```env
DATABASE_URL=postgresql://usuario:senha@localhost:5432/nome_do_banco
```

## ▶️ Execução

Para rodar a aplicação localmente, execute o seguinte comando:

```bash
python appy.py
```

A aplicação estará disponível em http://localhost:5000

## 🗄️ Estrutura da Tabela no PostgreSQL

O banco de dados utiliza uma tabela chamada `aceite` com a seguinte estrutura:

```sql
CREATE TABLE IF NOT EXISTS aceite (
    id SERIAL PRIMARY KEY,
    nome TEXT NOT NULL,
    email TEXT NOT NULL,
    status TEXT DEFAULT 'pendente',
    data_hora TIMESTAMP,
    ip TEXT,
    html_contrato TEXT,
    token TEXT UNIQUE NOT NULL
);
```

- **id**: Identificador único do usuário.
- **nome**: Nome do usuário.
- **email**: E-mail do usuário.
- **status**: Status do contrato (pendente ou aceito).
- **data_hora**: Data e hora em que o contrato foi aceito.
- **ip**: IP do usuário no momento do aceite.
- **html_contrato**: Conteúdo do contrato em formato HTML.
- **token**: Token único associado ao usuário.

## 📜 Fluxo do Sistema

1. O usuário acessa a rota `/aceite?token=<TOKEN_DO_USUARIO>`.
2. A aplicação consulta o banco de dados e exibe o contrato HTML com as informações do usuário.
3. O usuário marca a checkbox "Li e concordo com os termos do contrato" e clica em "Enviar".
4. O status do contrato é atualizado para "aceito" no banco de dados, juntamente com a data, hora e IP do usuário.
5. O usuário é redirecionado para a página `/obrigado`, agradecendo pela ação.

## 🐳 Docker — Execução Isolada

Se você quiser rodar a aplicação em um container Docker, crie a imagem com o seguinte comando:

### 🚀 Passo a Passo

1. **Criar a Imagem Docker**

No diretório do projeto, execute:
```bash
docker build -t aceite-contrato .
```
2. **Rodar o Container**

Após criar a imagem, execute o container com:

```bash
docker run --rm -it -p 5000:5000 aceite-contrato
```

3. **Acessar a Aplicação**

A aplicação estará disponível em [http://localhost:5000](http://localhost:5000) dentro do container Docker.

## ⚙️ Detalhes dos Arquivos

### 1. `appy.py`

O arquivo principal do backend, que contém:

- **Conexão com o banco de dados**: Utiliza a biblioteca `psycopg2`.
- **Rota `/aceite`**: Exibe o contrato e processa o aceite do usuário.
- **Rota `/obrigado`**: Exibe a página de agradecimento após o aceite.

### 2. `aceite.html`

Template HTML que exibe o contrato e permite que o usuário aceite os termos.

- **Checkbox de Concordância**: O usuário deve marcar a checkbox para habilitar o botão de envio.
- **Botão de Envio**: O botão só é habilitado quando o usuário marca a checkbox. Envia uma requisição `POST` para registrar o aceite.

### 3. `obrigado.html`

Template HTML exibido após o aceite do contrato. Ele contém a mensagem de agradecimento ao usuário pela ação.


