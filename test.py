import unittest

class TestGerenciadorDeMemoria(unittest.TestCase):
    def test_acesso_com_falha(self):
        memoria = Memoria(2, 4)
        tabela = TabelaDePaginas(4)
        gerenciador = GerenciadorDeMemoria(memoria, tabela)
        processo = Processo(0, [0, 1, 2, 3])

        for endereco in processo.enderecos:
            gerenciador.acessar_pagina(endereco, processo)

        self.assertEqual(gerenciador.falhas_de_pagina, 4)

if __name__ == '__main__':
    unittest.main()
