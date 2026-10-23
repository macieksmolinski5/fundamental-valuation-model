import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
import yfinance as yf
import pandas as pd

tickers = ["NVDA", "ASML", "TSM", "AVGO"]
results = []

for ticker in tickers:
    print(f"Pobieranie danych dla: {ticker}...")
    stock = yf.Ticker(ticker)
    
    try:
        # Pobieranie sprawozdań
        income_statement = stock.financials
        cash_flow = stock.cashflow
        
        # Pobieranie waluty raportowania i aktualnej kapitalizacji rynkowej
        currency = stock.info.get('financialCurrency', 'USD')
        market_cap = stock.info.get('marketCap', 0)
        
        # Fundamentalne wskaźniki
        net_income = income_statement.loc['Net Income'].iloc[0]
        amortization = cash_flow.loc['Depreciation And Amortization'].iloc[0]
        capex = cash_flow.loc['Capital Expenditure'].iloc[0]
        
        ebitda = income_statement.loc['EBITDA'].iloc[0]
        total_revenue = income_statement.loc['Total Revenue'].iloc[0]
        
        # Obliczenia bazowe
        owner_earnings = net_income + amortization + capex
        ebitda_margin = (ebitda / total_revenue) * 100

        # Przeliczanie walut dla spółek zagranicznych (np. ASML, TSMC)
        exchange_rate = 1.0
        if currency != 'USD':
            fx_ticker = f"{currency}USD=X"
            fx_data = yf.Ticker(fx_ticker).history(period="1d")
            if not fx_data.empty:
                exchange_rate = fx_data['Close'].iloc[-1]
        
        # Standaryzacja zysków do USD
        net_income_usd = net_income * exchange_rate
        owner_earnings_usd = owner_earnings * exchange_rate
        
        # Obliczenie Wskaźnika P/OE (Cena do Gotówki dla Właścicieli)
        if owner_earnings_usd > 0:
            p_oe_ratio = market_cap / owner_earnings_usd
        else:
            p_oe_ratio = 0 # Ochrona przed dzieleniem przez zero, gdy spółka traci gotówkę
            
        results.append({
            "Spółka": ticker,
            "Owner Earnings (mld USD)": round(owner_earnings_usd / 1e9, 2),
            "Kapitalizacja (mld USD)": round(market_cap / 1e9, 2),
            "Wskaźnik P/OE": round(p_oe_ratio, 2),
            "Marża EBITDA (%)": round(ebitda_margin, 2)
        })
        
    except KeyError as e:
        print(f" -> Błąd dla {ticker}: Brak klucza {e} w sprawozdaniu")
    except Exception as e:
        print(f" -> Nieoczekiwany błąd dla {ticker}: {e}")

df_results = pd.DataFrame(results)

print("\n" + "="*85)
print(" WYNIKI WYCENY FUNDAMENTALNEJ (ZAAKTUALIZOWANE DO USD ORAZ WSKAŹNIK P/OE)")
print("="*85)
df_results = df_results.sort_values(by="Wskaźnik P/OE")
print(df_results.to_string(index=False))

df_results.to_csv("owner_earnings_results.csv", index=False)
print("\nZapisano dane do pliku owner_earnings_results.csv")

import urllib.parse

try:
    load_dotenv()
    db_password = os.getenv("DB_PASS")
    
    
    encoded_password = urllib.parse.quote_plus(db_password)
    

    engine = create_engine(f'postgresql+psycopg2://postgres:{encoded_password}@localhost:5432/wyceny_spolek')
    
    df_results.to_sql('owner_earnings', engine, if_exists='replace', index=False)
    print("Sukces! Dane zostały wyeksportowane do bazy PostgreSQL.")
    
except Exception as e:
    print(f"Wystąpił błąd podczas eksportu do bazy: {e}")