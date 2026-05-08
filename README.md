Digitális biztonságtudatosság értékelő program

Ez a program egy Google Forms kérdőívből exportált CSV fájl feldolgozására készült. A program a válaszok alapján pontszámot számol, biztonságtudatossági kategóriába sorolja a kitöltőket, majd statisztikai összesítéseket és diagramokat készít

A program futtatásához Python szükséges.

A szükséges könyvtárak telepítése:
bash
pip install pandas matplotlib


A projekt főbb fájljai:
biztonsagtudatossag_ertekelo.py – a feldolgozóprogram
Digitális biztonságtudatosság kérdőív.csv – a kérdőívből exportált fájl
eredmenyek mappa, a program által létrehozott kimeneti fájlok mappája
