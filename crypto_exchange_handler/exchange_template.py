import csv
from typing import Optional, Tuple, Dict


class ExchangeAPI:
    """
    A base class for every exchange specific class.
    Defines common methods and contains common parameters.

    Attributes
    ----------
    name : str
        lowercase name of exchange
    access_key : str
        public API key
    secret_key : str
        private API key
    api_passphrase : str optional
        oassphrase required by some exchanges

    Methods
    -------
    """

    def __init__(
        self, name, access_key: str, secret_key: str, api_passphrase: Optional[str] = None
    ):
        """
        Constructs all the necessary attributes for the ExchangeAPI object.

        Parameters
        ----------
        name : str
            lowercase name of exchange
        access_key : str
            public API key
        secret_key : str
            private API key
        api_passphrase : str optional
            oassphrase required by some exchanges
        """
        self.name = name.lower()
        self.access_key = access_key
        self.secret_key = secret_key
        self.api_passphrase = api_passphrase

    def get_all_balances(self) -> Optional[Dict[str, str]]:
        """
        Gets all balances available on account.

        :return:
        Dictionary with coin - balance pair
        """
        raise NotImplementedError

    def get_balance(self, coin: str) -> Optional[str]:
        """
        Gets balance of coin specified in parameter.

        :param coin: str with coin name
        :return: str representing coin balance. If there is no such coin returns None
        """
        raise NotImplementedError

    def get_available_markets(self) -> Optional[Tuple[str, ...]]:
        raise NotImplementedError

    def get_coin_price(self, name, pair="BTC"):
        raise NotImplementedError

    def get_coins_prices(self) -> Optional[dict]:
        raise NotImplementedError

    def get_order_book(self, market, side):
        raise NotImplementedError

    ###########################################################
    # Actions
    ###########################################################

    def withdraw_asset(self, asset: str, target_addr: str, amount: str):
        """
        Sends request for asset withdrawal to the exchange.

        :param asset:
        :param target_addr:
        :param amount:
        :return: None
        """
        raise NotImplementedError

    def create_order(self, market, side, price, amount):
        raise NotImplementedError

    def get_candles(self, symbol: str, interval: str, start: str, end: str = None) -> tuple:
        raise NotImplementedError

    def get_last_candles(self, symbol: str, interval: str, amount):
        raise NotImplementedError

    ###########################################################
    # Data processing - Do not override!
    ###########################################################

    def dump_market_data_to_file(
        self,
        symbol: str,
        interval: str = "30m",
        file: str = "data.csv",
        amount=None,
        start: str = None,
        end: str = None,
    ):
        """
        Creates .csv file with market data gathered from exchange API.

        :param symbol:
        :param interval:
        :param file:
        :param amount:
        :param start:
        :param end:
        :return:
        """

        if amount is not None:
            candles = self.get_last_candles(symbol, interval, amount)
        else:
            if start is not None:
                candles = self.get_candles(symbol, interval, start, end)
            else:
                print("ERROR: Wrong paramaters. Provide amount or start")
                return

        with open(file, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile, delimiter=",", quotechar="|", quoting=csv.QUOTE_MINIMAL)
            templist = list(candles[0].keys())
            writer.writerow(templist)

            for line in candles:
                templist.clear()
                for val in line.values():
                    templist.append(val)
                writer.writerow(templist)

    @staticmethod
    def load_market_data_file(file):
        if file.find(".csv") == -1:
            print("ERROR: Please provide .csv file")
            return -1

        candles = []

        with open(file, encoding="utf-8") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=",")
            line_count = 0

            for row in csv_reader:
                if line_count != 0:
                    temp = {
                        "ts": float(row[0]),
                        "open": float(row[1]),
                        "high": float(row[2]),
                        "low": float(row[3]),
                        "close": float(row[4]),
                    }
                    candles.append(temp)
                    line_count += 1
                else:
                    line_count += 1
        return tuple(candles)
