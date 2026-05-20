import pytest
import pandas as pd
import base64
from services.file_service import FileService

def test_parse_uploaded_file_valid_csv():
    # Cria um CSV simples em memória
    csv_content = "nome,idade\nAlice,30\nBob,25"
    encoded = base64.b64encode(csv_content.encode('utf-8')).decode('utf-8')
    contents = f"data:text/csv;base64,{encoded}"
    
    df, erro = FileService.parse_uploaded_file(contents, "dados.csv")
    
    assert erro is None
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 2
    assert 'nome' in df.columns

def test_parse_uploaded_file_invalid_extension():
    contents = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII="
    df, erro = FileService.parse_uploaded_file(contents, "imagem.png")
    
    assert df is None
    assert "Formato não suportado" in erro

def test_parse_uploaded_file_corrupted_csv():
    # Base64 que não é decodificável para utf-8
    encoded = base64.b64encode(b"\xff\xfe\x00").decode('utf-8')
    contents = f"data:text/csv;base64,{encoded}"
    df, erro = FileService.parse_uploaded_file(contents, "dados.csv")
    
    assert df is None
    assert erro is not None


def test_parse_uploaded_file_case_normalization():
    # Cria um CSV com variações de case nas respostas
    csv_content = "pergunta\nASSIM\nAssim\nASsIm\nnão\nNÃO\nSim\nSIM"
    encoded = base64.b64encode(csv_content.encode('utf-8')).decode('utf-8')
    contents = f"data:text/csv;base64,{encoded}"
    
    df, erro = FileService.parse_uploaded_file(contents, "respostas.csv")
    
    assert erro is None
    assert isinstance(df, pd.DataFrame)
    
    # Verifica se os valores foram unificados e capitalizados
    valores_unicos = df['pergunta'].dropna().unique()
    assert len(valores_unicos) == 3
    assert set(valores_unicos) == {"Assim", "Não", "Sim"}


def test_ai_service_retry_on_429_success(monkeypatch):
    """
    Testa se o AIService faz retentativa sob erro 429 e retorna com sucesso na tentativa seguinte.
    """
    from services.ai_service import AIService
    import requests
    
    # Mockando a chave de API para o teste
    monkeypatch.setenv("OPENROUTER_API_KEY", "mock_key")
    from services import ai_service
    ai_service.OPENROUTER_API_KEY = "mock_key"

    calls = 0

    class MockResponse:
        def __init__(self, status_code, json_data):
            self.status_code = status_code
            self.json_data = json_data

        def raise_for_status(self):
            if self.status_code >= 400:
                raise requests.exceptions.HTTPError(f"HTTP {self.status_code}")

        def json(self):
            return self.json_data

    def mock_post(*args, **kwargs):
        nonlocal calls
        calls += 1
        if calls == 1:
            return MockResponse(429, {})
        return MockResponse(200, {"choices": [{"message": {"content": "Insight gerado!"}}]})

    monkeypatch.setattr(requests, "post", mock_post)
    
    # Mockando time.sleep para o teste rodar instantaneamente
    import time
    monkeypatch.setattr(time, "sleep", lambda x: None)

    resultado = AIService.get_ai_insights("{}", "Pergunta de teste")
    assert resultado == "Insight gerado!"
    assert calls == 2


def test_ai_service_retry_on_429_exhausted(monkeypatch):
    """
    Testa se o AIService retorna erro amigável quando todas as retentativas do 429 falham.
    """
    from services.ai_service import AIService
    import requests
    
    # Mockando a chave de API
    monkeypatch.setenv("OPENROUTER_API_KEY", "mock_key")
    from services import ai_service
    ai_service.OPENROUTER_API_KEY = "mock_key"

    class MockResponse:
        def __init__(self, status_code):
            self.status_code = status_code

        def raise_for_status(self):
            raise requests.exceptions.HTTPError(f"HTTP {self.status_code}")

    def mock_post(*args, **kwargs):
        return MockResponse(429)

    monkeypatch.setattr(requests, "post", mock_post)
    
    # Mockando time.sleep
    import time
    monkeypatch.setattr(time, "sleep", lambda x: None)

    resultado = AIService.get_ai_insights("{}", "Pergunta de teste")
    assert "extremamente congestionado" in resultado


