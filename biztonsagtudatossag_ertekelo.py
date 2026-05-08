import os
import sys
import pandas as pd
import matplotlib.pyplot as plt

KERDESEK = [
    "2. Milyen gyakran használ különböző jelszavakat a különböző online fiókjaihoz?",
    "3. Milyen gyakran használ legalább 12 karakter hosszú jelszavakat?",
    "4. Milyen gyakran használ speciális karaktereket a jelszavaiban?",
    "5. Milyen gyakran használ kétlépcsős azonosítást (2FA) online fiókjai védelmére?",
    "6. Milyen gyakran használ jelszókezelő alkalmazást jelszavai biztonságos tárolására?",
    "7. Milyen gyakran ellenőrzi az e-mailek feladóját megnyitás előtt?",
    "8. Milyen gyakran kerüli el az ismeretlen linkekre való kattintást e-mailekben?",
    "9. Milyen gyakran ismeri fel az adathalász e-maileket?",
    "10. Milyen gyakran ellenőrzi egy gyanús üzenet hitelességét?",
    "11. Milyen gyakran ad meg személyes adatokat online ellenőrzés nélkül?",
    "12. Milyen gyakran frissíti az operációs rendszert és az alkalmazásokat?",
    "13. Milyen gyakran használ vírusirtó vagy egyéb biztonsági szoftvert az eszközei védelmére?",
    "14. Milyen gyakran használ képernyőzárat (pl. PIN-kód, jelszó vagy biometria) az eszközein?",
    "15. Milyen gyakran használ nyilvános Wi-Fi-t érzékeny adatok elérésére?",
    "16. Milyen gyakran készít biztonsági mentést fontos adatairól?",
]




FORDITOTT = {
    "11. Milyen gyakran ad meg személyes adatokat online ellenőrzés nélkül?",
    "15. Milyen gyakran használ nyilvános Wi-Fi-t érzékeny adatok elérésére?",
}

KEPERNYOIDO = "1. Naponta átlagosan mennyi időt tölt digitális eszközök használatával?"
NEME = "Neme"
KORCSOPORT = "Melyik korcsoportba tartozik?"
LAKHELY = "Hol lakik?"
VEGZETTSEG = "Milyen iskolai végzettséggel rendelkezik?"

KATEGORIAK = [(15, 35, "Alacsony"), (36, 55, "Közepes"), (56, 75, "Magas")]
KEPERNYOIDO_SORREND = ["1 óránál kevesebb", "1–3 óra", "3–5 óra", "5–7 óra", "7 óránál több"]
VEGZETTSEG_SORREND = [
    "Doktori képzés (PhD/DLA)",
    "Egyetemi mesterképzés",
    "Egyetemi alapképzés",
    "Felsőfokú szakképzés",
    "Érettségi",
    "Szakiskola / Szakképzés / Szakmunkásképző",
    "Alapfokú végzettség (8 általános vagy kevesebb)",
]
SKALA = {
    "Egyáltalán nem jellemző rám": 1,
    "Inkább nem jellemző": 2,
    "Részben jellemző": 3,
    "Inkább jellemző": 4,
    "Teljes mértékben jellemző": 5,
    "1": 1, "2": 2, "3": 3, "4": 4, "5": 5,
}


def normalizal(szoveg):
    return " ".join(str(szoveg).replace("\xa0", " ").split()).strip().lower()


def oszlop_keres(df, minta):
    minta = normalizal(minta)
    for oszlop in df.columns:
        if minta in normalizal(oszlop):
            return oszlop
    raise KeyError(f"Nem található oszlop: {minta}")


def pont_ertek(valasz):
    szoveg = " ".join(str(valasz).replace("\xa0", " ").split()).strip()
    if szoveg in SKALA:
        return SKALA[szoveg]
    for karakter in szoveg:
        if karakter in "12345":
            return int(karakter)
    raise ValueError(f"Ismeretlen válaszérték: {valasz}")


