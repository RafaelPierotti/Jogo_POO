
from Carro import Carro


class Porsche(Carro):
    def __init__(self,x, y, caminho, maiorvelocidade):
        super().__init__(x, y, caminho)
        self.maiorvelocidade =   maiorvelocidade