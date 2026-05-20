import os
import pandas as pd

# ─── Detectar ambiente Vercel ────────────────────────────────────────────────
IS_VERCEL = os.environ.get("VERCEL", "") == "1"

if not IS_VERCEL:
    # Ambiente local: manter diskcache para persistência robusta
    try:
        import diskcache
        import uuid
        CACHE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "cache_data")
        _disk_cache = diskcache.Cache(CACHE_DIR)
    except ImportError:
        IS_VERCEL = True  # Fallback para modo serverless


class DataService:
    @staticmethod
    def store_data(df: pd.DataFrame) -> str:
        """
        Armazena o DataFrame e retorna um identificador.
        Local: usa diskcache (retorna UUID).
        Vercel: serializa o DataFrame inteiro como JSON (vive no browser via dcc.Store).
        """
        if IS_VERCEL:
            # No serverless, devolvemos o JSON direto — vive no sessionStorage do browser
            return df.to_json(orient="split", date_format="iso")
        else:
            cache_id = str(uuid.uuid4())
            _disk_cache.set(cache_id, df, expire=86400)
            return cache_id

    @staticmethod
    def get_data(store_value: str) -> pd.DataFrame:
        """
        Recupera o DataFrame.
        Local: busca no diskcache pelo UUID.
        Vercel: desserializa o JSON que veio do browser.
        """
        if not store_value:
            return None

        if IS_VERCEL:
            try:
                import io
                return pd.read_json(io.StringIO(store_value), orient="split")
            except (ValueError, TypeError):
                return None
        else:
            return _disk_cache.get(store_value)

    @staticmethod
    def get_filters_options(store_value: str, pergunta_selecionada: str):
        """
        Retorna as opções para os dropdowns de filtro, isolando a lógica do pandas.
        """
        df = DataService.get_data(store_value)
        if df is None:
            return [], []

        perguntas = [c for c in df.columns if "carimbo" not in c.casefold() and "timestamp" not in c.casefold()]
        opcoes_pergunta = [{"label": p, "value": p} for p in perguntas]

        opcoes_valor = []
        if pergunta_selecionada and pergunta_selecionada in df.columns:
            valores_unicos = df[pergunta_selecionada].dropna().unique()
            opcoes_valor = [{"label": str(v), "value": v} for v in valores_unicos]

        return opcoes_pergunta, opcoes_valor
