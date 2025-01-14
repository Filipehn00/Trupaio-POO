import sqlite3 #Importa o SQLite3, extensão Python que permite usar banco de dados SQL 

from almoxarif import Almoxarifado, Usuario
from Itens import Item, EquipamentoMedico, ProdutoLimpeza, Medicacao

#Função para iniciar o banco de dados, chamada no início da main
def init_db(db_name="almoxarifado.db"):
    #Inicializa o banco de dados e cria as tabelas necessárias.

    #cria uma conexão com o SQLite3
    conn = sqlite3.connect(db_name)
    #Cria um cursor para mexer nas tabelas
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
        quantidade INTEGER NOT NULL,
        tipo TEXT NOT NULL
    )
    ''')
    #Commita as tabelas na conexão
    conn.commit()
    #Fecha a conexão
    conn.close()

#Função para salvar dados, chamada sempre que um item ou usuário é adicionado ou retirado
def salvar_dados(almoxarifado, db_name="almoxarifado.db"):
    """Salva os dados do almoxarifado no banco de dados."""
    conn = sqlite3.connect(db_name) #cria uma conexão com o SQLite3
    cursor = conn.cursor() #Cria um cursor

    # Limpa os dados existentes
    cursor.execute("DELETE FROM usuarios")
    cursor.execute("DELETE FROM itens")

    # Insere os novos dados dos usuários
    for usuario in almoxarifado.usuarios:
        cursor.execute('''
        INSERT INTO usuarios (nome, funcao, login, senha)
        VALUES (?, ?, ?, ?)
        ''', (usuario.nome, usuario.funcao, usuario.login, usuario.senha))

    # Insere os novos dados em itens
    for lista_itens in [almoxarifado.itens_enfermeiro, almoxarifado.itens_farmaceutico, almoxarifado.itens_aux_servicos_gerais]:
        for item in lista_itens:
            cursor.execute('''
            INSERT INTO itens (nome, quantidade, tipo)
            VALUES (?, ?, ?)
            ''', (item.nome, item.quantidade, item.__class__.__name__))

    conn.commit() # Commita 
    conn.close() # Fecha a conexão

# Função para abrir um banco de dados existente, chamada quando o banco de dados é encontrado
def carregar_dados(db_name="almoxarifado.db"):
    # Carrega os dados do almoxarifado do banco de dados.
    almoxarifado = Almoxarifado() # cria um objeto da classe Almoxarifado
    conn = sqlite3.connect(db_name) # Cria a conexão
    cursor = conn.cursor() # Cria o cursor

    # executa a função que adiciona um tipo para os usuários de cada função, se não tiverem.
    corrigir_dados()

    # Carrega os usuários
    cursor.execute("SELECT nome, funcao, login, senha, tipo FROM usuarios")
    for row in cursor.fetchall(): # cria um dicionário para cada usuário

        usuario_data = {"nome": row[0], "funcao": row[1], "login": row[2], "senha": row[3], "tipo": row[4]}
        # cria um dicionário com todos usuários
        almoxarifado.usuarios.append(Usuario.from_dict(usuario_data))


    # Carrega os itens
    cursor.execute("SELECT nome, quantidade, tipo FROM itens")
    for row in cursor.fetchall():
        #cria um dicionário para cada item
        item_data = {"nome": row[0], "quantidade": row[1], "tipo": row[2]}
        item = Item.from_dict(item_data)
        #adiciona os itens em seus respectivos dicionários, com base no tipo
        if isinstance(item, EquipamentoMedico):
            almoxarifado.itens_enfermeiro.append(item)
        elif isinstance(item, Medicacao):
            almoxarifado.itens_farmaceutico.append(item)
        elif isinstance(item, ProdutoLimpeza):
            almoxarifado.itens_aux_servicos_gerais.append(item)

    conn.close()
    return almoxarifado #fecha a conexão e retorna o almoxarifado

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

    for usuario in usuarios: #atribui um tipo para cada funcionário.
        id, funcao = usuario
        if funcao == "TI":
            tipo = "Administrador"
        elif funcao == "Enfermeiro":
            tipo = "Enfermeiro"
        elif funcao == "Farmaceutico":
            tipo = "Farmaceutico"
        elif funcao == "Auxiliar de Serviços Gerais":
            tipo = "AuxServicosGerais"

        # Atualiza a coluna "tipo" da tabela usuários
        cur.execute("UPDATE usuarios SET tipo = ? WHERE id = ?", (tipo, id))

    con.commit()
    con.close() #commita e fecha