import backtrader as bt
import math

class ValueInvesting(bt.Strategy):
    params = dict(
        monthly_increase = 1000
    )

    def __init__(self):
        self.order = None
        self.total_cost = 0
        self.buys = 0
        self.sells = 0
        self.total_shares = 0
        self.com_cost = 0
        self.invested_amount = 0
        self.asset_amount_increase = 1000
        self.months_passed_since_start = 1

    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def start(self):
        self.broker.set_fundmode(fundmode=True, fundstartval=1000.0)
        self.cash_start = self.broker.get_cash()
        self.order_target_value(target=self.cash_start)
        print(f"Starting with {self.broker.get_value()}")

        # ADD A TIMER
        self.add_timer(
            when=bt.timer.SESSION_START,
            monthdays=[0],
            monthcarry=True
            # timername='buytimer',
        )

    def notify_timer(self, timer, when, *args):
        investment_period_value = self.params.monthly_increase * self.months_passed_since_start
        actual_value = self.broker.get_value()
        print(f"Equity Currently = {actual_value}, should have {investment_period_value}")
        difference_in_cost = actual_value - investment_period_value
        if difference_in_cost < 0:
            # Equity has decreased therefore need to add funds and buy
            print("Buying...")
            current_cash = self.broker.get_cash()
            topup_amount = abs(difference_in_cost - current_cash)
            print(f"Current Cash {current_cash}, Need to TopUp By {topup_amount}")
            self.broker.add_cash(topup_amount)
            self.order_target_value(target=difference_in_cost)
            
        elif difference_in_cost > 0:
            # Equity has increased and need to sell
            print("Selling...")
            self.order_target_value(target=difference_in_cost)
            
        
        else:
            pass
            
        self.months_passed_since_start += 1
    
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
        print('Value Investing')
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