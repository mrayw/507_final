import unittest
from model import *

class TestDatabase(unittest.TestCase):
    def test_calendar_table(self):
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()

        sql = 'SELECT Id FROM Calendar'
        results = cur.execute(sql)
        result_list = results.fetchall()
        self.assertEqual(len(result_list), 366)

        sql = 'Select Date FROM Calendar'
        results = cur.execute(sql)
        result_list = results.fetchall()
        self.assertIn(('12-31',),result_list)
        self.assertNotIn(('12-32',),result_list)

        conn.close()

    def test_holiday_table(self):
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()

        sql = 'SELECT Id FROM Holidays'
        results = cur.execute(sql)
        result_list = results.fetchall()
        self.assertEqual(len(result_list), 453)

        sql = 'Select * From Holidays GROUP BY DateString'
        results = cur.execute(sql)
        result_list = results.fetchall()
        self.assertEqual(len(result_list), 331)

        sql = 'SELECT Food FROM Holidays'
        results = cur.execute(sql)
        result_list = results.fetchall()
        self.assertNotIn(("National Bloody Mary Day",), result_list)
        self.assertIn(("Bloody Mary",), result_list)

        conn.close()

    def test_review_table(self):
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()

        sql = 'SELECT Rating FROM Reviews'
        results = cur.execute(sql)
        result_list = results.fetchall()
        self.assertIn((1,), result_list)
        self.assertIn((5,), result_list)
        self.assertNotIn((2,), result_list)

        conn.close()

    def test_review_holiday_table_link(self):
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()

        sql = 'SELECT h.Holiday FROM Holidays as h JOIN Reviews as r ON h.ID = r.Holiday'
        results = cur.execute(sql)
        result_list = results.fetchall()
        self.assertGreater(len(result_list), 0)

        conn.close()

    def test_select_holiday(self):
        result_list = select_holiday(1)
        self.assertGreater(len(result_list), 0)

unittest.main()
