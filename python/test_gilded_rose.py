# -*- coding: utf-8 -*-
from pytest import mark, param

from gilded_rose import GildedRose, Item

item_fixture = [param("+5 Dexterity Vest", 10, 20)]


@mark.parametrize('name, sell_in, quality', item_fixture)
def test_gilded_rose(name, sell_in, quality):
    items = [Item(name, sell_in, quality)]
    gilded_rose = GildedRose(items)
    gilded_rose.update_quality()
    assert items[0].sell_in == sell_in - 1