def kategoria(pont):
    for also, felso, nev in KATEGORIAK:
        if also <= pont <= felso:
            return nev
    return "Ismeretlen"


def diagram_oszlop(adatok, cim, fajlnev, ylabel="Darab"):
    fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
    bars = ax.bar(range(len(adatok)), adatok.tolist(), width=0.65)
    ax.set_title(cim, fontsize=14, weight="bold")
    ax.set_ylabel(ylabel)
    ax.set_xticks(range(len(adatok)))
    ax.set_xticklabels(adatok.index, rotation=20, ha="right")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    ax.set_axisbelow(True)
    maximum = max(adatok.tolist()) if len(adatok) else 0
    ax.set_ylim(0, maximum + max(maximum * 0.15, 1))
    for bar, ertek in zip(bars, adatok.tolist()):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.2,
                str(round(ertek, 2)).replace(".0", ""), ha="center", va="bottom", fontsize=10)
    fig.tight_layout()
    fig.savefig(fajlnev, bbox_inches="tight")
    plt.close(fig)

def diagram_vizszintes(stat, cim, fajlnev):
    fig, ax = plt.subplots(figsize=(10.5, max(5, len(stat) * 0.8 + 1.5)), dpi=300)
    ax.barh(range(len(stat)), stat["Átlag"].tolist(), height=0.62)
    ax.set_title(cim, fontsize=14, weight="bold")
    ax.set_xlabel("Átlag pontszám")
    ax.set_yticks(range(len(stat)))
    ax.set_yticklabels(stat.index)
    ax.invert_yaxis()
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(axis="x", linestyle="--", alpha=0.3)
    ax.set_axisbelow(True)
    maximum = stat["Átlag"].max() if len(stat) else 0
    ax.set_xlim(0, maximum + max(maximum * 0.22, 8))
    for i, (_, sor) in enumerate(stat.iterrows()):
        ax.text(sor["Átlag"] + 0.5, i, f"{sor['Átlag']:.2f} (n={int(sor['Elemszám'])})",
                va="center", fontsize=10)
    fig.tight_layout()
    fig.savefig(fajlnev, bbox_inches="tight")
    plt.close(fig)


