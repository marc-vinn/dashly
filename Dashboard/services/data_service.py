import diskcache
import uuid
import pandas as pd
import os

# Configuração do cache no disco (seguro contra expiração na memória e thread-safe)
CACHE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "cache_data")
cache = diskcache.Cache(CACHE_DIR)

class DataService:
    @staticmethod
    def store_data(df: pd.DataFrame) -> str:
        """
        Armazena o DataFrame no servidor e retorna um ID único.
        """
        cache_id = str(uuid.uuid4())
        cache.set(cache_id, df, expire=86400) # Expira em 24h
        return cache_id

    @staticmethod
    def get_data(cache_id: str) -> pd.DataFrame:
        """
        Recupera o DataFrame do servidor usando o ID.
        """
        if not cache_id:
            return None
        return cache.get(cache_id)

    @staticmethod
    def get_filters_options(cache_id: str, pergunta_selecionada: str):
        """
        Retorna as opções para os dropdowns de filtro, isolando a lógica do pandas.
        """
        df = DataService.get_data(cache_id)
        if df is None:
            return [], []
            
        perguntas = [c for c in df.columns if "carimbo" not in c.casefold() and "timestamp" not in c.casefold()]
        opcoes_pergunta = [{"label": p, "value": p} for p in perguntas]
        
        opcoes_valor = []
        if pergunta_selecionada and pergunta_selecionada in df.columns:
            valores_unicos = df[pergunta_selecionada].dropna().unique()
            opcoes_valor = [{"label": str(v), "value": v} for v in valores_unicos]
            
        return opcoes_pergunta, opcoes_valor
