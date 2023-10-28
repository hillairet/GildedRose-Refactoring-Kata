# -*- coding: utf-8 -*-
from typing import Callable, Optional


class GildedRose(object):
    def __init__(self, items):
        self.items = items

    def update_quality(self):
        for item in self.items:
            _update_item(item)


def _update_item(item):
    if _check_for_sulfuras(item):
        return

    if update_aged_brie := _check_for_aged_brie(item):
        update_aged_brie(item)
        return

    if update_backstage_passes := _check_for_backstage_passes(item):
        update_backstage_passes(item)
        return

    if update_conjured := _check_for_conjured(item):
        update_conjured(item)
        return

    _update_standard_item(item)


class Item:
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)


def _check_for_sulfuras(item: Item) -> bool:
    return item.name.startswith('Sulfuras')


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


def _check_for_conjured(item: Item) -> Optional[Callable]:
    if not item.name.startswith('Conjured'):
        return

    def _update_conjured(item: Item) -> None:
        item.sell_in = item.sell_in - 1
        if item.quality < 2:
            item.quality = 0
            return
        item.quality = item.quality - 2

    return _update_conjured


def _update_standard_item(item: Item) -> None:
    item.sell_in = item.sell_in - 1

    _degrade_regularly(item=item)


def _degrade_regularly(item: Item, decay_speed: int = 1) -> None:
    increment = 2 * decay_speed if item.sell_in < 0 else decay_speed

    if item.quality < increment:
        item.quality = 0
        return

    item.quality = item.quality - increment
