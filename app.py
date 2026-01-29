import streamlit as st
from groq import Groq

st.set_page_config(
    page_title="Asistent",
    page_icon="💬",
    layout="centered"
)

st.title("Kalkulator moč proti masi asistent")
st.write("Pozdravljeni, ali imate kakšno vprašanje o kalkulatorju ali pa razlago razmerja moč proti masa?")

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
                "content": (
                    "Si prijazen in strokoven asistent za fiziko. "
                    "Pomagaš pri razlagi moči, mase, sile, dela in energije "
                    "ter pri uporabi fizikalnega kalkulatorja na spletni strani. "
                    "Če vprašanje ni povezano s fiziko, razmerje moč proti masi(hp/kg) ali pa delovanjem kalkulatorja, "
                    "vljudno odgovori, da za to področje nimaš informacij. "
                    "Vedno odgovarjaj izključno v slovenščini."
                )
        }
    ]

for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"**Vi:** {msg['content']}")
    elif msg["role"] == "assistant":
        st.markdown(f"**AI:** {msg['content']}")

user_input = st.text_input("Vpišite vprašanje:")

if st.button("Pošlji") and user_input:
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=st.session_state.messages
        )

        ai_text = response.choices[0].message.content

        st.session_state.messages.append(
            {"role": "assistant", "content": ai_text}
        )

        st.rerun()

    except Exception as e:
        st.error(f"Napaka pri klicu API-ja: {e}")
