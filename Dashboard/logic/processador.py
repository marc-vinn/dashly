import pandas as pd
from dash import html
import dash_bootstrap_components as dbc


def auditoria_dados(df):

    #analise de colunas e tipos de dados
    colunas = df.columns
    tipos = df.dtypes.astype(str).values
    unicos = [df[col].nunique() for col in colunas]

    # Criando um DataFrame de resumo para exibição
    resumo_df = pd.DataFrame({
        "Coluna": colunas,
        "Tipo Original": tipos,
        "Valores Únicos": unicos
    })

    return resumo_df


def processar_estatisticas(df, coluna_selecionada):
    resultado = {}
    serie = df[coluna_selecionada].dropna()

    if serie.empty:
        return {'tipo': 'vazio', 'moda': 'N/A'}

    # Verifica se é numérico (int ou float)
    if pd.api.types.is_numeric_dtype(serie):
        resultado['tipo'] = 'numerico'
        resultado['media'] = round(serie.mean(), 2)
        resultado['moda'] = serie.mode()[0] if not serie.mode().empty else "N/A"
    else:
        resultado['tipo'] = 'categorico'
        resultado['moda'] = serie.mode()[0] if not serie.mode().empty else "N/A"
        resultado['contagem'] = serie.value_counts().to_dict()

    return resultado