from collections import deque

class Memoria:
    def __init__(self, tamanho_fisico, tamanho_virtual):
        self.tamanho_fisico = tamanho_fisico
        self.tamanho_virtual = tamanho_virtual
        self.memoria_fisica = [-1] * tamanho_fisico  # Inicializa com molduras vazias
        self.memoria_virtual = list(range(tamanho_virtual))  # Páginas virtuais disponíveis
        self.fila_fifo = deque()  # Fila para gerenciar substituições de páginas (FIFO)

class TabelaDePaginas:
    def __init__(self, tamanho_virtual):
        self.tabela = [{'presente': False, 'moldura': None} for _ in range(tamanho_virtual)]

    def atualizar_presenca(self, pagina, presente, moldura):
        self.tabela[pagina]['presente'] = presente
        self.tabela[pagina]['moldura'] = moldura

    def obter_moldura(self, pagina):
        return self.tabela[pagina]['moldura']

    def pagina_presente(self, pagina):
        return self.tabela[pagina]['presente']
    
class Processo:
    def __init__(self, id_processo, enderecos):
        self.id_processo = id_processo
        self.enderecos = enderecos

class Escalonador:
    def __init__(self, processos, algoritmo='FCFS'):
        self.processos = processos
        self.algoritmo = algoritmo
        self.index_atual = 0

    def obter_proximo_processo(self):
        if self.algoritmo == 'FCFS':
            processo = self.processos[self.index_atual]
            self.index_atual = (self.index_atual + 1) % len(self.processos)
            return processo
        elif self.algoritmo == 'Round Robin':
            processo = self.processos[self.index_atual]
            self.index_atual = (self.index_atual + 1) % len(self.processos)
            return processo
        
class GerenciadorDeMemoria:
    def __init__(self, memoria, tabela_paginas):
        self.memoria = memoria
        self.tabela_paginas = tabela_paginas
        self.falhas_de_pagina = 0

    def acessar_pagina(self, pagina):
        if not self.tabela_paginas.pagina_presente(pagina):
            self.tratar_falha_de_pagina(pagina)
        moldura = self.tabela_paginas.obter_moldura(pagina)
        print(f'Acessando página {pagina} na moldura {moldura}')

    def tratar_falha_de_pagina(self, pagina):
        self.falhas_de_pagina += 1
        if len(self.memoria.fila_fifo) < self.memoria.tamanho_fisico:
            moldura_livre = len(self.memoria.fila_fifo)
            self.memoria.memoria_fisica[moldura_livre] = pagina
            self.memoria.fila_fifo.append(pagina)
            self.tabela_paginas.atualizar_presenca(pagina, True, moldura_livre)
        else:
            pagina_substituida = self.memoria.fila_fifo.popleft()
            moldura_substituida = self.tabela_paginas.obter_moldura(pagina_substituida)
            self.memoria.memoria_fisica[moldura_substituida] = pagina
            self.memoria.fila_fifo.append(pagina)
            self.tabela_paginas.atualizar_presenca(pagina_substituida, False, None)
            self.tabela_paginas.atualizar_presenca(pagina, True, moldura_substituida)
        print(f'Falha de página: Página {pagina} carregada')

def main():
    tamanho_fisico = int(input('Digite o tamanho da memória física (em molduras): '))
    tamanho_virtual = int(input('Digite o tamanho da memória virtual (em páginas): '))
    algoritmo = input('Digite o algoritmo de escalonamento (FIFO ou Round Robin): ').strip().upper()
    enderecos = list(map(int, input('Digite a lista de endereços virtuais a serem acessados (separados por espaço): ').split()))

    memoria = Memoria(tamanho_fisico, tamanho_virtual)
    tabela_paginas = TabelaDePaginas(tamanho_virtual)
    gerenciador = GerenciadorDeMemoria(memoria, tabela_paginas)

    if algoritmo == 'ROUND ROBIN':
        escalonador = Escalonador([Processo(i, enderecos) for i in range(1)], algoritmo='Round Robin')
    else:
        escalonador = Escalonador([Processo(i, enderecos) for i in range(1)], algoritmo='FCFS')

    processo = escalonador.obter_proximo_processo()
    for endereco in processo.enderecos:
        gerenciador.acessar_pagina(endereco)

    print(f'Total de falhas de página: {gerenciador.falhas_de_pagina}')

if __name__ == '__main__':
    main()