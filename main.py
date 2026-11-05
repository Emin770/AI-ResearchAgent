import os
from dotenv import load_dotenv
from groq import Groq
from ddgs import DDGS
import requests
from bs4 import BeautifulSoup

# Umgebungsvariablen (.env) laden
load_dotenv()
client = Groq()


def fetch_page_content(url):
    """Besucht die echte Webseite und zieht den vollen Text heraus"""
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        response = requests.get(url, headers=headers, timeout=6)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            # Entferne Skripte, Navigationsleisten und Footer für sauberen Text
            for element in soup(["script", "style", "nav", "footer", "header"]):
                element.extract()
            text = soup.get_text(separator=" ", strip=True)
            # Kürzen auf max 3500 Zeichen pro Seite, um das KI-Limit nicht zu sprengen
            return text[:3500]
    except Exception as e:
        print(f"[!] konnte {url} nicht direkt auslesen: {e}")
    return ""


def deep_web_search(query, max_results=3):
    """Sucht via DuckDuckGo UND liest den echten Inhalt der besten Links aus"""
    print(f"[🔍] Suche im Web nach: '{query}'...")
    urls_to_scrape = []
    snippets = []

    try:
        with DDGS() as ddgs:
            for r in ddgs.text(query, max_results=max_results):
                body = r.get("body", "")
                href = r.get("href", "")
                snippets.append(f"Snippet: {body}\nLink: {href}")
                if href and href.startswith("http"):
                    urls_to_scrape.append(href)
    except Exception as e:
        print(f"[!] Hinweis bei Suche: {e}")

    # Jetzt echte Webseiten öffnen und Text auslesen
    print(
        f"[🌐] Öffne und lese den ECHTEN Inhalt von {len(urls_to_scrape[:2])} Webseiten..."
    )
    full_texts = []
    for url in urls_to_scrape[:2]:  # Öffnet die 2 relevantesten Ergebnisse
        print(f"  -> Surfe auf: {url}")
        content = fetch_page_content(url)
        if content:
            full_texts.append(
                f"=== VOLLTEXT VON SEITE ({url}) ===\n{content}\n=== ENDE VOLLTEXT ==="
            )

    combined_info = "\n\n".join(snippets) + "\n\n" + "\n\n".join(full_texts)
    return combined_info


# ==========================================
# ⚙️ EINSTELLUNGEN
# ==========================================
job_keyword = ""  # Optional: "Werkstudent", "Junior" oder leer lassen ""

companies_to_analyze = [
    "Consistency Beratungsgesellschaft Essen",
    # "SAP SE Walldorf",
]
# ==========================================

for company_name in companies_to_analyze:
    print(f"\n========================================")
    print(f" Starte Deep-Search-Recherche für: {company_name}")
    print(f"========================================")

    # Wir suchen direkt nach der Karriereseite der Firma
    query_jobs = (
        f"{company_name} karriere stellenangebote jobs jobs.consistency.de"
    )

    if job_keyword.strip():
        query_jobs += f" {job_keyword.strip()}"

    search_data = deep_web_search(query_jobs)

    print("### Starte die KI-Analyse des echten Seiteninhalts... ###")

    prompt_content = f"""
    Du hast hier den ECHTEN Text von den Webseiten des Unternehmens {company_name} vorliegen:
    
    {search_data}

    Erstelle eine präzise Unternehmens- und Karriereanalyse aus den obenstehenden Volltexten.

    1. **Unternehmensprofil & Kernkompetenzen**: Kurze Zusammenfassung der Dienstleistungen.
    2. **Abteilungen & Fachbereiche**: Welche Fachbereiche oder Teams lassen sich aus den Texten ablesen?
    3. **Konkrete offene Stellen & Karrieremöglichkeiten**:
       - Durchsuche den Text genau nach allen explizit genannten Stellenbezeichnungen (z. B. Senior Consultant, Werkstudent IT, Agile Coach, Junior Consultant etc.).
       - Nenne genau die Karrierestufen (Junior, Senior, Werkstudent, Praktikum), falls sie im Text stehen.
    4. **Quellenverzeichnis**: Liste alle verwendeten Links am Ende auf.
    """

    try:
        completion = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[
                {
                    "role": "system",
                    "content": "Du bist ein präziser HR-Analyst. Extrahiere konkrete Stellenbezeichnungen und Level (Junior, Senior, Werkstudent) direkt aus dem Fließtext der Webseite.",
                },
                {"role": "user", "content": prompt_content},
            ],
            temperature=0.1,
        )

        analysis_result = completion.choices[0].message.content

        safe_filename = (
            "analyse_"
            + company_name.lower()
            .replace(" ", "_")
            .replace("(", "")
            .replace(")", "")
            + ".md"
        )

        with open(safe_filename, "w", encoding="utf-8") as f:
            f.write(
                f"# Unternehmens- & Deep-Karriereanalyse: {company_name}\n\n"
            )
            f.write(analysis_result)

        print(f"[💾] Erfolgreich gespeichert als '{safe_filename}'")

    except Exception as e:
        print(f"[!] Fehler bei der KI-Generierung: {e}")

print("\n### Deep-Search erfolgreich abgeschlossen! ###")