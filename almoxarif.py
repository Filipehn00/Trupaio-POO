import os #importa o sistema operacional para usar a função clear corretamente

#Importamos os Funcionários e os Itens de seus respectivos códigos
from Usuarios import Usuario, Farmaceutico, AuxServicosGerais, Enfermeiro
from Itens import Item, EquipamentoMedico, ProdutoLimpeza, Medicacao

def Clear() -> None:
    os.system('cls' if os.name == 'nt' else 'clear')


#Cria a classe Almoxarifado
class Almoxarifado:
    def __init__(self) -> None: #Construtor do almoxarifado
        # 3 listas diferentes de item
        self.itens_enfermeiro = []
        self.itens_farmaceutico = []
        self.itens_aux_servicos_gerais = []
        #Lista de Funcionários
        self.usuarios = []

    def entrada_item(self, item, usuario)-> None: #método para adição de item
        if isinstance(usuario, Enfermeiro) and isinstance(item, EquipamentoMedico):
        #Checa se o funcionário está adicionando o item correto
            for i in self.itens_enfermeiro:
                if i.nome.lower() == item.nome.lower(): #Se o nome do item for igual, não cria um item novo.
                    i.quantidade +=item.quantidade #Somente a quantidade do item é aumentada
                    return
            self.itens_enfermeiro.append(item) #cria um item novo na lista de itens específica
        elif isinstance(usuario, Farmaceutico) and isinstance(item, Medicacao):
            for i in self.itens_farmaceutico:
                if i.nome.lower() == item.nome.lower():
                    i.quantidade +=item.quantidade
                    return
            self.itens_farmaceutico.append(item)
        elif isinstance(usuario, AuxServicosGerais) and isinstance(item, ProdutoLimpeza):
            for i in self.itens_aux_servicos_gerais:
                if i.nome.lower() == item.nome.lower():
                    i.quantidade +=item.quantidade
                    return
            self.itens_aux_servicos_gerais.append(item) 
        else: #Se o funcionário tenta adicionar um item que não é dele
            print("Erro: Este item não pode ser adicionado por este usuário.")
            input("Pressione Enter para retornar")
            #Isso não acontece em circunstâncias normais

    def saida_item(self, nome: str, usuario)-> None: #Método para retirada de itens
        #Pega o item, se o usuário tem acesso a ele
        if isinstance(usuario, Enfermeiro):
            self.itens_enfermeiro = [item for item in self.itens_enfermeiro if item.nome != nome]
        elif isinstance(usuario, Farmaceutico):
            self.itens_farmaceutico = [item for item in self.itens_farmaceutico if item.nome != nome]
        elif isinstance(usuario, AuxServicosGerais):
            self.itens_aux_servicos_gerais = [item for item in self.itens_aux_servicos_gerais if item.nome != nome]
        
        

#Mostra todos os itens aos quais o usuário tem acesso
    def listar_itens(self, usuario) -> list:
        if isinstance(usuario, Enfermeiro):
            return self.itens_enfermeiro
        elif isinstance(usuario, Farmaceutico):
            return self.itens_farmaceutico
        elif isinstance(usuario, AuxServicosGerais):
            return self.itens_aux_servicos_gerais
        

    def buscar_item(self, nome:str, usuario): #mostra um item com base no nome que o usuário pediu
        #Só mostra o item se ele estiver na lista que o usuário tem acesso
        if isinstance(usuario, Enfermeiro):
            return [item for item in self.itens_enfermeiro if item.nome.lower() == nome.lower()]
        elif isinstance(usuario, Farmaceutico):
            return [item for item in self.itens_farmaceutico if item.nome.lower() == nome.lower()]
        elif isinstance(usuario, AuxServicosGerais):
            return [item for item in self.itens_aux_servicos_gerais if item.nome.lower() == nome.lower()]

@classmethod
def from_dict(classe, data:dict, conexao) -> dict:
    almoxarifado = classe()
    cursor = conexao.cursor()

    # Insere os itens para cada tipo
    for item in data["itens_enfermeiro"]:
        cursor.execute("INSERT INTO itens (nome, quantidade, tipo) VALUES (?, ?, ?)",
                       (item["nome"], item["quantidade"], "EquipamentoMedico"))

    for item in data["itens_farmaceutico"]:
        cursor.execute("INSERT INTO itens (nome, quantidade, tipo) VALUES (?, ?, ?)",
                       (item["nome"], item["quantidade"], "Medicacao"))

    for item in data["itens_aux_servicos_gerais"]:
        cursor.execute("INSERT INTO itens (nome, quantidade, tipo) VALUES (?, ?, ?)",
                       (item["nome"], item["quantidade"], "ProdutoLimpeza"))

    # Insere os usuários
    for usuario in data["usuarios"]:
        cursor.execute("INSERT INTO usuarios (nome, funcao, login, senha, tipo) VALUES (?, ?, ?, ?, ?)",
                       (usuario["nome"], usuario["funcao"], usuario["login"], usuario["senha"], usuario["tipo"]))
    conexao.commit()
    return almoxarifado