import os
from bs4 import BeautifulSoup
from ddgs import DDGS
from dotenv import load_dotenv
from groq import Groq
import requests
import streamlit as st

load_dotenv()

st.set_page_config(
    page_title="AI Research Agent v2.0", page_icon="🤖", layout="wide"
)

client = Groq()


def fetch_page_content(url):
    """Besucht die Webseite mit verbesserten Headern"""
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept-Language": "de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7",
        }
        response = requests.get(url, headers=headers, timeout=6)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            for element in soup([
                "script",
                "style",
                "nav",
                "footer",
                "header",
                "noscript",
            ]):
                element.extract()
            text = soup.get_text(separator=" ", strip=True)
            return text[:4000]
    except Exception:
        pass
    return ""


def deep_web_search(query, max_results=4):
    """Sucht via DuckDuckGo und zieht Daten aus Snippets und Webseiten"""
    snippets = []
    urls_to_scrape = []
    try:
        with DDGS() as ddgs:
            for r in ddgs.text(query, max_results=max_results):
                body = r.get("body", "")
                href = r.get("href", "")
                if body:
                    snippets.append(f"Snippet: {body}\nLink: {href}")
                if href and href.startswith("http"):
                    urls_to_scrape.append(href)
    except Exception as e:
        st.error(f"Fehler bei der Websuche: {e}")

    full_texts = []
    for url in urls_to_scrape[:3]:
        content = fetch_page_content(url)
        if content and len(content) > 100:  # Nur nutzen, wenn echter Text da ist
            full_texts.append(
                f"=== VOLLTEXT VON SEITE ({url}) ===\n{content}\n=== ENDE VOLLTEXT ==="
            )

    combined = "\n\n".join(snippets) + "\n\n" + "\n\n".join(full_texts)
    return combined


# UI
st.title("🤖 AI-Research & Career Intelligence Agent")
st.markdown(
    "Willkommen in **Version 2.0**! Gib ein Unternehmen ein, um automatisch Abteilungen, Kernkompetenzen und offene Stellen analysieren zu lassen."
)

st.sidebar.header("⚙️ Einstellungen")
company_input = st.sidebar.text_input(
    "Unternehmensname", value="GFOS Essen Software"
)
keyword_input = st.sidebar.text_input(
    "Optionaler Job-Filter (z.B. Werkstudent, KI, Junior)", value=""
)

start_button = st.sidebar.button("🚀 Recherche starten", type="primary")

if start_button:
    if not company_input.strip():
        st.warning("Bitte gib einen Unternehmensnamen ein.")
    else:
        with st.spinner(
            f"Durchsuche das Web & Scrape Karriereseiten für '{company_input}'..."
        ):
            query_jobs = (
                f"{company_input} karriere stellenangebote jobs gfos.com"
            )
            if keyword_input.strip():
                query_jobs += f" {keyword_input.strip()}"

            search_data = deep_web_search(query_jobs)

        if not search_data.strip():
            st.error(
                "Keine Daten im Web gefunden. Bitte versuche einen präziseren Suchbegriff (z. B. 'GFOS Essen Software')."
            )
        else:
            with st.spinner("KI verarbeitet die Daten..."):
                prompt_content = f"""
                Hier sind Informationen aus dem Internet über das Unternehmen {company_input}:
                
                {search_data}

                Erstelle eine präzise Unternehmens- und Karriereanalyse. Wenn bestimmte Details in den Texten fehlen, nenne dies sachlich.

                1. **Unternehmensprofil & Kernkompetenzen**: Was macht das Unternehmen?
                2. **Abteilungen & Fachbereiche**: Welche Fachbereiche lassen sich ableiten?
                3. **Konkrete offene Stellen & Karrieremöglichkeiten**: Welche Rollen/Level (Werkstudent, Junior, Senior) werden erwähnt?
                4. **Quellenverzeichnis**: Liste alle verwendeten Links auf.
                """

                try:
                    completion = client.chat.completions.create(
                        model="openai/gpt-oss-20b",
                        messages=[
                            {
                                "role": "system",
                                "content": "Du bist ein präziser HR-Analyst.",
                            },
                            {"role": "user", "content": prompt_content},
                        ],
                        temperature=0.1,
                    )

                    analysis_result = completion.choices[0].message.content

                    if analysis_result and len(analysis_result.strip()) > 50:
                        st.success("Recherche erfolgreich abgeschlossen!")
                        st.markdown("---")
                        st.markdown(analysis_result)

                        safe_filename = f"analyse_{company_input.lower().replace(' ', '_')}.md"
                        st.download_button(
                            label="💾 Bericht als Markdown-Datei herunterladen",
                            data=f"# Unternehmensanalyse: {company_input}\n\n"
                            + analysis_result,
                            file_name=safe_filename,
                            mime="text/markdown",
                        )
                    else:
                        st.warning(
                            "Die KI konnte aus den gefundenen Daten keinen vollständigen Bericht generieren. Versuche den Suchbegriff anzupassen."
                        )

                except Exception as e:
                    st.error(f"Fehler bei der KI-Generierung: {e}")