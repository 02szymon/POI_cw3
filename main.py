import os
import numpy as np
import pandas as pd
from skimage import io, color, exposure
from skimage.feature import graycomatrix, graycoprops

def przetworz_obrazy_i_oblicz_cechy(katalog_wejsciowy, wyjscie_csv):

    #Funkcja przetwarza obrazy z katalogu wejściowego, oblicza cechy tekstur
    #na podstawie macierzy zdarzeń GLCM i zapisuje wyniki do pliku CSV.


    wyniki = []

    # Definicja odległości i kątów do analizy
    odleglosci = [1, 3, 5]
    katy = [0, np.pi/4, np.pi/2, 3*np.pi/4]  # 0, 45, 90, 135 stopni


    for kategoria in os.listdir(katalog_wejsciowy):
        sciezka_kategorii = os.path.join(katalog_wejsciowy, kategoria)

        if os.path.isdir(sciezka_kategorii):
            for nazwa_obrazu in os.listdir(sciezka_kategorii):
                sciezka_obrazu = os.path.join(sciezka_kategorii, nazwa_obrazu)


                try:
                    obraz = io.imread(sciezka_obrazu)
                except IOError:
                    print(f"Nie można otworzyć pliku {sciezka_obrazu}. Przechodzę do następnego.")
                    continue

                # Konwersja do skali szarości
                if len(obraz.shape) == 3:
                    obraz_szary = color.rgb2gray(obraz)
                else:
                    obraz_szary = obraz

                # Redukcja głębi jasności do 5 bitów (64 poziomy)
                obraz_64_poziomy = (obraz_szary * 63).astype(np.uint8)


                glcm = graycomatrix(obraz_64_poziomy, distances=odleglosci, angles=katy, levels=64, symmetric=True, normed=True)

                # Obliczanie cech tekstury dla każdej kombinacji odległości i kąta
                for odleglosc in odleglosci:
                    for kat in katy:
                        glcm_single = graycomatrix(obraz_64_poziomy, distances=[odleglosc], angles=[kat], levels=64, symmetric=True, normed=True)
                        dissimilarity = graycoprops(glcm_single, 'dissimilarity')[0, 0]
                        correlation = graycoprops(glcm_single, 'correlation')[0, 0]
                        contrast = graycoprops(glcm_single, 'contrast')[0, 0]
                        energy = graycoprops(glcm_single, 'energy')[0, 0]
                        homogeneity = graycoprops(glcm_single, 'homogeneity')[0, 0]
                        ASM = graycoprops(glcm_single, 'ASM')[0, 0]


                        wektor_cech = {
                            'kategoria': kategoria,
                            'odleglosc': odleglosc,
                            'kat': kat,
                            'dissimilarity': dissimilarity,
                            'correlation': correlation,
                            'contrast': contrast,
                            'energy': energy,
                            'homogeneity': homogeneity,
                            'ASM': ASM
                        }
                        wyniki.append(wektor_cech)


    df = pd.DataFrame(wyniki)
    df.to_csv(wyjscie_csv, index=False)
    print(f"Wyniki zapisano do pliku: {wyjscie_csv}")

if __name__ == "__main__":
    katalog_wejsciowy = "fragmenty"
    wyjscie_csv = "cechy.csv" 

    przetworz_obrazy_i_oblicz_cechy(katalog_wejsciowy, wyjscie_csv)