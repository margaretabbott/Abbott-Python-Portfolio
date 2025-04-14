import streamlit as st
import pandas as pd
import spacy

st.title("Streamlit SpaCy Entity Ruler")

# Load base model
nlp = spacy.load('en_core_web_sm')

# Text input section
st.header("Input Text")
text_source = st.radio("Choose input method:", ("Type or paste text", "Upload .txt file"))

if text_source == "Type or paste text":
    text = st.text_area("Enter your text here:", height=150)
else:
    uploaded_file = st.file_uploader("Upload a .txt file", type=["txt"])
    if uploaded_file is not None:
        text = uploaded_file.read().decode("utf-8")
    else:
        text = ""

# Pattern input section 
st.header("Create Your Own Custom Entity Patterns")

num_patterns = st.number_input("How many patterns do you want to add?", min_value=1, max_value=20, value=1)

custom_patterns = []
common_labels = [
    "PERSON", "ORG", "GPE", "LOC", "PRODUCT", "EVENT", "DATE", 
    "TIME", "MONEY", "ORDINAL", "CARDINAL", "LANGUAGE", "WORK_OF_ART"
]

for i in range(num_patterns):
    st.markdown(f"**Pattern {i+1}**")

    label_choice = st.selectbox(
        f"Select label for pattern {i+1}",
        options=common_labels + ["CUSTOM (type your own)"],
        key=f"label_dropdown_{i}"
    )

    if label_choice == "CUSTOM (type your own)":
        label = st.text_input(f"Enter custom label for pattern {i+1}", key=f"custom_label_{i}")
    else:
        label = label_choice

    phrase = st.text_input(f"Phrase to match for pattern {i+1}", key=f"phrase_{i}")

    if label and phrase:
        custom_patterns.append({"label": label.upper(), "pattern": phrase})

# Process Text
doc = None
if st.button("Process Text") and text:
    temp_nlp = spacy.load("en_core_web_sm")
    ruler = temp_nlp.add_pipe("entity_ruler", before="ner")
    if custom_patterns:
        ruler.add_patterns(custom_patterns)
    doc = temp_nlp(text)

# Display results
if doc:
    st.subheader("Recognized Entities")
    if doc.ents:
        for ent in doc.ents:
            st.markdown(f"**{ent.text}** — *{ent.label_}*")
    else:
        st.info("No entities detected.")

    st.subheader("Visualization")
    st.components.v1.html(spacy.displacy.render(doc, style="ent", page=True), height=400, scrolling=True)
