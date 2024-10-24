# Simulador-de-Memoria-Paginacao
Desenvolver um simulador para reproduzir o gerenciamento de memória por paginação, incluindo memória virtual e física, tabela de páginas, falhas de página, e substituição usando o algoritmo FIFO (First In, First Out)

## Interface do Simulador

### Linha de Comando:

Input: Configura o tamanho da memória, escolhe o algoritmo de escalonamento e lê a lista de endereços.

Exibição de Status: A cada acesso, exibe o status da tabela de páginas e se houve falha.

Resumo: Exibe o total de falhas de página.

## Relatório Explicativo

### Introdução

O gerenciamento de memória por paginação é uma técnica que divide a memória em blocos de tamanho fixo chamados páginas (na memória virtual) e molduras (na memória física). Essa técnica facilita a alocação de memória e melhora o uso eficiente, permitindo que partes do programa sejam carregadas conforme necessário, reduzindo fragmentação e possibilitando a execução de processos maiores que a memória física disponível.

### Arquitetura do Simulador

Componentes principais.

### Cenários de Teste e Resultados

Comparação dos resultados (número de falhas de página).

### Conclusão

Resultados e aprendizados.

Planejamento dos Cenários de Teste

### Tamanhos de Memória

Testar diferentes tamanhos de memória física e virtual.

### Listas de Endereços Aleatórios

Usar listas variando repetitividade e distribuição.

### Algoritmos de Escalonamento

Comparar resultados com Round Robin e FCFS.