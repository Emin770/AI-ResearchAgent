import os
from dotenv import load_dotenv
from groq import Groq
from ddgs import DDGS

# Umgebungsvariablen (.env) laden
load_dotenv()

client = Groq()


def web_search(query, max_results=3):
    """Sucht im Internet nach Informationen via DuckDuckGo"""
    print(f"[🔍] Suche im Internet nach: '{query}'...")
    results = []
    with DDGS() as ddgs:
        for r in ddgs.text(query, max_results=max_results):
            results.append(r.get("body", ""))
    return "\n".join(results)


# 1. Wir holen die Websuche-Daten außerhalb des LLMs ein
company_to_search = "Consistency Beratungsgesellschaft Essen"
search_snippets = web_search(company_to_search)

print("### Starte die KI-Analyse mit den Live-Webdaten... ###")

# 2. Wir übergeben die Daten rein als Text (ohne dass das Modell denkt, es müsse selbst suchen)
prompt_content = f"""
Hier sind Informationen aus dem Internet über ein Unternehmen:
{search_snippets}

Analysiere basierend ausschließlich auf diesen Text-Informationen das Unternehmen Consistency (Standort Essen), 
was sie machen, und fasse die wichtigsten Kernkompetenzen zusammen. Nutze keine externen Tools.
"""

completion = client.chat.completions.create(
    model="openai/gpt-oss-20b",
    messages=[
        {
            "role": "system",
            "content": "Du bist ein präziser Unternehmensanalyst. Antworte direkt auf Basis des Textes und nutze keine Werkzeuge.",
        },
        {"role": "user", "content": prompt_content},
    ],
    temperature=0.1,
)

print("\n### Ergebnis des Web-Agenten: ###")
print(completion.choices[0].message.content)