import uuid
import time
import os
import pandas as pd

# ─── Detectar ambiente Vercel ────────────────────────────────────────────────
IS_VERCEL = os.environ.get("VERCEL", "") == "1"

if not IS_VERCEL:
    # Ambiente local: manter diskcache para persistência robusta
    try:
        import diskcache
        CACHE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "cache_data")
        _disk_cache = diskcache.Cache(CACHE_DIR)
    except ImportError:
        # Fallback se diskcache não estiver instalado
        IS_VERCEL = True  # Força uso do cache in-memory

# Cache in-memory para ambiente serverless (Vercel)
_memory_cache = {}


class DataService:
    @staticmethod
    def store_data(df: pd.DataFrame) -> str:
        """
        Armazena o DataFrame e retorna um ID único.
        Local: usa diskcache (disco). Vercel: usa dicionário in-memory (ephemeral).
        """
        cache_id = str(uuid.uuid4())

        if IS_VERCEL:
            # Limpeza preventiva de entries antigas (>1h) para não explodir memória da função
            cutoff = time.time() - 3600
            expired = [k for k, v in _memory_cache.items() if v["ts"] < cutoff]
            for k in expired:
                del _memory_cache[k]
            _memory_cache[cache_id] = {"data": df, "ts": time.time()}
        else:
            _disk_cache.set(cache_id, df, expire=86400)  # Expira em 24h

        return cache_id

    @staticmethod
    def get_data(cache_id: str) -> pd.DataFrame:
        """
        Recupera o DataFrame usando o ID.
        """
        if not cache_id:
            return None

        if IS_VERCEL:
            entry = _memory_cache.get(cache_id)
            return entry["data"] if entry else None
        else:
            return _disk_cache.get(cache_id)

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
