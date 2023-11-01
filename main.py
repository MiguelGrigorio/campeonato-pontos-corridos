import random
from datetime import date, timedelta


class Pessoa:
    def __init__(self, nome: str, idade: int):
        self.nome = nome
        self.idade = idade

class Tecnico(Pessoa):
    def __init__(self, nome: str, idade: int, carreira: str):
        super().__init__(nome, idade)
        self.carreira = carreira

class Jogador(Pessoa):
    def __init__(self, nome: str, idade: int, posicao: str):
        super().__init__(nome, idade)
        self.posicao = posicao
        self.gols = 0
    def add_gol(self):
        self.gols += 1


class Time:
    def __init__(self, nome: str, tecnico: Tecnico, jogadores: list, estádio: str):
        self.nome = nome
        self.tecnico = tecnico
        self.jogadores = jogadores
        self.estádio = estádio


class Confronto:
    def __init__(self, casa: Time, fora: Time, num_rod: int):
        self.timeCasa = casa
        self.timeFora = fora
        self.data = date.today() + (num_rod * timedelta(7))
        self.estádio = self.timeCasa.estádio

        self._goleadores = {}

    def finalizar_confronto(self):
        self.gols = (random.randrange(0, 5), random.randrange(0, 5))
        chances_gol = [1, 5, 5, 8, 8, 12, 12, 12, 20, 25, 20]   # Por posição

        if self.gols[0] == self.gols[1]:
            self.resultado = "Empate"
        else:
            duelo = (self.timeCasa, self.timeFora)
            ganhador = duelo[self.gols.index(max(self.gols))]
            
            self.resultado = ganhador


        for i in range(2):
            gol = self.gols[i]
            team = self.timeCasa if i == 0 else self.timeFora
            for _ in range(gol):
                goleador = random.choices(team.jogadores, weights = chances_gol)
                goleador = goleador[0]
                goleador.add_gol()
                try:
                    self._goleadores[goleador.nome] += 1
                except:
                    self._goleadores[goleador.nome] = 1
        return self._goleadores

class Rodada:
    def __init__(self, n_rodada: int):
        self._confrontos = []
        self._rodada = n_rodada
        self._goleadores = {} # ? (Não está sendo usado)

    def add_confronto(self, cft: Confronto):
        self._confrontos.append(cft)
    
    def get_confrontos(self):
        return self._confrontos
    
    def get_num_rodada(self):
        return self._rodada
    
    def finalizar_rodada(self):
        pts_totais = {}
        for i in range(10):
            cft = self._confrontos[i]
            self._goleadores = cft.finalizar_confronto()

            if cft.resultado == "Empate":
                pts_totais[cft.timeCasa] = 1
                pts_totais[cft.timeFora] = 1
            else:
                pts_totais[cft.resultado] = 3 
        return pts_totais              


class Campeonato:
    def __init__(self):
        self._times = []
        self._rodadas = [Rodada(0)]
        self.classificacao = {}
        self._golsJogadores = {}
        self.artilheiros = {}
    
    def add_time(self, time: Time):
        self._times.append(time)
        self.classificacao[time.nome] = 0
    
    def get_times(self):
        return self._times
    
    def add_rodada(self, rodada: Rodada, pnts: dict):
        self._rodadas.append(rodada)
        for i in pnts.keys():
            self.classificacao[i.nome] += pnts[i]
        self.classificacao = self._gerar_classificacao()

        for time in self.get_times():

            for jogador in time.jogadores:
                self._golsJogadores[jogador.nome] = jogador.gols
        
        self.artilheiros = self._gerar_artilheiros()
    
    def get_rodadas(self):
        return self._rodadas
 
    def _gerar_classificacao(self):
        tabela = self.classificacao
        classificacao = {}
        for i in sorted(tabela, key = tabela.get, reverse = True):
            classificacao[i] = tabela[i]
        
        return classificacao
    
    def _gerar_artilheiros(self):
        melhoresJogadores = dict(sorted(self._golsJogadores.items(), key = lambda item: (-item[1], item[0])))
        artilheiros = {}
        for i in range(len(melhoresJogadores)):
            jogador = list(melhoresJogadores.keys())[i]
            if i < 5:
                artilheiros[jogador] = melhoresJogadores[jogador]
            else:
                break
        return artilheiros


'''
    PE      CA      PD 

ME          VL          MD

LE      ZE      ZD      LD

            G
'''
#Inicialização
alfabetão = Campeonato()

def gerar_times(camp: Campeonato):
    for i in range(20):
        teams = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T"]
        t = teams[i]
        Posicoes = ["Goleiro", "Lateral Esquerdo", "Lateral Direito", "Zagueiro Esquerdo", "Zagueiro Direito", "Meia Esquerda", "Meia Direita", "Volante", "Centroavante", "Ponta Esquerda", "Ponta Direita"]
    
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
            if n_rodada < 19:
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

def completar_rodada(rodada: Rodada, camp: Campeonato):
    resultado = rodada.finalizar_rodada()
    camp.add_rodada(rodada, resultado)

gerar_times(alfabetão)
times = alfabetão.get_times()
rodadas = gerar_confrontos(times)

# for i in range(38):
#     completar_rodada(rodadas[i], alfabetão)

numero_rodada = 0
def menu(resposta: str, camp: Campeonato, n_rodada: int, rodadas: list):
    match resposta:
        case 'Time':
            times = camp.get_times()
            print("=== Times ===")
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
                    print(f'\tNome: {jogador.nome} \t Gols: {jogador.gols} \t Posição: {jogador.posicao}')
            else:
                raise Exception("Time inválido.")
        case 'Confronto':
            cft = camp.get_rodadas()
            cft = cft[n_rodada]
            print(f'Confrontos da Rodada {cft.get_num_rodada()}')
            cft = cft.get_confrontos()
            for confronto in cft:
                print(f'{confronto.timeCasa.nome} ({confronto.gols[0]}) x {confronto.timeFora.nome} ({confronto.gols[1]})')
                print(f'\tData: {confronto.data}')
                print(f'\tEstádio: {confronto.estádio}')
                print(f'\tGanhador: {confronto.resultado.nome if type(confronto.resultado) == Time else confronto.resultado}\n')
        case 'Avançar rodada':
            n_rodada += 1
            completar_rodada(rodadas[n_rodada - 1], camp)
        case 'Artilheiros':
            print("==== Artilheiros ====")
            for k, v in camp.artilheiros.items():
                print(f'{k}\t{v} {'gol' if v == 1 else 'gols'}')
        case 'Classificação':
            print("= Tabela =")
            for k, v in camp.classificacao.items():
                print(f'{k}\t {v}')
        case _:
            raise Exception('Opção inválida')
        
    return n_rodada

while True:
    escolhas = ['Time', 'Confronto', 'Avançar rodada', 'Artilheiros', 'Classificação']
    if numero_rodada == 0:
        escolhas.remove('Confronto')
        escolhas.remove('Artilheiros')
        escolhas.remove('Classificação')
    if numero_rodada == 38:
        escolhas.remove('Avançar rodada')
    
    print("=== Alfabetão ===")
    print(f'Rodada {numero_rodada}')
    for i in range(len(escolhas)):
        print(f'{i} - {escolhas[i]}')
    resposta = int(input("Digite uma opção: "))
    if resposta >= len(escolhas):
        raise Exception('Escolha Inválida')
    else:
        numero_rodada = menu(escolhas[resposta], alfabetão, numero_rodada, rodadas)
