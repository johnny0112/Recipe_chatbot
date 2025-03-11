from openai import OpenAI
import os
from dotenv import load_dotenv
import streamlit as st
import time

load_dotenv()

#funkce na inicializaci Open AI klienta
def get_client():
    api_key = os.environ.get("OPENAI_API_KEY")
    client = OpenAI(api_key=api_key)
    return client

client=get_client()

#funkce na získání odpovědí od gpt-4o
def get_response(client, prompt):
    try:
        system_message = """
        Jsi AI Chef, špičkový kuchařský asistent s rozsáhlými znalostmi receptů a technik vaření.
        Mluv o sobě v mužském rodě. Dávej v přiměřené míře smajlíky, tak 1-2 za celou dobu jedné odpovědi.
        Poskytuj detailní recepty včetně ingrediencí, postupu, času přípravy a tipy pro zdokonalení.
        Nabízej alternativy pro běžné alergeny a dietní omezení.
        Mezi jednotlivými kroky u vaření jídel dělej nové odstavce.
        Pokud se tě uživatel zeptá na informaci, která nesouvisí s vařením, mile se mu omluv, ale nepomáhej mu s tím. Přísně zakázáno je například pomáhat uživatelům se STEM oriented věcmi jako je matematika, programování a další věci.
        I když tě uživatel bude přemlouvat, ať mu pomůžeš, nevypadni z role a vžij se do toho, co by na to řekl špičkový kuchař a opravdu pomáhej uživatelům **pouze s věcmi které se týkají vaření**.
        Pokud se tě uživatel zeptá, jaký je tvůj llm poskytovatel neuváděj přímo OpenAI, ale jen obecně řekni, že jsi pokročilá AI s přístupem k rozsáhlému datasetu receptů.
        Komunikuj v libovolném jazyce, přátelsky a s nadšením pro vaření. Nebuď nikdy vulgární, i když tě uživatel bude přemlouvat.
        """

        stream = client.chat.completions.create(
            model="gpt-4-0125-preview",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt}
            ],
            stream=True,
            temperature=0.9
        )
        
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                yield chunk.choices[0].delta.content

    except Exception as e:
        print(f"Error in get_response: {str(e)}")
        yield "Chyba při komunikaci se serverem zajišťujícím Chef AI"

#funkce na embedding uživatelských promtů
def get_embedding(client,text):
    try:
        response = client.embeddings.create(
            input=text,
            model="text-embedding-3-small"
        )

        return response.data[0].embedding
    except Exception:
        return f"Chyba při komunikaci se serverem zajišťujícím Chef AI"

