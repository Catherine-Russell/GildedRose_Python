# -*- coding: utf-8 -*-

class GildedRose(object):

    def __init__(self, items):
        self.items = items

    def update_quality(self):
        for item in self.items:
            if item.name == "Sulfuras, Hand of Ragnaros":
                continue
                # Aged Brie
            if item.name == "Aged Brie":
                if item.quality == 50:
                    continue
                item.quality += 1
                if item.sell_in < 0 and item.quality < 50:
                    item.quality += 1
                    


                # tivkets
            
                # other
            
            # This is the normal items thing
            elif item.name == "Backstage passes to a TAFKAL80ETC concert":
                if item.quality < 50:
                    item.quality += 1
                    if item.name == "Backstage passes to a TAFKAL80ETC concert":
                        if item.sell_in < 11:
                            if item.quality < 50:
                                item.quality = item.quality + 1
                        if item.sell_in < 6:
                            if item.quality < 50:
                                item.quality = item.quality + 1
            else:
                if item.quality > 0:
                    item.quality = item.quality - 1
                
            item.sell_in -= 1
            if item.sell_in < 0:
                if item.name != "Aged Brie":
                    if item.name != "Backstage passes to a TAFKAL80ETC concert":
                        if item.quality > 0:
                            item.quality = item.quality - 1
                    else:
                        item.quality = 0
            # item.sell_in -= 1


class Item:
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)


gilded_rose = GildedRose([Item("Aged Brie", -1, 5)])
gilded_rose.update_quality()
print("expect item quality to be 7")
print(gilded_rose.items)


