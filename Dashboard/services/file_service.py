import pandas as pd
import io
import base64

class FileService:
    @staticmethod
    def parse_uploaded_file(contents, filename):
        """
        Lê o conteúdo carregado, valida a extensão e converte para DataFrame.
        Retorna (DataFrame, erro) onde erro é uma string se houver falha.
        """
        if not contents:
            return None, "Nenhum conteúdo enviado."

        try:
            content_type, content_string = contents.split(',')
            decoded = base64.b64decode(content_string)
            
            # Defense in Depth: Validar pela extensão explicitamente usando casefold
            ext = filename.casefold().split('.')[-1]
            
            if ext == 'csv':
                # Tenta ler como utf-8, fallback para outros encodings se necessário no futuro
                df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
            elif ext in ['xls', 'xlsx']:
                df = pd.read_excel(io.BytesIO(decoded))
            else:
                return None, "Formato não suportado. Apenas CSV e XLS/XLSX."
            
            # Validação estrutural mínima
            if df.empty:
                return None, "O arquivo enviado está vazio."
                
            return df, None
            
        except UnicodeDecodeError:
            return None, "Erro de codificação. O arquivo CSV deve estar em UTF-8."
        except pd.errors.ParserError:
            return None, "Erro de formatação no arquivo CSV. Verifique os separadores."
        except Exception as e:
            # Captura de exceção genérica como última linha de defesa
            return None, f"Erro inesperado ao processar arquivo: {str(e)}"
