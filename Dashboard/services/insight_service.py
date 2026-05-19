import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules
import warnings

# Silenciar os avisos de divisão por zero do mlxtend
warnings.filterwarnings("ignore", category=RuntimeWarning)

class InsightService:
    @staticmethod
    def generate_quick_insights(df: pd.DataFrame, max_rules=4):
        """
        Gera insights estatísticos rápidos usando o algoritmo Apriori para Regras de Associação.
        Converte colunas categóricas em booleanas e detecta padrões de co-ocorrência.
        """
        if df.empty:
            return [{"title": "Tabela Vazia", "description": "Nenhum dado encontrado para análise."}]
            
        # Ignorar colunas relacionadas a data/hora para não gerar associações com o momento da resposta
        termos_ignorados = ["carimbo", "timestamp", "data", "hora", "time", "date", "submission", "submissão"]
        colunas_validas = [c for c in df.columns if not any(termo in str(c).casefold() for termo in termos_ignorados)]
            
        # Filtrar colunas que tenham poucos valores únicos para categorização lógica (One-Hot)
        # Evita explodir a memória com IDs únicos ou textos longos
        cat_cols = [c for c in colunas_validas if 1 < df[c].nunique() <= 15]
        
        if len(cat_cols) < 2:
            return [{"title": "Poucas Categorias", "description": "O algoritmo precisa de pelo menos 2 colunas categóricas para cruzar informações."}]
            
        try:
            # One-Hot Encoding com separador seguro para não quebrar a string depois
            df_encoded = pd.get_dummies(df[cat_cols], prefix_sep='_=_')
            
            # Garantir que todos os valores sejam booleanos (Obrigatório no mlxtend atual)
            df_encoded = df_encoded.astype(bool)
            
            # Encontrar padrões que ocorrem em pelo menos 10% da base (suporte)
            frequent_itemsets = apriori(df_encoded, min_support=0.1, use_colnames=True)
            
            if frequent_itemsets.empty:
                return [{"title": "Sem Padrões Obvios", "description": "Nenhum padrão ocorreu em mais de 10% da base."}]
                
            # Gerar regras com Confiança mínima de 50%
            rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=0.5)
            
            if rules.empty:
                return [{"title": "Baixa Confiança", "description": "As associações encontradas são muito fracas estatisticamente."}]
                
            # Filtrar apenas regras onde o lift > 1 (correlação positiva)
            rules = rules[rules['lift'] > 1.0].sort_values(by="lift", ascending=False)
            
            if rules.empty:
                 return [{"title": "Sem Associações Fortes", "description": "Não foram encontradas correlações positivas significativas."}]
            
            # Sorteamos de TODAS as regras positivas para dar mais variedade aos insights
            # Em vez de focar apenas no topo absoluto.
            sample_size = min(max_rules, len(rules))
            sampled_rules = rules.sample(n=sample_size)
            
            insights = []
            for _, row in sampled_rules.iterrows():
                # Pegando apenas o primeiro item
                ant = list(row['antecedents'])[0]
                con = list(row['consequents'])[0]
                conf_pct = round(row['confidence'] * 100, 1)
                
                # Títulos dinâmicos com base na força da correlação
                if conf_pct == 100.0:
                    titulo = "Padrão Absoluto (100%)"
                elif conf_pct >= 80.0:
                    titulo = f"Forte Tendência ({conf_pct}%)"
                else:
                    titulo = f"Correlação Notável ({conf_pct}%)"
                
                # Formatando "Coluna_=_Valor" de forma humana
                try:
                    ant_col, ant_val = str(ant).split('_=_', 1)
                    con_col, con_val = str(con).split('_=_', 1)
                except:
                    ant_col, ant_val = "Dado", str(ant)
                    con_col, con_val = "Dado", str(con)
                
                insights.append({
                    "title": titulo,
                    "description": f"Sempre que **{ant_col.strip()}** for **{ant_val.strip()}**, a tendência é que **{con_col.strip()}** seja **{con_val.strip()}**."
                })
                
            return insights
            
        except Exception as e:
            return [{"title": "Aviso Heurístico", "description": f"O formato dos dados impediu a análise de associação. Erro: {str(e)[:50]}"}]
