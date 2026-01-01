import streamlit as st
from modules import username_search

st.set_page_config(
    page_title="beatcodes",
    layout="wide"
)

st.markdown(
    "<h2 style='color:#4da6ff; cursor:pointer;'>beatcodes</h2>",
    unsafe_allow_html=True
)

st.markdown(
    "[guns.lol/beatcodes](https://guns.lol/beatcodes)",
    unsafe_allow_html=True
)

st.divider()

col1, col2 = st.columns([2, 1])

with col1:
    username = st.text_input("Username", placeholder="enter username")
    run = st.button("Run Username Scan")

with col2:
    st.info("Tor routing is disabled on web deployments")

st.divider()

if run:
    if not username.strip():
        st.warning("Enter a username")
    else:
        st.write("Scanning...")
        try:
            results = username_search.find_socials(username, tor=False)

            if not results:
                st.warning("No results found")
            else:
                for site, data in results.items():
                    with st.expander(f"{site} (confidence {data['weight']})"):
                        for url in sorted(set(data["urls"])):
                            st.write(url)

                st.success("Scan complete")

        except Exception as e:
            st.error(str(e))
