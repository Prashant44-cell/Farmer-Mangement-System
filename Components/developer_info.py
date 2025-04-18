import streamlit as st

def display():
    st.header("Developer Info")
    st.markdown("**Developer:** Prashant Gupta")
    st.markdown("[LinkedIn](https://www.linkedin.com/in/PrashantGupta)")

    with st.form("feedback_form"):
        feedback = st.text_area("Your Feedback")
        submitted = st.form_submit_button("Submit")
        if submitted:
            st.success("Thanks for your feedback!")
