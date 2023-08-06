from __future__ import unicode_literals

import os

import numpy as np
import pandas as pd
import pytest

from fastparquet.util import tempdir
from fastparquet import write, ParquetFile
from fastparquet.api import statistics, sorted_partitioned_columns

TEST_DATA = "test-data"


def test_statistics(tempdir):
    df = pd.DataFrame({'x': [1, 2, 3],
                       'y': [1.0, 2.0, 1.0],
                       'z': ['a', 'b', 'c']})

    fn = os.path.join(tempdir, 'foo.parquet')
    write(fn, df, row_group_offsets=[0, 2])

    p = ParquetFile(fn)

    s = statistics(p)
    expected = {'distinct_count': {'x': [None, None],
                                   'y': [None, None],
                                   'z': [None, None]},
                'max': {'x': [2, 3], 'y': [2.0, 1.0], 'z': ['b', 'c']},
                'min': {'x': [1, 3], 'y': [1.0, 1.0], 'z': ['a', 'c']},
                'null_count': {'x': [0, 0], 'y': [0, 0], 'z': [0, 0]}}

    assert s == expected


def test_logical_types(tempdir):
    df = pd.util.testing.makeMixedDataFrame()

    fn = os.path.join(tempdir, 'foo.parquet')
    write(fn, df, row_group_offsets=[0, 2])

    p = ParquetFile(fn)

    s = statistics(p)

    assert isinstance(s['min']['D'][0], (np.datetime64, pd.tslib.Timestamp))


def test_empty_statistics(tempdir):
    p = ParquetFile(os.path.join(TEST_DATA, "nation.impala.parquet"))

    s = statistics(p)
    assert s == {'distinct_count': {'n_comment': [None],
                                    'n_name': [None],
                                    'n_nationkey': [None],
                                    'n_regionkey': [None]},
                  'max': {'n_comment': [None],
                          'n_name': [None],
                          'n_nationkey': [None],
                          'n_regionkey': [None]},
                  'min': {'n_comment': [None],
                          'n_name': [None],
                          'n_nationkey': [None],
                          'n_regionkey': [None]},
                  'null_count': {'n_comment': [None],
                                 'n_name': [None],
                                 'n_nationkey': [None],
                                 'n_regionkey': [None]}}


def test_sorted_row_group_columns(tempdir):
    df = pd.DataFrame({'x': [1, 2, 3, 4],
                       'v': [{'a': 0}, {'b': -1}, {'c': 5}, {'a': 0}],
                       'y': [1.0, 2.0, 1.0, 2.0],
                       'z': ['a', 'b', 'c', 'd']})

    fn = os.path.join(tempdir, 'foo.parquet')
    write(fn, df, row_group_offsets=[0, 2], object_encoding={'v': 'json',
                                                             'z': 'utf8'})

    pf = ParquetFile(fn)

    # string stats should be stored without byte-encoding
    zcol = [c for c in pf.row_groups[0].columns
            if c.meta_data.path_in_schema == ['z']][0]
    assert zcol.meta_data.statistics.min == b'a'

    result = sorted_partitioned_columns(pf)
    expected = {'x': {'min': [1, 3], 'max': [2, 4]},
                'z': {'min': ['a', 'c'], 'max': ['b', 'd']}}

    # NB column v should not feature, as dict are unorderable
    assert result == expected


def test_iter(tempdir):
    df = pd.DataFrame({'x': [1, 2, 3, 4],
                       'y': [1.0, 2.0, 1.0, 2.0],
                       'z': ['a', 'b', 'c', 'd']})
    df.index.name = 'index'

    fn = os.path.join(tempdir, 'foo.parquet')
    write(fn, df, row_group_offsets=[0, 2], write_index=True)
    pf = ParquetFile(fn)
    out = iter(pf.iter_row_groups(index='index'))
    d1 = next(out)
    pd.util.testing.assert_frame_equal(d1, df[:2])
    d2 = next(out)
    pd.util.testing.assert_frame_equal(d2, df[2:])
    with pytest.raises(StopIteration):
        next(out)


