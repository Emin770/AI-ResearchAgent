import os
import requests
from bs4 import BeautifulSoup
from ddgs import DDGS
from dotenv import load_dotenv
from groq import Groq
import streamlit as st

# Umgebungsvariablen (.env) laden
load_dotenv()

# Streamlit Page Config (Layout & Titel im Browser-Tab)
st.set_page_config(
    page_title="AI Research Agent v2.0", page_icon="🤖", layout="wide"
)

# API-Client initialisieren
client = Groq()


def fetch_page_content(url):
    """Besucht die Webseite und extrahiert den Volltext"""
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        response = requests.get(url, headers=headers, timeout=6)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            for element in soup(["script", "style", "nav", "footer", "header"]):
                element.extract()
            text = soup.get_text(separator=" ", strip=True)
            return text[:3500]
    except Exception as e:
        st.warning(f"Hinweis: Konnte {url} nicht direkt auslesen: {e}")
    return ""


def deep_web_search(query, max_results=3):
    """Sucht via DuckDuckGo und führt Deep-Scraping auf den Top-Links aus"""
    snippets = []
    urls_to_scrape = []
    try:
        with DDGS() as ddgs:
            for r in ddgs.text(query, max_results=max_results):
                body = r.get("body", "")
                href = r.get("href", "")
                snippets.append(f"Snippet: {body}\nLink: {href}")
                if href and href.startswith("http"):
                    urls_to_scrape.append(href)
    except Exception as e:
        st.error(f"Fehler bei der Websuche: {e}")

    full_texts = []
    for url in urls_to_scrape[:2]:
        content = fetch_page_content(url)
        if content:
            full_texts.append(
                f"=== VOLLTEXT VON SEITE ({url}) ===\n{content}\n=== ENDE VOLLTEXT ==="
            )

    return "\n\n".join(snippets) + "\n\n" + "\n\n".join(full_texts)


# --- STREAMLIT USER INTERFACE ---
st.title("🤖 AI-Research & Career Intelligence Agent")
st.markdown(
    "Willkommen in **Version 2.0**! Gib ein Unternehmen ein, um automatisch Abteilungen, Kernkompetenzen und offene Stellen analysieren zu lassen."
)

st.sidebar.header("⚙️ Einstellungen")
company_input = st.sidebar.text_input(
    "Unternehmensname", value="Consistency Beratungsgesellschaft Essen"
)
keyword_input = st.sidebar.text_input(
    "Optionaler Job-Filter (z.B. Werkstudent, KI, Junior)", value=""
)

start_button = st.sidebar.button("🚀 Recherche starten", type="primary")

# Hauptbereich der App
if start_button:
    if not company_input.strip():
        st.warning("Bitte gib einen Unternehmensnamen ein.")
    else:
        with st.spinner(
            f"Durchsuche das Web & Scrape Karriereseiten für '{company_input}'..."
        ):
            # 1. Deep Search
            query_jobs = f"{company_input} karriere stellenangebote jobs"
            if keyword_input.strip():
                query_jobs += f" {keyword_input.strip()}"

            search_data = deep_web_search(query_jobs)

        with st.spinner("KI verarbeitet die Daten und erstellt den Bericht..."):
            # 2. Prompting
            prompt_content = f"""
            Du hast hier den ECHTEN Text von den Webseiten des Unternehmens {company_input} vorliegen:
            
            {search_data}

            Erstelle eine präzise Unternehmens- und Karriereanalyse aus den obenstehenden Volltexten.

            1. **Unternehmensprofil & Kernkompetenzen**: Kurze Zusammenfassung der Dienstleistungen.
            2. **Abteilungen & Fachbereiche**: Welche Fachbereiche oder Teams lassen sich aus den Texten ablesen?
            3. **Konkrete offene Stellen & Karrieremöglichkeiten**:
               - Durchsuche den Text genau nach allen explizit genannten Stellenbezeichnungen.
               - Nenne genau die Karrierestufen (Junior, Senior, Werkstudent, Praktikum), falls sie im Text stehen.
            4. **Quellenverzeichnis**: Liste alle verwendeten Links am Ende auf.
            """

            try:
                completion = client.chat.completions.create(
                    model="openai/gpt-oss-20b",
                    messages=[
                        {
                            "role": "system",
                            "content": "Du bist ein präziser HR- und Unternehmensanalyst.",
                        },
                        {"role": "user", "content": prompt_content},
                    ],
                    temperature=0.1,
                )

                analysis_result = completion.choices[0].message.content

                st.success("Recherche erfolgreich abgeschlossen!")
                st.markdown("---")

                # Formatierter Output im Browser
                st.markdown(analysis_result)

                # Download-Button für das Ergebnis
                safe_filename = f"analyse_{company_input.lower().replace(' ', '_')}.md"
                st.download_button(
                    label="💾 Bericht als Markdown-Datei herunterladen",
                    data=f"# Unternehmens- & Deep-Karriereanalyse: {company_input}\n\n"
                    + analysis_result,
                    file_name=safe_filename,
                    mime="text/markdown",
                )

            except Exception as e:
                st.error(f"Fehler bei der KI-Generierung: {e}")
else:
    st.info(
        "👈 Stelle links in der Seitennavigation deine Kriterien ein und klicke auf **Recherche starten**."
    )