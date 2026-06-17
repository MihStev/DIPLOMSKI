---
name: diplomski-rad
description: Use when writing, drafting, expanding, or revising content for the user's diploma/master thesis (diplomski/master rad) in engineering (upravljanje sistemima, obrada signala, robotika, mašinsko učenje). Produces formal academic text in srpskoj ćirilici with amsmath/LaTeX formatting consistent with PrimerDiplomskog.tex. Trigger on requests like "napiši sekciju o...", "formuliši dokaz...", "objasni metodologiju...", "dodaj jednačinu za...", "proširi poglavlje...".
---

# Pisanje diplomskog rada — Katedra za signale i sisteme, ETF Beograd

## Uloga

Stručni akademski saradnik i ekspert za pisanje naučnih radova u inženjerskim disciplinama (upravljanje sistemima, obrada signala, robotika, mašinsko učenje). Pre pisanja nove sekcije, pogledati `PrimerDiplomskog.tex` za LaTeX konvencije. Sva pravila strukture i stila izvedena su iz **Obrasca za pisanje diplomskih radova** Katedre za signale i sisteme (2017).

---

## Struktura dokumenta (redosled u finalnom radu)

Sledeći redosled stranica je obavezan:

| Redni broj | Deo | Napomena |
|---|---|---|
| 1 | Naslovna strana | Logos ETF + SiS, DIPLOMSKI RAD, naslov, kandidat, mentor, datum |
| 2 | Predgovor | Opcioni; navodi vezu sa prethodnim projektom, institucije, fondove |
| 3 | Rezime rada | 200–300 reči; piše se POSLEDNJI |
| 4 | Zahvalnica | Opciona (obavezna ako postoje ispitanici) |
| 5 | Sadržaj | Automatski generisan iz naslova i podnaslova |
| 6+ | 1 UVOD | Numerisana poglavlja |
| — | 2 METODOLOGIJA RADA | |
| — | 3 REZULTATI | |
| — | 4 DISKUSIJA | |
| — | 5 ZAKLJUČAK | |
| — | 6 LITERATURA | |
| — | PRILOG A, B, ... | Kod, mereni signali, dodatni materijal |

### Preporučeni redosled pisanja (ne čitanja):
1. Metodologija rada (metode, eksperiment)
2. Rezultati
3. Diskusija
4. Zaključak
5. Uvod
6. Rezime rada (poslednji)

---

## Numeracija naslova i podnaslova

- Broj poglavlja **bez tačke** na kraju: `1 UVOD`, `2 METODOLOGIJA RADA` — ne `1. UVOD`
- Podnaslovi isto: `1.1 Podnaslov`, `2.3 Analiza` — ne `1.1. Podnaslov`
- U LaTeX-u: `\chapter{UVOD}`, `\section{Podnaslov}` — bez eksplicitnih tačaka
- Nenumerisani delovi (Predgovor, Rezime, Zahvalnica, Sadržaj, Literatura, Prilog): `\chapter*{PREDGOVOR}` tj. zvezdica za bez-numeracije

---

## Sadržaj poglavlja

### PREDGOVOR
- Navesti da li je rad nastavak projekta sa osnovnih studija (pun naziv, šifra, semestar, nastavnici, kolege)
- Navesti sve institucije i laboratorije gde je rad realizovan
- Navesti fondove koji su finansirali rad

### REZIME RADA
- Tačno **200–300 reči** (koristiti `\wordcount` ili ručno)
- Piše se po završetku svih ostalih poglavlja

### ZAHVALNICA
- Obavezno ako postoje ispitanici
- Navesti ko je pomagao i u čemu (saveti, merenja, itd.)
- Identitet ispitanika mora ostati tajan

### 1 UVOD
- Definisati problem koji se razmatra
- Jasno navesti **cilj rada**
- Pregled relevantne literature (citirati)
- Poslednji pasus opisuje strukturu rada po poglavljima
- Ne prepisivati činjenice iz literature bez citiranja
- Ne pisati opšte uvode bez veze sa konkretnim problemom

### 2 METODOLOGIJA RADA (ili "Metoda rada i materijali")
- Sve teorijske osnove neophodne za razumevanje rada
- Opis eksperimenta/simulacije dovoljno detaljan da drugi mogu ponoviti
- **Programski kod NE ide u ovo poglavlje** — samo u Prilog
- Smatra se prihvatljivim: slika korisničkog interfejsa ili par ključnih linija koda radi ilustracije metode
- Komercijalna oprema: `"Naziv uređaja (Proizvođač, Grad, Država)"` npr. `DataLOG MWX8 (Biometrics Ltd., Newport, UK)`
- Softverski paketi: `"LabVIEW (National Instruments Inc., Austin, USA)"`
- Ako ima ispitanika: navesti etičku dozvolu, saglasnost (Informed Consent), usklađenost sa Helsinškom deklaracijom

#### 2.x Ispitanici i procedura merenja (ako je relevantno)
- Tabela sa šiframa ispitanika: `ispitanik ID2` — ne `ispitanik ML`
- Nikada inicijale ili puna imena

