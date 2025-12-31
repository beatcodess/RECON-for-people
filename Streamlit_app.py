import streamlit as st
from modules import username_search

st.set_page_config(page_title="beatcodes",layout="wide")

st.markdown(
    "<h2 style='color:#4da6ff;cursor:pointer;'>beatcodes</h2>",
    unsafe_allow_html=True
)

st.markdown("[guns.lol/beatcodes](https://guns.lol/beatcodes)")

username=st.text_input("Username")
use_tor=st.checkbox("Use Tor Routing (local only)")

if st.button("Run Username Scan"):
    if username:
        st.write("Scanning...")
        results=username_search.find_socials(username,tor=False)
        for site,data in results.items():
            st.subheader(site)
            for url in set(data["urls"]):
                st.write(url)
