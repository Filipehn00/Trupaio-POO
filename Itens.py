#Classe item e suas subclasses
#Não é necessário importar nada

class Item:
    def __init__(self, nome, qtd): #Construtor(Inicializador) da classe item
        self.nome = nome
        self.qtd = qtd

    def to_dict(self): #Criação do dicionário
        return {"tipo": self.__class__.__name__, "nome": self.nome, "qtd": self.qtd}

    @classmethod #médoto de classe
    def from_dict(cls, data):
        #Decide o tipo de item que é criado com base no que é pedido
        tipo = data.pop("tipo")
        if tipo == "Medicacao":
            return Medicacao(**data)
        elif tipo == "EquipamentoMedico":
            return EquipamentoMedico(**data)
        elif tipo == "ProdutoLimpeza":
            return ProdutoLimpeza(**data)
#Medicação é uma subclasse de item que só pode ser acesada por farmacêuticos
class Medicacao(Item):
    def __init__(self, nome,  qtd):
        super().__init__(nome,  qtd)

    def to_dict(self):
        data = super().to_dict()
        return data

#Equipamento Medico é uma subclasse de item que só pode ser acessada por enfermeiros
class EquipamentoMedico(Item):
    def __init__(self, nome,  qtd):
        super().__init__(nome,  qtd)


    def to_dict(self):
        data = super().to_dict()
        return data

#Produto de Limpeza é uma subclasse de item que só pode ser acessada por Auxiliares de Serviços Gerais
class ProdutoLimpeza(Item):
    def __init__(self, nome, qtd):
        super().__init__(nome,  qtd)


    def to_dict(self):
        data = super().to_dict()
        return data