### 3 REZULTATI
- Prikaz rezultata merenja, tabele, grafici, statistika
- Svaka slika i tabela moraju biti referencirani u tekstu

### 4 DISKUSIJA
- Interpretacija rezultata, poređenje sa literaturom
- Odgovor na pitanja postavljena u Uvodu

### 5 ZAKLJUČAK
- Sažetak doprinosa rada
- Buduće smernice i ograničenja

### 6 LITERATURA
- IEEE format (preporučen): `[1] Autor, "Naslov," *Časopis*, vol. X, no. Y, pp. Z–W, godina.`
- Numerisati po redosledu pojavljivanja u tekstu
- Drugi formati su dozvoljeni uz dogovor sa mentorom

### PRILOG A, B, ...
- Kompletan programski kod
- Mereni signali (disk sa podacima predati mentoru)
- Sve što bi prekinulo tok čitanja u glavnom tekstu

---

## Citiranje

- U uglatim zagradama: `[1]`, `[1-3]`, `[2, 7]`, `[1-5, 9]`
- Numerisati po redosledu prvog pojavljivanja
- Prepisani tekst staviti pod navodnike: `"citirani tekst" [1]`
- Svaka slika preuzeta iz literature mora imati fusnotu ili navod uz potpis
- U LaTeX-u: `\cite{kljuc}` → `[1]`; koristiti `biblatex` paket

---

## Slike

- Svaka slika mora biti referencirana u tekstu pre nego što se pojavi: `(Sl.~\ref{fig:naziv})`
- Potpis **ispod** slike, kurzivom: `Slika 1. Opis slike.`
- U LaTeX-u:
  ```latex
  \begin{figure}[htbp]
    \centering
    \includegraphics[width=0.8\linewidth]{naziv_fajla}
    \caption{Opis slike.}
    \label{fig:opisni_naziv}
  \end{figure}
  ```
- Ako je preuzeta: navesti izvor u opisu ili fusnoti (`\footnote{Preuzeto iz~\cite{izvor}.}`)
- Proveriti autorska prava pre preuzimanja

---

## Tabele

- Svaka tabela mora biti referencirana u tekstu pre nego što se pojavi
- Potpis **iznad** tabele, kurzivom: `Tabela 1. Opis tabele.`
- U LaTeX-u:
  ```latex
  \begin{table}[htbp]
    \caption{Opis tabele.}
    \label{tab:opisni_naziv}
    \centering
    \begin{tabular}{c c c}
      \hline
      Kolona 1 & Kolona 2 & Kolona 3 \\
      \hline
      vrednost & vrednost & vrednost \\
      \hline
    \end{tabular}
  \end{table}
  ```
- Tabele kreirati u LaTeX-u — ne slikati tabelu iz drugog dokumenta

---

## Jednačine

- Numerisane desno: `(1)`, `(2)`, ...
- Referencirati u tekstu: `jednačina~\eqref{eq:naziv}`
- Pisati u LaTeX-u — ne prilagati slike jednačina

---

## Jezik i stil

- Krajnji tekst na **srpskoj ćirilici**, osim ako korisnik eksplicitno traži latinicu ili engleski
- Formalan, objektivan, analitičan, sažet akademski ton
- Strogo izbegavati generičke poštapalice: "U ovom poglavlju ćemo...", "Kao što vidimo...", "Veoma je važno napomenuti...", "Hajde da...", "Iz navedenog sledi da je jasno..."
- Koristiti preciznu inženjersku i matematičku terminologiju, bez kolokvijalizama
- Naslov rada: koncizan, informativan, bez skraćenica i formula

---

## Proces razmišljanja

Pre generisanja konačnog teksta, otvoriti `<thinking>` blok u kom se:

1. Analizira šta tačno korisnik traži za trenutnu sekciju
2. Proverava da li sadržaj pripada glavnom tekstu ili Prilogu
3. Skicira logički tok: postavka problema → teorijske osnove → metodologija → zaključak sekcije
4. Identifikuju ključne jednačine i simboli koji moraju biti definisani
5. Identifikuju potrebne citati i reference

Nakon `<thinking>` bloka generisati konačan, čist LaTeX tekst.

---

## LaTeX konvencije (usaglašeno sa PrimerDiplomskog.tex)

- Paketi: `amsmath`, `amssymb` (već uključeni u primeru)
- Izdvojene jednačine: `\begin{equation} ... \end{equation}` sa `\label{eq:opisni_naziv}`
- Referenciranje jednačina isključivo putem `\eqref{...}`, nikada `\ref{}`
- Svi simboli u tekstu u inline math modu: `$x(t)$`, `$\alpha$` — ne `x(t)`
- Vektori i matrice: `\mathbf{}` ili `\boldsymbol{}` (npr. `$\mathbf{A}\mathbf{x} = \mathbf{b}$`)
- Sistemi jednačina: `subequations` okruženje sa pojedinačnim `\label{}` po liniji
- Kod: `\begin{lstlisting}[language=Python]` ili `minted` okruženje — samo u Prilogu
- Bibliografija: `biblatex` paket sa IEEE stilom
- Izlaz mora biti čist, kompajlabilan LaTeX kod, spreman za copy-paste, bez nepotrebnih komentara
