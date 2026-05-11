"""
TDD — Testes do Roteador e Callbacks de Upload
Escritos ANTES das correções de implementação.
"""
import pytest
import sys
import os

# Adiciona o diretório raiz ao path para importações
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))


# ─── TESTES DO ROTEADOR ──────────────────────────────────────────────────────

class TestRoteadorLayout:
    """
    O roteador deve retornar o layout correto para cada rota,
    sem quebrar com IDs ausentes.
    """

    def test_rota_raiz_retorna_landing(self):
        """'/' deve retornar o layout da landing page (sem sidebar/header)."""
        from pages.landing import layout_landing
        layout = layout_landing()
        # Verifica que o canvas de partículas está presente
        assert layout is not None
        # O layout deve ser um html.Div (componente Dash)
        assert layout.__class__.__name__ == 'Div'

    def test_rota_dashboard_retorna_layout_com_grid(self):
        """'/dashboard' deve conter o ID 'grid-de-cards'."""
        from pages.dashboard import layout_dashboard
        import json
        layout = layout_dashboard()
        layout_str = str(layout)
        assert 'grid-de-cards' in layout_str

    def test_rota_dashboard_nao_tem_location_duplicado(self):
        """O layout do dashboard NÃO deve conter dcc.Location (já existe no root)."""
        from pages.dashboard import layout_dashboard
        layout = layout_dashboard()
        layout_str = str(layout)
        # 'Location' não deve aparecer no layout das páginas filhas
        assert 'Location' not in layout_str

    def test_rota_landing_nao_tem_location_duplicado(self):
        """O layout da landing NÃO deve conter dcc.Location extra."""
        from pages.landing import layout_landing
        layout = layout_landing()
        layout_str = str(layout)
        assert 'redirect-after-upload' not in layout_str

    def test_rota_analises_retorna_layout(self):
        from pages.dashboard import layout_analises
        layout = layout_analises()
        assert layout is not None
        assert 'output-data-upload' in str(layout)

    def test_rota_dados_retorna_layout(self):
        from pages.dashboard import layout_dados
        layout = layout_dados()
        assert layout is not None
        assert 'tabela-dados-brutos' in str(layout)


# ─── TESTES DO UPLOAD DA LANDING ─────────────────────────────────────────────

class TestUploadLanding:
    """
    O upload da landing deve processar o arquivo e retornar um cache_id válido.
    Não deve redirecionar via dcc.Location filho — isso é responsabilidade do
    Output('url', 'pathname') no store callback.
    """

    def test_upload_csv_valido_retorna_cache_id(self):
        import base64
        from services.file_service import FileService
        from services.data_service import DataService

        csv_content = "pergunta_1,pergunta_2\nSim,Não\nNão,Sim"
        encoded = base64.b64encode(csv_content.encode('utf-8')).decode('utf-8')
        contents = f"data:text/csv;base64,{encoded}"

        df, erro = FileService.parse_uploaded_file(contents, "teste.csv")
        assert erro is None
        assert df is not None

        cache_id = DataService.store_data(df)
        assert cache_id is not None
        assert len(cache_id) == 36  # UUID tem 36 chars

        # O dado deve ser recuperável
        df_recuperado = DataService.get_data(cache_id)
        assert df_recuperado is not None
        assert len(df_recuperado) == 2

    def test_upload_invalido_retorna_erro(self):
        from services.file_service import FileService
        import base64

        # Arquivo com extensão inválida
        contents = "data:image/png;base64,AAAA"
        df, erro = FileService.parse_uploaded_file(contents, "foto.png")
        assert df is None
        assert erro is not None


# ─── TESTES DO DATA SERVICE ───────────────────────────────────────────────────

class TestDataServiceFiltros:
    """Filtros agora só por pergunta, sem filtro-valor."""

    def test_get_filters_retorna_apenas_perguntas_sem_carimbo(self):
        import pandas as pd
        from services.data_service import DataService

        df = pd.DataFrame({
            "Carimbo de data/hora": ["01/01/2024", "02/01/2024"],
            "Pergunta 1": ["Sim", "Não"],
            "Pergunta 2": ["A", "B"]
        })
        cache_id = DataService.store_data(df)
        opcoes, _ = DataService.get_filters_options(cache_id, None)

        valores = [o["value"] for o in opcoes]
        assert "Carimbo de data/hora" not in valores
        assert "Pergunta 1" in valores
        assert "Pergunta 2" in valores

    def test_filtro_sem_valor_retorna_lista_vazia_de_valores(self):
        """Como removemos filtro-valor, get_filters_options com None deve retornar [] para opcoes_valor."""
        import pandas as pd
        from services.data_service import DataService

        df = pd.DataFrame({"Q1": ["Sim", "Não"]})
        cache_id = DataService.store_data(df)
        _, opcoes_valor = DataService.get_filters_options(cache_id, None)
        assert opcoes_valor == []
