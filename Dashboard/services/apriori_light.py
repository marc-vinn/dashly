"""
Implementação leve do algoritmo Apriori para Regras de Associação.
Substitui a dependência pesada do mlxtend (~400MB com scikit-learn/scipy/matplotlib)
por uma implementação pura em Python + Pandas (~0MB extra).
"""
import pandas as pd
from itertools import combinations


def apriori_light(df: pd.DataFrame, min_support: float = 0.1):
    """
    Encontra itemsets frequentes usando o algoritmo Apriori.
    
    Args:
        df: DataFrame com colunas booleanas (One-Hot encoded).
        min_support: Suporte mínimo (fração de 0 a 1).
    
    Returns:
        DataFrame com colunas 'support' e 'itemsets' (frozenset).
    """
    n_rows = len(df)
    if n_rows == 0:
        return pd.DataFrame(columns=["support", "itemsets"])

    columns = list(df.columns)
    
    # Passo 1: Encontrar itemsets de tamanho 1 que atendem ao min_support
    results = []
    frequent_items = []
    
    for col in columns:
        support = df[col].sum() / n_rows
        if support >= min_support:
            itemset = frozenset([col])
            results.append({"support": support, "itemsets": itemset})
            frequent_items.append(col)
    
    # Passo 2: Gerar candidatos de tamanho 2 a partir dos items frequentes
    # Para datasets pequenos (<1000 linhas), tamanho 2 é suficiente para insights úteis
    for combo in combinations(frequent_items, 2):
        mask = df[combo[0]] & df[combo[1]]
        support = mask.sum() / n_rows
        if support >= min_support:
            results.append({"support": support, "itemsets": frozenset(combo)})

    return pd.DataFrame(results) if results else pd.DataFrame(columns=["support", "itemsets"])


def generate_association_rules(frequent_itemsets: pd.DataFrame, metric: str = "confidence", min_threshold: float = 0.5):
    """
    Gera regras de associação a partir de itemsets frequentes.
    
    Args:
        frequent_itemsets: DataFrame do apriori_light com 'support' e 'itemsets'.
        metric: Métrica para filtrar (apenas 'confidence' suportado).
        min_threshold: Valor mínimo da métrica.
    
    Returns:
        DataFrame com colunas: antecedents, consequents, support, confidence, lift.
    """
    if frequent_itemsets.empty:
        return pd.DataFrame(columns=["antecedents", "consequents", "support", "confidence", "lift"])

    # Mapear itemsets para seus suportes
    support_map = {}
    for _, row in frequent_itemsets.iterrows():
        support_map[row["itemsets"]] = row["support"]

    rules = []
    # Apenas itemsets de tamanho >= 2 geram regras
    multi_itemsets = frequent_itemsets[frequent_itemsets["itemsets"].apply(len) >= 2]

    for _, row in multi_itemsets.iterrows():
        itemset = row["itemsets"]
        itemset_support = row["support"]

        # Para cada item no itemset, criar regra: {resto} -> {item}
        for item in itemset:
            antecedent = frozenset(itemset - {item})
            consequent = frozenset([item])

            # Suporte do antecedente (deve existir como itemset frequente)
            ant_support = support_map.get(antecedent)
            con_support = support_map.get(consequent)

            if ant_support is None or con_support is None or ant_support == 0:
                continue

            confidence = itemset_support / ant_support
            lift = confidence / con_support if con_support > 0 else 0

            if confidence >= min_threshold:
                rules.append({
                    "antecedents": antecedent,
                    "consequents": consequent,
                    "support": itemset_support,
                    "confidence": confidence,
                    "lift": lift,
                })

    return pd.DataFrame(rules) if rules else pd.DataFrame(columns=["antecedents", "consequents", "support", "confidence", "lift"])
