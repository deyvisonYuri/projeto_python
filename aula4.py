from optparse import Values
import tkinter as tk
from tkinter import ttk
from tkinter.tix import Tree
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
        table= cursor.fetchall()
        print('\n Usuarios: ')

        columns= ('id','nome','sobrenome','cidade','estado','data_nascimento')
        Tree= ttk.Treeview(janelaUsuarios, columns=columns, show= 'headings')

        #define cabeçalhos
        Tree.heading('id',text='#')
        Tree.heading('nome',text= 'nome')
        Tree.heading('sobrenome',text= 'sobrenome')
        Tree.heading('cidade',text='cidade')
        Tree.heading('estado',text='estado')
        Tree.heading('data_nascimento',text='data de nascimento')

        def item_selected(self):
                item= Tree.focus()
        Tree.bind('<<treeviewselect>>', item_selected)
        Tree.grid(row=0, column=0, sticky=tk.NSEW)
        
        #adicionar uma barra de rolagem
        scrollbar= ttk.Scrollbar(janelaUsuarios,orient=tk.VERTICAL,command=Tree.yview)
        Tree.configure(yscroll= scrollbar.set)
        scrollbar.grid(row=0, column=1,sticky='ns')
        usuarios=[]
        for row in table:
                usuarios.append((f'{row[0]}',f'{row[1]}',f'{row[2]}',f'{row[3]}',f'{row[4]}',f'{row[5]}'))

        for user in usuarios:
                Tree.insert('',tk.END,values=user)

        #for row in table:
                


def inserirUsuarios(usuario):
        con=conexao()
        cursor=con.cursor()
        cursor.execute(f"INSERT INTO usuarios(id,nome,sobrenome,cidade,estado,data_nascimento)" f"VALUES('{usuario.id}','{usuario.nome}','{usuario.sobrenome}','{usuario.cidade}','{usuario.estado}','{usuario.data_nascimento}')")
        con.commit()
        desconectar(con)

def abrirTelaUsuarios():
    janelaUsuarios = tk.Toplevel(app)
    selecionarUsuarios(janelaUsuarios)

    lblid=tk.Label(janelaUsuarios,text="informe o Id:"
                ,font="times"
                ,bg="white",foreground="black")
    lblid.place(x=100,y=230)
    entryid=tk.Entry(janelaUsuarios)
    entryid.place(x=230,y=235)

    lblNome = tk.Label(janelaUsuarios,text="Informe o seu nome: "

            ,font="Times"
            ,bg="white",foreground="black")
    lblNome.place(x=100,y=250)
    entryNome = tk.Entry(janelaUsuarios)
    entryNome.place(x=230,y=255)
    
    lblSobrenome = tk.Label(janelaUsuarios,text="Informe o seu sobrenome: "
            ,font="Times"
            ,bg="white",foreground="black")
    lblSobrenome.place(x=100,y=275)
    entrySobrenome = tk.Entry(janelaUsuarios)
    entrySobrenome.place(x=260, y=275)

    lblDataNascimento = tk.Label(janelaUsuarios,text="Informe sua data de nascimento"
            ,font="Times"
            ,bg="white", foreground="black")
    lblDataNascimento.place(x=100, y=300)
    entryDataNascimento = tk.Entry(janelaUsuarios)
    entryDataNascimento.place(x=300, y=300)

    lblCidade = tk.Label(janelaUsuarios,text="Informe a sua cidade"
            ,font="Times"
            ,bg="white", foreground="black")
    lblCidade.place(x=100,y=325)
    entryCidade = tk.Entry(janelaUsuarios)
    entryCidade.place(x=230,y=325)

    lblEstado = tk.Label(janelaUsuarios, text="Informe o estado: "
            ,font="Times"
            ,bg="white",foreground="black")
    lblEstado.place(x=100, y=350)
    entryEstado = tk.Entry(janelaUsuarios)
    entryEstado.place(x=230, y=350)
    
    def salvarUsuario():
        conn = conexao()
        Usuario= Usuarios(None,entryNome.get(),entrySobrenome.get(),entryCidade.get(),entryEstado.get(),entryDataNascimento.get())
        inserirUsuarios(Usuario)
        #print("O nome informado foi: ",entryNome.get())
        #print("O sobrenome informado foi: ", entrySobrenome.get())
        #print("A data de nascimento informada foi: ", entryDataNascimento.get())
        #print("A cidade informada foi: ", entryCidade.get())
        #print("O estado informado foi: ",entryEstado.get())
    btnSalvar = tk.Button(janelaUsuarios,width=20
            ,text="Salvar", command=salvarUsuario)
    btnSalvar.place(x=100,y=400)
    
    #entryNome.insert("end","teste")
    #entryNome.insert("end","tormes")
    
    janelaUsuarios.title("Cadastro de Usuários")
    janelaUsuarios.geometry("800x600")
def abrirTelaProdutos():
    janelaProduto = tk.Toplevel(app)
    janelaProduto.title("Cadastro de Produtos")
    janelaProduto.geometry("800x600")
app = tk.Tk()
menuPrincipal = tk.Menu(app)
app.config(menu=menuPrincipal)

fileMenu = tk.Menu(menuPrincipal)
fileMenu.add_command(label="Cadastrar Usuários"
            ,command=abrirTelaUsuarios)
fileMenu.add_command(label="Cadastrar Produtos"
            ,command=abrirTelaProdutos)
menuPrincipal.add_cascade(label="Funcao"
                        ,menu=fileMenu)

#buttonExample = tk.Button(app, 
#              text="Create new window",
#              command=createNewWindow)
#buttonExample.place(x=100,y=50)
app.title("Sistema Tarumã")
app.geometry("800x600")

app.mainloop()
app.destroy()