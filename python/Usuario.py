class Usuario(object):
    def __init__(self, id,nome, cpf,email, senha, nivel_acesso):
        self.id = id;
        self.nome = nome;
        self.cpf = cpf;
        self.email = email;
        self.senha = senha;
        self.nivel_acesso = nivel_acesso;