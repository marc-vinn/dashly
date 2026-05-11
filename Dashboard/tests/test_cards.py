"""
TDD — Testes de criação de gráficos em cards.py
Escritos ANTES da correção do bug de 'legend' duplicado.
"""
import pytest
import sys
import os
import pandas as pd
import base64

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))


class TestCriarBlocoPergunta:
    """Testes para os 3 tipos de gráfico gerados em cards.py."""

    def _df_categorico(self):
        return pd.DataFrame({"Pergunta": ["Sim", "Não", "Sim", "Talvez", "Sim"]})

    def _df_pizza(self):
        """Dados com ≤ 3 valores únicos → pizza."""
        return pd.DataFrame({"Binaria": ["Sim", "Não", "Sim", "Não"]})

    def _df_numerico(self):
        """Dados numéricos → histograma."""
        return pd.DataFrame({"Nota": [7, 8, 9, 10, 6, 7, 8]})

    def _info_basica(self, df, col):
        from logic.processador import processar_estatisticas
        return processar_estatisticas(df, col)

    def test_bloco_barra_nao_lanca_excecao(self):
        """criar_bloco_pergunta com tipo 'barra' não deve lançar exceção."""
        from components.cards import criar_bloco_pergunta
        df = self._df_categorico()
        info = self._info_basica(df, "Pergunta")
        # Não deve lançar TypeError
        resultado = criar_bloco_pergunta(df, "Pergunta", info, 8, "barra")
        assert resultado is not None

    def test_bloco_pizza_nao_lanca_excecao(self):
        """criar_bloco_pergunta com tipo 'pizza' NÃO deve lançar TypeError de 'legend' duplicado."""
        from components.cards import criar_bloco_pergunta
        df = self._df_pizza()
        info = self._info_basica(df, "Binaria")
        # Este teste vai FALHAR antes da correção
        resultado = criar_bloco_pergunta(df, "Binaria", info, 4, "pizza")
        assert resultado is not None

    def test_bloco_histograma_nao_lanca_excecao(self):
        """criar_bloco_pergunta com tipo 'histograma' não deve lançar exceção."""
        from components.cards import criar_bloco_pergunta
        df = self._df_numerico()
        info = self._info_basica(df, "Nota")
        resultado = criar_bloco_pergunta(df, "Nota", info, 8, "histograma")
        assert resultado is not None

    def test_pizza_tem_textinfo_percent(self):
        """Gráfico pizza deve mostrar porcentagens (textinfo contendo 'percent')."""
        from components.cards import criar_bloco_pergunta
        from dash import dcc
        df = self._df_pizza()
        info = self._info_basica(df, "Binaria")
        bloco = criar_bloco_pergunta(df, "Binaria", info, 4, "pizza")
        bloco_str = str(bloco)
        assert "percent" in bloco_str

    def test_cores_roxas_nas_barras(self):
        """Gráficos de barra devem usar a cor roxa #9858f1."""
        from components.cards import criar_bloco_pergunta
        df = self._df_categorico()
        info = self._info_basica(df, "Pergunta")
        bloco = criar_bloco_pergunta(df, "Pergunta", info, 8, "barra")
        bloco_str = str(bloco)
        assert "#9858f1" in bloco_str or "9858f1" in bloco_str

    def test_cores_roxas_no_histograma(self):
        """Histogramas devem usar a cor #732dd3."""
        from components.cards import criar_bloco_pergunta
        df = self._df_numerico()
        info = self._info_basica(df, "Nota")
        bloco = criar_bloco_pergunta(df, "Nota", info, 8, "histograma")
        bloco_str = str(bloco)
        assert "732dd3" in bloco_str