def test_attributes(tempdir):
    df = pd.DataFrame({'x': [1, 2, 3, 4],
                       'y': [1.0, 2.0, 1.0, 2.0],
                       'z': ['a', 'b', 'c', 'd']})

    fn = os.path.join(tempdir, 'foo.parquet')
    write(fn, df, row_group_offsets=[0, 2])
    pf = ParquetFile(fn)
    assert pf.columns == ['x', 'y', 'z']
    assert len(pf.row_groups) == 2
    assert pf.count == 4
    assert fn == pf.info['name']
    assert fn in str(pf)
    for col in df:
        assert pf.dtypes[col] == df.dtypes[col]


def test_cast_index(tempdir):
    df = pd.DataFrame({'i8': np.array([1, 2, 3, 4], dtype='uint8'),
                       'i16': np.array([1, 2, 3, 4], dtype='int16'),
                       'i32': np.array([1, 2, 3, 4], dtype='int32'),
                       'i62': np.array([1, 2, 3, 4], dtype='int64'),
                       'f16': np.array([1, 2, 3, 4], dtype='float16'),
                       'f32': np.array([1, 2, 3, 4], dtype='float32'),
                       'f64': np.array([1, 2, 3, 4], dtype='float64'),
                       })
    fn = os.path.join(tempdir, 'foo.parquet')
    write(fn, df)
    pf = ParquetFile(fn)
    for col in list(df):
        d = pf.to_pandas(index=col)
        if d.index.dtype.kind == 'i':
            assert d.index.dtype == 'int64'
        elif d.index.dtype.kind == 'u':
            # new UInt64Index
            assert pd.__version__ >= '0.20'
            assert d.index.dtype == 'uint64'
        else:
            assert d.index.dtype == 'float64'
        assert (d.index == df[col]).all()


def test_zero_child_leaf(tempdir):
    df = pd.DataFrame({'x': [1, 2, 3]})

    fn = os.path.join(tempdir, 'foo.parquet')
    write(fn, df)

    pf = ParquetFile(fn)
    assert pf.columns == ['x']

    pf._schema[1].num_children = 0
    assert pf.columns == ['x']


def test_request_nonexistent_column(tempdir):
    df = pd.DataFrame({'x': [1, 2, 3]})

    fn = os.path.join(tempdir, 'foo.parquet')
    write(fn, df)

    pf = ParquetFile(fn)
    with pytest.raises(ValueError):
        pf.to_pandas(columns=['y'])


def test_read_multiple_no_metadata(tempdir):
    df = pd.DataFrame({'x': [1, 5, 2, 5]})
    write(tempdir, df, file_scheme='hive', row_group_offsets=[0, 2])
    os.unlink(os.path.join(tempdir, '_metadata'))
    os.unlink(os.path.join(tempdir, '_common_metadata'))
    import glob
    flist = list(sorted(glob.glob(os.path.join(tempdir, '*'))))
    pf = ParquetFile(flist)
    assert len(pf.row_groups) == 2
    out = pf.to_pandas()
    pd.util.testing.assert_frame_equal(out, df)


def test_single_upper_directory(tempdir):
    df = pd.DataFrame({'x': [1, 5, 2, 5], 'y': ['aa'] * 4})
    write(tempdir, df, file_scheme='hive', partition_on='y')
    pf = ParquetFile(tempdir)
    out = pf.to_pandas()
    assert (out.y == 'aa').all()

    os.unlink(os.path.join(tempdir, '_metadata'))
    os.unlink(os.path.join(tempdir, '_common_metadata'))
    import glob
    flist = list(sorted(glob.glob(os.path.join(tempdir, '*/*'))))
    pf = ParquetFile(flist, root=tempdir)
    assert pf.fn == os.path.join(tempdir, '_metadata')
    out = pf.to_pandas()
    assert (out.y == 'aa').all()


def test_numerical_partition_name(tempdir):
    df = pd.DataFrame({'x': [1, 5, 2, 5], 'y1': ['aa', 'aa', 'bb', 'aa']})
    write(tempdir, df, file_scheme='hive', partition_on=['y1'])
    pf = ParquetFile(tempdir)
    out = pf.to_pandas()
    assert out[out.y1 == 'aa'].x.tolist() == [1, 5, 5]
    assert out[out.y1 == 'bb'].x.tolist() == [2]


