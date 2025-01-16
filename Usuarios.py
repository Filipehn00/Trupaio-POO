import sqlite3, bcrypt
#Usuários salvos e as sublcasses de usuários
class Usuario:
    def __init__(self, nome, funcao, login, senha): #Construtor da classe com seus atributos
        self.nome = nome
        self.funcao = funcao
        self.login = login
        self.senha = senha

    def autenticar(self, senha):
        return bcrypt.checkpw(senha.encode('utf-8'), self.senha.encode('utf-8') if isinstance(self.senha, str) else self.senha)



    @classmethod
    def to_dict(self): #Salva funcionários no dicionário
        return {
            "tipo": self.__class__.__name__,
            "nome": self.nome,
            "funcao": self.funcao,
            "login": self.login,
            "senha": self.senha,
        }
    
    @staticmethod
    def verificar_login(login, senha, db_name="almoxarifado.db"):
        """Verifica o login e a senha de um usuário."""
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()

        cursor.execute("SELECT senha FROM usuarios WHERE login = ?", (login,))
        result = cursor.fetchone()

        if result:
            senha_hash = result[0]
            # Verifica a senha usando bcrypt
            if bcrypt.checkpw(senha.encode('utf-8'), senha_hash):
                conn.close()
                return True

        conn.close()
        return False

    @classmethod
    def from_dict(classe, data): #Puxa os Funcionários do dicionário
        tipo = data.pop("tipo")
        #Dependendo do tipo de funcionário adicionado, cria a subclasse de usuário
        if tipo == "Administrador":
            return Administrador(**data)
        elif tipo == "Enfermeiro":
            return Enfermeiro(**data)
        elif tipo == "Farmaceutico":
            return Farmaceutico(**data)
        elif tipo == "AuxServicosGerais":
            return AuxServicosGerais(**data)
        else:
            return classe(**data)


class Administrador(Usuario): #ADM
    #Somente o adm tem os métdos que adicionam ou removem usuários.
    def cadastrar_usuario(self, usuarios): 
        print("\nEscolha a função do usuário a ser cadastrado:")
        print("1) Enfermeiro")
        print("2) Farmacêutico")
        print("3) Auxiliar de Serviços Gerais")
        tipo_usuario = input("Escolha uma opção: ")

        if tipo_usuario not in ["1", "2", "3"]:
        #Um usuário só é adicionado se ele for Enfermeiro, Farmacêutico, ou Auxiliar de Serviços Gerais
            input("Opção inválida! Pressione enter para retornar ao menu...")
            return
        
        nome = input("Nome do novo usuário: ")
        if(nome != ""): #Verifica se o nome é vazio. Se for, volta para o menu
            login = input("Login: ")
            if(login != ""): #Verifica se o login é vazio. Se for, volta para o menu
                if any(user.login == login for user in usuarios): # Verifica se o login já existe
                    print("Erro: Usuário já cadastrado.")
                    return
                #Não cria usuários com o mesmo login

                senha = input("Senha: ")
                if(senha != ""): #Verifica se a senha é vazia. Se for, volta para o menu
                    if tipo_usuario == "1":
                        novo_usuario = Enfermeiro(nome, "Enfermeiro", login, senha)
                    elif tipo_usuario == "2":
                        novo_usuario = Farmaceutico(nome, "Farmacêutico", login, senha)
                    elif tipo_usuario == "3":
                        novo_usuario = AuxServicosGerais(nome, "Auxiliar de Serviços Gerais", login, senha)
                    #Cria a classe com base no tipo escolhido e adiciona o usuário no dicionário.
                    usuarios.append(novo_usuario)
                    print(f"{nome} cadastrado com sucesso!")
                else: print(f"Senha invalida.")
            else: print(f"Login invalido.")
        else: print(f"Nome invalido.")    

    def listar_usuarios(self, usuarios):
        #Mostra todos os usuários
        return [f"Nome: {user.nome}, Login: {user.login}, Função: {user.funcao}" for user in usuarios]

    def remover_usuario(self, usuarios, login):
        #Remove um usuário
        if any(user.login == login and isinstance(user, Administrador) for user in usuarios):
            #Checa se o usuário é TI
            print("Erro: O Profissional de TI não pode ser removido.")
            return usuarios
        #Checa se o usuário existe.
        if not any(user.login == login for user in usuarios):
            print("Erro: Usuário não encontrado")
            return usuarios
        #Se o usuário existir, ele será removido
        print("Usuário removido com sucesso!!")
        return [user for user in usuarios if user.login != login]

    def limpar_usuarios(self, usuarios):
        #Remove todos os usuários
        # Preserva apenas os usuários do tipo Administrador
        return [user for user in usuarios if isinstance(user, Administrador)]

#Subclasse Enfermeiro e sua versão do método de acesso aos itens.
class Enfermeiro(Usuario):
    def acessar_itens(self, almoxarifado):
        return almoxarifado.itens_enfermeiro


#Subclasse Auxiliar de Serviços Gerais e sua versão do método de acesso aos itens.
class AuxServicosGerais(Usuario):
    def acessar_itens(self, almoxarifado):
        return almoxarifado.itens_aux_servicos_gerais


#Subclasse Farmaceutico e sua versão do método de acesso aos itens.
class Farmaceutico(Usuario):
    def acessar_itens(self, almoxarifado):
        return almoxarifado.itens_farmaceutico

