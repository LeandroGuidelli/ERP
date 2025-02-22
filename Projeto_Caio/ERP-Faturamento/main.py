from flask import Flask, render_template, request, jsonify
import mysql.connector

app = Flask(__name__, static_folder="static", template_folder="templates")

def init_db():
    """Inicializa o banco de dados e a tabela, se não existirem"""
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="123456"
    )

    cursor = conn.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS sistema_nf")
    conn.close()

    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="123456",
        database="sistema_nf"
    )

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notas_fiscais (
            id INT AUTO_INCREMENT PRIMARY KEY,
            numero_nota VARCHAR(50) NOT NULL,
            data_nota DATE NOT NULL,
            deposito VARCHAR(100) NOT NULL,
            dia_lancamento DATETIME DEFAULT NOW()
        )
    """)

    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/adicionar_nf', methods=['POST'])
def adicionar_nf():
    """Recebe os dados do formulário e insere no banco de dados"""
    try:
        data_nota = request.form.get('data')
        deposito = request.form.get('deposito')
        numero_nf = request.form.get('numero_nf')

        if not data_nota or not deposito or not numero_nf:
            return jsonify({"erro": "Todos os campos são obrigatórios!"}), 400

        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="123456",
            database="sistema_nf"
        )

        cursor = conn.cursor()
        cursor.execute("INSERT INTO notas_fiscais (numero_nota, data_nota, deposito) VALUES (%s, %s, %s)", 
                       (numero_nf, data_nota, deposito))

        conn.commit()
        conn.close()

        return jsonify({"mensagem": "Nota fiscal adicionada com sucesso!"})

    except Exception as e:
        return jsonify({"erro": f"Erro ao salvar no banco: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
