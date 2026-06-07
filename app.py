import streamlit as st
import requests
import pandas as pd


st.set_page_config(page_title="SAFIK HYDERABAD BIRIYANI🍗",layout = "wide")


st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url("https://static.vecteezy.com/system/resources/previews/032/940/126/large_2x/gourmet-biryani-with-saffron-rice-and-chicken-free-photo.jpg");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}

    h1, h2, h3, h4, h5, h6, p, label, div {{
        color: white !important;
        font-weight: bold;
    }}

    [data-testid="stSidebar"] {{
        background-color: rgba(0,0,0,0.7);
    }}

    </style>
    """,
    unsafe_allow_html=True
)

backend_url = st.secrets["server_url"]
st.title("SAFIK HYDERABAD BIRIYANI🍗")

page = st.sidebar.selectbox(
                              "Select Page ",
                              ["Customer Feedback","Owner Dashboard","Today's Feedback",
        "Analytics","AI Summary"]
                            )

 
# customer feedback

if page == "Customer Feedback":
    st.header("📝Give Your Feedback")

    name = st.text_input("Customer Name")
    rating = st.slider("Rating", 1,5,5)
    feedback_type = st.selectbox("Feedback Type",["Compleint","suggestion","Appreciation"])
    message = st.text_area("Write your feedback")

    if st.button("Submit Feedback"):
        if name =="" or message == "":
            st.warning("Please Enter Name and feedback")
        else:
            data = {
                      "name":name,
                      "rating":rating,
                      "feedback_type":feedback_type,
                      "message":message
                    }
            response = requests.post(f"{backend_url}/feedback",json=data)
            if response.status_code == 200:
                  st.success("Feedback Submitted Successfully")
            else:
                st.error("something went wrong")
                st.write(response.text)
elif page == "Owner Dashboard":
    st.header("📝Owner Dashboard")
    if st.button("Load feedback"):
        response = requests.get(f"{backend_url}/feedback")
        if response.status_code == 200:
            data = response.json()
            if len(data) == 0:
                st.info("No Feedback Found")
            else:
                st.dataframe(data,use_container_width=True)
        else:
             st.error("Unable to fetch feedback")
             st.write(response.text)

elif page == "Today's Feedback":

    st.header("📅 Today's Customer Feedback")

    response = requests.get(
        f"{backend_url}/feedback/today"
    )

    if response.status_code == 200:

        data = response.json()

        if len(data) == 0:
            st.info("No Feedback Available Today")

        else:
            df = pd.DataFrame(data)

            st.dataframe(
                df,
                use_container_width=True
            )

    else:
        st.error("Unable to fetch today's feedback")
        st.write(response.text)
elif page == "Analytics":

    st.header("📈 Feedback Analytics")

    response = requests.get(
        f"{backend_url}/feedback/analyze"
    )

    if response.status_code == 200:

        data = response.json()

        if len(data) == 0:
            st.info("No Analytics Available")

        else:
            df = pd.DataFrame(data)

            st.dataframe(
                df,
                use_container_width=True
            )

    else:
        st.error("Unable to load analytics")
        st.write(response.text)
elif page == "AI Summary":

    st.header("🤖 AI Daily Restaurant Report")

    if st.button("Generate AI Summary"):

        with st.spinner("Analyzing today's feedback..."):

            response = requests.get(
                f"{backend_url}/feedback/ai-summary"
            )

            if response.status_code == 200:

                result = response.json()

                st.success("AI Analysis Completed ✅")

                st.markdown(result["summary"])

            else:
                st.error("Unable to generate AI summary")
                st.write(response.text)
