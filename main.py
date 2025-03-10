import streamlit as st
import time
from openai_api import get_client, get_embedding, get_response
from RAG import search_similarity, RAG_based_response

client = get_client()

if 'show_chat' not in st.session_state:
    st.session_state.show_chat = False

if 'current_menu' not in st.session_state:
    st.session_state.current_menu = "Chat"


def activate_chat():
    st.session_state.show_chat = True


def set_menu(menu_option):
    st.session_state.current_menu = menu_option


if not st.session_state.show_chat:
    left, middle, right = st.columns(3)
    middle.image("Image2.png", width=200)
    st.header("AI chef-Osobní Michelinský kuchař 24/7 🧑‍🍳")
    st.subheader("Mějte k dispozici špičkového kuchaře, který se nikdy neunaví")
    st.write("AI chef je chatbot poháněný pokročilou umělou inteligencí, který vám umožní:")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader("🍴Recepty krok za krokem")
        st.write("Podrobné vysvětlení jednotlivých receptů a možnost se na cokoliv doptat.")
    with col2:
        st.subheader("💸Přístup zcela zdarma")
        st.write("Přístup ke špičkovým receptům a pokročilé umělé inteligenci za 0 kč měsíčně.")
    with col3:
        st.subheader("🪴Dietní omezení")
        st.write("Nemůžete například lepek, mléko či jiný alergen? Žádný problém!")

    left, middle, right = st.columns(3)
    middle.button("Vyzkoušet zdarma ještě dnes", on_click=activate_chat)

    st.warning("⚠️Neklikejte na toto tlačítko, pokud chcete nadále⚠️")
    st.write("✖️ Platit za předražené kuchařky")
    st.write("✖️ Vařit špatná a nedochucená jídla")
    st.write("✖️ Neznat efektivní techniky na dobré vaření")
    st.write("✖️ Nedopřát svým nejbližším chutné a zdravé jídlo")
    st.write("✖️ Ztrácet zbytečné množství času u vaření")

    st.success("Co se stane, pokud na toto tlačítko kliknete")
    st.write("☑️ Získáte přístup k pokročilé umělé inteligenci, která má přístup k unikátnímu datasetu recpetů")
    st.write("☑️ Naučíte se pokročilé kuchařské techniky")
    st.write("☑️ Vaši blízcí k vám budou častěji chodit-vaše jídlo si prostě nepůjde nezamilovat")
    st.write("☑️ Budete jíst zdravé a extrémně chutné jídlo za velmi rozumnou cenu")
    st.write("☑️ Ušetříte denně i spoustu drahocenného času díky vyšší efektivitě ve vaření")

    st.subheader("Časté dotazy")
    with st.expander("Je tato AI skutečně zdarma? Že je v tom nějaký háček?"):
        st.write(
            "Tato pokročilá umělá inteligence s datasetem unikátních receptů je skutečně zdarma žádný háček v tom není :) Vyzkoušejte sami")
    with st.expander("Proč bych měl používat vaši AI, když můžu to stejné zadat do ChatGPT?"):
        st.write(
            "Naše AI disponuje unikátním datasetem receptů, ke kterým má přístup díky sofistikovaným algoritmům, z toho důvodu naše AI bude poskytovat výrazně lepší výsledky :)")
    with st.expander("Nejsem technicky zdatný, zvládnu to používat?"):
        st.write("Ano, stačí jen umět psát na počítači, nic víc, nic míň. O zbytek se už AI postará sama")

    left, middle, right = st.columns(3)
    middle.button("Vyzkoušet zdarma ještě dnes!", on_click=activate_chat)

else:
    image = st.sidebar.image("Image2.png", width=200)
    st.sidebar.header("Menu")

    chat_btn_style = "primary" if st.session_state.current_menu == "Chat" else "secondary"
    history_btn_style = "primary" if st.session_state.current_menu == "Historie" else "secondary"

    st.sidebar.button("Chat", type=chat_btn_style, key="chat_btn", use_container_width=True, on_click=set_menu,
                      args=("Chat",))
    st.sidebar.button("Historie", type=history_btn_style, key="history_btn", use_container_width=True,
                      on_click=set_menu, args=("Historie",))

    if st.session_state.current_menu == "Chat":
        st.header("AI Chef - Osobní Michelinský kuchař 24/7")
        st.write("Zeptejte se na jakýkoliv recept nebo nahrajte obrázek jídla.")

        if 'messages' not in st.session_state:
            st.session_state.messages = []

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.write(message["content"])

        prompt = st.chat_input("Zadejte recept, který chcete vyhledat...")
        if prompt:
            st.session_state.messages.append({"role": "user", "content": prompt})

            with st.chat_message("user"):
                st.write(prompt)

            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                full_response = ""

                with st.spinner("AI Chef připravuje odpověď..."):
                    similar_recipe = search_similarity(prompt)
                    response_stream = get_response(client, RAG_based_response(similar_recipe, prompt))

                for chunk in response_stream:
                    if chunk is not None:
                        full_response += chunk
                        message_placeholder.write(full_response + "▌")

                message_placeholder.write(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})

    elif st.session_state.current_menu == "Historie":
        st.header("Historie vašich receptů")
        st.write("Zde najdete své dříve vyhledané recepty.")

        if 'messages' in st.session_state and len(st.session_state.messages) > 0:
            recipe_count = 0
            for i, message in enumerate(st.session_state.messages):
                if message["role"] == "user" and i + 1 < len(st.session_state.messages):
                    recipe_count += 1
                    with st.expander(f"Recept {recipe_count}: {message['content']}"):
                        st.write(f"**Váš dotaz:** {message['content']}")
                        st.write("**Odpověď AI Chef:**")
                        st.write(st.session_state.messages[i + 1]["content"])
        else:
            st.info("Zatím nemáte žádné vyhledané recepty. Vraťte se do chatu a začněte vaření!")
