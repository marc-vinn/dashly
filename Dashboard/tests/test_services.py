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
