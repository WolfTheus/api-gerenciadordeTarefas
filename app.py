from flask import Flask, request, jsonify
import sqlite3


app = Flask(__name__)

def conectar():
    return sqlite3.connect('tarefas.db')

def criar_tabela():
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tarefas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tarefa TEXT NOT NULL,
                status TEXT DEFAULT 'pendente'
            )
        ''')
        conn.commit()

@app.route('/tarefas', methods=['GET'])
def listar_tarefas():
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tarefas")
        tarefas = cursor.fetchall()
        tarefasa_formatadas = [{'id': tarefa[0], 'tarefa': tarefa[1], 'status': tarefa[2]} for tarefa in tarefas]
        return jsonify(tarefasa_formatadas)
    
@app.route('/tarefas', methods=['POST'])
def adicionar_tarefa():
    nova_tarefa = request.json.get('tarefa')
    status = request.json.get('status', 'pendente')
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO tarefas (tarefa, status) VALUES (?, ?)", (nova_tarefa, status))
        conn.commit()
        return jsonify({'id': cursor.lastrowid, 'tarefa': nova_tarefa, 'status': status}), 201
        
@app.route('/tarefas/<int:id>', methods=['PUT'])
def atualizar_tarefa(id):
    tarefa_atualizada = request.json.get('tarefa')
    status = request.json.get('status')
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE tarefas SET tarefa = ?, status = ? WHERE id = ?", (tarefa_atualizada, status, id))
        conn.commit()
        return jsonify({'id': id, 'tarefa': tarefa_atualizada, 'status': status})
        
@app.route('/tarefas/<int:id>', methods=['DELETE'])
def deletar_tarefa(id):
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tarefas WHERE id = ?", (id,))
        conn.commit()
        return jsonify({'mensagem': 'Tarefa deletada com sucesso!'}), 204
        
if __name__ == '__main__':
    criar_tabela()
    app.run(debug=True)
        
    

