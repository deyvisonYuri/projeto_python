from Usuario import Usuario
from flask import Flask, request,redirect,url_for

import mysql.connector
app = Flask(__name__)

@app.route('/', methods=['GET'])
def homepage():
    return 'A API esta no ar'

@app.route('/buscarListaFixa', methods=['GET'])
def helps():
    trucks = [
        {'id': 1, 'year': 2016,'make':'Toyota', 'model':'RAV4'}
        ,{'id': 2, 'year': 2017,'make':'Honda', 'model':'MAG2'}
    ]
    return trucks

@app.route('/buscarUsuariosById/<int:id>', methods=['GET'])
def buscarUsuariosById(id: int):
        myList = []
        db = mysql.connector.connect(host='localhost',user='root',password='', db="db_noticias")
        if db.is_connected():
            cursor = db.cursor()
            cursor.execute(f"SELECT * FROM db_noticias.usuario WHERE ID = {id}")
            
            
            for row in cursor.fetchall():
                string = {'id': row[0], 'nome': row[1],'cpf':row[2],'email':row[3],'senha':row[4],'nivel_acesso':row[5]}
                myList.append(string)
            if(len(myList) == 0):
                myList.append('Nao encontrado')
            cursor.close()
            db.close()
        return myList

@app.route('/cadastrarUsuarios', methods=['POST'])
def cadastrarUsuarios():
    request_data = request.get_json()

    nome = request_data['nome']
    cpf = request_data['cpf']
    email = request_data['email']
    senha = request_data['senha']
    nivel_acesso = request_data['nivel_acesso']

    db = mysql.connector.connect(host='localhost',user='root',password='', db="db_noticias")
    if db.is_connected():
        cursor = db.cursor()
        cursor.execute(f"INSERT INTO db_noticias.usuario(nome,cpf,email,senha,nivel_acesso)" f"VALUES('{nome}','{cpf}','{email}','{senha}','{nivel_acesso}')")
        db.commit()
    return 'Cadastrado com Sucesso!'

@app.route('/deletarUsuarios/<int:id>', methods=['DELETE'])
def deletarUsuarios(id: int):
    request_data = request.get_json()

    db = mysql.connector.connect(host='localhost',user='root',password='', db="db_noticias")
    if db.is_connected():
        cursor = db.cursor()
        cursor.execute(f"DELETE FROM db_noticias.usuario WHERE ID = {id}")
        db.commit()
    return 'Deletado com Sucesso!'

@app.route('/atualizarUsuarios/<int:id>', methods=['PUT'])
def atualizarUsuarios(id: int):
    request_data = request.get_json()

    nome = request_data['nome']
    cpf = request_data['cpf']
    email = request_data['email']
    senha = request_data['senha']
    nivel_acesso = request_data['nivel_acesso']

    db = mysql.connector.connect(host='localhost',user='root',password='', db="db_noticias")
    if db.is_connected():
        cursor = db.cursor()
        sql ="UPDATE db_noticias.usuario SET nome = %s,cpf = %s,email = %s,senha = %s,nivel_acesso = %s WHERE id = %s"
        val = (f'{nome}',f'{cpf}',f'{email}',f'{senha}',f'{nivel_acesso}', f'{id}')
        cursor.execute(sql, val)
        db.commit()
    return 'Atualizado com Sucesso!'

@app.route('/buscarUsuarios', methods=['GET'])
def buscarUsuarios():
    try:
        myList = []
        db = mysql.connector.connect(host='localhost',user='root',password='', db="db_noticias")
        if db.is_connected():
            cursor = db.cursor()
            cursor.execute("SELECT * FROM db_noticias.usuario")
            
            
            for row in cursor.fetchall():
                string = {'id': row[0], 'nome': row[1],'cpf':row[2],'email':row[3],'senha':row[4],'nivel_acesso':row[5]}
                myList.append(string)
            if(len(myList) == 0):
                myList.append('Nao encontrado')

            cursor.close()
            db.close()
    except:
        print('Erro, ao conectar')
    return myList
if __name__ == "__main__":
    app.run(host='0.0.0.0')