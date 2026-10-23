# Kalkulator Wyceny Fundamentalnej (Owner Earnings Model)

## O projekcie
Narzędzie analityczne stworzone w Pythonie do automatycznego pobierania danych finansowych spółek technologicznych (m.in. NVIDIA, ASML, TSMC, Broadcom) i wyliczania ich rzeczywistej zdolności do generowania gotówki przy pomocy wskaźnika **Owner Earnings** (Zysk netto + Amortyzacja - CAPEX). 

Projekt integruje pobieranie danych giełdowych, transformację za pomocą biblioteki Pandas, eksport do relacyjnej bazy danych PostgreSQL oraz końcową wizualizację analityczną w Tableau.

## Wykorzystane technologie
* **Python**: `yfinance` (pobieranie sprawozdań), `pandas` (transformacja danych).
* **Bazy danych**: `PostgreSQL`, `SQLAlchemy` (automatyczny eksport przetworzonych wyników).
* **Data Visualization**: Tableau (analiza wskaźnikowa i porównanie rentowności).

## Dashboard Analityczny
![Dashboard Wyceny](ashboard_poe.png)

**Wnioski analityczne:**
Powyższy dashboard obrazuje relację między wyceną mnożnikową a rentownością operacyjną analizowanych spółek. Z zebranych danych wynika, że choć TSM charakteryzuje się najwyższą marżą EBITDA (~72%), jest jednocześnie najdrożej wyceniane przez rynek w stosunku do generowanej gotówki (najwyższy wskaźnik P/OE). Z kolei NVIDIA (NVDA) oferuje atrakcyjniejszy wskaźnik P/OE przy zachowaniu bardzo wysokiej marży (niemal 67%).
