from PIL import Image
import os

def wycinanie_fragmentow(katalog_wejsciowy, katalog_wyjsciowy, rozmiar_fragmentu=(128, 128)):
    """
    Funkcja wczytuje obrazy z katalogu wejściowego, wycina fragmenty o zadanym rozmiarze
    i zapisuje je do odpowiednich katalogów reprezentujących kategorie tekstur.

    :param katalog_wejsciowy: Ścieżka do katalogu wejściowego zawierającego obrazy
    :param katalog_wyjsciowy: Ścieżka do katalogu wyjściowego, gdzie będą zapisywane fragmenty
    :param rozmiar_fragmentu: Krotka określająca rozmiar fragmentu (szerokość, wysokość)
    """
    # Lista dostępnych kategorii tekstur
    kategorie = ['drzwi', 'mata', 'tynk']

    # Utworzenie katalogu wyjściowego, jeśli nie istnieje
    if not os.path.exists(katalog_wyjsciowy):
        os.makedirs(katalog_wyjsciowy)

    # Iterowanie przez katalogi reprezentujące kategorie tekstur
    for kategoria in kategorie:
        sciezka_kategorii = os.path.join(katalog_wejsciowy, kategoria)

        # Sprawdzenie, czy ścieżka jest katalogiem
        if os.path.isdir(sciezka_kategorii):
            # Utworzenie katalogu docelowego dla tej kategorii
            katalog_docelowy = os.path.join(katalog_wyjsciowy, kategoria)
            if not os.path.exists(katalog_docelowy):
                os.makedirs(katalog_docelowy)

            # Iterowanie przez obrazy w danej kategorii
            for nazwa_obrazu in os.listdir(sciezka_kategorii):
                sciezka_obrazu = os.path.join(sciezka_kategorii, nazwa_obrazu)

                # Wczytanie obrazu
                try:
                    obraz = Image.open(sciezka_obrazu)
                except IOError:
                    print(f"Nie można otworzyć pliku {sciezka_obrazu}. Przechodzę do następnego.")
                    continue

                szerokosc, wysokosc = obraz.size
                szerokosc_fragmentu, wysokosc_fragmentu = rozmiar_fragmentu

                # Wycinanie fragmentów z obrazu
                for x in range(0, szerokosc, szerokosc_fragmentu):
                    for y in range(0, wysokosc, wysokosc_fragmentu):
                        # Sprawdzenie, czy fragment mieści się w obrazie
                        if x + szerokosc_fragmentu <= szerokosc and y + wysokosc_fragmentu <= wysokosc:
                            fragment = obraz.crop((x, y, x + szerokosc_fragmentu, y + wysokosc_fragmentu))

                            # Zapisanie fragmentu do odpowiedniego katalogu
                            nazwa_fragmentu = f"{os.path.splitext(nazwa_obrazu)[0]}_{x}_{y}.png"
                            sciezka_zapisu = os.path.join(katalog_docelowy, nazwa_fragmentu)
                            fragment.save(sciezka_zapisu)
                            print(f"Zapisano fragment: {sciezka_zapisu}")

if __name__ == "__main__":
    katalog_wejsciowy = "obrazy"  # Ścieżka do katalogu wejściowego z obrazami
    katalog_wyjsciowy = "fragmenty"  # Ścieżka do katalogu wyjściowego
    rozmiar_fragmentu = (256, 256)  # Rozmiar fragmentów

    wycinanie_fragmentow(katalog_wejsciowy, katalog_wyjsciowy, rozmiar_fragmentu)