# -*- coding: utf-8 -*-
import csv

from pytest import mark, param

from generate_item_test_data import ITEMS_DATA_CSV
from gilded_rose import GildedRose, Item


def item_fixture():
    params = []
    with open(ITEMS_DATA_CSV, newline='') as csvfile:
        itemreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        next(itemreader)
        for row in itemreader:
            data = [row[0]] + [int(r) for r in row[1:]]
            params.append(param(*data))

    return params


@mark.parametrize(
    'name, input_sell_in, input_quality, expected_sell_in, expected_quality', item_fixture()
)
def test_gilded_rose(name, input_sell_in, input_quality, expected_sell_in, expected_quality):
    items = [Item(name, input_sell_in, input_quality)]
    gilded_rose = GildedRose(items)
    gilded_rose.update_quality()

    actual = items[0]
    assert actual.sell_in == expected_sell_in
    assert actual.quality == expected_quality
