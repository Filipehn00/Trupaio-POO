import os;
import sqlite3;

#Importa os arquivos do trabalho
from almoxarif import Almoxarifado, Usuario
from Usuarios import Administrador, AuxServicosGerais, Farmaceutico, Enfermeiro
from Itens import Item, EquipamentoMedico, ProdutoLimpeza, Medicacao

#Persistência de dados.
def init_db(db_name="almoxarifado.db"):
    """Inicializa o banco de dados e cria as tabelas necessárias."""
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Cria as tabelas para os usuários e itens
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        funcao TEXT NOT NULL,
        login TEXT UNIQUE NOT NULL,
        senha TEXT NOT NULL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS itens (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        qtd INTEGER NOT NULL,
        tipo TEXT NOT NULL
    )
    ''')

    # cursor.execute('''
    # ALTER TABLE usuarios ADD COLUMN tipo TEXT DEFAULT 'Usuario'
    # ''')
    
    conn.commit()
    conn.close()

def salvar_dados(almoxarifado, db_name="almoxarifado.db"):
    """Salva os dados do almoxarifado no banco de dados."""
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Limpa os dados existentes
    cursor.execute("DELETE FROM usuarios")
    cursor.execute("DELETE FROM itens")

    # Insere os usuários
    for usuario in almoxarifado.usuarios:
        cursor.execute('''
        INSERT INTO usuarios (nome, funcao, login, senha)
        VALUES (?, ?, ?, ?)
        ''', (usuario.nome, usuario.funcao, usuario.login, usuario.senha))

    # Insere os itens
    for lista_itens in [almoxarifado.itens_enfermeiro, almoxarifado.itens_farmaceutico, almoxarifado.itens_aux_servicos_gerais]:
        for item in lista_itens:
            cursor.execute('''
            INSERT INTO itens (nome, qtd, tipo)
            VALUES (?, ?, ?)
            ''', (item.nome, item.qtd, item.__class__.__name__))

    conn.commit()
    conn.close()

def carregar_dados(db_name="almoxarifado.db"):
    """Carrega os dados do almoxarifado do banco de dados."""
    almoxarifado = Almoxarifado()
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Corrige os dados (tenta ajustar o banco)
    try:
        corrigir_dados()
    except Exception as e:
        print(f"Erro ao corrigir dados: {e}")

    # Carrega os usuários
    cursor.execute("SELECT nome, funcao, login, senha FROM usuarios")
    for row in cursor.fetchall():
        usuario_data = {"nome": row[0], "funcao": row[1], "login": row[2], "senha": row[3]}
        almoxarifado.usuarios.append(Usuario.from_dict(usuario_data))

    # Carrega os itens
    cursor.execute("SELECT nome, qtd, tipo FROM itens")
    for row in cursor.fetchall():
        item_data = {"nome": row[0], "qtd": row[1], "tipo": row[2]}
        item = Item.from_dict(item_data)
        if isinstance(item, EquipamentoMedico):
            almoxarifado.itens_enfermeiro.append(item)
        elif isinstance(item, Medicacao):
            almoxarifado.itens_farmaceutico.append(item)
        elif isinstance(item, ProdutoLimpeza):
            almoxarifado.itens_aux_servicos_gerais.append(item)

    conn.close()
    return almoxarifado



def corrigir_dados():
    con = sqlite3.connect("almoxarifado.db")
    cur = con.cursor()

    # Adicionar a coluna "tipo" se ela não existir
    try:
        cur.execute("ALTER TABLE usuarios ADD COLUMN tipo TEXT")
    except sqlite3.OperationalError:
        # A coluna já existe
        pass

    # Atualizar os registros existentes com base na função
    cur.execute("SELECT id, funcao FROM usuarios")
    usuarios = cur.fetchall()

    for usuario in usuarios:
        id, funcao = usuario
        if funcao == "Administrador":
            tipo = "Administrador"
        elif funcao == "Enfermeiro":
            tipo = "Enfermeiro"
        elif funcao == "Farmaceutico":
            tipo = "Farmaceutico"
        elif funcao == "Auxiliar de Serviços Gerais":
            tipo = "AuxServicosGerais"
        else:
            tipo = "Usuario"

        # Atualiza a coluna "tipo"
        cur.execute("UPDATE usuarios SET tipo = ? WHERE id = ?", (tipo, id))

    con.commit()
    con.close()


def Clear(): #Função para limpar o console
    os.system('cls' if os.name == 'nt' else 'clear')  
    #Usa o comando adequado para limpar o console dependendo do Sistema


