#include <iostream>
#include <cmath>
#include <iomanip>
#include <vector>
#include <string>

struct Rata 
{
    int miesiac;
    double rata_calkowita;
    double odsetki;
    double kapital;
    double pozostale_saldo;
};

int main() 
{
    // Parametry kredytu
    const double kwota_kredytu = 1000000;
    const int okres_lat = 20;
    const int liczba_rat = okres_lat * 12;
    const double oprocentowanie_rocze = 0.04;
    const double oprocentowanie_miesieczne = oprocentowanie_rocze / 12;

    // Obliczenie miesięcznej raty annuitetowej
    double rata_miesieczna = (kwota_kredytu * oprocentowanie_miesieczne * std::pow(1 + oprocentowanie_miesieczne, liczba_rat)) /
                             (std::pow(1 + oprocentowanie_miesieczne, liczba_rat) - 1);

    // Wydruk nagłówka
    std::cout << std::fixed << std::setprecision(2);
    std::cout << "Miesiac\tRata\t\tOdsetki\t\tKapital\t\tPozostale saldo\n";

    std::vector<Rata> harmonogram;
    double saldo = kwota_kredytu;

    for (int miesiac = 1; miesiac <= liczba_rat; ++miesiac) 
    {
        double czesc_odsetkowa = saldo * oprocentowanie_miesieczne;
        double czesc_kapitalowa = rata_miesieczna - czesc_odsetkowa;
        saldo -= czesc_kapitalowa;

        if (saldo < 0.01) saldo = 0; // Korekta na ostatnią ratę, żeby nie zostało np. 0.001 zł

        harmonogram.push_back({
            miesiac,
            rata_miesieczna,
            czesc_odsetkowa,
            czesc_kapitalowa,
            saldo
        });
    }

    // Wydruk tabeli
    for (const auto& rata : harmonogram) 
    {
        std::cout << rata.miesiac << "\t"
                  << rata.rata_calkowita << "\t"
                  << rata.odsetki << "\t"
                  << rata.kapital << "\t"
                  << rata.pozostale_saldo << "\n";
    }

    return 0;
}
