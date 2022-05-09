import math
import backtrader as bt

class ComissionInfo(bt.CommissionInfo):
    params = (
        ("commission", 0.00075),
        ("mult", 1.0),
        ("margin", None),
        ("commtype", None),
        ("stocklike", False),
        ("percabs", False),
        ("interest", 0.0),
        ("interest_long", False),
        ("leverage", 1.0),
        ("automargin", False),
    )

    def getsize(self, price, cash):
        """Returns fractional size for cash operation @price"""
        return self.p.leverage * (cash / price)

class CashMarket(bt.analyzers.Analyzer):
    """
    Analyzer returning cash and market values
    """
    def create_analysis(self):
        self.rets = {}

    def notify_cashvalue(self, cash, value):
        total = cash + value
        self.rets[self.strategy.datetime.datetime()] = math.floor(total)

    def get_analysis(self):
        return self.rets

