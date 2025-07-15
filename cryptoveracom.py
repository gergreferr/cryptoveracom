import requests
import time
import numpy as np

SYMBOLS = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "ADAUSDT", "XRPUSDT"]
INTERVAL = 60  # секунд между запросами
WINDOW = 10    # количество точек данных для корреляции

class CryptoVeraCom:
    def __init__(self):
        self.prices = {symbol: [] for symbol in SYMBOLS}

    def fetch_price(self, symbol):
        url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
        try:
            r = requests.get(url, timeout=5)
            r.raise_for_status()
            data = r.json()
            return float(data["price"])
        except Exception as e:
            print(f"Ошибка при запросе цены {symbol}: {e}")
            return None

    def update_prices(self):
        for symbol in SYMBOLS:
            price = self.fetch_price(symbol)
            if price is not None:
                self.prices[symbol].append(price)
                if len(self.prices[symbol]) > WINDOW:
                    self.prices[symbol].pop(0)

    def calculate_correlations(self):
        valid_symbols = [s for s in SYMBOLS if len(self.prices[s]) == WINDOW]
        if len(valid_symbols) < 2:
            return None

        data = np.array([self.prices[s] for s in valid_symbols])
        corr_matrix = np.corrcoef(data)
        return valid_symbols, corr_matrix

    def run(self):
        print("Запуск CryptoVeraCom — мониторинг корреляций цен криптовалют...")
        while True:
            self.update_prices()
            corrs = self.calculate_correlations()
            if corrs:
                symbols, matrix = corrs
                print("Текущие корреляции между криптовалютами:")
                for i, sym1 in enumerate(symbols):
                    for j, sym2 in enumerate(symbols):
                        if j <= i:
                            continue
                        print(f"  {sym1} и {sym2}: {matrix[i][j]:.3f}")
                print("-" * 40)
            time.sleep(INTERVAL)

if __name__ == "__main__":
    cv = CryptoVeraCom()
    cv.run()
