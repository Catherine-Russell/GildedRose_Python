# -*- coding: utf-8 -*-

class GildedRose(object):

    def __init__(self, items):
        self.items = items

    def update_quality(self):
        for item in self.items:
            if item.name == "Sulfuras, Hand of Ragnaros":
                continue

            if item.name == "Aged Brie":
                self.update_aged_brie(item) 
            elif item.name == "Backstage passes to a TAFKAL80ETC concert":
                self.update_tickets(item)
            else:
                self.update_normal_item(item)

        item.sell_in -= 1



    def update_aged_brie(self, item):        
        if item.sell_in >= 0:
            item.quality += 1
        else:
            item.quality += 2

        if item.quality > 50:
            item.quality = 50

    def update_tickets(self, item):
        match item:
            case int if item.sell_in <= 0:
                item.quality = 0
            case int if item.sell_in > 10:
                item.quality += 1
            case int if item.sell_in > 5:
                item.quality += 2
            case int if item.sell_in > 0:
                item.quality += 3
        if item.quality > 50:
            item.quality = 50
        
    def update_normal_item(self, item):                
        if item.sell_in >= 0:
            item.quality -= 1
        else:
            item.quality -= 2

        if item.quality < 0:
            item.quality = 0

class Item:
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)
