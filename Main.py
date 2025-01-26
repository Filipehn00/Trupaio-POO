import os;

#Importa os arquivos do trabalho
from almoxarif import Almoxarifado, Usuario
from Usuarios import Administrador, AuxServicosGerais, Farmaceutico, Enfermeiro
from Itens import Item, EquipamentoMedico, ProdutoLimpeza, Medicacao
import database


class QuantidadeNegativaError(Exception):
    print('O ')
    def init(self, message="A quantidade de itens não pode ser negativa."):
        super().init(message)
        print(message)

def Clear(): #Função para limpar o console
    os.system('cls' if os.name == 'nt' else 'clear')  
    #Usa o comando adequado para limpar o console dependendo do Sistema

if __name__ == "__main__":
    # Inicializa o banco de dados
    database.init_db()

    # Carrega os dados do banco
    almoxarifado = database.carregar_dados()

    #Se não há usuários, cria um administrador
    if not almoxarifado.usuarios:
        admin = Administrador("Admin", "TI", "admin", "123")
        almoxarifado.usuarios.append(admin)
        database.salvar_dados(almoxarifado)

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
                        Clear() #Menu do administrador do programa
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
                            database.salvar_dados(almoxarifado)
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
                            database.salvar_dados(almoxarifado)
                            input("Pressione Enter para retornar")
                            

                        elif escolha == "4": #remove todo mundo que não é adm
                            Clear()
                            almoxarifado.usuarios = usuario.limpar_usuarios(almoxarifado.usuarios)
                            database.salvar_dados(almoxarifado)
                            input("Pressione Enter para retornar")

                        elif escolha == "5": #quebra esse if e Volta para o menu de login
                            database.salvar_dados(almoxarifado) 

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
                                    if qtd_item <= 0: raise QuantidadeNegativaError
                                    item = None
                                    #Adiciona o item com base na função do usuário que o adiciona
                                    if isinstance(usuario, Enfermeiro):
                                        item = EquipamentoMedico(nome_item, qtd_item)
                                    elif isinstance(usuario, Farmaceutico):
                                        item = Medicacao(nome_item, qtd_item)
                                    elif isinstance(usuario, AuxServicosGerais):
                                        item = ProdutoLimpeza(nome_item, qtd_item)
                                    if item:
                                        almoxarifado.entrada_item(item, usuario)
                                        print('Item adicionado!')
                                except ValueError: #Não adiciona o item se a quantidade não for um inteiro.
                                    print("Insira uma quantidade válida")
                                except QuantidadeNegativaError:  # Trata a exceção de quantidade negativa
                                    print("Insira uma quantidade válida")
                                #volta para o menu da função
                                database.salvar_dados(almoxarifado)
                                input("Pressione Enter para retornar")
                                



                        elif opcao == "2": #Mostra a lista dos itens aos quais o usuário tem acesso
                            Clear()
                            itens = almoxarifado.listar_itens(usuario)
                            if itens:
                                for item in itens:
                                    print(f"Item: {item.nome}, Quantidade: {item.quantidade}")
                            else:
                                print("Nenhum item encontrado.")
                            input("Pressione Enter para confirmar")
                        
                        elif opcao == "3": #Retira um "nome" de item
                            Clear()
                            nome_item = input("Digite o nome do item a ser retirado: ")
                            itens_encontrados = almoxarifado.buscar_item(nome_item, usuario)
                            #Procura o item que o usuário está pedindo.
                            
                            if itens_encontrados: 
                                print(f"Item: {itens_encontrados[0].nome}, Quantidade: {itens_encontrados[0].quantidade}")
                                #mostra o item encontrado
                                try:
                                    qtd_remover = int(input("Digite a quantidade a ser retirada: ")) #Pede a quantidade a ser retirada
                                    if qtd_remover <= 0 : raise QuantidadeNegativaError
                                    item = itens_encontrados[0]
                                    if qtd_remover <= item.quantidade:
                                        item.quantidade -= qtd_remover
                                        if item.quantidade == 0: #Remove o item do almoxarifado se a quantidade for igual a zero
                                            almoxarifado.remover_item(item.nome, usuario)
                                        print("Item retirado com sucesso! Faça bom proveito!!")
                                    else: #Não remove mais do que tem
                                        print("Erro: Quantidade insuficiente em estoque.")
                                except ValueError: #Não retira  o item se a quantidade não for um inteiro.
                                    print("Insira uma quantidade válida")
                                except QuantidadeNegativaError as e:  # Trata a exceção de quantidade negativa
                                    print("Insira uma quantidade válida")
                            else: #Se o item não é encontrado, encerramos aqui
                                print("Item não encontrado.")
                            database.salvar_dados(almoxarifado)
                            input("Pressione Enter para retornar")

                        elif opcao == "4": #Volta para o menu de Login, deslogando o funcionário
                            print("Saindo...") 
                            break

                        else:
                            print("Opção inválida.")

            else: #Se o usuário não está cadastrado, volta para a tela de login
                Clear()
                input("Usuário ou senha inválidos. Pressione Enter para voltar.")  

        elif opcao == "2": 
            #Salva tudo e sai do programa
            database.salvar_dados(almoxarifado) 
            Clear()
            print("Saindo....")
            print("Até logo!")
            break
