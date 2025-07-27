# Hockey Stats API – NHL Saison 2021/2022

**Analyseplattform mit FastAPI, PostgreSQL und Jinja2 zur Visualisierung von Team- und Spielerstatistiken der NHL-Saison 2021/22**

Dieses Projekt basiert auf Modulen meiner früheren Arbeit bei [DryShaft Data Lab](https://dryshaft.net) und dient als technisches Showcase zur Analyse von Eishockeydaten. Es kombiniert Spielstatistiken, Quotenanalysen und Spielerbiografien in einem modularen Web-Interface.

- **Projektbeschreibung:** [pythia.one/hockey](https://pythia.one/hockey.html)
- **Live-Demo (bald online):** https://hockey.up.railway.app

---

## Projektüberblick

- Komplette NHL-Saison 2021/22 mit allen Spielen, Ergebnissen und Spielphasen (REG, OT, SO)
- Teamseiten mit aggregierten Statistiken, Upset-Raten, Heim-/Auswärtsprofil, OT-Verhalten
- Detaillierte Matchseiten mit Teamleistung, Torschüssen, Quoten und Goalie-Stats
- Eigene Spieler- und Goalieprofile mit Biografie (Scraping via Playwright)
- Aggregierte Metriken zu Upsets, Serien und Bookmaker-Abweichungen

Die Daten stammen aus öffentlich zugänglichen NHL-Endpunkten sowie historischen Buchmacherquoten.

---

## Tech Stack

- **Backend:** FastAPI, SQLAlchemy (async), PostgreSQL
- **Frontend:** Jinja2 Templates, Tailwind CSS
- **Parser:** Playwright (biografische Daten und Spielerfotos von NHL.com)
- **Deployment:** Docker, Railway

---

## Projektstruktur

```plaintext
hockey-stats/
├── app/
│   ├── main.py              # FastAPI-Startpunkt
│   ├── routers/             # API-Endpunkte (teams, players, games, insights, goalies)
│   ├── repositories/        # Datenlogik und Businessfunktionen
│   ├── models/              # SQLAlchemy-Datenmodelle
│   ├── crud/                # Datenbankzugriffe
│   ├── templates/           # HTML-Templates (Jinja2)
│   ├── static/              # Tailwind CSS, JS, Logos
│   └── utils/               # Playwright, Upset-Logik, Hilfsfunktionen
├── docker-compose.yml
├── Dockerfile
└── requirements.txt
```

---

## Lokaler Start (Docker)

```bash
# 1. Repository klonen
https://github.com/alexandr-gessel/hockey-stats.git

# 2. Docker-Container starten
docker-compose up --build
```

Die Anwendung lädt vorberechnete Tabellen für Upsets, Teamstatistiken und Spielerprofilseiten. Ideal für Deployment ohne aktive Hintergrundprozesse.

---

## Hinweise

- Dieses Projekt ist ein MVP mit Fokus auf Performance und Lesbarkeit.
- Alle gezeigten Metriken basieren auf öffentlich zugänglichen Daten.
- Einige Methoden (insb. Upset-Klassifizierung, Bookmaker-Auswertung) wurden aus meiner NDA-geschützten Arbeit abstrahiert und vereinfacht.

---

**📍 Vollständige Kontextseite und Projektreflexion:**  
[https://pythia.one/hockey](https://pythia.one/hockey.html)
