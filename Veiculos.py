from Carro import Carro

IMG_PORSCHE = 'assets/porsche.png'
IMG_F1 = 'assets/jogo_carro.png'

class Porsche(Carro):
    def __init__(self,x, y):
        super().__init__(x, y, IMG_PORSCHE,
                         vida_maxima=3,
                         vel_normal=12,
                         vel_lenta=5)
        self.nome = "Porsche"
        self.descricao = ["Velocidade: Alta", "Resistência: Baixa"]

class F1(Carro):
    def __init__(self,x, y):
        super().__init__(x, y, IMG_F1,
                         vida_maxima=2,
                         vel_normal=20,
                         vel_lenta=5)
        self.nome = "F1"
        self.descricao = ["Velocidade: Alta", "Resistência: Baixa"]