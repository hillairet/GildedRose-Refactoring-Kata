# -*- coding: utf-8 -*-
from itertools import product

from pytest import mark, param

from gilded_rose import GildedRose, Item

NAMES = [
    "+5 Dexterity Vest",
    "Aged Brie",
    "Elixir of the Mongoose",
    "Backstage passes to a TAFKAL80ETC concert",
    "Conjured Mana Cake",
]
LEGENDARY_ITEM = "Sulfuras, Hand of Ragnaros"


def item_fixture():
    sell_ins = range(50, -31, -5)
    qualities = range(50, -1, -5)

    sell_ins_qualities = product(sell_ins, qualities)

    items_2tuples = product(NAMES, sell_ins_qualities)

    params = [param(it[0], it[1][0], it[1][1]) for it in items_2tuples]

    params.append(param(LEGENDARY_ITEM, 0, 80))
    params.append(param(LEGENDARY_ITEM, -1, 80))

    return params


@mark.parametrize('name, sell_in, quality', item_fixture())
def test_gilded_rose(name, sell_in, quality):
    items = [Item(name, sell_in, quality)]
    gilded_rose = GildedRose(items)
    gilded_rose.update_quality()

    if name == LEGENDARY_ITEM:
        assert items[0].sell_in == sell_in
    else:
        assert items[0].sell_in == sell_in - 1