if __name__ == "__main__":
    # Inicializa o banco de dados
    init_db()

    # Carrega os dados do banco
    almoxarifado = carregar_dados()

    if not almoxarifado.usuarios:
        admin = Administrador("Admin", "TI", "admin", "123")
        almoxarifado.usuarios.append(admin)
        salvar_dados(almoxarifado)

    while True:
        Clear()
        #Menu inicial
        
        print("Bem-vindo ao Sistema de Almoxarifado Hospitalar!")
        print("\n1. Login")
        print("2. Sair")
        opcao = input("Escolha uma opção: ")
        
        if opcao == "1":
            Clear()
            #Tela de Login
            login = input("Insira seu Login: ")
            senha = input("Insira sua Senha: ")
            usuario = next((u for u in almoxarifado.usuarios if u.login == login), None)

            if usuario and usuario.autenticar(senha):
                if isinstance(usuario, Administrador):
                    #Abre o menu de administrador se o usuário logado for um administrador
                    
                    while True:
                        Clear()

                    #Menu do administrador do programa
                        print(f"Bem-vindo, {usuario.nome}!")
                        print("\nMenu Administrador")
                        print("1. Cadastrar usuário")
                        print("2. Listar usuários")
                        print("3. Remover usuário")
                        print("4. Limpar todos os usuários")
                        print("5. Voltar à tela de login")
                        escolha = input("Escolha uma opção: ")

                        if escolha == "1": #cria um novo usuário
                            Clear()
                            usuario.cadastrar_usuario(almoxarifado.usuarios)
                            salvar_dados(almoxarifado)
                            input("Pressione Enter para continuar")

                        elif escolha == "2": #Mostra o Nome, Função e Login de todos os funcionários
                            Clear()
                            usuarios = usuario.listar_usuarios(almoxarifado.usuarios)
                            print("\nUsuários cadastrados:")
                            print("\n".join(usuarios))
                            input("Pressione Enter para continuar")

                        elif escolha == "3": #Remove um único usuário
                            Clear()
                            login_remover = input("Login do usuário a ser removido: ")
                            almoxarifado.usuarios = usuario.remover_usuario(almoxarifado.usuarios, login_remover)
                            salvar_dados(almoxarifado)
                            input("Pressione Enter para retornar")
                            

                        elif escolha == "4": #remove todo mundo que não é adm
                            Clear()
                            almoxarifado.usuarios = usuario.limpar_usuarios(almoxarifado.usuarios)
                            salvar_dados(almoxarifado)
                            input("Pressione Enter para retornar")

                        elif escolha == "5": #quebra esse if e Volta para o menu de login
                            salvar_dados(almoxarifado) 

                            break

                        else:
                            Clear()
                            print("Opção inválida.")

                #Abre o menu de funcionário quando o usuário não é admnistrador
                elif isinstance(usuario, Enfermeiro) or \
                isinstance(usuario, Farmaceutico) or \
                isinstance(usuario, AuxServicosGerais):
                    #Mostra o menu que controla itens
                    while True:
                        Clear()
                        print('Menu do', usuario.funcao)
                        print('Bem-vindo', usuario.nome)
                        print("1) Entrada de Itens")
                        print("2) Listar Itens")
                        print("3) Saída de Itens")
                        print("4) Sair")

                        opcao = input("Escolha uma opção: ")
                        
                        if opcao == "1": #Adiciona um item
                            Clear()
                            nome_item = input("Nome do item: ")
                            if(nome_item != ""): #Não podemos adicionar um item sem nome
                                try:
                                    qtd_item = int(input(f"Quantidade de {nome_item}: "))

                                    item = None
                                    #Adiciona o item com base na função do usuário que o adiciona
                                    if isinstance(usuario, Enfermeiro):
                                        item = EquipamentoMedico(nome_item, qtd_item)
                                    elif isinstance(usuario, Farmaceutico):
                                        item = Medicacao(nome_item, qtd_item)
                                    elif isinstance(usuario, AuxServicosGerais):
                                        item = ProdutoLimpeza(nome_item, qtd_item)
                                    if item:
                                        almoxarifado.adicionar_item(item, usuario)
                                        print('Item adicionado!')
                                    else:
                                        print("Erro: Você não tem permissão para adicionar este tipo de item.")
                                except ValueError:
                                    #Não adiciona o item se a quantidade não for um inteiro.
                                    print("Insira uma quantidade válida")
                                salvar_dados(almoxarifado)
                                input("Pressione Enter para retornar")

                        elif opcao == "2": #Mostra a lista
                            Clear()
                            itens = almoxarifado.listar_itens(usuario)
                            if itens:
                                for item in itens:
                                    print(f"Item: {item.nome}, Quantidade: {item.qtd}")
                            else:
                                print("Nenhum item encontrado.")
                            input("Pressione Enter para confirmar")
                        elif opcao == "3": #Retira um "nome" de item
                            Clear()
                            nome_item = input("Digite o nome do item a ser retirado: ")
                            itens_encontrados = almoxarifado.buscar_item(nome_item, usuario)
                            #Procura o item que o usuário está pedindo.
                            
                            if itens_encontrados: 
                                print(f"Item: {itens_encontrados[0].nome}, Quantidade: {itens_encontrados[0].qtd}")
                                #mostra o item encontrado
                                try:
                                    qtd_remover = int(input("Digite a quantidade a ser retirada: ")) #Pede a quantidade a ser retirada
                                    item = itens_encontrados[0]
                                    if qtd_remover <= item.qtd:
                                        item.qtd -= qtd_remover
                                        if item.qtd == 0: #Remove o item do almoxarifado se a quantidade for igual a zero
                                            almoxarifado.remover_item(item.nome, usuario)
                                        print("Item retirado com sucesso! Faça bom proveito!!")
                                    else: #Não remove mais do que tem
                                        print("Erro: Quantidade insuficiente em estoque.")
                                except ValueError: #Não retira  o item se a quantidade não for um inteiro.
                                    print("Insira uma quantidade válida")
                            else: #Se o item não é encontrado, encerramos aqui
                                print("Item não encontrado.")
                            salvar_dados(almoxarifado)
                            input("Pressione Enter para retornar")


                        elif opcao == "4": #Volta para o menu de Login, deslogando o funcionário
                            print("Saindo...") 
                            break

                        else:
                            print("Opção inválida.")

            else:
                #Se o usuário não está cadastrado, mandamos ele logar
                Clear()
                input("Usuário ou senha inválidos. Pressione Enter para voltar.")  

        elif opcao == "2":
            salvar_dados(almoxarifado) 
            Clear()
            print("Saindo....")
            print("Até logo!")
            break

