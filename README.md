# Racing Coders 🏁

Este é um jogo de corrida 2D vertical desenvolvido em Python utilizando a biblioteca Pygame e SQLAlchemy para gerenciamento de pontuação via banco de dados.

## Funcionalidades

* Movimentação do veículo com desvio de obstáculos.
* Coleta de moedas para pontuação.
* Sistema de menu (Inicial, Pausa, Game Over).
* Múltiplos veículos (Porsche, Mercedes) com diferentes atributos (Velocidade, Resistência).
* Sistema de Vida: O jogador pode receber dano antes de perder.
* Sistema de Tempo: O tempo de sobrevivência é salvo junto com a pontuação.
* Ranking de pontuação com persistência em banco de dados (PostgreSQL).

## Conceitos de Programação Orientada a Objetos (POO) Aplicados

Este projeto utiliza diversos conceitos fundamentais de POO para organizar o código, torná-lo reutilizável e fácil de manter.

### 1. Classes e Objetos



* **`Tela`**: Gerencia a janela do jogo, o desenho do fundo e todos os sub-menus (Pausa, Game Over, Escolha de Carro, etc.).
* **`Carro`**: Classe base para todos os veículos. Controla a movimentação, a vida e a velocidade.
* **`Obstaculo`**: Gerencia o comportamento dos obstáculos que caem.
* **`Moeda`**: Gerencia o comportamento das moedas que caem.
* **`Usuario` / `Ponto`**: Classes (Modelos) que representam as tabelas no banco de dados, gerenciadas pelo SQLAlchemy.

### 2. Herança

A herança permite que uma classe "filha" receba (herde) todos os atributos e métodos de uma classe "mãe", permitindo a especialização.

* **`Objetos(ABC)` -> `Carro` / `Obstaculo`**: As classes `Carro` e `Obstaculo` herdam da classe abstrata `Objetos`.
* **`Carro` -> `Porsche` / `Mercedes`**: As classes `Porsche` e `Mercedes` (definidas em `Veiculos.py`) herdam da classe `Carro`. Elas reutilizam os métodos `mover()`, `desenhar()` e `receber_dano()` da classe `Carro`, mas definem seus próprios atributos (como `vida_maxima`, `velocidade_normal`, nome e descrição) no construtor.

### 3. Polimorfismo

Polimorfismo (muitas formas) é evidente na forma como tratamos objetos de classes diferentes que compartilham uma interface comum (Herança).

* O exemplo mais claro é o método `desenhar()`, definido na classe abstrata `Objetos`. Tanto `Carro` quanto `Obstaculo` implementam seu próprio método `desenhar()`. O `Main.py` pode então chamar `carro.desenhar(tela)` e `obstaculo.desenhar(tela)`; o Python sabe qual método `desenhar()` específico executar para cada objeto.

### 4. Abstração

A abstração foca em esconder a complexidade interna e expor apenas as funcionalidades essenciais.

* **Classe Abstrata `Objetos`**: A classe `Objetos` é uma Classe Abstrata (usando `ABC` e `@abstractmethod`). Ela define um "contrato" que obriga qualquer classe que herde dela (como `Carro` e `Obstaculo`) a implementar o método `desenhar()`.
* **Métodos como interface**: O `Main.py` não precisa saber *como* um carro se move na grama vs. no asfalto. Ele apenas chama `carro.mover()`. A lógica complexa está "abstraída" (escondida) dentro do método `mover` da classe `Carro`.

### 5. Encapsulamento

O encapsulamento é a prática de agrupar dados (atributos) e os métodos que operam nesses dados dentro de uma única unidade (a classe).

* A classe `Carro` "encapsula" seus próprios dados (`self.rect`, `self.vida_atual`, `self.velocidade_normal`).
* O `Main.py` não modifica `carro.vida_atual` diretamente. Em vez disso, ele chama o método `carro.receber_dano(1)`. Isso protege os dados do carro; a classe `Carro` decide *se* e *como* o dano deve ser aplicado (por exemplo, verificando se o carro está invencível).