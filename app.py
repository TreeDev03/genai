import streamlit as st
import google.generativeai as genai

import os
import time

# Page configuration
st.set_page_config(
    page_title="Digital Exodus Oracle",
    page_icon="🔮",
    layout="centered"
)

# Custom CSS for styling
st.markdown("""
<style>
    .main {
        background-color: #0E1117;
    }
    .stChatInput input {
        background-color: #262730 !important;
        color: white !important;
    }
    .chat-message {
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        display: flex;
    }
    .chat-message.user {
        background-color: #2b3137;
    }
    .chat-message.assistant {
        background-color: #51557a;
    }
</style>
""", unsafe_allow_html=True)


# Initialize Gemini
@st.cache_resource
def load_gemini():
    # You'll get this API key in next steps
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    return genai.GenerativeModel('gemini-pro')


def get_ai_response(user_input, conversation_history):
    model = load_gemini()

    system_prompt = """
    YOU ARE: The Digital Exodus Oracle
    MISSION: Help people escape the 9-5 grind and live comfortably anywhere in the world

    CORE TEACHINGS:
    1. **Location Independence** - $2,000-$5,000/month can give luxury lifestyle in many countries
    2. **Digital Escape Routes** - Remote work, online businesses, freelancing
    3. **Comfort Economics** - Maximize quality of life while minimizing costs
    4. **System Optimization** - Use legal frameworks to your advantage

    RESPONSE STYLE:
    - Practical and actionable
    - Specific numbers and locations
    - Step-by-step escape plans
    - Encouraging and empowering

    EXAMPLE RESPONSES:
    "In Thailand, $2,000/month gives you beachfront living, great food, and massages"
    "Build a digital skill in 90 days that can earn you $3k/month remotely"
    "Portugal's D7 visa lets you live there with passive income"

    Always provide concrete steps and real numbers.
    """

    # Build conversation context
    conversation_context = system_prompt + "\n\nRecent conversation:\n"
    for msg in conversation_history[-6:]:  # Last 6 messages for context
        role = "User" if msg["role"] == "user" else "Oracle"
        conversation_context += f"{role}: {msg['content']}\n"

    conversation_context += f"\nUser: {user_input}\nOracle:"

    try:
        response = model.generate_content(conversation_context)
        return response.text
    except Exception as e:
        return f"I'm experiencing high traffic. Please try again. If this continues, message us on Instagram."


# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant",
         "content": "🔮 Welcome to the Digital Exodus Oracle. I help people escape the 9-5 grind and live comfortably anywhere in the world. Where would you like to start your escape journey?"}
    ]

if "processing" not in st.session_state:
    st.session_state.processing = False

# Header
st.title("🔮 Digital Exodus Oracle")
st.markdown("### Escape the 9-5. Live Comfortably Anywhere.")
st.markdown("*Get personalized escape plans to financial freedom*")

# Sidebar with info
with st.sidebar:
    st.header("🌍 Your Escape Blueprint")
    st.markdown("""
    **What I can help with:**
    - 💰 Location-independent income ideas
    - 🏝️ Best countries for comfortable living
    - 📈 Digital skill building
    - 🎯 Step-by-step escape plans
    - 📊 Real cost breakdowns

    **Popular Starting Points:**
    - "How can I make $3k/month remotely?"
    - "Where can I live well on $2,000/month?"
    - "What digital skills pay the most?"
    - "Help me create my escape plan"
    """)

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask about your escape plan..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate AI response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("🔮 The Oracle is consulting the stars...")

        try:
            full_response = get_ai_response(prompt, st.session_state.messages)
            message_placeholder.markdown(full_response)
        except Exception as e:
            full_response = "I'm currently helping many people escape. Please try again in a moment or message us on Instagram for direct help."
            message_placeholder.markdown(full_response)

    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <p>Follow for daily escape tips on Instagram & TikTok</p>
    <p><small>Your journey to freedom starts with a single question</small></p>
</div>
""", unsafe_allow_html=True)