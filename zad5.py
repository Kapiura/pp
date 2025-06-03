import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize

# ----------------------------
# Wczytanie i przygotowanie danych
# ----------------------------

# Wczytanie danych z plików CSV
df_dino = pd.read_csv("dino_w.csv", parse_dates=['Data'])
df_pko = pd.read_csv("pko_w.csv", parse_dates=['Data'])

# Sortowanie i czyszczenie danych dla obu spółek
for df, company_name in zip([df_dino, df_pko], ["Dino", "PKO BP"]):
    df.sort_values("Data", inplace=True)  # Sortowanie po dacie
    df.rename(columns={"Zamkniecie": "Close"}, inplace=True)  # Ujednolicenie nazwy kolumny
    df["Return"] = df["Close"].pct_change()  # Obliczenie stóp zwrotu
    df.dropna(inplace=True)  # Usunięcie brakujących wartości
    print(f"Liczba dostępnych tygodni dla {company_name}: {len(df)}")

# Filtrowanie danych od 2024 roku
df_dino = df_dino[df_dino["Data"].dt.year >= 2024].copy()
df_pko = df_pko[df_pko["Data"].dt.year >= 2024].copy()

# ----------------------------
# Analiza podstawowych statystyk
# ----------------------------

def analyze_stock(company_name, returns):
    """Funkcja obliczająca kluczowe statystyki dla akcji"""
    avg_return = returns.mean()
    risk = returns.std()
    sharpe_ratio = avg_return / risk if risk else np.nan

    print(f"\nAnaliza {company_name}:")
    print(f"- Średni tygodniowy zwrot: {avg_return:.2%}")
    print(f"- Ryzyko (odchylenie std.): {risk:.2%}")
    print(f"- Współczynnik Sharpe'a: {sharpe_ratio:.4f}")

    return avg_return, risk, sharpe_ratio

# Analiza obu spółek
stats_dino = analyze_stock("Dino", df_dino["Return"])
stats_pko = analyze_stock("PKO Bank Polski", df_pko["Return"])

# ----------------------------
# Wizualizacja wyników
# ----------------------------

# Obliczenie skumulowanych zwrotów dla inwestycji 1000 zł
initial_investment = 1000
df_dino["Cumulative"] = initial_investment * (1 + df_dino["Return"]).cumprod()
df_pko["Cumulative"] = initial_investment * (1 + df_pko["Return"]).cumprod()

# Stylizacja wykresu
plt.style.use('seaborn')
plt.figure(figsize=(12, 7))

# Wykres dla Dino
plt.plot(df_dino["Data"], df_dino["Cumulative"],
         label="Dino", color='#2ca02c', linewidth=2.5, alpha=0.8)
plt.scatter(df_dino["Data"], df_dino["Cumulative"],
            color='#2ca02c', s=40, alpha=0.6)

# Wykres dla PKO BP
plt.plot(df_pko["Data"], df_pko["Cumulative"],
         label="PKO BP", color='#1f77b4', linewidth=2.5, alpha=0.8)
plt.scatter(df_pko["Data"], df_pko["Cumulative"],
            color='#1f77b4', s=40, alpha=0.6)

# Formatowanie wykresu
plt.title("Wartość inwestycji 1000 zł w akcje Dino i PKO BP (od 2024)", pad=20, fontsize=14)
plt.xlabel("Data", labelpad=10)
plt.ylabel("Wartość portfela [zł]", labelpad=10)
plt.legend(fontsize=12)
plt.grid(True, linestyle='--', alpha=0.4)
plt.tight_layout()

# ----------------------------
# Analiza portfela
# ----------------------------

# Połączenie stóp zwrotu dla obliczenia kowariancji
returns_combined = pd.merge(
    df_dino[["Data", "Return"]],
    df_pko[["Data", "Return"]],
    on="Data",
    suffixes=("_dino", "_pko")
).dropna()

cov_matrix = returns_combined[["Return_dino", "Return_pko"]].cov()

# Funkcja optymalizacyjna
def portfolio_variance(weights):
    """Oblicza wariancję portfela dla danych wag"""
    w_dino = weights[0]
    w_pko = 1 - w_dino
    variance = (w_dino**2 * cov_matrix.iloc[0, 0] +
                w_pko**2 * cov_matrix.iloc[1, 1] +
                2 * w_dino * w_pko * cov_matrix.iloc[0, 1])
    return variance

# Minimalizacja ryzyka portfela
optimization_result = minimize(
    portfolio_variance,
    x0=[0.5],
    bounds=[(0, 1)]  # Ograniczenie wag do przedziału [0, 1]
)

# Wyodrębnienie wyników optymalizacji
optimal_weight_dino = optimization_result.x[0]
optimal_weight_pko = 1 - optimal_weight_dino
portfolio_risk = np.sqrt(optimization_result.fun)

# Prezentacja wyników
print("\n" + "="*50)
print("Optymalna alokacja portfela (minimalizacja ryzyka):")
print(f"- Dino: {optimal_weight_dino:.2%}")
print(f"- PKO Bank Polski: {optimal_weight_pko:.2%}")
print(f"- Ryzyko portfela (odchylenie std.): {portfolio_risk:.2%}")
print("="*50)

plt.show()