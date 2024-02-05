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
    def run_gilded_rose_n_times(self, items, days):
        gilded_rose = GildedRose(items)
        for _ in range(days):
            gilded_rose.update_quality()
        return items
    
    # helper for running 1 day of depreciation
    def run_gilded_rose_once(self, items):
        return self.run_gilded_rose_n_times(items, 1)

    def test_name_does_not_change_when_quality_updated(self):
        items = self.run_gilded_rose_once([Item("foo", 0, 0)])
        self.assertEqual("foo", items[0].name)

    def test_quality_does_not_drop_below_zero(self):
        items = self.run_gilded_rose_once([Item("foo", 0, 0)])
        self.assertEqual(0, items[0].quality)

    def test_normal_item_decreases_quality_by_1_each_day_for_2_days(self):
        items = self.run_gilded_rose_n_times([Item("foo", 5, 5)], 2)
        self.assertEqual(3, items[0].quality)

    def test_normal_item_decreases_quality_by_2_after_sellIn(self):
        items = self.run_gilded_rose_once([Item("foo", -1, 5)])
        self.assertEqual(3, items[0].quality)

    def test_aged_brie_increases_daily(self):
        items = self.run_gilded_rose_once([Item("Aged Brie", 5, 5)])
        self.assertEqual(6, items[0].quality)
    
    def test_aged_brie_never_increases_more_than_50(self):
        items = self.run_gilded_rose_n_times([Item("Aged Brie", 5, 50)], 5)
        self.assertEqual(50, items[0].quality)

    def test_aged_brie_doesnt_go_above_50_even_if_on_49(self):
        items = self.run_gilded_rose_once([Item("Aged Brie", -1, 49)])
        self.assertEqual(50, items[0].quality)

    def test_aged_brie_continues_increasing_in_quality_after_sellIn_expires(self):
        items = self.run_gilded_rose_once([Item("Aged Brie", -1, 5)])
        self.assertEqual(7, items[0].quality)

    def test_aged_brie_sellIn_goes_down_even_if_quality_is_50(self):
        items = self.run_gilded_rose_once([Item("Aged Brie", -1, 50)])
        self.assertEqual(-2, items[0].sell_in)

    def test_aged_brie_quality_goes_up_by_one_when_sellIn_is_zero(self):
        items = self.run_gilded_rose_once([Item("Aged Brie", 0, 20)])
        self.assertEqual(21, items[0].quality)
    
    def test_sulfuras_quality_is_always_80(self):
        items = self.run_gilded_rose_once([Item("Sulfuras, Hand of Ragnaros", 5, 80)])
        self.assertEqual(80, items[0].quality)

    def test_backstage_pass_quality_increases_by_1_more_than_10days_before(self):
        items = self.run_gilded_rose_once([Item("Backstage passes to a TAFKAL80ETC concert", 11, 25)])
        self.assertEqual(26, items[0].quality)

    def test_backstage_pass_quality_increases_by_2_10_days_before(self):
        items = self.run_gilded_rose_once([Item("Backstage passes to a TAFKAL80ETC concert", 10, 25)])
        self.assertEqual(27, items[0].quality)

    def test_backstage_pass_quality_increases_by_2_less_than_10days_but_above_5_before(self):
        items = self.run_gilded_rose_once([Item("Backstage passes to a TAFKAL80ETC concert", 7, 25)])
        self.assertEqual(27, items[0].quality)

    def test_backstage_pass_quality_increases_by_3_5days_before(self):
        items = self.run_gilded_rose_once([Item("Backstage passes to a TAFKAL80ETC concert", 5, 25)])
        self.assertEqual(28, items[0].quality)

    def test_backstage_pass_quality_increases_by_3_less_than_5days_before(self):
        items = self.run_gilded_rose_once([Item("Backstage passes to a TAFKAL80ETC concert", 2, 25)])
        self.assertEqual(28, items[0].quality)

    def test_backstage_pass_quality_drops_to_0_after_sellIn_expires(self):
        items = self.run_gilded_rose_once([Item("Backstage passes to a TAFKAL80ETC concert", 0, 25)])
        self.assertEqual(0, items[0].quality)

    def test_backstage_pass_quality_doesnt_go_above_50(self):
        items = self.run_gilded_rose_once([Item("Backstage passes to a TAFKAL80ETC concert", 3, 50)])
        self.assertEqual(50, items[0].quality)
    
    def test_sellIn_drops_by_one_for_normal_item(self):
        items = self.run_gilded_rose_once([Item("Normal Item,", 3, 20)])
        self.assertEqual(2, items[0].sell_in)

    def test_sellIn_drops_by_one_for_Aged_brie(self):
        items = self.run_gilded_rose_once([Item("Aged Brie", 3, 20)])
        self.assertEqual(2, items[0].sell_in)

    def test_sellIn_drops_by_one_for_tickets(self):
        items = self.run_gilded_rose_once([Item("Backstage passes to a TAFKAL80ETC concert", 3, 20)])
        self.assertEqual(2, items[0].sell_in)
    
    def test_sellIn_doesnt_drop_for_sulfuras(self):
        items = self.run_gilded_rose_once([Item("Sulfuras, Hand of Ragnaros", 3, 80)])
        self.assertEqual(3, items[0].sell_in)



    # """
    # Parameterised tests
    # """
    def test_item_name(self):
            param_list = [
            ([Item("Normal Item", 0, 0)], 'Normal Item'),
            ([Item("Aged Brie", 0, 0)], 'Aged Brie'),
            ([Item("Backstage passes to a TAFKAL80ETC concert", 0, 0)], 'Backstage passes to a TAFKAL80ETC concert'),
            ([Item("Sulfuras, Hand of Ragnaros", 0, 0)], 'Sulfuras, Hand of Ragnaros')
            ]
            for inputItems, expectedName in param_list:
                with self.subTest(msg=f"Item {inputItems[0].name} should equal {expectedName}", inputItems=inputItems, expectedName=expectedName):
                    items = self.run_gilded_rose_once(inputItems)
                    self.assertEqual(items[0].name, expectedName)

    def test_sell_in_drops_by_one_for_everything_except_Sulfuras(self):
            param_list = [
            ([Item("Normal Item", 20, 20)], 19),
            ([Item("Aged Brie", 20, 20)], 19),
            ([Item("Backstage passes to a TAFKAL80ETC concert", 20, 20)], 19),
            ([Item("Sulfuras, Hand of Ragnaros", 20, 80)], 20)
            ]
            for inputItems, expected_sell_in in param_list:
                with self.subTest(msg=f"Item {inputItems[0].sell_in} should equal {expected_sell_in}", inputItems=inputItems, expected_sell_in=expected_sell_in):
                    items = self.run_gilded_rose_once(inputItems)
                    self.assertEqual(items[0].sell_in, expected_sell_in)

    def test_item_quality(self):
            param_list = [
            ([Item("Normal Item", 20, 20)], 19),
            ([Item("Normal Item", -1, 20)], 18),
            ([Item("Normal Item", 20, 0)], 0),

            ([Item("Aged Brie", 20, 20)], 21),
            ([Item("Aged Brie", -1, 20)], 22),
            ([Item("Aged Brie", 20, 50)], 50),
            ([Item("Aged Brie", -1, 50)], 50),

            ([Item("Backstage passes to a TAFKAL80ETC concert", 20, 20)], 21),
            ([Item("Backstage passes to a TAFKAL80ETC concert", 10, 20)], 22),
            ([Item("Backstage passes to a TAFKAL80ETC concert", 7, 20)], 22),
            ([Item("Backstage passes to a TAFKAL80ETC concert", 5, 20)], 23),
            ([Item("Backstage passes to a TAFKAL80ETC concert", 1, 20)], 23),
            ([Item("Backstage passes to a TAFKAL80ETC concert", 0, 20)], 0),
            ([Item("Backstage passes to a TAFKAL80ETC concert", -1, 20)], 0),
            ([Item("Backstage passes to a TAFKAL80ETC concert", -5, 0)], 0),
            ([Item("Backstage passes to a TAFKAL80ETC concert", 1, 50)], 50),
            ([Item("Backstage passes to a TAFKAL80ETC concert", 1, 49)], 50),

            ([Item("Sulfuras, Hand of Ragnaros", 20, 80)], 80),
            ([Item("Sulfuras, Hand of Ragnaros", 0, 80)], 80)
            ]

            for inputItems, expected_quality in param_list:
                with self.subTest(
                    msg=f"Item {inputItems[0].quality} should equal {expected_quality}",
                    inputItems=inputItems,
                    expected_quality=expected_quality
                    ):

                    items = self.run_gilded_rose_once(inputItems)
                    self.assertEqual(items[0].quality, expected_quality)

    def test_sell_in_with_multiple_days(self):
            param_list = [
            ([Item("Normal Item", 20, 20)], 2, 18),
            ([Item("Normal Item", 20, 20)], 5, 15),
            ([Item("Normal Item", 5, 20)], 10, -5),
            ([Item("Normal Item", 0, 20)], 7, -7),

            ([Item("Aged Brie", 20, 20)], 2, 18),
            ([Item("Aged Brie", 20, 20)], 5, 15),
            ([Item("Aged Brie", 5, 20)], 10, -5),
            ([Item("Aged Brie", 0, 20)], 7, -7),

            ([Item("Backstage passes to a TAFKAL80ETC concert", 20, 20)], 2, 18),
            ([Item("Backstage passes to a TAFKAL80ETC concert", 20, 20)], 5, 15),
            ([Item("Backstage passes to a TAFKAL80ETC concert", 5, 20)], 10, -5),
            ([Item("Backstage passes to a TAFKAL80ETC concert", 0, 20)], 7, -7),

            ([Item("Sulfuras, Hand of Ragnaros", 20, 80)], 2, 20),
            ([Item("Sulfuras, Hand of Ragnaros", 20, 80)], 5, 20),
            ([Item("Sulfuras, Hand of Ragnaros", 5, 80)], 10, 5),
            ([Item("Sulfuras, Hand of Ragnaros", 0, 80)], 7, 0)
            ]
            for inputItems, iterations, expected_sell_in in param_list:
                with self.subTest(
                    msg=f"Item {inputItems[0].sell_in} should equal {expected_sell_in}",
                    inputItems=inputItems,
                    iterations=iterations,
                    expected_sell_in=expected_sell_in

                    ):
                    items = self.run_gilded_rose_n_times(inputItems, iterations)
                    self.assertEqual(items[0].sell_in, expected_sell_in)

    def test_item_quality_over_multiple_days(self):
            param_list = [
            # 2 days
            ([Item("Normal Item", 20, 20)], 2, 18),
            ([Item("Normal Item", -1, 20)], 2, 16),
            ([Item("Normal Item", 20, 0)], 2, 0),

            ([Item("Aged Brie", 20, 20)], 2, 22),
            ([Item("Aged Brie", -1, 20)], 2, 24),
            ([Item("Aged Brie", 20, 50)], 2, 50),
            ([Item("Aged Brie", -1, 50)], 2, 50),

            ([Item("Backstage passes to a TAFKAL80ETC concert", 20, 20)], 2, 22),
            ([Item("Backstage passes to a TAFKAL80ETC concert", 10, 20)], 2, 24),
            ([Item("Backstage passes to a TAFKAL80ETC concert", 7, 20)], 2, 24),
            ([Item("Backstage passes to a TAFKAL80ETC concert", 5, 20)], 2, 26),
            ([Item("Backstage passes to a TAFKAL80ETC concert", 3, 20)], 2, 26),
            ([Item("Backstage passes to a TAFKAL80ETC concert", 1, 20)], 2, 0),
            ([Item("Backstage passes to a TAFKAL80ETC concert", 0, 20)], 2, 0),
            ([Item("Backstage passes to a TAFKAL80ETC concert", -5, 0)], 2, 0),

            ([Item("Sulfuras, Hand of Ragnaros", 20, 80)], 2, 80),
            ([Item("Sulfuras, Hand of Ragnaros", 0, 80)], 2, 80),
            
            # 5 days
            ([Item("Normal Item", 20, 20)], 5, 15),
            ([Item("Normal Item", -1, 20)], 5, 10),
            ([Item("Normal Item", 20, 0)], 5, 0),

            ([Item("Aged Brie", 20, 20)], 5, 25),
            ([Item("Aged Brie", -1, 20)], 5, 30),
            ([Item("Aged Brie", 20, 50)], 5, 50),
            ([Item("Aged Brie", -1, 50)], 5, 50),

            ([Item("Backstage passes to a TAFKAL80ETC concert", 20, 20)], 5, 25),
            ([Item("Backstage passes to a TAFKAL80ETC concert", 20, 50)], 5, 50),
            ([Item("Backstage passes to a TAFKAL80ETC concert", 10, 20)], 5, 30),
            ([Item("Backstage passes to a TAFKAL80ETC concert", 7, 20)], 5, 33),
            ([Item("Backstage passes to a TAFKAL80ETC concert", 6, 20)], 5, 34),
            ([Item("Backstage passes to a TAFKAL80ETC concert", 5, 20)], 5, 35),
            ([Item("Backstage passes to a TAFKAL80ETC concert", 4, 20)], 5, 0),
            ([Item("Backstage passes to a TAFKAL80ETC concert", 0, 20)], 5, 0),
            ([Item("Backstage passes to a TAFKAL80ETC concert", -5, 0)], 5, 0),

            ([Item("Sulfuras, Hand of Ragnaros", 20, 80)], 5, 80),
            ([Item("Sulfuras, Hand of Ragnaros", 0, 80)], 5, 80)
            ]

            for inputItems, iterations, expected_quality in param_list:
                with self.subTest(
                    msg=f"Item {inputItems[0].name} {inputItems[0].quality} should equal {expected_quality}",
                    inputItems=inputItems,
                    iterations=iterations,
                    expected_quality=expected_quality
                    ):

                    items = self.run_gilded_rose_n_times(inputItems, iterations)
                    self.assertEqual(items[0].quality, expected_quality)


    def test_item_name(self):
            param_list = [
            ([Item("Normal Item", 0, 0), Item("Normal Item2", 1, 1)], ["Normal Item", "Normal Item2"]),
            ([Item("Aged Brie", 0, 0), Item("Aged Brie2", 0, 0), Item("Aged Brie3", 0, 0)], ['Aged Brie', 'Aged Brie2', 'Aged Brie3']),
            ([Item("Sulfuras, Hand of Ragnaros", 0, 0), Item("Aged Brie", 0, 0)], ['Sulfuras, Hand of Ragnaros', "Aged Brie"])
            ]
            for inputItems, expectedItems in param_list:
                with self.subTest(msg=f"Item {inputItems} should equal {expectedItems}", inputItems=inputItems, expectedItems=expectedItems):
                    items = self.run_gilded_rose_once(inputItems)
                    for i in range(len(inputItems)):
                        self.assertEqual(items[i].name, expectedItems[i])
"""
TDD for update
- __"Conjured"__ items degrade in `Quality` twice as fast as normal items

"""
        

if __name__ == '__main__':
    unittest.main()
