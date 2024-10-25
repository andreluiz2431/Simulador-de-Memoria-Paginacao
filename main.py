from collections import deque

class Memoria:
    def __init__(self, tamanho_fisico, tamanho_virtual):
        self.tamanho_fisico = tamanho_fisico
        self.tamanho_virtual = tamanho_virtual
        self.memoria_fisica = [-1] * tamanho_fisico  # Inicializa com molduras vazias
        self.memoria_virtual = list(range(tamanho_virtual))  # Páginas virtuais disponíveis
        self.fila_fifo = deque()  # Fila para gerenciar substituições de páginas (FIFO)
        self.fila_round_robin = deque()  # Fila para escalonamento Round Robin

class TabelaDePaginas:
    def __init__(self, tamanho_virtual):
        # Inicializa a tabela de páginas com o tamanho especificado, 
        # marcando cada página como não presente e sem moldura atribuída.
        self.tabela = [{'presente': False, 'moldura': None} for _ in range(tamanho_virtual)]

    def atualizar_presenca(self, pagina, presente, moldura):
        # Atualiza o status de presença da página e a moldura associada.
        self.tabela[pagina]['presente'] = presente
        self.tabela[pagina]['moldura'] = moldura

    def obter_moldura(self, pagina):
        # Retorna a moldura associada à página especificada.
        return self.tabela[pagina]['moldura']

    def pagina_presente(self, pagina):
        # Retorna se a página especificada está presente na memória física.
        return self.tabela[pagina]['presente']
    
class Processo:
    def __init__(self, id_processo, enderecos):
        # Inicializa o id do processo
        self.id_processo = id_processo
        # Inicializa a lista de endereços que o processo acessará
        self.enderecos = enderecos

class Escalonador:
    def __init__(self, processos, algoritmo='FCFS'):
        # Inicializa a lista de processos a serem escalonados
        self.processos = processos
        # Define o algoritmo de escalonamento a ser usado
        self.algoritmo = algoritmo
        # Índice do processo atual na lista de processos
        self.index_atual = 0
        # Quantum para o algoritmo Round Robin
        self.quantum = 2

    def obter_proximo_processo(self):
        # Verifica se o algoritmo de escalonamento é FCFS
        if self.algoritmo == 'FCFS':
            # Obtém o próximo processo na lista
            processo = self.processos[self.index_atual]
            # Atualiza o índice atual para o próximo processo
            self.index_atual = (self.index_atual + 1) % len(self.processos)
            # Retorna o próximo processo
            return processo
        # Verifica se o algoritmo de escalonamento é Round Robin
        elif self.algoritmo == 'Round Robin':
            # Obtém o próximo processo na lista
            processo = self.processos[self.index_atual]
            # Atualiza o índice atual para o próximo processo
            self.index_atual = (self.index_atual + 1) % len(self.processos)
            # Retorna o próximo processo
            return processo
        
