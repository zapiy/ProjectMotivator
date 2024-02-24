from .initial import InitialState
from .coin_bank import CoinBankState
from aiogram_qumit.extended_states.inline import InlineSelectorState

TELEGRAM_STATES = [
    InlineSelectorState,
    InitialState, CoinBankState,
]
