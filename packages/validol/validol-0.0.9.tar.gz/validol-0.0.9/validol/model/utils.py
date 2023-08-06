import datetime as dt
import heapq
import itertools
from bisect import bisect_left
from functools import reduce
from time import mktime
import numpy as np
from tabula import read_pdf
import pandas as pd
import os


def to_timestamp(date):
    return int(mktime(date.timetuple()))


def take_closest(l, date):
    pos = bisect_left(l, date)

    if pos == 0:
        return 0
    elif pos == len(l):
        return len(l) - 1

    before = l[pos - 1]
    after = l[pos]

    if after.toordinal() - date.toordinal() < date.toordinal() - before.toordinal():
        return pos
    else:
        return pos - 1


def flatten(l):
    while type(l[0]) == list:
        l = list(itertools.chain.from_iterable(l))

    return l


def split(l, value):
    return [list(group) for key, group in itertools.groupby(l, lambda x: x == value) if not key]


def my_division(a, b):
    if b != 0:
        return a / b
    else:
        return None


def none_filter(f):
    def func(*args):
        if None in args:
            return None
        else:
            return f(*args)

    return func


def parse_isoformat_date(date):
    return dt.datetime.strptime(date, "%Y-%m-%d").date()


def zip_map(funcList, values):
    return list(map(lambda f, x: f(x), funcList, values))


def merge_lists(lists):
    heads = [(lists[i][0], i) for i in range(len(lists))]
    indexes = [[] for _ in range(len(lists))]
    poses = [1 for _ in range(len(lists))]
    result = []
    heapq.heapify(heads)
    while len(heads):
        val, index = heapq.heappop(heads)
        pos = poses[index]
        if pos != len(lists[index]):
            heapq.heappush(heads, (lists[index][pos], index))
            poses[index] += 1

        index_pos = len(result) - 1
        if not result or val != result[-1]:
            result.append(val)
            index_pos += 1

        indexes[index].append(index_pos)

    return result, indexes


def intersect_lists(lists):
    return reduce(np.intersect1d, lists)


def group_by(df, columns):
    return df.groupby(columns, sort=False)[[col for col in df.columns if col not in columns]]


def date_to_timestamp(df):
    df.Date = df.apply(lambda row: to_timestamp(row['Date']), axis=1)
    return df


def remove_duplications(arr):
    s = set()
    result = []
    for item in arr:
        if item not in s:
            s.add(item)
            result.append(item)

    return result


def pdf(fname, pages, spreadsheet):
    df = pd.DataFrame()

    for page, area in pages:
        df = df.append(read_pdf(fname,
                                pages=page,
                                area=area,
                                spreadsheet=spreadsheet,
                                pandas_options={'header': None}))

    return df


def date_range(first, last):
    return [first + dt.timedelta(i) for i in range(0, (last - first).days + 1)]


def merge_dfs(dfa, dfb):
    suffix = "_y"

    merged = dfa.merge(dfb, 'outer', left_index=True, right_index=True,
                       sort=True, suffixes=("", suffix))

    intersection = set(dfa.columns) & set(dfb.columns)

    for col in intersection:
        merged[col].fillna(merged[col + suffix], inplace=True)
        del merged[col + suffix]

    return merged


def merge_dfs_list(dfs):
    result = dfs[0]
    for df in dfs[1:]:
        result = merge_dfs(result, df)

    return result


def isfile(ftp, file):
    try:
        ftp.size(file)
        return True
    except:
        return False


def concat(dfs):
    if dfs:
        return pd.concat(dfs)
    else:
        return pd.DataFrame()


class TempFile:
    def __init__(self):
        self.name = 'tempfile{}'.format(np.random.randint(1e8))

    def __enter__(self):
        self.file = open(self.name, 'wb')

        return self.file

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.file.close()

        os.remove(self.name)