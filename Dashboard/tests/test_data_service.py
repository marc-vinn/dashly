import pytest
import pandas as pd
from services.data_service import DataService

def test_cache_storage_and_retrieval():
    df = pd.DataFrame({"col1": [1, 2], "col2": [3, 4]})
    cache_id = DataService.store_data(df)
    
    assert cache_id is not None
    assert isinstance(cache_id, str)
    
    df_retrieved = DataService.get_data(cache_id)
    assert df_retrieved is not None
    assert len(df_retrieved) == 2
    assert "col1" in df_retrieved.columns

def test_get_data_invalid_id():
    df_retrieved = DataService.get_data("invalid_id")
    assert df_retrieved is None

def test_get_filters_options():
    df = pd.DataFrame({"Pergunta_1": ["Sim", "Não", "Sim"], "Carimbo de data": ["a", "b", "c"]})
    cache_id = DataService.store_data(df)
    
    opcoes_pergunta, opcoes_valor = DataService.get_filters_options(cache_id, None)
    
    assert len(opcoes_pergunta) == 1
    assert opcoes_pergunta[0]["value"] == "Pergunta_1"
    assert len(opcoes_valor) == 0
    
    opcoes_pergunta, opcoes_valor = DataService.get_filters_options(cache_id, "Pergunta_1")
    assert len(opcoes_valor) == 2
    assert opcoes_valor[0]["value"] == "Sim"
