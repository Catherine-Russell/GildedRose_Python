# -*- coding: utf-8 -*-
import unittest

from gilded_rose import Item, GildedRose
"""
normal_item_decreases_quality_by_1_each_day_for_2_days
normal_item_decreases_quality_by_2_after_sellIn

aged brie - increases daily
aged_brie_never_increases_more_than_50
aged_brie_continues_increasing_in_quality_after_sellIn_expires

sulfuras_quality_is_always_80

backstage_pass_quality_increases_by_1_more_than_10days_before
backstage_pass_quality_increases_by_2_10_days_before
backstage_pass_quality_increases_by_2_less_than_10days_before
backstage_pass_quality_drops_to_0_after_sellIn_expires
backstage_pass_quality_doesnt_go_above_50


"""

class GildedRoseTest(unittest.TestCase):
    
    
    # helper for running a select number of days of depreciation
    def run_update_quality_n_times(self, items, days):
        gilded_rose = GildedRose(items)
        for _ in range(days):
            gilded_rose.update_quality()
        return items
    
    # helper for running 1 day of depreciation
    def run_update_quality_once(self, items):
        return self.run_update_quality_n_times(items, 1)

    def test_name_does_not_change_when_quality_updated(self):
        items = self.run_update_quality_once([Item("foo", 0, 0)])
        self.assertEqual("foo", items[0].name)

    def test_quality_does_not_drop_below_zero(self):
        items = self.run_update_quality_once([Item("foo", 0, 0)])
        self.assertEqual(0, items[0].quality)

    def test_normal_item_decreases_quality_by_1_each_day_for_2_days(self):
        items = self.run_update_quality_n_times([Item("foo", 5, 5)], 2)
        self.assertEqual(3, items[0].quality)

    def test_normal_item_decreases_quality_by_2_after_sellIn(self):
        items = self.run_update_quality_once([Item("foo", -1, 5)])
        self.assertEqual(3, items[0].quality)

    def test_aged_brie_increases_daily(self):
        items = self.run_update_quality_once([Item("Aged Brie", 5, 5)])
        self.assertEqual(6, items[0].quality)
    
    def test_aged_brie_never_increases_more_than_50(self):
        items = self.run_update_quality_n_times([Item("Aged Brie", 5, 50)], 5)
        self.assertEqual(50, items[0].quality)

    def test_aged_brie_doesnt_go_above_50_even_if_on_49(self):
        items = self.run_update_quality_once([Item("Aged Brie", -1, 49)])
        self.assertEqual(50, items[0].quality)

    def test_aged_brie_continues_increasing_in_quality_after_sellIn_expires(self):
        items = self.run_update_quality_once([Item("Aged Brie", -1, 5)])
        self.assertEqual(7, items[0].quality)

    def test_aged_brie_sellIn_goes_down_even_if_quality_is_50(self):
        items = self.run_update_quality_once([Item("Aged Brie", -1, 50)])
        self.assertEqual(-2, items[0].sell_in)

    def test_aged_brie_quality_goes_up_by_one_when_sellIn_is_zero(self):
        items = self.run_update_quality_once([Item("Aged Brie", 0, 20)])
        self.assertEqual(21, items[0].quality)
    
    def test_sulfuras_quality_is_always_80(self):
        items = self.run_update_quality_once([Item("Sulfuras, Hand of Ragnaros", 5, 80)])
        self.assertEqual(80, items[0].quality)

    def test_backstage_pass_quality_increases_by_1_more_than_10days_before(self):
        items = self.run_update_quality_once([Item("Backstage passes to a TAFKAL80ETC concert", 11, 25)])
        self.assertEqual(26, items[0].quality)

    def test_backstage_pass_quality_increases_by_2_10_days_before(self):
        items = self.run_update_quality_once([Item("Backstage passes to a TAFKAL80ETC concert", 10, 25)])
        self.assertEqual(27, items[0].quality)

    def test_backstage_pass_quality_increases_by_2_less_than_10days_but_above_5_before(self):
        items = self.run_update_quality_once([Item("Backstage passes to a TAFKAL80ETC concert", 7, 25)])
        self.assertEqual(27, items[0].quality)

    def test_backstage_pass_quality_increases_by_3_5days_before(self):
        items = self.run_update_quality_once([Item("Backstage passes to a TAFKAL80ETC concert", 5, 25)])
        self.assertEqual(28, items[0].quality)

    def test_backstage_pass_quality_increases_by_3_less_than_5days_before(self):
        items = self.run_update_quality_once([Item("Backstage passes to a TAFKAL80ETC concert", 2, 25)])
        self.assertEqual(28, items[0].quality)

    def test_backstage_pass_quality_drops_to_0_after_sellIn_expires(self):
        items = self.run_update_quality_once([Item("Backstage passes to a TAFKAL80ETC concert", 0, 25)])
        self.assertEqual(0, items[0].quality)

    def test_backstage_pass_quality_doesnt_go_above_50(self):
        items = self.run_update_quality_once([Item("Backstage passes to a TAFKAL80ETC concert", 3, 50)])
        self.assertEqual(50, items[0].quality)
    
    def test_sellIn_drops_by_one_for_normal_item(self):
        items = self.run_update_quality_once([Item("Normal Item,", 3, 20)])
        self.assertEqual(2, items[0].sell_in)

    def test_sellIn_drops_by_one_for_Aged_brie(self):
        items = self.run_update_quality_once([Item("Aged Brie", 3, 20)])
        self.assertEqual(2, items[0].sell_in)

    def test_sellIn_drops_by_one_for_tickets(self):
        items = self.run_update_quality_once([Item("Backstage passes to a TAFKAL80ETC concert", 3, 20)])
        self.assertEqual(2, items[0].sell_in)
    
    def test_sellIn_doesnt_drop_for_sulfuras(self):
        items = self.run_update_quality_once([Item("Sulfuras, Hand of Ragnaros", 3, 80)])
        self.assertEqual(3, items[0].sell_in)

"""
TDD for update
- __"Conjured"__ items degrade in `Quality` twice as fast as normal items

"""
        

if __name__ == '__main__':
    unittest.main()
