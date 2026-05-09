import yfinance as yf
from app.llm.provider import generate_reply
from ..services.prompt import MARKET_RESEARCH_PROMPT
from datetime import datetime


def get_market_summary():
    indexes = {
        "Nifty 50": "^NSEI",
        "Sensex": "^BSESN",
    }

    index_summaries = []

    for name, ticker in indexes.items():
        history = yf.Ticker(ticker).history(period="2d")
        if len(history) < 2:
            continue

        prev_close = history["Close"].iloc[-2]
        current_close = history["Close"].iloc[-1]

        change = current_close - prev_close
        change_percent = (change / prev_close) * 100
        index_summaries.append(
            f"{name}: {current_close:.2f} ({change:+.2f}, {change_percent:+.2f}%)"
        )

    market_data = "\n".join(index_summaries)
    prompt = f"""{MARKET_RESEARCH_PROMPT} index_data: {market_data}"""

    user_message = f"""Today date: {datetime.now().strftime('%Y-%m-%d')} 
    Today market report: {market_data}"""

    summary = generate_reply(user_message, prompt, history=[])
    return summary
