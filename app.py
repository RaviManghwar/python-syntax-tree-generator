{\rtf1\ansi\ansicpg1252\cocoartf2639
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;\f1\fnil\fcharset0 AppleColorEmoji;\f2\fnil\fcharset0 LucidaGrande;
}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 import streamlit as st\
import spacy\
from graphviz import Digraph\
import subprocess\
import sys\
\
# Ensure spaCy model is installed\
@st.cache_resource\
def load_model():\
    try:\
        return spacy.load("en_core_web_sm")\
    except OSError:\
        subprocess.run(\
            [sys.executable, "-m", "spacy", "download", "en_core_web_sm"],\
            check=True\
        )\
        return spacy.load("en_core_web_sm")\
\
nlp = load_model()\
\
def build_dependency_tree(doc):\
    dot = Digraph()\
    dot.attr(rankdir="TB")\
\
    for token in doc:\
        dot.node(str(token.i), f"\{token.text\}\\n(\{token.dep_\})")\
        if token.head != token:\
            dot.edge(str(token.head.i), str(token.i), label=token.dep_)\
\
    return dot\
\
st.set_page_config(page_title="Visual Syntax Tree Generator")\
\
st.title("
\f1 \uc0\u55356 \u57139 
\f0  Visual Syntax Tree Generator")\
st.write("Enter a sentence to visualize its syntactic structure.")\
\
sentence = st.text_area(\
    "Enter a complex sentence:",\
    height=120,\
    placeholder="The curious little boy with bright eyes quickly solved the difficult puzzle."\
)\
\
if st.button("Generate Syntax Tree"):\
    if sentence.strip():\
        doc = nlp(sentence)\
        st.graphviz_chart(build_dependency_tree(doc))\
\
        st.subheader("Word Relations")\
        for token in doc:\
            st.write(\
                f"**\{token.text\}** 
\f2 \uc0\u8594 
\f0  head: *\{token.head.text\}*, relation: *\{token.dep_\}*"\
            )\
    else:\
        st.warning("Please enter a sentence.")}