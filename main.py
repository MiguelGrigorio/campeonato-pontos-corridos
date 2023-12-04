from classes import Tecnico, Jogador, Time, Confronto, Rodada, Campeonato
import random
import os

alfabetão = Campeonato()    # Inicialização

#region Funções
#region Geração
def gerar_times(camp: Campeonato):
    teams = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T']
    random.shuffle(teams)
    for i in range(20):
        t = teams[i]
        Posicoes = ['Goleiro', 'Lateral Esquerdo', 'Lateral Direito', 'Zagueiro Esquerdo', 'Zagueiro Direito', 'Meia Esquerda', 'Meia Direita', 'Volante', 'Centroavante', 'Ponta Esquerda', 'Ponta Direita']
    
        tec = Tecnico(f'Técnico {t}', random.randrange(18, 60), f'Já foi técnico no time {random.choice(teams)}')
        jogs = []
        for p in range(11):
            jog = Jogador(f'Jogador {t} ({p+1})', random.randrange(17, 40), Posicoes[p])
            jogs.append(jog)
        std = f'Estádio {t}'
        camp.add_time(Time(nome = t, tecnico = tec, jogadores = jogs, estádio = std))

def gerar_confrontos(times: list):
    rodadas = []
    for n_rodada in range(1, 39):
        rodada = Rodada(n_rodada)
        for i in range(10):
            if n_rodada < 20:
                casa = times[i]
                fora = times[-i - 1]
            else:
                casa = times[-i - 1]
                fora = times[i]

            confronto = Confronto(casa, fora, n_rodada)
            rodada.add_confronto(confronto)
        rodadas.append(rodada)
        times = [times[0]] + [times[-1]] + times[1:-1]
    return rodadas

#endregion
#region Menu
def completar_rodada(rodada: Rodada, camp: Campeonato):
    resultado = rodada.finalizar_rodada()
    camp.add_rodada(rodada, resultado)

clear = lambda: os.system('cls' if os.name == 'nt' else 'clear')
clear()
gerar_times(alfabetão)
times = alfabetão.get_times()
rodadas = gerar_confrontos(times)

numero_rodada = 0
def menu(resposta: str, camp: Campeonato, n_rodada: int, rodadas: list):
    match resposta:
        case 'Times':
            times = camp.get_times()
            print('=== Times ===')
            for i in range(len(times)):
                t = times[i].nome
                print(f'{i} - {t}')
            r = int(input(f'Qual time deseja ver? '))
            if r >= 0 and r < 20: 
                time = times[r]
                print(f'Nome: {time.nome}')
                print(f'Estádio: {time.estádio}')
                print(f'Técnico: {time.tecnico.nome}\tCarreira: {time.tecnico.carreira}')
                print('Jogadores:')
                for jogador in time.jogadores:
                    print(f'\tNome: {jogador.nome} \t {'Gol' if jogador.gols == 1 else 'Gols'} {jogador.gols} \t Posição: {jogador.posicao}')
            else:
                raise Exception('Time inválido.')
        case 'Confrontos':
            cft = camp.get_rodadas()
            for c in cft:
                if c.get_num_rodada() == n_rodada:
                    conf = c
                    break
            print(f'Confrontos da Rodada {conf.get_num_rodada()}')
            conf = conf.get_confrontos()
            for confronto in conf:
                print(f'{confronto.timeCasa.nome} ({confronto.gols[0]}) x {confronto.timeFora.nome} ({confronto.gols[1]})')
                print(f'\tData: {confronto.data}')
                print(f'\tEstádio: {confronto.estádio}')
                print(f'\tGanhador: {confronto.resultado.nome if type(confronto.resultado) == Time else confronto.resultado}\n')
        case 'Avançar rodada':
            n_rodada += 1
            for r in rodadas:
                if r.get_num_rodada() == n_rodada:
                    rodada = r
                    break
            completar_rodada(rodada, camp)
        case 'Goleadores da rodada':
            rds = camp.get_rodadas()
            for r in rds:
                if r.get_num_rodada() == n_rodada:
                    rods = r
                    break
            print(f'= Goleadores da rodada {rods.get_num_rodada()} =')
            for k, v in rods.goleadores.items():
               print(f'{k}\t {v} {'gol' if v == 1 else 'gols'}\n')
        case 'Artilheiros':
            print('==== Artilheiros ====')
            for k, v in camp.artilheiros.items():
                print(f'{k}\t{v} {'gol' if v == 1 else 'gols'}\n')
        case 'Classificação':
            print('= Tabela =')
            for k, v in camp.classificacao.items():
                print(f'{k}\t {v}')
        case 'Confrontos anteriores':
            resp = int(input("Digite a rodada de confrontos que deseja visualizar: "))
            if resp < 1 or resp > 38:
                raise Exception('Rodada inválida')
            menu('Confrontos', camp, resp, rodadas)
        case 'Finalizar campeonato':
            for i in range(n_rodada + 1, 38):
                completar_rodada(rodadas[i], camp)
            n_rodada = 38
        case _:
            raise Exception('Opção inválida')
        
    return n_rodada

def user(n_rodada: int):
    global numero_rodada

    if numero_rodada == 0:
        escolhas = ['Times', 'Avançar rodada', 'Finalizar campeonato']
    elif numero_rodada == 38:
        escolhas = ['Times', 'Confrontos', 'Goleadores da rodada', 'Artilheiros', 'Classificação', 'Confrontos anteriores']
    else:
        escolhas = ['Times', 'Confrontos', 'Avançar rodada', 'Goleadores da rodada', 'Artilheiros', 'Classificação', 'Finalizar campeonato']
    
    if n_rodada != numero_rodada:
        escolhas.remove('Times')
        escolhas.remove('Artilheiros')
        escolhas.remove('Classificação')

    print('=== Alfabetão ===')
    print(f'Rodada {n_rodada}')
    for i in range(len(escolhas)):
        print(f'{i} - {escolhas[i]}')
    resposta = int(input('Digite uma opção: '))
    if resposta >= len(escolhas):
        raise Exception('Escolha Inválida')
    else:
        #clear()
        return menu(escolhas[resposta], alfabetão, n_rodada, rodadas)
#endregion
#endregion

while True:
    numero_rodada = user(numero_rodada)
