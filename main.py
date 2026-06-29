import yfinance as yf
import matplotlib.pyplot as plt

ticker = yf.Ticker("LLY")

history = ticker.history(period="1y")

print(history.head())

plt.plot(history.index, history["Close"])

plt.title("Eli Lilly Stock Price")
plt.xlabel("Date")
plt.ylabel("Price ($)")

plt.show()