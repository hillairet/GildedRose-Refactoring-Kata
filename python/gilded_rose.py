# -*- coding: utf-8 -*-
from typing import Callable, Optional


class GildedRose(object):
    def __init__(self, items):
        self.items = items

    def update_quality(self):
        for item in self.items:
            _update_item(item)


def _update_item(item):
    item_ext = ItemExtended(name=item.name, sell_in=item.sell_in, quality=item.quality)

    if item_ext.is_sulfuras:
        return

    if update_aged_brie := _check_for_aged_brie(item):
        update_aged_brie(item)
        return

    if update_backstage_passes := _check_for_backstage_passes(item):
        update_backstage_passes(item)
        return

    if item.quality > 0:
        item.quality = item.quality - 1

    item.sell_in = item.sell_in - 1
    if item.sell_in < 0:
        if item.quality > 0:
            item.quality = item.quality - 1


class Item:
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)


def _check_for_aged_brie(item: Item) -> Optional[Callable]:
    if item.name != 'Aged Brie':
        return

    def _update_aged_brie(item: Item) -> None:
        quality_increment = 1 if item.sell_in > 0 else 2
        item.sell_in = item.sell_in - 1
        if item.quality > 49:
            return
        item.quality = item.quality + quality_increment
        return

    return _update_aged_brie


def _check_for_backstage_passes(item: Item) -> Optional[Callable]:
    if not item.name.startswith('Backstage passes'):
        return

    def _update_backstage_passes(item: Item) -> None:
        item.sell_in = item.sell_in - 1
        if item.sell_in < 0:
            item.quality = 0
            return
        if item.quality > 49:
            return

        quality_increment = 1
        if item.sell_in < 10:
            quality_increment += 1
        if item.sell_in < 5:
            quality_increment += 1

        item.quality = item.quality + quality_increment
        return

    return _update_backstage_passes


class ItemExtended(Item):
    @property
    def is_sulfuras(self) -> bool:
        return self.name.startswith('Sulfuras')

    @property
    def is_conjured(self) -> bool:
        return self.name.startswith('Conjured')
