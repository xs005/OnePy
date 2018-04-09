from itertools import count

from dataclasses import dataclass, field

from OnePy.constants import OrderType
from OnePy.environment import Environment


@dataclass
class Signal(object):
    env = Environment

    counter = count(1)

    order_type: OrderType
    size: int
    ticker: str
    datetime: str = None
    takeprofit: float = None
    takeprofit_pct: float = None
    stoploss: float = None
    stoploss_pct: float = None
    trailingstop: float = None
    trailingstop_pct: float = None
    price: float = None
    price_pct: float = None
    execute_price: float = None  # 用来确定是否是必成单
    first_cur_price: float = None

    mkt_id: float = None
    id: int = field(init=False)

    def __post_init__(self):
        self.datetime = self.env.feeds[self.ticker].date
        self.id = next(self.counter)
        self.check_all_conflict()
        self.save_signals()

    def save_signals(self):
        self.env.signals_normal_cur.append(self)
        self.env.signals_normal.append(self)

    def check_all_conflict(self):
        self._check_conflict(self.price, self.price_pct)
        self._check_conflict(self.takeprofit, self.takeprofit_pct)
        self._check_conflict(self.stoploss, self.stoploss_pct)
        self._check_conflict(self.trailingstop, self.trailingstop_pct)

    def get(self, name):
        return getattr(self, name)

    def set(self, name, value):
        setattr(self, name, value)

    @staticmethod
    def _check_conflict(obj, obj_pct):
        if obj and obj_pct:
            raise Exception("$ and pct can't be set together")

    def is_absolute_signal(self):
        return True if self.execute_price else False


@dataclass
class SignalByTrigger(Signal):
    counter = count(1)

    exec_type: str = None

    def save_signals(self):
        self.env.signals_trigger_cur.append(self)
        self.env.signals_trigger.append(self)
