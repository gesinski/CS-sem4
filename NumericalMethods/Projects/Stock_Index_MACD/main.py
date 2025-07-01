import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def ema(N, prizes):
    alfa = 2/(N+1)
    numerator = prizes[0]
    denumerator = 1

    for i in range(1, N+1):
        numerator += (1-alfa)*prizes[i]
        denumerator += (1-alfa)**i

    return numerator/denumerator

def macd_designation(prizes):
    macd = []
    for i in range(26, elements):
        macd.append(ema(12, prizes[i-12:i+1]) - ema(26, prizes[i-26:i+1]))
    return macd

def signal_designation(macd):
    signal = []
    for i in range(9, len(macd)):
        signal.append(ema(9, macd[i-9:i+1]))
    return signal

def get_buy_sell_signals(macd, signal):
    buy_signals = [None] * len(macd)  
    sell_signals = [None] * len(macd)

    for i in range(1, len(macd)):  
        if macd[i] > signal[i] and macd[i - 1] <= signal[i - 1]: 
            buy_signals[i] = macd[i]
        elif macd[i] < signal[i] and macd[i - 1] >= signal[i - 1]:
            sell_signals[i] = macd[i]

    return buy_signals, sell_signals

def create_table_from_csv(csv_file_name, start_row=None,limit=None):
    csv_table = pd.read_csv(csv_file_name, sep="\s+", header=None, 
                            usecols=[0, 2, 3, 4, 5, 6], 
                            names=["date", "open", "high", "low", "close", "volume"],
                            skiprows=start_row,
                            nrows=limit)
    csv_table["date"] = pd.to_datetime(csv_table["date"])
    return csv_table

def draw_graph_from_table(data):
    sns.set_style("whitegrid")

    plt.figure(figsize=(12, 6))
    sns.lineplot(x=data["date"], y=data["close"], color="blue", label="Close Price")

    plt.xlabel("Date", fontsize=12)
    plt.ylabel("Close Price (USD)", fontsize=12)
    plt.title("Bitcoin Close Price Over Time", fontsize=14)
    plt.xticks(rotation=45)
    plt.legend() 

    plt.show()

def draw_macd_signal_graph(data, macd, signal, buy_signals, sell_signals, x_first, max_signals=None):
    plt.figure(figsize=(10, 5))

    if x_first == True:
        plt.plot(data, label="BTC", color="orange", linewidth=2, zorder=1)
    plt.plot(macd, label="MACD", color="blue", linewidth=2, zorder=1)
    plt.plot(signal, label="Signal", color="red", linewidth=2, zorder=1)

    if max_signals is not None:
        buy_x = [i for i in range(len(buy_signals)) if buy_signals[i] is not None][:max_signals-1]
        buy_y = [buy_signals[i] for i in buy_x]

        sell_x = [i for i in range(len(sell_signals)) if sell_signals[i] is not None][:max_signals]
        sell_y = [sell_signals[i] for i in sell_x]
    else:
        buy_x = [i for i in range(len(buy_signals)) if buy_signals[i] is not None]
        buy_y = [buy_signals[i] for i in buy_x]

        sell_x = [i for i in range(len(sell_signals)) if sell_signals[i] is not None]
        sell_y = [sell_signals[i] for i in sell_x]

    if x_first is True:
        if buy_x and sell_x:
            if sell_x[0] < buy_x[0]:
                sell_x.pop(0)
                sell_y.pop(0)
    
    for i in range(max(len(buy_x), len(sell_x))):
        if sell_x[i] > buy_x[i]:
            plt.axvspan(buy_x[i], sell_x[i], color="skyblue", alpha=0.5)

    if x_first == True:
        for x in buy_x:
            plt.axvline(x, color="green", linestyle="--", linewidth=0.8, alpha=0.7, zorder=0)
        
        for x in sell_x:
            plt.axvline(x, color="red", linestyle="--", linewidth=0.8, alpha=0.7, zorder=0)

    plt.scatter(buy_x, buy_y, color="green", marker="^", s=50, label="Buy Signal", zorder=2)
    plt.scatter(sell_x, sell_y, color="yellow", marker="v", s=50, label="Sell Signal", zorder=2)

    plt.xlabel("Time [days]")
    plt.axhline(macd[0], color="black", linewidth=1, linestyle="--", zorder=0)
    plt.legend(loc="upper right")
    plt.grid(True)
    plt.show()

def simulate_trading(data, macd, buy_signals, sell_signals, starting_capital):
    current_stock_number = starting_capital/data[0]
    transactions_wallet = []

    for i in range(len(data)):
        if macd[i] in sell_signals:
            transactions_wallet.append(current_stock_number*data[i])
        elif macd[i] in buy_signals:
            current_stock_number = transactions_wallet[len(transactions_wallet)-1]/data[i]

    transactions_wallet.insert(0, 1000.0)
    return transactions_wallet

def draw_transaction_graph(wallet):
    transactions = list(range(0, len(wallet)))

    plt.figure(figsize=(8, 5))
    plt.plot(transactions, wallet, linestyle='-', color='b', label='Wallet')

    plt.xticks(transactions)

    plt.xlabel("Transaction Number")
    plt.ylabel("Capital")
    plt.title("Changes in funds in the investment wallet during the simulation")
    plt.legend()
    plt.grid(True)

    plt.show()

elements = 1035
data = create_table_from_csv("BTCUSDT1440.csv", 0, 1050)
draw_graph_from_table(data)

macd_data = macd_designation(data["close"].tolist())
signal_data = signal_designation(macd_data)
purchase_signals, sell_signals = get_buy_sell_signals(macd_data[9:], signal_data)

draw_macd_signal_graph(data["close"].tolist(), macd_data[9:], signal_data, purchase_signals, sell_signals, False)
draw_macd_signal_graph(data["close"].tolist()[34:195], macd_data[34:195], signal_data[25:186], purchase_signals[25:186], sell_signals[25:186], True, 3)
draw_macd_signal_graph(data["close"].tolist()[210:1010], macd_data[210:], signal_data[201:], purchase_signals[201:], sell_signals[201:], True, 3)

capital = 1000
transactions_profit = simulate_trading(data["close"].tolist()[35:1035], macd_data[9:], purchase_signals, sell_signals, capital)

draw_transaction_graph(transactions_profit)