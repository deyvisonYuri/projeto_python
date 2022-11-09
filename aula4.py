import tkinter as tk
from tkinter import ttk
import mysql.connector
from tkinter.messagebox import showinfo
#pip install mysql-connector

class Usuarios:
        def __init__(self, id, nome,sobrenome,cidade,estado,data_nascimento):
                self.id = id
                self.nome = nome
                self.sobrenome = sobrenome
                self.cidade = cidade
                self.estado = estado
                self.data_nascimento = data_nascimento


def conexao():
        try:
                conexao = mysql.connector.connect(
                        host = "localhost",
                        user = "root",
                        passwd = "",
                        db = "banco_python"
                )
                print("conectado")
                return conexao
        except mysql.connector.Error as e:
                print(f'Erro ao conectar no Servidor MySql: {e}')

def desconectar(conexao):
        if conexao:
                conexao.close()

def selecionarUsuarios(janelaUsuarios):
        conn = conexao()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuarios")
        table = cursor.fetchall()
        print('\n Usuarios: ')

        columns = ('id','nome','sobrenome','cidade','estado','data_nascimento')
        tree = ttk.Treeview(janelaUsuarios, columns=columns, show='headings')

        #define cabeçalhos
        tree.heading('id',text='#')
        tree.heading('nome',text='Nome')
        tree.heading('sobrenome', text='Sobrenome')
        tree.heading('cidade',text='Cidade')
        tree.heading('estado',text='Estado')
        tree.heading('data_nascimento',text='Data de Nascimento')
        
        def item_selected(self):
                item = tree.focus()

                global id_usuario
                global nome_usuario
                global sobrenome_usuario
                global cidade_usuario
                global estado_usuario
                global data_usuario

                id_usuario.set(tree.item(item)["values"][0])
                nome_usuario.set(tree.item(item)["values"][1])
                sobrenome_usuario.set(tree.item(item)["values"][2])
                cidade_usuario.set(tree.item(item)["values"][3])
                estado_usuario.set(tree.item(item)["values"][4])
                data_usuario.set(tree.item(item)["values"][5])

        tree.bind('<<TreeviewSelect>>', item_selected)
        tree.grid(row=0, column=0, sticky=tk.NSEW)

        #adicionar uma barra de rolagem
        scrollbar = ttk.Scrollbar(janelaUsuarios, orient=tk.VERTICAL,command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=0, column=1,sticky='ns')

        usuarios = []
        for row in table:
                usuarios.append((f'{row[0]}', f'{row[1]}', f'{row[2]}', f'{row[3]}', f'{row[4]}', f'{row[5]}'))
        
        for user in usuarios:
                tree.insert('',tk.END,values=user)
def inserirUsuarios(usuario):
        con = conexao()
        cursor = con.cursor()
        cursor.execute(
        f"INSERT INTO usuarios(id, nome, sobrenome, cidade, estado, data_nascimento)" 
        f"VALUES('{usuario.id}','{usuario.nome}','{usuario.sobrenome}','{usuario.cidade}','{usuario.estado}','{usuario.data_nascimento}')")
        con.commit()
        desconectar(con)

