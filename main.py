import yfinance as yf
import matplotlib.pyplot as plt

companies = {
    "AZN": "AstraZeneca",
    "LLY": "Eli Lilly",
    "RHHBY": "Roche",
    "SNY": "Sanofi",
    "GSK": "GSK"
}

returns = {}
volatility = {}
risk_score = {}



plt.figure(figsize=(14,8))

for ticker, company in companies.items():

    stock = yf.Ticker(ticker)
    history = stock.history(period="1y")

    # calculate yearly return
    start_price = history["Close"].iloc[0]
    end_price = history["Close"].iloc[-1]

    yearly_return = ((end_price - start_price) / start_price) * 100

    returns[company] = yearly_return
    daily_returns = history["Close"].pct_change()

    annual_volatility = daily_returns.std() * (252 ** 0.5) * 100

    volatility[company] = annual_volatility
    risk_score[company] = yearly_return / annual_volatility

    # create normalized graph
    normalized = history["Close"] / start_price * 100

    plt.plot(
        normalized.index,
        normalized,
        label=company
    )

# graph
plt.title("PharmaPulse: 1-Year Relative Performance")
plt.xlabel("Date")
plt.ylabel("Indexed Return (Start = 100)")
plt.legend(loc="upper left")
plt.grid(True)

plt.savefig("pharmapulse_comparison.png")
plt.show()

# ranking section
print("\n")
print("=" * 40)
print("      PHARMAPULSE RANKINGS")
print("=" * 40)

ranking = sorted(
    returns.items(),
    key=lambda x: x[1],
    reverse=True
)

for i, (company, ret) in enumerate(ranking, 1):
    print(f"{i}. {company:<15} {ret:.2f}%")

winner = ranking[0]

print("\n🏆 Winner:")
print(f"{winner[0]} ({winner[1]:.2f}%)")
print("\n")
print("=" * 40)
print("      VOLATILITY RANKINGS")
print("=" * 40)

vol_rank = sorted(
    volatility.items(),
    key=lambda x: x[1]
)

for i, (company, vol) in enumerate(vol_rank, 1):
    print(f"{i}. {company:<15} {vol:.2f}%")

print("\n")
print("=" * 40)
print("      RISK-ADJUSTED RANKINGS")
print("=" * 40)

risk_rank = sorted(
    risk_score.items(),
    key=lambda x: x[1],
    reverse=True
)

for i, (company, score) in enumerate(risk_rank, 1):
    print(f"{i}. {company:<15} {score:.2f}")

print("\n🏆 Best Risk-Adjusted Investment:")
print(f"{risk_rank[0][0]} ({risk_rank[0][1]:.2f})")