def test_filter_without_paths(tempdir):
    fn = os.path.join(tempdir, 'test.parq')
    df = pd.DataFrame({
        'x': [1, 2, 3, 4, 5, 6, 7],
        'letter': ['a', 'b', 'c', 'd', 'e', 'f', 'g']
    })
    write(fn, df)

    pf = ParquetFile(fn)
    out = pf.to_pandas(filters=[['x', '>', 3]])
    pd.util.testing.assert_frame_equal(out, df)
    out = pf.to_pandas(filters=[['x', '>', 30]])
    assert len(out) == 0


def test_filter_special(tempdir):
    df = pd.DataFrame({
        'x': [1, 2, 3, 4, 5, 6, 7],
        'symbol': ['NOW', 'OI', 'OI', 'OI', 'NOW', 'NOW', 'OI']
    })
    write(tempdir, df, file_scheme='hive', partition_on=['symbol'])
    pf = ParquetFile(tempdir)
    out = pf.to_pandas(filters=[('symbol', '==', 'NOW')])
    assert out.x.tolist() == [1, 5, 6]
    assert out.symbol.tolist() == ['NOW', 'NOW', 'NOW']


def test_in_filter(tempdir):
    symbols = ['a', 'a', 'b', 'c', 'c', 'd']
    values = [1, 2, 3, 4, 5, 6]
    df = pd.DataFrame(data={'symbols': symbols, 'values': values})
    write(tempdir, df, file_scheme='hive', partition_on=['symbols'])
    pf = ParquetFile(tempdir)
    out = pf.to_pandas(filters=[('symbols', 'in', ['a', 'c'])])
    assert set(out.symbols) == {'a', 'c'}


def test_in_filter_numbers(tempdir):
    symbols = ['a', 'a', 'b', 'c', 'c', 'd']
    values = [1, 2, 3, 4, 5, 6]
    df = pd.DataFrame(data={'symbols': symbols, 'values': values})
    write(tempdir, df, file_scheme='hive', partition_on=['values'])
    pf = ParquetFile(tempdir)
    out = pf.to_pandas(filters=[('values', 'in', ['1', '4'])])
    assert set(out.symbols) == {'a', 'c'}
    out = pf.to_pandas(filters=[('values', 'in', [1, 4])])
    assert set(out.symbols) == {'a', 'c'}


def test_filter_stats(tempdir):
    df = pd.DataFrame({
        'x': [1, 2, 3, 4, 5, 6, 7],
    })
    write(tempdir, df, file_scheme='hive', row_group_offsets=[0, 4])
    pf = ParquetFile(tempdir)
    out = pf.to_pandas(filters=[('x', '>=', 5)])
    assert out.x.tolist() == [5, 6, 7]


def test_index_not_in_columns(tempdir):
    df = pd.DataFrame({'a': ['x', 'y', 'z'], 'b': [4, 5, 6]}).set_index('a')
    write(tempdir, df, file_scheme='hive')
    pf = ParquetFile(tempdir)
    out = pf.to_pandas(columns=['b'])
    assert out.index.tolist() == ['x', 'y', 'z']
    out = pf.to_pandas(columns=['b'], index=False)
    assert out.index.tolist() == [0, 1, 2]


def test_no_index_name(tempdir):
    df = pd.DataFrame({'__index_level_0__': ['x', 'y', 'z'],
                       'b': [4, 5, 6]}).set_index('__index_level_0__')
    write(tempdir, df, file_scheme='hive')
    pf = ParquetFile(tempdir)
    out = pf.to_pandas()
    assert out.index.name is None
    assert out.index.tolist() == ['x', 'y', 'z']

    df = pd.DataFrame({'__index_level_0__': ['x', 'y', 'z'],
                       'b': [4, 5, 6]})
    write(tempdir, df, file_scheme='hive')
    pf = ParquetFile(tempdir)
    out = pf.to_pandas(index='__index_level_0__', columns=['b'])
    assert out.index.name is None
    assert out.index.tolist() == ['x', 'y', 'z']

    pf = ParquetFile(tempdir)
    out = pf.to_pandas()
    assert out.index.name is None
    assert out.index.tolist() == [0, 1, 2]