def abrirTelaUsuarios():
    janelaUsuarios = tk.Toplevel(app)
    selecionarUsuarios(janelaUsuarios)

    lblId = tk.Label(janelaUsuarios,text="Informe o Id: "
                        , font="Times"
                        ,foreground="black")
    lblId.place(x=100, y=230)

    entryId = tk.Entry(janelaUsuarios, textvariable=id_usuario)
    entryId.place(x=230,y=235)

    lblNome = tk.Label(janelaUsuarios,text="Informe o seu nome: "
            ,font="Times"
            ,bg="white",foreground="black")
    lblNome.place(x=100,y=250)

    entryNome = tk.Entry(janelaUsuarios, textvariable=nome_usuario)
    entryNome.place(x=230,y=255)
    
    lblSobrenome = tk.Label(janelaUsuarios,text="Informe o seu sobrenome: "
            ,font="Times"
            ,bg="white",foreground="black")
    lblSobrenome.place(x=100,y=275)

    entrySobrenome = tk.Entry(janelaUsuarios, textvariable=sobrenome_usuario)
    entrySobrenome.place(x=260, y=275)

    lblDataNascimento = tk.Label(janelaUsuarios,text="Informe sua data de nascimento"
            ,font="Times"
            ,bg="white", foreground="black")
    lblDataNascimento.place(x=100, y=300)

    entryDataNascimento = tk.Entry(janelaUsuarios, textvariable=data_usuario)
    entryDataNascimento.place(x=300, y=300)

    lblCidade = tk.Label(janelaUsuarios,text="Informe a sua cidade"
            ,font="Times"
            ,bg="white", foreground="black")
    lblCidade.place(x=100,y=325)

    entryCidade = tk.Entry(janelaUsuarios, textvariable=cidade_usuario)
    entryCidade.place(x=230,y=325)

    lblEstado = tk.Label(janelaUsuarios, text="Informe o estado: "
            ,font="Times"
            ,bg="white",foreground="black")
    lblEstado.place(x=100, y=350)
    
    entryEstado = tk.Entry(janelaUsuarios, textvariable=estado_usuario)
    entryEstado.place(x=230, y=350)
    
    def salvarUsuario():
        usuario = Usuarios(None, entryNome.get(), entrySobrenome.get(),entryCidade.get(),
        entryEstado.get(), entryDataNascimento.get())
        inserirUsuarios(usuario)
        selecionarUsuarios(janelaUsuarios)

    def deletarUsuarios():
        con = conexao()
        if(entryId.get()):
                cursor = con.cursor()
                sql = f"DELETE FROM usuarios where id = {entryId.get()}"
                cursor.execute(sql)
                con.commit()
                selecionarUsuarios(janelaUsuarios)
        else:
                showinfo(title='Informação', message='Erro, Id não informado')
    
    def atualizarUsuarios():
        con = conexao()
        if(entryId.get()):
                usuario = Usuarios(None, entryNome.get(), entrySobrenome.get()
                ,entryCidade.get(), entryEstado.get(), entryDataNascimento.get())
                cursor = con.cursor()
                sql = "UPDATE usuarios set nome = %s, sobrenome = %s, cidade = %s, estado = %s, data_nascimento = %s WHERE id = %s"
                val = (f'{usuario.nome}',f'{usuario.sobrenome}', f'{usuario.cidade}')
    btnSalvar = tk.Button(janelaUsuarios,width=20
            ,text="Salvar", command=salvarUsuario)
    btnSalvar.place(x=100,y=375)

    btnAtualizar = tk.Button(janelaUsuarios,width=20,text='Atualizar'
      , command=deletarUsuarios, state= tk.ACTIVE)
    btnAtualizar.place(x=250,y=375)

    btnDeletar = tk.Button(janelaUsuarios,width=20,text='Deletar'
    ,command=deletarUsuarios, state=tk.ACTIVE)
    btnDeletar.place(x=400,y=375)
    
    #entryNome.insert("end","teste")
    #entryNome.insert("end","tormes")
    
    janelaUsuarios.title("Cadastro de Usuários")
    janelaUsuarios.geometry("800x600")
def abrirTelaProdutos():
    janelaProduto = tk.Toplevel(app)
    janelaProduto.title("Cadastro de Produtos")
    janelaProduto.geometry("800x600")

app = tk.Tk()

id_usuario = tk.StringVar()
nome_usuario = tk.StringVar()
sobrenome_usuario = tk.StringVar()
cidade_usuario = tk.StringVar()
estado_usuario = tk.StringVar()
data_usuario = tk.StringVar()


menuPrincipal = tk.Menu(app)
app.config(menu=menuPrincipal)

fileMenu = tk.Menu(menuPrincipal)
fileMenu.add_command(label="Cadastrar Usuários"
            ,command=abrirTelaUsuarios)
fileMenu.add_command(label="Cadastrar Produtos"
            ,command=abrirTelaProdutos)
menuPrincipal.add_cascade(label="Funcao"
                        ,menu=fileMenu)


app.title("Sistema Tarumã")
app.geometry("800x600")

app.mainloop()
#app.destroy()