import streamlit as st
import json
import google.generativeai as genai
import os

# Configure Gemini API
api_key = os.getenv("GEMINI_API_KEY")  # Read API key from environment variable
if not api_key:
    st.error("GEMINI_API_KEY environment variable is not set. Please configure it in Streamlit Cloud.")
    st.stop()
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-pro')  # Use 'gemini-flash' if available

# Risk stratification algorithm (SELECT I logic)
def risk_stratification(data):
    """
    Classify participants into low, medium, or high CVD risk based on SELECT I algorithm.
    """
    risk = "Low"
    if data.get("history_of_stroke", False) or data.get("history_of_MI", False):
        risk = "High"
    elif data.get("hypertension", False) or data.get("diabetes", False):
        risk = "Medium"
    return risk

# Generate advice based on risk level
def generate_advice(risk_level):
    """
    Provide lifestyle advice based on risk level.
    """
    if risk_level == "High":
        return "You are at high risk for cardiovascular disease. Please schedule a teleconsultation with a doctor immediately."
    elif risk_level == "Medium":
        return "You are at moderate risk. Consider lifestyle changes such as reducing salt intake, exercising regularly, and quitting smoking."
    else:
        return "You are at low risk. Maintain a healthy lifestyle with a balanced diet and regular physical activity."

# Streamlit UI
def main():
    st.title("SELECT Part II: CVD Risk Assessment Chatbot")
    st.sidebar.header("Input Options")

    # Sidebar for JSON file upload
    uploaded_file = st.sidebar.file_uploader("Upload JSON File for Testing", type=["json"])
    if uploaded_file:
        test_data = json.load(uploaded_file)
        st.sidebar.write("Uploaded JSON Data:")
        st.sidebar.json(test_data)

    # Chat interface
    st.header("Chat Interface")
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Input from user (simulating WhatsApp interaction)
    user_input = st.text_input("Type your message here (e.g., 'I have high blood pressure'):")

    if user_input:
        # Simulate WhatsApp interaction
        st.session_state.chat_history.append({"role": "user", "text": user_input})

        # Generate response using Gemini 2.0 Flash
        prompt = f"Analyze the following message for CVD risk factors: {user_input}"
        response = model.generate_content(prompt)
        st.session_state.chat_history.append({"role": "assistant", "text": response.text})

        # Perform risk stratification (mock data for demonstration)
        risk_data = {
            "history_of_stroke": "stroke" in user_input.lower(),
            "history_of_MI": "heart attack" in user_input.lower(),
            "hypertension": "blood pressure" in user_input.lower(),
            "diabetes": "diabetes" in user_input.lower(),
        }
        risk_level = risk_stratification(risk_data)
        advice = generate_advice(risk_level)

        # Display risk assessment and advice
        st.session_state.chat_history.append({"role": "assistant", "text": f"Risk Level: {risk_level}"})
        st.session_state.chat_history.append({"role": "assistant", "text": f"Advice: {advice}"})

    # Display chat history
    for message in st.session_state.chat_history:
        if message["role"] == "user":
            st.write(f"**You:** {message['text']}")
        else:
            st.write(f"**Bot:** {message['text']}")

    # Display JSON summary (if uploaded)
    if uploaded_file:
        st.header("JSON Summary")
        st.json(test_data)

# Run the app
if __name__ == "__main__":
    main()
