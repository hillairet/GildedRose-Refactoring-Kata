from .items import extended_item_factory


class GildedRose(object):
    def __init__(self, items):
        self.items = items

    def update_quality(self):
        for item in self.items:
            extended_item = extended_item_factory(item)
            extended_item.update_daily()
