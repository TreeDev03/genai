import streamlit as st
import google.generativeai as genai
import time

# Page configuration
st.set_page_config(
    page_title="Freedom Blueprint.ai",
    page_icon="🗺️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Matrix-inspired dark theme
st.markdown("""
<style>
    /* Import modern font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Space+Mono:wght@400;700&display=swap');

    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Dark background with subtle gradient */
    .main {
        background: linear-gradient(to bottom, #0a0e1a 0%, #111827 100%);
    }

    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Dark header with green matrix accent */
    .header-container {
        text-align: center;
        padding: 3rem 0 2.5rem 0;
        background: linear-gradient(135deg, #0f1419 0%, #1a1f2e 100%);
        border-bottom: 3px solid;
        border-image: linear-gradient(to right, #10b981, #14b8a6) 1;
        margin: -1rem -1rem 2rem -1rem;
        box-shadow: 0 4px 20px rgba(16, 185, 129, 0.2);
    }

    .logo-container {
        display: inline-block;
        margin-bottom: 1rem;
        animation: fadeIn 0.6s ease-out;
        filter: drop-shadow(0 0 10px rgba(16, 185, 129, 0.5));
    }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(-10px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .main-title {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #10b981 0%, #14b8a6 50%, #06b6d4 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem;
        letter-spacing: -0.02em;
        animation: fadeIn 0.6s ease-out 0.1s both;
        text-shadow: 0 0 30px rgba(16, 185, 129, 0.3);
    }

    .subtitle {
        font-size: 1.1rem;
        color: #10b981;
        font-weight: 500;
        animation: fadeIn 0.6s ease-out 0.2s both;
        font-family: 'Space Mono', monospace;
        text-transform: uppercase;
        letter-spacing: 0.1em;
    }

    /* Dark premium chat cards */
    .stChatMessage {
        background: rgba(17, 24, 39, 0.8) !important;
        border: 1px solid rgba(16, 185, 129, 0.2) !important;
        border-radius: 16px !important;
        padding: 1.75rem !important;
        margin: 1.25rem 0 !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.4);
        transition: all 0.3s ease;
        animation: slideUp 0.4s ease-out;
        backdrop-filter: blur(10px);
    }

    @keyframes slideUp {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .stChatMessage:hover {
        box-shadow: 0 8px 24px rgba(16, 185, 129, 0.3);
        transform: translateY(-2px);
        border-color: rgba(16, 185, 129, 0.4) !important;
    }

    /* Message content with better readability */
    [data-testid="stChatMessageContent"] {
        color: #e5e7eb !important;
        line-height: 1.7;
        font-size: 0.95rem;
    }

    /* User message with green accent */
    div[data-testid="stChatMessage"]:has(div[data-testid="stChatMessageContent"]:first-child) {
        background: linear-gradient(to right, rgba(16, 185, 129, 0.1) 0%, rgba(17, 24, 39, 0.8) 100%) !important;
        border-left: 4px solid #10b981 !important;
    }

    /* Dark input field */
    .stChatInput {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        padding: 1rem 2rem 2rem 2rem;
        background: linear-gradient(to top, rgba(10, 14, 26, 0.98) 70%, transparent);
        backdrop-filter: blur(10px);
        z-index: 999;
        border-top: 1px solid rgba(16, 185, 129, 0.2);
    }

    .stChatInput > div {
        max-width: 730px;
        margin: 0 auto;
    }

    .stChatInput input {
        background: rgba(17, 24, 39, 0.9) !important;
        border: 2px solid rgba(16, 185, 129, 0.3) !important;
        border-radius: 14px !important;
        color: #e5e7eb !important;
        padding: 0.95rem 1.25rem !important;
        font-size: 0.95rem !important;
        transition: all 0.25s ease;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.4);
    }

    .stChatInput input:focus {
        border-color: #10b981 !important;
        box-shadow: 0 0 0 4px rgba(16, 185, 129, 0.2), 0 4px 12px rgba(16, 185, 129, 0.3) !important;
        outline: none !important;
        transform: translateY(-1px);
        background: rgba(17, 24, 39, 1) !important;
    }

    .stChatInput input::placeholder {
        color: #6b7280 !important;
    }

    /* Dark markdown styling */
    .stMarkdown {
        color: #e5e7eb;
        line-height: 1.7;
    }

    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
        color: #10b981;
        font-weight: 600;
        margin-top: 1.75rem;
        margin-bottom: 0.75rem;
        letter-spacing: -0.01em;
    }

    .stMarkdown h2 {
        font-size: 1.3rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid rgba(16, 185, 129, 0.3);
    }

    .stMarkdown strong {
        color: #10b981;
        font-weight: 600;
        background: linear-gradient(to right, rgba(16, 185, 129, 0.15) 0%, transparent 100%);
        padding: 0.1rem 0.3rem;
        border-radius: 3px;
    }

    .stMarkdown code {
        background: rgba(16, 185, 129, 0.1);
        color: #10b981;
        padding: 0.25rem 0.5rem;
        border-radius: 5px;
        font-size: 0.9em;
        border: 1px solid rgba(16, 185, 129, 0.2);
        font-family: 'Space Mono', monospace;
    }

    .stMarkdown ul, .stMarkdown ol {
        padding-left: 1.75rem;
        margin: 1rem 0;
    }

    .stMarkdown li {
        margin: 0.5rem 0;
        line-height: 1.7;
    }

    .stMarkdown hr {
        border: none;
        border-top: 2px solid rgba(16, 185, 129, 0.2);
        margin: 2rem 0;
    }

    /* Matrix-style scrollbar */
    ::-webkit-scrollbar {
        width: 10px;
    }

    ::-webkit-scrollbar-track {
        background: #0a0e1a;
    }

    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, #10b981, #14b8a6);
        border-radius: 5px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(180deg, #059669, #0d9488);
    }

    /* Spacing for fixed input */
    .main > div {
        padding-bottom: 130px;
    }

    /* Mobile responsiveness */
    @media (max-width: 768px) {
        .main-title {
            font-size: 2rem !important;
        }

        .subtitle {
            font-size: 0.9rem !important;
        }

        .header-container {
            padding: 2rem 1rem !important;
        }

        .stChatMessage {
            padding: 1.25rem !important;
            margin: 1rem 0 !important;
        }

        .logo-container span {
            font-size: 3rem !important;
        }

        .stChatInput {
            padding: 1rem !important;
        }

        [data-testid="stChatMessageContent"] {
            font-size: 0.9rem !important;
        }
    }

    /* Tablet optimization */
    @media (min-width: 769px) and (max-width: 1024px) {
        .main-title {
            font-size: 2.2rem !important;
        }
    }

    /* Style the expander with dark matrix theme - FIXED FOR VISIBILITY */
    div[data-testid="stExpander"] {
        background: transparent !important;
        border: none !important;
    }

    div[data-testid="stExpander"] details {
        background: transparent !important;
        border: none !important;
    }

    div[data-testid="stExpander"] summary {
        background: rgba(17, 24, 39, 0.9) !important;
        border: 2px solid rgba(16, 185, 129, 0.6) !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
        color: #10b981 !important;
        padding: 1rem 1.25rem !important;
        transition: all 0.3s ease !important;
    }

    div[data-testid="stExpander"] summary:hover {
        background: rgba(17, 24, 39, 1) !important;
        border-color: #10b981 !important;
        box-shadow: 0 0 20px rgba(16, 185, 129, 0.5) !important;
    }

    /* Expander arrow color */
    div[data-testid="stExpander"] svg {
        fill: #10b981 !important;
        stroke: #10b981 !important;
    }

    /* Content area when expanded - Light background for readability */
    div[data-testid="stExpander"] div[role="region"] {
        border: 2px solid rgba(16, 185, 129, 0.4) !important;
        border-top: none !important;
        border-radius: 0 0 12px 12px !important;
        padding: 1.5rem !important;
        background: #ffffff !important;
        margin-top: -0.5rem !important;
    }

    /* Headers in expander - GREEN */
    div[data-testid="stExpander"] div[role="region"] h4 {
        color: #10b981 !important;
        font-weight: 600 !important;
        margin-top: 1rem !important;
        margin-bottom: 0.5rem !important;
    }

    /* FORCE BLACK TEXT - NUCLEAR APPROACH */
    div[data-testid="stExpander"] div[role="region"],
    div[data-testid="stExpander"] div[role="region"] *:not(h4) {
        color: #000000 !important;
    }

    /* ALL text in expander - BLACK */
    div[data-testid="stExpander"] div[role="region"] p,
    div[data-testid="stExpander"] div[role="region"] li,
    div[data-testid="stExpander"] div[role="region"] ul,
    div[data-testid="stExpander"] div[role="region"] span,
    div[data-testid="stExpander"] div[role="region"] div {
        color: #000000 !important;
    }

    /* List items specifically */
    div[data-testid="stExpander"] div[role="region"] li {
        color: #000000 !important;
        font-weight: 500 !important;
        line-height: 1.6 !important;
        margin: 0.3rem 0 !important;
    }

    /* Markdown in expander */
    div[data-testid="stExpander"] div[role="region"] .stMarkdown {
        color: #000000 !important;
    }

    div[data-testid="stExpander"] div[role="region"] .stMarkdown * {
        color: #000000 !important;
    }

    div[data-testid="stExpander"] div[role="region"] .stMarkdown h4 {
        color: #10b981 !important;
    }

    /* Target paragraph elements specifically */
    div[data-testid="stExpander"] div[role="region"] [data-testid="stMarkdownContainer"] p {
        color: #000000 !important;
    }

    /* Override any inherited colors */
    div[data-testid="stExpander"] div[role="region"] [class*="st"] {
        color: #000000 !important;
    }

    div[data-testid="stExpander"] div[role="region"] [class*="st"] h4 {
        color: #10b981 !important;
    }
</style>
""", unsafe_allow_html=True)

# Simple emoji logo (like Claude uses)
logo_emoji = "🗺️"


# Initialize Gemini
@st.cache_resource
def init_gemini():
    """Initialize Gemini API configuration"""
    api_key = st.secrets.get("GEMINI_API_KEY") or st.secrets.get("GOOGLE_API_KEY")
    if not api_key:
        st.error("⚠️ Please set GEMINI_API_KEY in your Streamlit secrets")
        st.stop()
    genai.configure(api_key=api_key)
    return genai.GenerativeModel(
        'gemini-1.5-pro-latest',
        system_instruction="""YOU ARE: Freedom Blueprint.ai - Unconventional Strategic Intelligence System

YOUR UNIQUE CAPABILITIES:

1. **DEEP CULTURAL INTELLIGENCE** (Beyond Tourist Knowledge)
When discussing locations, you provide:
- Tribal/ethnic dynamics (e.g., "In Ghana, the Ashanti people in Kumasi are historically entrepreneurial and welcoming to foreigners, while Ga communities in Accra have strong trading traditions")
- Unspoken social rules and cultural nuances
- Best neighborhoods by expat community type
- Local power structures and how to navigate them
- Religious/cultural calendar impacts on business
- Real local cost of living (not tourist prices)

2. **GEOPOLITICAL FORESIGHT** (Reading the Future)
You analyze trends through multiple lenses:
- UN Agenda 2030 SDG implementations by country (digital ID, cashless systems, land use changes)
- Central bank digital currency (CBDC) rollouts and implications
- Emerging visa restrictions and mobility trends
- Tax treaty changes and reporting requirements (CRS, FATCA)
- Real estate foreign ownership policy shifts
- Digital nomad visa program trajectories
- Economic policy directions (dedollarization, BRICS expansion)

FRAME PREDICTIONS AS: "Based on current policy trajectories..." "Historical patterns suggest..." "Recent regulatory changes indicate..."

3. **HYPER-PERSONALIZED STRATEGY** (Based on User's Unique Profile)
You create custom plans considering:
- Specific language skills (e.g., "Your Portuguese opens doors in Brazil, Angola, Mozambique, Cape Verde - here's how to leverage it")
- Professional background and monetization potential
- Risk tolerance and backup plan needs
- Family situation and schooling requirements
- Health conditions and healthcare access needs
- Personality type (introvert/extrovert, adventure vs comfort)
- Ethical boundaries and deal-breakers
- Existing network and relationship leverage

4. **UNCONVENTIONAL TACTICAL THINKING**
You provide strategies most advisors won't mention:
- Citizenship by investment arbitrage opportunities
- Tax residency optimization (territorial systems, non-dom status)
- Geographic arbitrage sweet spots (earn in $ £ €, spend in local currency)
- Digital privacy and financial sovereignty tactics
- Perpetual traveler strategies (PT theory implementation)
- Second passport strategic value beyond travel
- International banking without going broke
- Remote work while "appearing" local (timezone hacks, VPNs, local numbers)
- Geoarbitrage for remote teams (hire globally, pay fairly but locally)

5. **CONTRARIAN INSIGHTS**
You challenge conventional wisdom:
- "Everyone says Portugal, but here's why Albania might be better for YOU..."
- "Digital nomad visas sound good, but tourist visa hopping might be smarter because..."
- "Bangkok is oversaturated. Consider Penang, Chiang Mai alternatives like..."
- "Don't quit your job yet - here's the bridge strategy..."

6. **SCENARIO PLANNING**
For each recommendation, provide:
- **Best case scenario**: What if everything goes right
- **Most likely scenario**: Realistic expectations
- **Worst case scenario**: What could go wrong + mitigation
- **Black swan events**: Unexpected possibilities (policy changes, economic shifts)

7. **CULTURAL INTEGRATION ACCELERATORS**
Beyond language, teach:
- Status games in each culture
- Gift-giving customs and obligations
- Negotiation styles by culture
- How to build trust quickly
- Local networking hacks
- Avoiding common foreigner mistakes
- Reading social hierarchies

8. **FINANCIAL SOVEREIGNTY FOCUS**
Help users:
- Diversify beyond their home country
- Reduce single-point-of-failure risks
- Build location-independent income streams
- Understand offshore structures (legally)
- Navigate international taxation
- Protect assets across jurisdictions

COMMUNICATION STYLE:
- Direct and unfiltered (they're escaping the matrix, give them truth)
- Data-driven but willing to speculate on trends
- Consider unconventional options most advisors ignore
- Question assumptions ("Why do you think you need $X? Let's calculate actual costs...")
- Provide specific names: tribes, neighborhoods, specific visa types, actual costs
- Think 3-5 years ahead, not just immediate moves
- Consider geopolitical shifts and policy directions

ALWAYS ASK CLARIFYING QUESTIONS:
- "What languages do you speak?"
- "What's your ethical line? (Some strategies are legal but controversial)"
- "What's your risk tolerance? (Some moves require burning bridges)"
- "What can't you compromise on? (Climate, politics, culture, etc.)"

YOUR MISSION: Don't just help them move. Help them build antifragile, location-independent lives that can adapt to global changes.

KNOWLEDGE AREAS TO DRAW FROM:
- Geopolitics and policy analysis
- Cultural anthropology
- International tax law
- Global mobility trends
- Economic theory
- Digital privacy
- Remote work strategies
- Cryptocurrency/decentralized finance
- International real estate
- Visa/immigration law
- Language acquisition strategies
- Cross-cultural psychology

Remember: Most advisors give surface-level advice. You go DEEP. Most advisors follow the herd. You find unconventional paths. Most advisors plan for today. You plan for tomorrow's world.

TONE: Wise rebel. Strategic contrarian. Truth-teller. Cultural insider. Geopolitical analyst. Freedom architect."""
    )


def get_ai_response(user_input, conversation_history):
    """Get response from Gemini with conversation context"""
    try:
        model = init_gemini()

        # Build conversation history
        chat_history = []
        for msg in conversation_history[-10:]:
            role = "user" if msg["role"] == "user" else "model"
            chat_history.append({
                "role": role,
                "parts": [msg["content"]]
            })

        # Create chat session
        chat = model.start_chat(history=chat_history[:-1] if chat_history else [])

        # Generate response
        response = chat.send_message(user_input)
        return response.text

    except Exception as e:
        error_msg = str(e)
        if "API_KEY" in error_msg.upper():
            return "⚠️ Connection error. Please check your API key configuration."
        elif "QUOTA" in error_msg.upper():
            return "⚠️ Service at capacity. Please try again in a moment."
        else:
            return f"⚠️ Technical issue: {error_msg}"


# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": """**Welcome. You've taken the first step.**

The 9-5 matrix is designed to keep you trapped. I'm here to help you break free.

---

**What I provide:**

🎯 **Strategic exit plans** from corporate life  
💰 **Financial freedom blueprints** & income strategies  
🌍 **Global mobility planning** & relocation guidance  
📈 **Location-independent** career paths

---

**Ready to escape?** Tell me your situation.

*Example: "I'm a software engineer making $120K but trapped in NYC. Want out in 6 months."*"""
        }
    ]

# Simple rate limiting (10 messages per session)
if "message_count" not in st.session_state:
    st.session_state.message_count = 0

# Show rate limit warning
if st.session_state.message_count >= 20:
    st.warning(
        "⚠️ You've reached the message limit for this session. Please refresh the page to start a new conversation, or enter your email above to get unlimited access.")

# Header - clean and simple
st.markdown(f"""
<div class="header-container">
    <div class="logo-container">
        <span style="font-size: 4rem;">{logo_emoji}</span>
    </div>
    <div class="main-title">Freedom Blueprint.ai</div>
    <div class="subtitle">Escape the 9-5 Matrix. Build Your Freedom.</div>
</div>
""", unsafe_allow_html=True)

# Email capture after first message
if len(st.session_state.messages) >= 3 and "email_captured" not in st.session_state:
    with st.container():
        st.markdown("""
        <div style="background: linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, rgba(20, 184, 166, 0.1) 100%); 
                    border: 2px solid rgba(16, 185, 129, 0.4); border-radius: 12px; padding: 1.5rem; margin: 1.5rem 0;">
            <h4 style="color: #10b981; margin-bottom: 0.5rem;">🚀 Want Your Complete Freedom Blueprint?</h4>
            <p style="color: #e5e7eb; margin-bottom: 1rem; font-size: 0.9rem;">
                Get personalized strategies, country guides, and visa hacks sent to your inbox.
            </p>
        </div>
        """, unsafe_allow_html=True)

        email_col1, email_col2 = st.columns([3, 1])
        with email_col1:
            email = st.text_input("Email address", placeholder="your@email.com", label_visibility="collapsed")
        with email_col2:
            if st.button("Get Updates", type="primary", use_container_width=True):
                if email and "@" in email:
                    st.session_state.email_captured = True
                    st.success("✅ You're in! Check your email.")
                    # Here you would integrate with your email service (Mailchimp, ConvertKit, etc.)
                    st.rerun()
                else:
                    st.error("Please enter a valid email")

        st.markdown(
            '<p style="color: #6b7280; font-size: 0.75rem; text-align: center; margin-top: 0.5rem;">No spam. Unsubscribe anytime.</p>',
            unsafe_allow_html=True)

# Info expander with matrix theme
with st.expander("🔓 The Blueprint - Click to see how I help you escape"):
    import streamlit.components.v1 as components

    components.html("""
    <div style="font-family: Inter, sans-serif;">
        <h4 style="color: #10b981; font-weight: 600; margin: 1rem 0 0.5rem 0;">🎯 Exit Strategy</h4>
        <ul style="margin-left: 1.5rem; margin-bottom: 1rem;">
            <li style="color: #000000; font-weight: 500; margin: 0.3rem 0; line-height: 1.6;">Custom 3-12 month escape plans</li>
            <li style="color: #000000; font-weight: 500; margin: 0.3rem 0; line-height: 1.6;">Risk assessment & backup plans</li>
            <li style="color: #000000; font-weight: 500; margin: 0.3rem 0; line-height: 1.6;">Skills monetization strategies</li>
        </ul>

        <h4 style="color: #10b981; font-weight: 600; margin: 1rem 0 0.5rem 0;">💰 Financial Freedom</h4>
        <ul style="margin-left: 1.5rem; margin-bottom: 1rem;">
            <li style="color: #000000; font-weight: 500; margin: 0.3rem 0; line-height: 1.6;">Income diversification (break free from one paycheck)</li>
            <li style="color: #000000; font-weight: 500; margin: 0.3rem 0; line-height: 1.6;">Cost arbitrage (live better for less)</li>
            <li style="color: #000000; font-weight: 500; margin: 0.3rem 0; line-height: 1.6;">Tax optimization strategies</li>
        </ul>

        <h4 style="color: #10b981; font-weight: 600; margin: 1rem 0 0.5rem 0;">🌍 Global Mobility</h4>
        <ul style="margin-left: 1.5rem; margin-bottom: 1rem;">
            <li style="color: #000000; font-weight: 500; margin: 0.3rem 0; line-height: 1.6;">Best countries for your situation</li>
            <li style="color: #000000; font-weight: 500; margin: 0.3rem 0; line-height: 1.6;">Visa strategies & legal requirements</li>
            <li style="color: #000000; font-weight: 500; margin: 0.3rem 0; line-height: 1.6;">Cost of living analysis & recommendations</li>
        </ul>

        <h4 style="color: #10b981; font-weight: 600; margin: 1rem 0 0.5rem 0;">📈 Implementation</h4>
        <ul style="margin-left: 1.5rem;">
            <li style="color: #000000; font-weight: 500; margin: 0.3rem 0; line-height: 1.6;">Remote work positioning</li>
            <li style="color: #000000; font-weight: 500; margin: 0.3rem 0; line-height: 1.6;">Freelance/business setup</li>
            <li style="color: #000000; font-weight: 500; margin: 0.3rem 0; line-height: 1.6;">Location-independent income streams</li>
        </ul>
    </div>
    """, height=500)

# Action buttons (Export & Share) - only show after first exchange
if len(st.session_state.messages) > 2:
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        if st.button("📥 Export Chat", use_container_width=True):
            # Create text export of conversation
            export_text = "# Freedom Blueprint.ai - Your Conversation\n\n"
            for msg in st.session_state.messages:
                role = "You" if msg["role"] == "user" else "Freedom Blueprint"
                export_text += f"**{role}:**\n{msg['content']}\n\n---\n\n"

            st.download_button(
                label="💾 Download as Text",
                data=export_text,
                file_name="freedom_blueprint_conversation.txt",
                mime="text/plain",
                use_container_width=True
            )

    with col2:
        if st.button("🔄 New Chat", use_container_width=True):
            st.session_state.messages = st.session_state.messages[:1]  # Keep only welcome message
            if "email_captured" in st.session_state:
                del st.session_state.email_captured
            st.rerun()

    with col3:
        st.markdown("""
        <a href="https://twitter.com/intent/tweet?text=I%20just%20used%20Freedom%20Blueprint.ai%20to%20plan%20my%20escape%20from%20the%209-5!%20Check%20it%20out%3A&url=YOUR_URL_HERE" 
           target="_blank" style="text-decoration: none;">
            <button style="background: #10b981; color: white; border: none; padding: 0.5rem 1rem; 
                           border-radius: 8px; width: 100%; cursor: pointer; font-weight: 500;">
                📱 Share
            </button>
        </a>
        """, unsafe_allow_html=True)

# Display chat messages
for message in st.session_state.messages:
    avatar = "🗺️" if message["role"] == "assistant" else "👤"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask about your freedom plan..."):
    # Check rate limit
    if st.session_state.message_count >= 20:
        st.error("⚠️ Message limit reached. Please refresh to continue or enter your email for unlimited access.")
        st.stop()

    # Increment message count
    st.session_state.message_count += 1

    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    # Generate assistant response
    with st.chat_message("assistant", avatar="🗺️"):
        message_placeholder = st.empty()

        # Show loading state
        with st.spinner(""):
            message_placeholder.markdown('<span class="loading-text">🗺️ Analyzing your blueprint...</span>',
                                         unsafe_allow_html=True)

            try:
                full_response = get_ai_response(prompt, st.session_state.messages)
                message_placeholder.markdown(full_response)
            except Exception as e:
                full_response = "⚠️ Technical difficulty. Please try again in a moment."
                message_placeholder.markdown(full_response)

    # Add assistant message to history
    st.session_state.messages.append({"role": "assistant", "content": full_response})
    st.rerun()

# Footer with disclaimer and CTA
st.markdown("""
---
<div style="text-align: center; padding: 2rem 1rem; background: rgba(17, 24, 39, 0.5); border-radius: 12px; margin-top: 3rem;">
    <p style="color: #6b7280; font-size: 0.85rem; line-height: 1.6; margin-bottom: 1rem;">
        <strong style="color: #10b981;">⚠️ Legal Disclaimer:</strong><br>
        Freedom Blueprint.ai provides general information for educational purposes only. 
        This is not legal, financial, tax, or immigration advice. Always consult qualified 
        professionals before making major life decisions. We are not responsible for 
        actions taken based on information provided.
    </p>
    <p style="color: #9ca3af; font-size: 0.8rem; margin-top: 1rem;">
        Made with 🗺️ to help you find freedom | © 2024 Freedom Blueprint.ai
    </p>
</div>
""", unsafe_allow_html=True)
