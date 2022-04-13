def apply(df, cond):
    return df.apply(eval(cond))

def columns(df):
    return df.columns

def groupby(df, param):
    par=list(param.split(","))
    return df.groupby(eval(param)).agg['mean', 'count']

def head(df, number):
    return df.head(number)

def isin(df, value):
    val=list(value.split(","))
    return df.isin(val)

def max(df, column):
    return df[column].max()

def min(df, column):
    return df[column].min()

def items(df):
    aux=[]
    for label, content in df.items():
        aux.append(f'label:' + str(label))
        aux.append(f'content:' + str(content))
    return aux
