from collections import deque

class Memoria:
    def __init__(self, tamanho_fisico, tamanho_virtual):
        self.tamanho_fisico = tamanho_fisico
        self.tamanho_virtual = tamanho_virtual
        self.memoria_fisica = [-1] * tamanho_fisico
        self.memoria_virtual = list(range(tamanho_virtual))
        self.fila_paginas = deque()  # Usada para FIFO e Round Robin

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
        self.falhas = 0  # Contador de falhas por processo

class Escalonador:
    def __init__(self, processos, algoritmo='FIFO'):
        self.processos = processos
        self.algoritmo = algoritmo
        self.index_atual = 0

    def obter_proximo_processo(self):
        processo = self.processos[self.index_atual]
        self.index_atual = (self.index_atual + 1) % len(self.processos)
        return processo

class GerenciadorDeMemoria:
    def __init__(self, memoria, tabela_paginas, algoritmo='FIFO'):
        self.memoria = memoria
        self.tabela_paginas = tabela_paginas
        self.falhas_de_pagina = 0
        self.algoritmo = algoritmo

    def acessar_pagina(self, pagina, processo):
        if not self.tabela_paginas.pagina_presente(pagina):
            processo.falhas += 1
            self.falhas_de_pagina += 1
            self.substituir_pagina(pagina)
        moldura = self.tabela_paginas.obter_moldura(pagina)
        print(f'Acessando página {pagina} na moldura {moldura}')

    def substituir_pagina(self, pagina):
        if len(self.memoria.fila_paginas) < self.memoria.tamanho_fisico:
            moldura_livre = len(self.memoria.fila_paginas)
            self.memoria.memoria_fisica[moldura_livre] = pagina
            self.memoria.fila_paginas.append(pagina)
        else:
            pagina_substituida = self.memoria.fila_paginas.popleft()
            moldura_substituida = self.tabela_paginas.obter_moldura(pagina_substituida)
            self.memoria.memoria_fisica[moldura_substituida] = pagina
            self.memoria.fila_paginas.append(pagina)
            self.tabela_paginas.atualizar_presenca(pagina_substituida, False, None)
        self.tabela_paginas.atualizar_presenca(pagina, True, moldura_substituida)
        print(f'Falha de página: Página {pagina} carregada')

def main():
    try:
        tamanho_fisico = int(input('Tamanho da memória física: '))
        tamanho_virtual = int(input('Tamanho da memória virtual: '))
        algoritmo = input('Algoritmo (FIFO ou Round Robin): ').strip().upper()
        enderecos = list(map(int, input('Endereços virtuais: ').split()))
    except ValueError:
        print("Entrada inválida. Tente novamente.")
        return

    memoria = Memoria(tamanho_fisico, tamanho_virtual)
    tabela_paginas = TabelaDePaginas(tamanho_virtual)
    processos = [Processo(0, enderecos)]
    escalonador = Escalonador(processos, algoritmo)
    gerenciador = GerenciadorDeMemoria(memoria, tabela_paginas, algoritmo)

    processo = escalonador.obter_proximo_processo()
    for endereco in processo.enderecos:
        gerenciador.acessar_pagina(endereco, processo)

    print(f'Total de falhas de página: {gerenciador.falhas_de_pagina}')
    print(f'Falhas por processo: {processo.falhas}')

if __name__ == '__main__':
    main()
