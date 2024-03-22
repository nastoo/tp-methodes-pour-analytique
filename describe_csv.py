import os
import numpy as np
import pandas as pd

def change_file_extension(path, ext):
    """
    Change extension of file. New extension is ext
    """
    prefix, _ = os.path.splitext(path)
    return prefix + "." + ext

def approximate_row_count(file):
    """
    Return approximate count of rows of file
    """
    n = 0
    with open(file) as f:
        for i, l in enumerate(f):
            n += len(l)
            if i == 10**6:
                break
    return i * (os.path.getsize(file) / n)

def optimal_type(col, min_value, max_value):
    """
    Return optimal type of column col, whose min value is min_value, and max value is max_value
    """
    t = col.dtype
    if np.issubdtype(t, np.integer):
        if min_value >= np.iinfo(np.int8).min and max_value <= np.iinfo(np.int8).max:
            opt_type = 'int8'
        elif min_value >= np.iinfo(np.int16).min and max_value <= np.iinfo(np.int16).max:
            opt_type = 'int16'
        elif min_value >= np.iinfo(np.int32).min and max_value <= np.iinfo(np.int32).max:
            opt_type = 'int32'
        else:
            opt_type = 'int64'
    elif t == float or t == np.float16 or t == np.float32 or t == np.float64:

        # if every non-null value is integer, then convert to integer type
        col_no_null = col.dropna()
        if np.all(col_no_null.astype(np.int64) == col_no_null):
            return optimal_type(col_no_null.astype(np.int64), min_value, max_value)

        if min_value >= np.finfo(np.float16).min and max_value <= np.finfo(np.float16).max:
            opt_type = 'float16'
        elif min_value >= np.finfo(np.float32).min and max_value <= np.finfo(np.float32).max:
            opt_type = 'float32'
        else:
            opt_type = 'float64'
    else:
        opt_type = np.dtype(t).name

    return opt_type

def describe_csv(file, delimiter, chunksize=10 ** 4, nrows=None):
    """
    Describe file
    """
    print(int(approximate_row_count(file)) // 10**6, "M rows approx.")

    top_df = pd.read_csv(file, delimiter=delimiter, nrows=10**4)
    c = 0
    usecols = []
    min_col = {}
    max_col = {}
    nulls_col = {}
    type_col = {}
    for col in top_df.columns:
        min_col[col] = np.inf
        max_col[col] = -np.inf
        nulls_col[col] = 0
        if top_df[col].dtype != object:
            usecols += [c]
        else:
            try:
                _ = pd.to_datetime(top_df[col], format='mixed')
                type_col[col] = np.datetime64
            except (TypeError, ValueError):
                type_col[col] = object

        c += 1

   # read_csv par morceaux de 10**4 chunksize (10 000) par ex. --> donc 1000 chunks (10 000 000 / 10 000)
    chunks = pd.read_csv(file, delimiter=delimiter, usecols=usecols, chunksize=chunksize, engine='c', nrows=nrows)
    chunk_num = 0
    for chunk in chunks:
        for col in chunk.columns:
            min_col[col] = min(min_col[col], chunk[col].min())
            max_col[col] = max(max_col[col], chunk[col].max())
            nulls_col[col] += len(chunk[chunk[col].isnull()])

        chunk_num += 1
        print(chunk_num, end=' ')

    # build decription
    print("\n---------------------------------------------------")
    print(file)
    print("---------------------------------------------------")
    desc = pd.DataFrame(columns=['Col', 'type', 'min', 'max', 'nulls', 'optimal type'])
    r = 0
    columns = []
    for col in top_df.columns:
        if col in chunk.columns:
            opt_type = optimal_type(chunk[col], min_col[col], max_col[col])
            rec = [col, chunk[col].dtype, min_col[col], max_col[col], nulls_col[col], opt_type]
            c1 = "'" + col + "': " + ("(" if nulls_col[col] > 0 else "") \
                + ('np.' if opt_type.startswith('int') or opt_type.startswith('float') else "") + opt_type \
                + (", " + (str(min_col[col]-1) + ")") if nulls_col[col] > 0 else "")
        else:
            rec = [col, np.dtype(type_col[col]).name, "-", "-", "-", top_df[col].dtype]
            c1 = "'" + col + "': " + np.dtype(type_col[col]).name

        desc.loc[r] = rec
        columns += [c1]
        r += 1
    print(desc)
    print("\n", chunksize * (chunk_num - 1) + (len(chunk) if len(chunk) < chunksize else 0), " rows")
