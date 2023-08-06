from cytoolz import dissoc
from cytoolz import partial
from cytoolz import reduce
from cytoolz import sliding_window
from merlin import functions as f
from merlin import timeseries
from merlin.support import aardvark as ma
from operator import eq
from operator import gt
import pytest
import test


def test_csort():
    data = list()
    data.append({'acquired': '2015-04-01'})
    data.append({'acquired': '2017-04-01'})
    data.append({'acquired': '2017-01-01'})
    data.append({'acquired': '2016-04-01'})
    results = timeseries.sort(data)
    assert(results[0]['acquired'] > results[1]['acquired'] >
           results[2]['acquired'] > results[3]['acquired'])


def test_create():
    # data should be shaped: ( ((chip_x, chip_y, x1, y1),{}),
    #                          ((chip_x, chip_y, x1, y2),{}), )

    # This should fail because the test data contains additional qa chips
    with pytest.raises(Exception):
        data = timeseries.create(
                   point=(-182000, 300400),
                   specs_fn=ma.chip_specs,
                   chips_url='http://localhost',
                   chips_fn=ma.chips,
                   acquired='1980-01-01/2015-12-31',
                   queries=test.chip_spec_queries('http://localhost'))


    # test with chexists to handle quality assymetry
    data = timeseries.create(
                    point=(-182000, 300400),
                    dates_fn=partial(f.chexists,
                                     check_fn=timeseries.symmetric_dates,
                                     keys=['quality']),
                    specs_fn=ma.chip_specs,
                    chips_url='http://localhost',
                    chips_fn=ma.chips,
                    acquired='1980-01-01/2015-12-31',
                    queries=test.chip_spec_queries('http://localhost'))

    # make sure we have 10000 results
    assert len(data) == 10000
    assert isinstance(data, tuple)
    assert isinstance(data[0], tuple)
    assert isinstance(data[0][0], tuple)
    assert isinstance(data[0][1], dict)

    # chip_x, chip_y, x, y.  data[0][1] is the dictionary of measurements
    assert len(data[0][0]) == 4

    # check to make sure we have equal length values and that the values
    # are not empty.  FYI -- only spot checking the first returned result
    queries = test.chip_spec_queries('http://localhost')
    lens = [len(data[0][1][item]) for item in queries]
    print("Lengths:{}".format(lens))
    assert all([eq(*x) for x in sliding_window(2, lens)]) == True

    # make sure everything isn't zero length
    assert all([gt(x, 0) for x in lens]) == True
