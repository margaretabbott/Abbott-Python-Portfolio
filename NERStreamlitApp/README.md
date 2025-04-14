if text:
    doc = nlp(text)
    st.subheader("Named Entities")
    for ent in doc.ents:
        st.markdown(f"**{ent.text}** — *{ent.label_}*")

    st.subheader("Visualization")
    st.components.v1.html(spacy.displacy.render(doc, style="ent", page=True), height=400, scrolling=True)

streamlit run C:\Users\marga\OneDrive\Documents\Abbott-Python-Portfolio\NERStreamlitApp\StreamlitNER.py