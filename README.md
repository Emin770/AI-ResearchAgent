# 🤖 AI-Research & Career Intelligence Agent

Ein autonomer KI-Agent in Python zur automatisierten Recherche von Unternehmensprofilen, Fachbereichen und Karriereangeboten. 

Der Agent führt eine **Deep-Search-Recherche** durch: Er kombiniert Live-Websuche mit gezieltem Web-Scraping von Karriereseiten, analysiert die Volltexte über ein Large Language Model (LLM via Groq) und generiert strukturierte Berichte im Markdown-Format samt Quellenverzeichnis.

---

## 💡 Features

- **🔍 Live-Websuche & Deep Scraping**: Durchsucht das Netz via DuckDuckGo und besucht automatisiert die echten Karriereseiten (HTML-Parsing mit `BeautifulSoup`).
- **🤖 LLM-Analyse**: Nutzt Groq (GPT-basierte Modelle) zur Extraktion von Kernkompetenzen, Fachbereichen und Karrierestufen (Junior, Senior, Werkstudent, Praktikum).
- **⚙️ Modulare Einstellungen**: Unterstützt Batch-Analysen für mehrere Firmen sowie optionale Keyword-Filter (z. B. gezielt nach *Werkstudent* oder *KI*).
- **💾 Automatischer Export**: Speichert strukturierte Berichte als `.md`-Dateien inkl. Quellenverzeichnis (URLs).

---

## 🛠️ Tech Stack

- **Programmiersprache**: Python 3.10+
- **LLM API**: `groq`
- **Web-Suche & Scraping**: `ddgs` (DuckDuckGo), `requests`, `beautifulsoup4`
- **Umgebungsvariablen**: `python-dotenv`

---

## 🚀 Schnellstart

### 1. Repository klonen
bash
git clone https://github.com/Emin770/AI-ResearchAgent.git
cd AI-ResearchAgent

### 2. Virtuelle Umgebung erstellen & Pakete installieren

python -m venv venv

Windows:
venv\Scripts\activate

Mac/Linux:
source venv/bin/activate

pip install groq ddgs requests beautifulsoup4 python-dotenv

### 3. API-Key einrichten
Erstelle eine `.env`-Datei im Hauptverzeichnis und trage deinen Groq API-Key ein:

env
GROQ_API_KEY=dein_groq_api_key_hier

### 4. Agenten ausführen

bash
python main.py

---

## 📂 Beispiel-Output

Der Agent generiert Markdown-Dateien wie `analyse_company.md` mit folgendem Aufbau:
1. **Unternehmensprofil & Kernkompetenzen**
2. **Abteilungen & Fachbereiche** (Matrix)
3. **Offene Stellen & Karrieremöglichkeiten** (inkl. Level-Zuordnung)
4. **Quellenverzeichnis** (Direktlinks)