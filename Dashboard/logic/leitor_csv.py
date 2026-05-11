import pandas as pd
import io
import base64

def leitor_csv(contents, filename):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)

    try:
        if 'csv' in filename:
            df= pd.read_csv(io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            df= pd.read_excel(io.BytesIO(decoded))
        else:
            return None, "Formato não suportado."

        return df, None
    except Exception as e:
        return None, str(e)