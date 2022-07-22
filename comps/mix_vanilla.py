#############################################
# Funções que não precisam importar módulos #
############################################# 

def format_link(text = '', name = '', url = ''):
    '''retorna f\'string com texto e link para url '''
    return f'{text}[{name}]({url})'


def chart_summary(df, display):
    ''' Exibe um resumo dos dados e retorna o numero de raios do Histograma'''
    items = len(df.index)
    if display == 'Range_pct':
        bins_chart = len(df['Range_pct'].value_counts())
    else:
        bins_chart = len(df['Range'].value_counts())
    #bins_chart = df[display].value_counts()
    return bins_chart,(f'Foram encontrados {items} periodos com {bins_chart} valores distintos') 
    

def cooking_range(df):
    '''Executa o tratamento dos dados. Neste caso, cria a coluna de ranges e elimina as colunas desnecessárias'''
    if len(df) > 0:
        # 1. pega os valores de máxima e mínima do dia
        # 2. Calcula range numérico e percentual
        if 'High' in df:
            # cria colunas com valores que serão usados
            df['Range_pct'] = (df.High/df.Low - 1) * 100
            df['Range'] = abs(df.High - df.Low)
            # elimina colunas desnecessárias
            df.drop(['Open', 'High', 'Low', 'Close',
                     'Adj Close', 'Volume'], axis=1, inplace=True)
    else:
        #st.write('Ops! Não encontramos informações deste ativo. O código pode não existir, ter sido mudado ou desativado. Confira e tente novamente.')
        return False    
    return True