import random
from datetime import date, timedelta

#region Indivíduo
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
#endregion

#region Time
class Time:
    def __init__(self, nome: str, tecnico: Tecnico, jogadores: list, estádio: str):
        self.nome = nome
        self.tecnico = tecnico
        self.jogadores = jogadores
        self.estádio = estádio
#endregion

#region Confrontos
class Confronto:
    def __init__(self, casa: Time, fora: Time, num_rod: int):
        self.timeCasa = casa
        self.timeFora = fora
        self.data = date.today() + (num_rod * timedelta(7))
        self.estádio = self.timeCasa.estádio

        self.goleadores = {}

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
                    self.goleadores[goleador.nome] += 1
                except:
                    self.goleadores[goleador.nome] = 1
        return self.goleadores

class Rodada:
    def __init__(self, n_rodada: int):
        self._confrontos = []
        self._rodada = n_rodada
        self.goleadores = {}

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
            self.goleadores.update(cft.finalizar_confronto())

            if cft.resultado == "Empate":
                pts_totais[cft.timeCasa] = 1
                pts_totais[cft.timeFora] = 1
            else:
                pts_totais[cft.resultado] = 3 
        return pts_totais              
#endregion

#region Campeonato
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
#endregion