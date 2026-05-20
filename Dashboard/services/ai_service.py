import json
import os
import requests
import pandas as pd

OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY", "")

class AIService:
    @staticmethod
    def get_data_summary(df: pd.DataFrame) -> str:
        """
        Converte o DataFrame em um resumo JSON extremamente enxuto (Minimização de Input).
        Extrai apenas tipos, dados numéricos básicos e correlações para evitar enviar o CSV bruto.
        """
        # Ignorar colunas de data/hora
        termos_ignorados = ["carimbo", "timestamp", "data", "hora", "time", "date", "submission", "submissão"]
        colunas_validas = [c for c in df.columns if not any(termo in str(c).casefold() for termo in termos_ignorados)]
        df_limpo = df[colunas_validas]

        summary = {
            "columns": list(df_limpo.columns),
            "dtypes": {col: str(dtype) for col, dtype in df_limpo.dtypes.items()},
            "shape": df_limpo.shape,
            "numeric_summary": {},
            "categorical_summary": {}
        }

        # Separar colunas
        numeric_cols = df_limpo.select_dtypes(include=['number']).columns
        cat_cols = df_limpo.select_dtypes(include=['object', 'category', 'string']).columns

        # Resumo Numérico
        if not numeric_cols.empty:
            desc = df_limpo[numeric_cols].describe().to_dict()
            summary["numeric_summary"] = desc
            
            # Matriz de correlação básica se houver mais de uma coluna numérica
            if len(numeric_cols) > 1:
                corr = df_limpo[numeric_cols].corr().round(2).to_dict()
                summary["correlations"] = corr

        # Resumo Categórico (Apenas Top 3 valores frequentes para economizar tokens)
        for col in cat_cols:
            if df_limpo[col].nunique() < 20: # Ignorar textos longos/IDs únicos
                top_values = df_limpo[col].value_counts().head(3).to_dict()
                summary["categorical_summary"][col] = {"top_values": top_values, "unique_count": df_limpo[col].nunique()}

        return json.dumps(summary, ensure_ascii=False)

    @staticmethod
    def get_ai_insights(df_summary: str, user_question: str) -> str:
        """
        Envia a pergunta do usuário para o DeepSeek V4 Flash via OpenRouter.
        Aplica os guardrails restritos exigidos no documento Adds.md.
        """
        if not OPENROUTER_API_KEY:
            return "⚠️ A chave da API (OPENROUTER_API_KEY) não está configurada. Defina-a como variável de ambiente."
        
        system_prompt = f"""Você é um Consultor de Dados experiente e analista de BI. 
Seu objetivo é responder a perguntas com base estritamente no seguinte resumo de dados:
{df_summary}

REGRAS ESTRITAS DE GUARDRAIL (DEFESA DE ESCOPO):
1. Avalie se a pergunta do usuário é estritamente sobre os dados fornecidos no contexto ou sobre análises de negócios diretamente aplicáveis a eles.
2. Se a pergunta for sobre qualquer outro assunto (exemplos: programação, saudações informais longas, culinária, história, piadas, ferramentas externas) ou se não puder ser respondida com as informações do JSON, você DEVE abortar a análise imediatamente.
3. Em caso de aborto por escopo, sua resposta DEVE ser EXATAMENTE a frase abaixo, sem adicionar caracteres, saudações, desculpas ou pontos finais extras:
Faça perguntas relacionadas aos dados

REGRAS DE FORMATAÇÃO E OTIMIZAÇÃO (ANTI-EXCESS):
- Gere no máximo 3 insights por requisição.
- Cada insight deve ter entre 15 e 30 palavras.
- Vá direto ao ponto, não use introduções genéricas ("Com base nos dados...").
- Utilize Markdown (listas ordenadas, negrito para termos técnicos/números importantes).
- Não liste números brutos exatos desnecessariamente se o usuário já tem acesso às tabelas. Arredonde para melhorar a leitura.
- Não gere códigos HTML, URLs ou links.
"""

        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": os.environ.get("VERCEL_URL", "http://localhost:8050"), # Referer dinâmico
            "X-Title": "Dashly Local Analises"
        }
        
        payload = {
            "model": "deepseek/deepseek-v4-flash:free", # ID correto do modelo na OpenRouter
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_question}
            ],
            "temperature": 0.3, # Baixa temperatura para fatos precisos
            "max_tokens": 300  # Otimizado para serverless (menor latência)
        }

        try:
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json=payload,
                timeout=15  # Reduzido para caber no timeout serverless da Vercel
            )
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"]
        except Exception as e:
            return f"Erro de comunicação com a IA: {str(e)}"