class GerenciadorDeMemoria:
    def __init__(self, memoria, tabela_paginas, algoritmo='FIFO'):
        # Inicializa a memória do gerenciador
        self.memoria = memoria
        # Inicializa a tabela de páginas
        self.tabela_paginas = tabela_paginas
        # Inicializa o contador de falhas de página
        self.falhas_de_pagina = 0
        # Define o algoritmo de substituição de páginas
        self.algoritmo = algoritmo

    def acessar_pagina(self, pagina):
        # Verifica se a página está presente na memória
        if not self.tabela_paginas.pagina_presente(pagina):
            # Trata a falha de página caso a página não esteja presente
            self.tratar_falha_de_pagina(pagina)
        # Obtém a moldura associada à página
        moldura = self.tabela_paginas.obter_moldura(pagina)
        # Imprime a mensagem de acesso à página
        print(f'Acessando página {pagina} na moldura {moldura}')

    def tratar_falha_de_pagina(self, pagina):
        # Incrementa o contador de falhas de página
        self.falhas_de_pagina += 1
        # Verifica se o algoritmo de substituição é FIFO
        if self.algoritmo == 'FIFO':
            # Substitui a página usando o algoritmo FIFO
            self.substituir_pagina_fifo(pagina)
        # Verifica se o algoritmo de substituição é Round Robin
        elif self.algoritmo == 'Round Robin':
            # Substitui a página usando o algoritmo Round Robin
            self.substituir_pagina_round_robin(pagina)

    def substituir_pagina_fifo(self, pagina):
        # Verifica se há espaço livre na fila FIFO
        if len(self.memoria.fila_fifo) < self.memoria.tamanho_fisico:
            # Define a moldura livre como o tamanho atual da fila FIFO
            moldura_livre = len(self.memoria.fila_fifo)
            # Coloca a página na memória física
            self.memoria.memoria_fisica[moldura_livre] = pagina
            # Adiciona a página à fila FIFO
            self.memoria.fila_fifo.append(pagina)
            # Atualiza a tabela de páginas com a nova presença
            self.tabela_paginas.atualizar_presenca(pagina, True, moldura_livre)
        else:
            # Remove a página da frente da fila FIFO
            pagina_substituida = self.memoria.fila_fifo.popleft()
            # Obtém a moldura da página substituída
            moldura_substituida = self.tabela_paginas.obter_moldura(pagina_substituida)
            # Substitui a página na memória física
            self.memoria.memoria_fisica[moldura_substituida] = pagina
            # Adiciona a nova página à fila FIFO
            self.memoria.fila_fifo.append(pagina)
            # Atualiza a tabela de páginas para remover a presença da página substituída
            self.tabela_paginas.atualizar_presenca(pagina_substituida, False, None)
            # Atualiza a tabela de páginas com a nova presença
            self.tabela_paginas.atualizar_presenca(pagina, True, moldura_substituida)
        # Imprime a mensagem de falha de página
        print(f'Falha de página: Página {pagina} carregada')

    def substituir_pagina_round_robin(self, pagina):
        # Verifica se há espaço livre na fila Round Robin
        if len(self.memoria.fila_round_robin) < self.memoria.tamanho_fisico:
            # Define a moldura livre como o tamanho atual da fila Round Robin
            moldura_livre = len(self.memoria.fila_round_robin)
            # Coloca a página na memória física
            self.memoria.memoria_fisica[moldura_livre] = pagina
            # Adiciona a página à fila Round Robin
            self.memoria.fila_round_robin.append(pagina)
            # Atualiza a tabela de páginas com a nova presença
            self.tabela_paginas.atualizar_presenca(pagina, True, moldura_livre)
        else:
            # Remove a página da frente da fila Round Robin
            pagina_substituida = self.memoria.fila_round_robin.popleft()
            # Obtém a moldura da página substituída
            moldura_substituida = self.tabela_paginas.obter_moldura(pagina_substituida)
            # Substitui a página na memória física
            self.memoria.memoria_fisica[moldura_substituida] = pagina
            # Adiciona a nova página à fila Round Robin
            self.memoria.fila_round_robin.append(pagina)
            # Atualiza a tabela de páginas para remover a presença da página substituída
            self.tabela_paginas.atualizar_presenca(pagina_substituida, False, None)
            # Atualiza a tabela de páginas com a nova presença
            self.tabela_paginas.atualizar_presenca(pagina, True, moldura_substituida)
        # Imprime a mensagem de falha de página
        print(f'Falha de página: Página {pagina} carregada')
        
def main():
    # Pede o tamanho da memória física ao usuário
    tamanho_fisico = int(input('Digite o tamanho da memória física (em molduras): '))
    # Pede o tamanho da memória virtual ao usuário
    tamanho_virtual = int(input('Digite o tamanho da memória virtual (em páginas): '))
    # Pede o algoritmo de escalonamento ao usuário
    algoritmo = input('Digite o algoritmo de escalonamento (FIFO ou Round Robin): ').strip().upper()
    # Pede a lista de endereços virtuais a serem acessados ao usuário
    enderecos = list(map(int, input('Digite a lista de endereços virtuais a serem acessados (separados por espaço): ').split()))

    # Cria a memória com o tamanho especificado
    memoria = Memoria(tamanho_fisico, tamanho_virtual)
    # Cria a tabela de páginas com o tamanho especificado
    tabela_paginas = TabelaDePaginas(tamanho_virtual)
    # Cria o gerenciador de memória com o algoritmo especificado
    gerenciador = GerenciadorDeMemoria(memoria, tabela_paginas, algoritmo=algoritmo)

    # Cria a lista de processos com um processo
    processos = [Processo(i, enderecos) for i in range(1)]  # Ajustado para garantir que pelo menos um processo seja criado
    # Cria o escalonador com o algoritmo especificado
    escalonador = Escalonador(processos, algoritmo=algoritmo)

    # Obtém o próximo processo a ser executado
    processo = escalonador.obter_proximo_processo()
    # Verifica se há um processo para executar
    if processo is None:
        print("Nenhum processo encontrado para executar.")
        return

    # Executa as instruções do processo
    for endereco in processo.enderecos:
        # Acessa a página na memória
        gerenciador.acessar_pagina(endereco)

    # Imprime o total de falhas de página
    print(f'Total de falhas de página: {gerenciador.falhas_de_pagina}')

if __name__ == '__main__':
    # Executa a função main
    main()