def main(csv_fajl):

    df = pd.read_csv(csv_fajl)
    os.makedirs("eredmenyek", exist_ok=True)
    kerdes_oszlopok = {kerdes: oszlop_keres(df, kerdes) for kerdes in KERDESEK}
    kepernyoido_oszlop = oszlop_keres(df, KEPERNYOIDO)
    neme_oszlop = oszlop_keres(df, NEME)
    korcsoport_oszlop = oszlop_keres(df, KORCSOPORT)
    lakhely_oszlop = oszlop_keres(df, LAKHELY)
    vegzettseg_oszlop = oszlop_keres(df, VEGZETTSEG)

    pontszamok, kategoriak_lista = [], []
    for _, sor in df.iterrows():
        pont = 0
        for kerdes, oszlop in kerdes_oszlopok.items():
            ertek = pont_ertek(sor[oszlop])
            pont += 6 - ertek if kerdes in FORDITOTT else ertek
        pontszamok.append(pont)
        kategoriak_lista.append(kategoria(pont))
    df["Pontszám"] = pontszamok
    df["Kategória"] = kategoriak_lista
    df.to_csv("eredmenyek/pontozott_valaszok.csv", index=False, encoding="utf-8-sig")


    kat_db = df["Kategória"].value_counts().reindex(["Alacsony", "Közepes", "Magas"], fill_value=0)
    ido_db = df[kepernyoido_oszlop].value_counts().reindex(KEPERNYOIDO_SORREND).dropna()
    ido_stat = df.groupby(kepernyoido_oszlop)["Pontszám"].agg(["mean", "count"]).round(2)
    ido_stat.columns = ["Átlag", "Elemszám"]
    ido_stat = ido_stat.reindex([x for x in KEPERNYOIDO_SORREND if x in ido_stat.index])

    demografiak = [
        ("Nem", neme_oszlop, "nemek_atlagpontszam.png"),
        ("Korcsoport", korcsoport_oszlop, "korcsoport_atlagpontszam.png"),
        ("Lakhely", lakhely_oszlop, "lakhely_atlagpontszam.png"),
        ("Iskolai végzettség", vegzettseg_oszlop, "vegzettseg_atlagpontszam.png"),
    ]

    demografiai_statok = {}
    for cim, oszlop, fajlnev in demografiak:
        stat = df.groupby(oszlop)["Pontszám"].agg(["mean", "count"]).round(2)
        stat.columns = ["Átlag", "Elemszám"]
        if cim == "Iskolai végzettség":
            sorrend = [x for x in VEGZETTSEG_SORREND if x in stat.index]
            maradek = [x for x in stat.index if x not in sorrend]
            stat = stat.reindex(sorrend + maradek)
        else:
            stat = stat.sort_values(["Átlag", "Elemszám"], ascending=[False, False])
        demografiai_statok[cim] = (stat, fajlnev)



    with open("eredmenyek/statisztika.txt", "w", encoding="utf-8") as f:
        f.write("ALAPSTATISZTIKÁK\n")
        f.write(f"Válaszadók száma: {len(df)}\n")
        f.write(f"Átlag pontszám: {df['Pontszám'].mean():.2f}\n")
        f.write(f"Minimum pontszám: {int(df['Pontszám'].min())}\n")
        f.write(f"Maximum pontszám: {int(df['Pontszám'].max())}\n\n")
        f.write("KATEGÓRIÁK SZERINTI ELOSZLÁS\n")
        for nev, db in kat_db.items():
            f.write(f"{nev}: {int(db)}\n")
        f.write("\nKÉPERNYŐIDŐ SZERINTI DARABSZÁM\n")
        for nev, db in ido_db.items():
            f.write(f"{nev}: {int(db)}\n")
        f.write("\nKÉPERNYŐIDŐ SZERINTI ÁTLAGPONTSZÁM ÉS ELEMSZÁM\n")
        for nev, sor in ido_stat.iterrows():
            f.write(f"{nev}: átlag = {sor['Átlag']:.2f}; n = {int(sor['Elemszám'])}\n")
        for cim, _, _ in demografiak:
            f.write(f"\n{cim.upper()} SZERINTI ÁTLAGPONTSZÁM ÉS ELEMSZÁM\n")
            for nev, sor in demografiai_statok[cim][0].iterrows():
                f.write(f"{nev}: átlag = {sor['Átlag']:.2f}; n = {int(sor['Elemszám'])}\n")



    diagram_oszlop(kat_db, "Biztonságtudatossági kategóriák", "eredmenyek/kategoriak_oszlopdiagram.png")
    fig, ax = plt.subplots(figsize=(7, 7), dpi=300)
    ax.pie(kat_db, labels=kat_db.index, autopct="%1.1f%%", startangle=90)
    ax.set_title("Biztonságtudatossági kategóriák", fontsize=14, weight="bold")
    fig.tight_layout()
    fig.savefig("eredmenyek/kategoriak_kordiagram.png", bbox_inches="tight")
    plt.close(fig)
    diagram_oszlop(ido_db, "Napi képernyőidő kategóriák", "eredmenyek/kepernyoido_oszlopdiagram.png")
    diagram_vizszintes(ido_stat, "Képernyőidő szerinti átlagos biztonságtudatossági pontszám",
                       "eredmenyek/kepernyoido_atlagpontszam.png")
    for cim, (stat, fajlnev) in demografiai_statok.items():
        diagram_vizszintes(stat, f"{cim} szerinti átlagpontszám", f"eredmenyek/{fajlnev}")

    print("Feldolgozás kész.")
    print("Eredmények az 'eredmenyek' mappában találhatók.")


if __name__ == "__main__":
    fajl = sys.argv[1] if len(sys.argv) > 1 else input("CSV fájl: ").strip()
    main(fajl)
