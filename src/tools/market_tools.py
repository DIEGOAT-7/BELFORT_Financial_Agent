import yfinance as yf

def get_market_data(ticker: str):
    """
    Obtiene datos de mercado en tiempo real para un activo financiero.
    Input: ticker (str) - El símbolo del activo (ej: AAPL, BTC-USD, COP=X).
    Output: String con precio, cambio y noticias.
    """
    try:
        # Limpiamos espacios por si el LLM alucina
        ticker = ticker.strip().upper()
        stock = yf.Ticker(ticker)
        
        # Datos rápidos
        info = stock.fast_info
        price = info.last_price
        prev_close = info.previous_close
        
        if price is None:
            return f"No se encontraron datos para el ticker {ticker}. Verifica el símbolo."

        change_pct = ((price - prev_close) / prev_close) * 100
        
        # Noticias (últimos 3 titulares)
        news = stock.news[:3] if stock.news else []
        news_summary = [f"- {n.get('title', 'Sin título')}" for n in news]
        
        return str({
            "ticker": ticker,
            "current_price": round(price, 2),
            "change_pct_24h": f"{round(change_pct, 2)}%",
            "latest_news": news_summary
        })
    except Exception as e:
        return f"Error obteniendo datos de mercado para {ticker}: {str(e)}"