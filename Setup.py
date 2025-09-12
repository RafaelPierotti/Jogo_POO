import cx_Freeze

executables = [cx_Freeze.Executable('Main.py')]

cx_Freeze.setup(
    name="Racing Coders",
    options={'build_exe': {'packages': ['pygame'],
                           'include_files': ['Carro.py', 'Moeda.py', 'Obstaculo.py', 'Tela.py', 'estrada.png', 'jogo_carro.png', 'parade.png', 'smw_coin.wav']}},
    executables=executables
)