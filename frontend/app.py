import streamlit as st
import requests

st.title("Google Drive AI Agent")

user_input = st.text_input("Ask something")

if st.button("Search"):

    response = requests.post(
        "http://127.0.0.1:8000/chat",
        json={"message": user_input}
    )

    data = response.json()

    results = data.get("results", [])

    if results:

        st.subheader("Results")

        for file in results:

            st.write(f"📄 {file['name']}")

            if "webViewLink" in file:
                st.markdown(
                    f"[Open File]({file['webViewLink']})"
                )

    else:
        st.write("No files found")