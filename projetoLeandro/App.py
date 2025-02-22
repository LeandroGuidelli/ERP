from flask import Flask, jsonify, render_template, request, redirect, url_for
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)

CORS(app)

def create_connection():
    return mysql.connector.connect (
        host="localhost",
        user="root",
        password="123456",
        database="financeiro"
    )
@app.route("/")
def index():
    conexao = create_connection()
    cursor = conexao.cursor(dictionary=True)
    cursor.execute("SELECT * FROM transacao")
    transacoes = cursor.fetchall()
    cursor.close()
    conexao.close()

    # Calcular saldo
    # Calcular saldo considerando a quantidade
    # Calcular saldo começando com 1000 e considerando a quantidade
    saldo_inicial = 1000
    saldo = saldo_inicial + sum(
        (t["valor"] * t["quantidade"]) if t["tipo"] == "receita" else -(t["valor"] * t["quantidade"]) 
        for t in transacoes
    )

    return render_template("index.html", transacoes=transacoes, saldo=saldo)

# Rota para adicionar uma nova transação
@app.route("/adicionar", methods=["GET", "POST"])
def adicionar():
    if request.method == "POST":
        descricao = request.form["descricao"]
        produto = request.form["produto"]
        quantidade = request.form["quantidade"]
        valor = float(request.form["valor"])
        tipo = request.form["tipo"]

        conexao = create_connection()
        cursor = conexao.cursor()
        sql = "INSERT INTO transacao (descricao, produto, quantidade, valor, tipo) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(sql, (descricao, produto, quantidade, valor, tipo))
        conexao.commit()
        cursor.close()
        conexao.close()

        return redirect(url_for("index"))

    return render_template("adicionar.html")

if __name__ == '__main__':
    app.run(debug=True)