from abc import ABC, abstractmethod


class Item:
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return '%s, %s, %s' % (self.name, self.sell_in, self.quality)


class ExtendedItem(ABC):
    def __init__(self, item: Item):
        self.item = item

    @staticmethod
    @abstractmethod
    def is_matching(item: Item) -> bool:
        return True

    @abstractmethod
    def update_daily(self) -> None:
        pass

    def _calculate_standard_decay(self, decay_rate: int = 1) -> None:
        increment = 2 * decay_rate if self.item.sell_in < 0 else decay_rate

        if self.item.quality < increment:
            self.item.quality = 0
            return

        self.item.quality = self.item.quality - increment


def extended_item_factory(item: Item) -> ExtendedItem:
    special_items = [SulfurasItem, AgedBrieItem, BackstagePassesItem, ConjuredItem]

    for special_item in special_items:
        if special_item.is_matching(item):
            return special_item(item)

    return StandardItem(item)


class StandardItem(ExtendedItem):
    @staticmethod
    def is_matching(item: Item):
        return True

    def update_daily(self) -> None:
        self.item.sell_in = self.item.sell_in - 1

        self._calculate_standard_decay()


class ConjuredItem(ExtendedItem):
    @staticmethod
    def is_matching(item: Item):
        return item.name.startswith('Conjured')

    def update_daily(self) -> None:
        self.item.sell_in = self.item.sell_in - 1

        self._calculate_standard_decay(decay_rate=2)


class SulfurasItem(ExtendedItem):
    @staticmethod
    def is_matching(item: Item):
        return item.name.startswith('Sulfuras')

    def update_daily(self) -> None:
        return


class AgedBrieItem(ExtendedItem):
    @staticmethod
    def is_matching(item: Item):
        return item.name == 'Aged Brie'

    def update_daily(self) -> None:
        quality_increment = 1 if self.item.sell_in > 0 else 2
        self.item.sell_in = self.item.sell_in - 1

        if self.item.quality > 49:
            return

        self.item.quality = self.item.quality + quality_increment


class BackstagePassesItem(ExtendedItem):
    @staticmethod
    def is_matching(item: Item):
        return item.name.startswith('Backstage passes')

    def update_daily(self) -> None:
        self.item.sell_in = self.item.sell_in - 1
        if self.item.sell_in < 0:
            self.item.quality = 0
            return
        if self.item.quality > 49:
            return

        quality_increment = 1
        if self.item.sell_in < 10:
            quality_increment += 1
        if self.item.sell_in < 5:
            quality_increment += 1

        self.item.quality = self.item.quality + quality_increment
