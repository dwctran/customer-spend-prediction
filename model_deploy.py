import streamlit as st
import pandas as pd
import plotly.express as px


def main():
    prediction_data = pd.read_csv("prediction.csv")
    prediction_data.head()

    st.set_page_config(
        page_title="Customer Spend Prediction", page_icon="🖖", layout="wide"
    )
    st.markdown(
        "<style> @import url('https://fonts.googleapis.com/css2?family=Inter:wght@100;200;300;400;500;600;700;800;900&display=swap'); .stMarkdown, .css-18e3th9, .css-1inwz65 .stApp, .css-fg4pbf, .streamlit-wide,.eczokvf0 { padding-top: 0.5em; padding-left: 2em; padding-right: 2em; font-family: Inter} h1, h2, h3, h6, .st-ae {font-family: Inter} .stSlider, .stDownloadButton {padding-left: 2em; font-family: Inter} .css-13sdm1b, .e16nr0p33 {font-family: Inter; padding-top: 0px} .css-1ggh3qq {gap: 0em} </style>",
        unsafe_allow_html=True,
    )
    # cola, colb = st.columns(2)
    st.title("Customer Spend Prediction")
    st.markdown(
        "###### Explore Customers by Predicted Spend versus Actual Spend during the 90-day evaluation period."
    )

    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown("### Spend Actual vs Predicted")
        st.markdown(
            "###### Segment Customers that were predicted to spend but didn't. Target these customers with appropriate marketing campaigns."
        )
        temp_options = [i for i in range(-3000, 17000, 1000)]
        temp = st.select_slider(label="", options=temp_options, value=[0, 1000])
        # st.slider(label = '', options = temp_optionvalue = [100])
        st.markdown("###### Difference between \${} & \${} ".format(temp[0], temp[1]))

        def convert_df(df):
            return df.to_csv(index=None).encode("utf-8")

        df_data = convert_df(
            prediction_data[
                (prediction_data["Actual vs Predicted Amount Difference"] > temp[0])
                & (prediction_data["Actual vs Predicted Amount Difference"] <= temp[1])
            ]
        )

        st.download_button(
            label="Download Segmentation",
            data=df_data,
            file_name="segmentation.csv",
            mime="text/csv",
        )

    with col2:
        fig = px.scatter(
            prediction_data[
                (prediction_data["Actual vs Predicted Amount Difference"] > temp[0])
                & (prediction_data["Actual vs Predicted Amount Difference"] <= temp[1])
            ],
            x="Purchase Frequency",
            y="Predicted Purchasing Probability",
            color="Actual vs Predicted Amount Difference",
            hover_name="CustomerID",
            hover_data=["Actual Amount Spent", "Predicted Amount Spent"],
            width=1000,
            height=500,
        )
        fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", font_family="Inter")
        fig.update_traces(marker={"size": 12})
        st.write(fig)

    st.markdown(
        """
        - The customers with negative ***Actual vs Predicted Amount Difference*** and high ***Predicted Purchasing Probability*** are the ones who have not spent as much as expected. Business operators should launch campaigns targeting these customers to encourage them to come back and make more purchases.
        - The customers with positive ***Actual vs Predicted Amount Difference*** and high ***Predicted Purchasing Probability*** are the ones who have already spent more than expected. However, Business operators should also pay appropriate attention to these customers to make them stay longer.
        
        """
    )


if __name__ == "__main__":
    main()
