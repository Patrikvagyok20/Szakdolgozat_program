Digitális biztonságtudatosság értékelő program

Ez a program egy Google Forms kérdőívből exportált CSV fájl feldolgozására készült. A program a válaszok alapján pontszámot számol, biztonságtudatossági kategóriába sorolja a kitöltőket, majd statisztikai összesítéseket és diagramokat készít.

A program futtatásához Python szükséges.

A szükséges könyvtárak telepítése:
bash
pip install pandas matplotlib


A projekt főbb fájljai:
biztonsagtudatossag_ertekelo.py – a feldolgozóprogram
Digitális biztonságtudatosság kérdőív.csv – a kérdőívből exportált fájl
eredmenyek mappa, a program által létrehozott kimeneti fájlok mappája

A program futtatása:

Parancssorból történik meg a program futattása.

Ha nem adunk meg fájlnevet parancssori argumentumként, akkor a program futás közben kéri be a CSV fájl nevét.

Kimenetek:

A program futása után a kimeneti fájlok az eredmenyek mappában lesznek megtalálhatóak.

A létrejövő főbb kimenetek:

pontozott_valaszok.csv – a válaszok pontszámokkal és kategóriákkal kiegészítve.
statisztika.txt – alapstatisztikai eredmények szöveges formában.

diagramok PNG formátumban, például:
biztonságtudatossági kategóriák
képernyőidő szerinti eredmények
nem, korcsoport, lakhely és végzettség szerinti átlagpontszámok

Megjegyzés:

A program a saját kérdőívemhez és annak oszlopszerkezetéhez készült. Más kérdőív vagy eltérő oszlopnevek esetén a program nem fog mükődni.
