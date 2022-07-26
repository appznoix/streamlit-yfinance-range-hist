#############################################
# Funções que não precisam importar módulos #
############################################# 

def format_link(text = '', name = '', url = ''):
    '''retorna f\'string com texto e link para url '''
    return f'{text}[{name}]({url})'

def chart_summary(df, display):
    ''' Exibe um resumo dos dados e retorna o numero de raios do Histograma e uma mensagem sumarizada'''
    items = len(df.index)
    if display == 'Range_pct':
        bins_chart = len(df['Range_pct'].value_counts())
    else:
        bins_chart = len(df['Range'].value_counts())
    #bins_chart = df[display].value_counts()
    return bins_chart,(f'Foram encontrados {items} periodos com {bins_chart} valores distintos') 
  
def cooking_range(df, multiplier = 1):
    '''Executa o tratamento dos dados. Neste caso, cria a coluna de ranges e elimina as colunas desnecessárias'''
    if len(df) <= 0:
        return False    
    # 1. pega os valores de máxima e mínima do dia
    # 2. Calcula range numérico e percentual
    if 'High' in df:
        # cria colunas com valores que serão usados
        df['Range_pct'] = round(df.High/df.Low - 1 , 4) * 100
        df['Range'] = abs(round(df.High,2) - round(df.Low,2)) * 10 ** (multiplier-1)
        # df['Range_pct'] = (df.High/df.Low - 1) * 100
        # df['Range'] = abs(df.High - df.Low)
        # elimina colunas desnecessárias
        # print(df)
        #df.drop(['Open', 'High', 'Low', 'Close',
        #            'Adj Close', 'Volume'], axis=1, inplace=True)
    return True    