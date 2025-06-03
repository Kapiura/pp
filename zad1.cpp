#include <iostream>
#include <cmath>
#include <iomanip>
#include <limits>

// Oblicza realną stopę zwrotu przy uwzględnieniu inflacji
double realna_stopa(double nominalna, double inflacja) 
{
    return (1 + nominalna) / (1 + inflacja) - 1;
}

// Oblicza wartość bieżącą renty (ang. Present Value of Annuity)
double oblicz_pva(double wyplata, double stopa, double okres) 
{
    if (std::abs(stopa) < std::numeric_limits<double>::epsilon()) 
    {
        return wyplata * okres;
    }
    return wyplata * (1 - 1 / std::pow(1 + stopa, okres)) / stopa;
}

// Oblicza ratę potrzebną do zgromadzenia określonej kwoty w przyszłości
double oblicz_rate(double przyszla_wartosc, double stopa, double okres) 
{
    if (std::abs(stopa) < std::numeric_limits<double>::epsilon()) 
    {
        return przyszla_wartosc / okres;
    }
    return (przyszla_wartosc * stopa) / (std::pow(1 + stopa, okres) - 1);
}

int main() {
    const auto domyslna_precyzja = std::cout.precision();
    std::cout << std::fixed;

    // Parametry wspólne dla wszystkich scenariuszy
    const double wyplata = 2500.00;       // miesięczna wypłata na emeryturze
    const double okres_wyplat = 240.0;    // liczba miesięcy wypłat (25 lat)
    const double okres_wplat = 480.0;     // liczba miesięcy oszczędzania (40 lat)

    // Scenariusze: [nazwa, nominalna stopa zwrotu, stopa inflacji]
    struct Scenariusz 
    {
        const char* nazwa;
        double nominalna;
        double inflacja;
    };

    Scenariusz scenariusze[] = 
    {
        {"Pesymistyczny", 0.03 / 12, 0.045 / 12}, // 3% zysk, 4.5% inflacja
        {"Umiarkowany",   0.04 / 12, 0.043 / 12}, // 4% zysk, 4.3% inflacja
        {"Optymistyczny", 0.06 / 12, 0.025 / 12}  // 6% zysk, 2.5% inflacja
    };

    for (const auto& s : scenariusze) 
    {
        double stopa_realna = realna_stopa(s.nominalna, s.inflacja);
        double pv = oblicz_pva(wyplata, stopa_realna, okres_wyplat);
        double rata = oblicz_rate(pv, stopa_realna, okres_wplat);

        std::cout << "====== Scenariusz: " << s.nazwa << " ======\n";
        std::cout << "Nominalna stopa zwrotu: " << std::setprecision(3) 
                  << s.nominalna * 12 * 100 << "%\n";
        std::cout << "Stopa inflacji: " << s.inflacja * 12 * 100 << "%\n";
        std::cout << "Realna stopa: " << stopa_realna * 12 * 100 << "%\n";
        std::cout << std::setprecision(2);
        std::cout << "Wartość do zgromadzenia: " << pv << " zł\n";
        std::cout << "Miesięczna rata oszczędności: " << rata << " zł\n\n";
        std::cout << std::setprecision(domyslna_precyzja);
    }

    return 0;
}
