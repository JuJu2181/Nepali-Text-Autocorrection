# Here I will be deploying the nepali autocorrection system as a webapp using streamlit
import streamlit as st 
from nep_autocorrect import check_spell


st.title("Nepali Spelling Checker")

input_word = st.text_input("Input Word: ","नेपाब")
results = check_spell(input_word)
st.write("Suggested Words: ")
st.write(", ".join(results))
