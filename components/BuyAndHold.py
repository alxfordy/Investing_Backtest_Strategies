import backtrader as bt
import math


class BuyAndHold(bt.Strategy):
    def __init__(self):
        self.order = None
        self.total_cost = 0
        self.buys = 0
        self.sells = 0
        self.total_shares = 0
        self.com_cost = 0
        self.invested_amount = 0
        
    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))
        
    def start(self):
        self.cash_start = self.broker.get_cash()

    def nextstart(self):
        size = math.floor( (self.broker.get_cash() - 10) / self.data[0] )
        self.buy(size=size)
    
    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return
        
        if order.status in [order.Completed]:
            if order.isbuy():
                self.buys += 1
                self.total_shares += order.executed.size
                self.invested_amount += order.executed.value
                self.total_cost += order.executed.value + order.executed.comm
                self.com_cost += order.executed.comm
                
            elif order.issell():
                self.sells += 1
                self.total_shares -= order.executed.size
                self.com_cost += order.executed.comm
                self.total_cost += order.executed.comm


        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            pass
#             self.log('Order Canceled/Margin/Rejected')
#             print(order.status, [order.Canceled, order.Margin, order.Rejected])

        self.order = None

    def stop(self):
        # calculate actual returns
        self.roi = (self.broker.get_value() / self.cash_start) - 1
        self.froi = (self.broker.get_fundvalue() - self.cash_start)
        value = self.datas[0].close * self.total_shares + self.broker.get_cash()
        print('-'*50)
        print('Buy and HODL')
#         print('Time in Market: {:.1f} years'.format((endDate - actualStart).days/365))
        print(f'Buy Orders:\t\t{self.buys:.0f}')
        print(f'Sell Orders:\t\t{self.sells:.0f}')
        print(f'Total Shares:\t\t{self.total_shares:.2f}')
        print(f'Total Value:\t\t${value:,.2f}')
        print(f'Total Shares Value:\t\t${self.broker.get_value():,.2f}')
        print(f'Total Cash Value:\t\t${self.broker.get_cash():,.2f}')
        print(f'Cost:\t\t${self.total_cost:,.2f}')
        print(f'Gross Return:\t\t${(value - self.total_cost):,.2f}')
        print(f'Gross %:\t\t{((value/self.total_cost - 1) * 100):.2f}%')
        print(f'ROI:\t\t{(100.0 * self.roi):.2f}%')
        print(f'Fund Value:\t\t{self.froi:.2f}%')
        print(f'Commission Cost:\t\t${self.com_cost:.2f}')
        print('-'*50)