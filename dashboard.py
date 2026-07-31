import streamlit as st
import streamlit as st
import yfinance as yf

st.set_page_config(
    page_title="PharmaPulse",
    page_icon="💊",
    layout="wide"
)

companies = {
    "AstraZeneca": "AZN",
    "Eli Lilly": "LLY",
    "Roche": "RHHBY",
    "Sanofi": "SNY",
    "GSK": "GSK"
}

def get_company_metrics(ticker):
    stock = yf.Ticker(ticker)
    history = stock.history(period="1y")

    start = history["Close"].iloc[0]
    end = history["Close"].iloc[-1]

    yearly_return = ((end - start) / start) * 100

    daily_returns = history["Close"].pct_change()
    volatility = daily_returns.std() * (252 ** 0.5) * 100

    risk_score = yearly_return / volatility

    return {
        "return": yearly_return,
        "volatility": volatility,
        "risk_score": risk_score,
        "history": history
    }

st.title("💊 PharmaPulse")
st.subheader("Pharmaceutical market intelligence dashboard")

company = st.selectbox(
    "Select a company",
    list(companies.keys())
)

metrics = get_company_metrics(companies[company])

st.write(f"Analyzing **{company}**")

col1, col2, col3 = st.columns(3)

col1.metric("1-Year Return", f"{metrics['return']:.2f}%")
col2.metric("Volatility", f"{metrics['volatility']:.2f}%")
col3.metric("Risk Score", f"{metrics['risk_score']:.2f}")

st.line_chart(metrics["history"]["Close"])