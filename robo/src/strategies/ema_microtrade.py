import pandas as pd

def getShortTermEMAStrategy(
    stock_data: pd.DataFrame,
    ema_window: int = 5,
    profit_target_pct: float = 1,  # alvo de lucro em porcentagem
    verbose: bool = True
):
    """
    Estratégia baseada em EMA visando lucro curto de no máximo 1.2%.

    - Compra quando o preço atual é o menor dos últimos N candles (mínimo local).
    - Vende quando o preço atual atinge 1.2% de lucro em relação à mínima recente.
    
    Parâmetros:
        - stock_data: DataFrame com colunas ['close_price']
        - ema_window: período da média móvel exponencial
        - profit_target_pct: lucro alvo em %
        - verbose: se True, imprime os logs

    Retorno:
        - True para Compra
        - False para Venda
        - None para Nenhuma ação
    """
    
    stock_data = stock_data.copy()

    if 'close_price' not in stock_data.columns:
        if verbose:
            print("❌ Coluna 'close_price' não encontrada no DataFrame.")
        return None

    # Calcula a EMA
    stock_data["ema"] = stock_data["close_price"].ewm(span=ema_window, adjust=False).mean()

    # Garante que há dados suficientes
    if len(stock_data) < ema_window:
        if verbose:
            print("⚠️ Dados insuficientes após o cálculo da EMA. Pulando período...")
        return None

    # Últimos valores
    current_price = stock_data["close_price"].iloc[-1]
    last_ema = stock_data["ema"].iloc[-1]
    recent_min_price = stock_data["close_price"].iloc[-ema_window:].min()
    target_price = recent_min_price * (1 + profit_target_pct / 100)

    # Lógica de decisão
    buy_condition = current_price <= recent_min_price * 1.001  # 0.1% de tolerância
    sell_condition = current_price >= target_price

    # Decisão final
    decision = True if buy_condition else False if sell_condition else None

    if verbose:
        print("-------")
        print("📊 Estratégia: EMA com Lucro Curto")
        print(f" | EMA({ema_window}): {last_ema:.3f}")
        print(f" | Preço atual: {current_price:.3f}")
        print(f" | Mínimo recente: {recent_min_price:.3f}")
        print(f" | Alvo de venda (1%): {target_price:.3f}")
        print(f" | Decisão: {'Comprar' if decision is True else 'Vender' if decision is False else 'Nenhuma'}")
        print("-------")

    return decision
