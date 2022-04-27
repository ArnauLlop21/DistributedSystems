def apply(df, cond):
    return str(df.apply(eval(cond)))

def columns(df):
    return str(df.columns)

def groupby(df, param):
    return str(df.groupby(param).agg(['mean', 'count']).values.tolist())

def head(df, number):
    return str(df.head(number))

def isin(df, value):
    val=list(value.split(","))
    return str(df.isin(val))

def max(df, column):
    return df[column].max()

def min(df, column):
    return df[column].min()

def items(df):
    aux=[]
    for label, content in df.items():
        aux.append(f'label:' + str(label))
        aux.append(f'content:' + str(content))
    return str(aux)

