import streamlit as st
import pandas as pd

st.title("🤖 Chatbot Response Evaluator")

uploaded_file = st.file_uploader("Upload your chatbot responses CSV", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.write("### Uploaded Responses", df.head())

    st.write("### Rate Each Response")
    ratings = []

    for index, row in df.iterrows():
        st.write(f"**{index + 1}. User Question:** {row['prompt']}")
        st.write(f"**Bot Response:** {row['response']}")

        correctness = st.slider("Correctness (0-5)", 0, 5, key=f"c{index}")
        tone = st.slider("Tone (0-5)", 0, 5, key=f"t{index}")
        helpfulness = st.slider("Helpfulness (0-5)", 0, 5, key=f"h{index}")

        ratings.append({
            "question": row['prompt'],
            "response": row['response'],
            "correctness": correctness,
            "tone": tone,
            "helpfulness": helpfulness,
            "average_score": (correctness + tone + helpfulness) / 3  # Average score calculation
        })

    # Calculate the average scores for all responses
    avg_score = sum([rating['average_score'] for rating in ratings]) / len(ratings) if ratings else 0
    st.write(f"### Average Score for All Responses: {avg_score:.2f} / 5")

    # Create the result_df to be used for both saving and downloading
    result_df = pd.DataFrame(ratings)

    # Save Ratings Button
    if st.button("Save Ratings"):
        result_df.to_csv("chatbot_ratings.csv", index=False)
        st.success("Ratings saved to chatbot_ratings.csv ✅")

    # Provide Downloadable CSV Button
    csv = result_df.to_csv(index=False).encode('utf-8')
    st.download_button("Download Ratings as CSV", csv, "chatbot_ratings.csv", "text/csv")

    # Provide Downloadable JSON Button
    json_data = result_df.to_json(orient='records', lines=True).encode('utf-8')
    st.download_button("Download Ratings as JSON", json_data, "chatbot_ratings.json", "application/json")
