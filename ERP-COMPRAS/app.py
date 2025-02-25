from flask import Flask, render_template, request, jsonify
from tinydb import TinyDB, Query

app = Flask(__name__)

db = TinyDB('estoque.json')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/estoque', methods=['GET'])
def obter_estoque():
    registros = db.all()
    estoque = {}
    
    for registro in registros:
        material = registro['material']
        quantidade = registro['quantidade']
        
        if material in estoque:
            estoque[material] += quantidade
        else:
            estoque[material] = quantidade
            
    return jsonify(estoque)

@app.route('/adicionar_compra', methods=['POST'])
def adicionar_compra():
    dados = request.json
    material = dados.get('material')
    quantidade = int(dados.get('quantidade'))
    
    if material and quantidade > 0:
        db.insert({'material': material, 'quantidade': quantidade})
        return jsonify({"mensagem": "Compra adicionada com sucesso!"})
    
    return jsonify({"erro": "Dados inválidos!"}), 400

@app.route('/retirar_estoque', methods=['POST'])
def retirar_estoque():
    dados = request.json
    material = dados.get('material')
    quantidade = int(dados.get('quantidade'))
    
    if material and quantidade > 0:
        registro = Query()
        item = db.search(registro.material == material)
        
        if item:
            estoque_atual = item[0]['quantidade']
            if estoque_atual >= quantidade:
                db.update({'quantidade': estoque_atual - quantidade}, registro.material == material)
                if estoque_atual - quantidade == 0:
                    db.remove(registro.material == material)
                return jsonify({"mensagem": "Retirada realizada com sucesso!"})
            else:
                return jsonify({"erro": "Quantidade insuficiente!"}), 400
        else:
            return jsonify({"erro": "Material não encontrado!"}), 400

    return jsonify({"erro": "Dados inválidos!"}), 400

if __name__ == '__main__':
    app.run(debug=True)
