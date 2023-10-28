import csv
from copy import deepcopy
from itertools import product

from gilded_rose import GildedRose, Item

ITEMS_DATA_CSV = 'items_data.csv'

NAMES = [
    '+5 Dexterity Vest',
    'Aged Brie',
    'Elixir of the Mongoose',
    'Backstage passes to a TAFKAL80ETC concert',
    'Conjured Mana Cake',
]
LEGENDARY_ITEM = 'Sulfuras, Hand of Ragnaros'
SELL_INS = range(50, -31, -5)
QUALITIES = range(50, -1, -5)


def generate_items() -> list[Item]:
    sell_ins_qualities = product(SELL_INS, QUALITIES)

    items_2tuples = product(NAMES, sell_ins_qualities)

    items = []
    for it in items_2tuples:
        items.append(Item(name=it[0], sell_in=it[1][0], quality=it[1][1]))

    items.append(Item(name=LEGENDARY_ITEM, sell_in=0, quality=80))
    items.append(Item(name=LEGENDARY_ITEM, sell_in=-1, quality=80))

    return items


if __name__ == '__main__':
    items = generate_items()
    expected_items = [deepcopy(item) for item in items]
    GildedRose(expected_items).update_quality()

    item_data = []
    for item, expected in zip(items, expected_items):
        if 'Conjured' in item.name and item.sell_in < 1:
            expected_quality = item.quality - 4 if item.quality > 3 else 0
            item_data.append(
                (item.name, item.sell_in, item.quality, expected.sell_in, expected_quality)
            )
            continue
        item_data.append(
            (item.name, item.sell_in, item.quality, expected.sell_in, expected.quality)
        )

    with open(ITEMS_DATA_CSV, 'w', newline='') as csvfile:
        itemmwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        header = ['name', 'input_sell_in', 'input_quality', 'expected_sell_in', 'expected_quality']
        itemmwriter.writerow(header)
        for item in item_data:
            itemmwriter.writerow(item)
