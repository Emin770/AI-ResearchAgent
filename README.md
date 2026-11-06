# 🤖 AI-Research & Career Intelligence Agent (v2.0)

Ein autonomer KI-Agent in Python zur automatisierten Recherche von Unternehmensprofilen, Fachbereichen und Stellenangeboten. 

Der Agent führt eine **Deep-Search-Recherche** durch: Er kombiniert Live-Websuche mit gezieltem Web-Scraping von Karriereseiten, analysiert die Volltexte über ein Large Language Model (LLM via Groq) und stellt die Ergebnisse in einem **interaktiven Web-Dashboard** oder als Markdown-Dateien zur Verfügung.

---

## 💡 Features

- **🌐 Interaktives Web-Dashboard (v2.0)**: Benutzeroberfläche mit Streamlit, Live-Analyseanzeige und direktem Markdown-Download.
- **💻 CLI & Batch-Modus (v1.0)**: Terminal-Ausführung für automatisierte Skriptabläufe über mehrere Unternehmen.
- **🔍 Deep Web Scraping**: Kombination aus DuckDuckGo-Websuche und echtem HTML-Parsing (`requests` & `BeautifulSoup`) zur Erkennung relevanter Stellenangebote.
- **🤖 LLM-Analyse**: Nutzt Groq (GPT-basierte Modelle) zur Extraktion von Kernkompetenzen, Fachbereichen und Karrierestufen (Junior, Senior, Werkstudent, Praktikum).
- **💾 Automatischer Export**: Speichert strukturierte Berichte inklusive Quellenverzeichnis (URLs).

---

## 🛠️ Tech Stack

- **GUI / Dashboard**: Streamlit
- **Programmiersprache**: Python 3.10+
- **LLM API**: `groq`
- **Web-Suche & Scraping**: `ddgs` (DuckDuckGo), `requests`, `beautifulsoup4`
- **Umgebungsvariablen**: `python-dotenv`

---

## 🚀 Schnellstart

### 1. Repository klonen
```bash
git clone [https://github.com/Emin770/AI-ResearchAgent.git](https://github.com/Emin770/AI-ResearchAgent.git)
cd AI-ResearchAgent
2. Virtuelle Umgebung erstellen & Abhängigkeiten installieren
Bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

pip install groq ddgs requests beautifulsoup4 python-dotenv streamlit
3. API-Key einrichten
Erstelle eine .env-Datei im Hauptverzeichnis und trage deinen Groq API-Key ein:

Code-Snippet
GROQ_API_KEY=dein_groq_api_key_hier
🖥️ Anwendung starten
Option A: Web-Dashboard (v2.0 – Empfohlen)
Starte die interaktive Benutzeroberfläche im Browser:

Bash
streamlit run app.py
Option B: Terminal-Skript (v1.0 CLI)
Starte den automatisierten CLI-Agenten im Terminal:

Bash
python main.py
📂 Beispiel-Output
Der Agent generiert strukturierte Analysen mit folgendem Aufbau:

Unternehmensprofil & Kernkompetenzen

Abteilungen & Fachbereiche (Matrix/Tabelle)

Offene Stellen & Karrieremöglichkeiten (Werkstudent, Junior, Senior, Praktika)

Quellenverzeichnis (Direktlinks zu den Scrape-Quellen)


---

### Auf GitHub hochladen

Führe diese Befehle in deinem Terminal aus, um das Update inklusive `app.py` und der neuen `README.md` auf GitHub zu veröffentlichen:

```cmd
git add .
git commit -m "Feat: Upgrade to v2.0 with Streamlit Web Dashboard and updated documentation"
git push origin main