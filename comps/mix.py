
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
    