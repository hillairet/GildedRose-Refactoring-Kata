# -*- coding: utf-8 -*-


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

    if (not item_ext.is_aged_brie) and (not item_ext.is_backstage_passes):
        if item.quality > 0:
            item.quality = item.quality - 1
    else:
        if item.quality < 50:
            item.quality = item.quality + 1
            if item_ext.is_backstage_passes:
                if item.sell_in < 11:
                    if item.quality < 50:
                        item.quality = item.quality + 1
                if item.sell_in < 6:
                    if item.quality < 50:
                        item.quality = item.quality + 1
    item.sell_in = item.sell_in - 1
    if item.sell_in < 0:
        if not item_ext.is_aged_brie:
            if not item_ext.is_backstage_passes:
                if item.quality > 0:
                    item.quality = item.quality - 1
            else:
                item.quality = item.quality - item.quality
        else:
            if item.quality < 50:
                item.quality = item.quality + 1


class Item:
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)


class ItemExtended(Item):
    @property
    def is_aged_brie(self) -> bool:
        return self.name == 'Aged Brie'

    @property
    def is_backstage_passes(self) -> bool:
        return self.name.startswith('Backstage passes')

    @property
    def is_sulfuras(self) -> bool:
        return self.name.startswith('Sulfuras')

    @property
    def is_conjured(self) -> bool:
        return self.name.startswith('Conjured')
