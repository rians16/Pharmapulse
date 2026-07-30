import yfinance as yf
import matplotlib.pyplot as plt
import time

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
market_caps = {}
dividend_yields = {}

def get_market_cap(stock):
    # fast_info is quicker and less prone to silently returning None
    try:
        cap = stock.fast_info.get("marketCap")
        if cap:
            return cap
    except Exception:
        pass

    # fallback: derive it manually from shares outstanding * last price
    try:
        info = stock.info
        cap = info.get("marketCap")
        if cap:
            return cap
        shares = info.get("sharesOutstanding")
        last_price = stock.fast_info.get("lastPrice")
        if shares and last_price:
            return shares * last_price
    except Exception:
        pass

    return 0

def get_info_field(stock, field, default=0):
    """Fetch a single field from .info with basic retry on transient failures."""
    for attempt in range(3):
        try:
            info = stock.info
            value = info.get(field)
            if value is not None:
                return value
            return default
        except Exception:
            time.sleep(1.5 * (attempt + 1))
    return default

plt.figure(figsize=(14, 8))

for ticker, company in companies.items():

    stock = yf.Ticker(ticker)
    history = stock.history(period="1y")

    market_caps[company] = get_market_cap(stock)
    dividend_yields[company] = get_info_field(stock, "dividendYield", 0)
    print(company, market_caps[company])

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

    time.sleep(1)  # small delay avoids throttling

# graph
plt.title("PharmaPulse: 1-Year Relative Performance")
plt.xlabel("Date")
plt.ylabel("Indexed Return (Start = 100)")
plt.legend(loc="upper left")
plt.grid(True)

plt.savefig("pharmapulse_comparison.png")
plt.show()


def format_market_cap(value):
    if value >= 1_000_000_000_000:
        return f"${value / 1_000_000_000_000:.2f}T"
    elif value >= 1_000_000_000:
        return f"${value / 1_000_000_000:.0f}B"
    else:
        return f"${value:,.0f}"
    


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

print("\n")
print("=" * 40)
print("      MARKET CAP RANKINGS")
print("=" * 40)

market_rank = sorted(
    market_caps.items(),
    key=lambda x: x[1],
    reverse=True
)

for i, (company, cap) in enumerate(market_rank, 1):
    print(f"{i}. {company:<15} {format_market_cap(cap)}")
    print("\n")
print("=" * 40)
print("      DIVIDEND YIELD RANKINGS")
print("=" * 40)

div_rank = sorted(
    dividend_yields.items(),
    key=lambda x: x[1],
    reverse=True
)

for i, (company, yld) in enumerate(div_rank, 1):
    print(f"{i}. {company:<15} {yld:.2f}%")
print("\n")
print("=" * 40)
    