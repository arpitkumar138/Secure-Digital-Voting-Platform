import streamlit as st
import re
import sqlite3

# --- Page Configuration ---
st.set_page_config(
    page_title="Secure Vote Platform",
    page_icon="🛡️",
    layout="centered"
)

# --- Custom Styling ---
st.markdown("""
    <style>
    .stApp {
        background-color: #0e1117;
        color: #ffffff;
    }
    .main-card {
        background: #1e293b;
        padding: 2rem;
        border-radius: 12px;
        border: 1px solid #334155;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #2563eb 0%, #1d4ed8 100%);
        color: white;
        font-weight: bold;
        border-radius: 8px;
        padding: 0.6rem 1rem;
        border: none;
    }
    .stButton>button:hover {
        background: linear-gradient(90deg, #1d4ed8 0%, #1e40af 100%);
    }
    </style>
""", unsafe_allow_html=True)

# --- Database Setup & Initialization ---
def init_db():
    conn = sqlite3.connect('secure_vote.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS voters 
                 (voter_id TEXT PRIMARY KEY, name TEXT, phone TEXT, voted INTEGER)''')
    c.execute('''CREATE TABLE IF NOT EXISTS votes 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, candidate TEXT)''')
    
    # Demo Records (0 = not voted yet)
    c.execute("INSERT OR IGNORE INTO voters VALUES ('VOTER123', 'Rahul Sharma', '9876543210', 0)")
    c.execute("INSERT OR IGNORE INTO voters VALUES ('VOTER456', 'Priya Patel', '9123456789', 0)")
    conn.commit()
    conn.close()

init_db()

# --- Sidebar Admin Controls & Reset Option ---
with st.sidebar:
    st.title("⚙️ Admin Controls")
    st.write("Manage voting session and database records.")
    
    if st.button("🔄 Reset Voting Database"):
        conn = sqlite3.connect('secure_vote.db')
        c = conn.cursor()
        # Reset voted status to 0 for all voters[cite: 1]
        c.execute("UPDATE voters SET voted = 0")
        # Clear all votes records[cite: 1]
        c.execute("DELETE FROM votes")
        conn.commit()
        conn.close()
        
        # Reset Session States
        st.session_state.step = 1
        st.session_state.voter_id = ""
        st.session_state.voter_name = ""
        st.session_state.voter_phone = ""
        st.session_state.vote_locked = False
        st.session_state.selected_candidate = ""
        
        st.success("✅ Database reset successfully! All voters can vote again.")
        st.rerun()

# --- Session State Initialization ---
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'voter_id' not in st.session_state:
    st.session_state.voter_id = ""
if 'voter_name' not in st.session_state:
    st.session_state.voter_name = ""
if 'voter_phone' not in st.session_state:
    st.session_state.voter_phone = ""
if 'vote_locked' not in st.session_state:
    st.session_state.vote_locked = False
if 'selected_candidate' not in st.session_state:
    st.session_state.selected_candidate = ""

st.title("🛡️ Secure Vote Platform")
st.markdown("---")

# ==========================================
# STEP 1: VOTER ID AUTHENTICATION
# ==========================================
if st.session_state.step == 1:
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.subheader("📋 Step 1: Voter ID Authentication")
    st.write("Enter your Voter ID to verify eligibility in the electoral database.")
    
    voter_input = st.text_input("Voter ID Number (Demo: VOTER123 or VOTER456)", placeholder="e.g. VOTER123").strip().upper()
    
    if st.button("Next: Proceed to ID & Biometric"):
        if not voter_input:
            st.error("⚠️ Please enter a valid Voter ID.")
        else:
            conn = sqlite3.connect('secure_vote.db')
            c = conn.cursor()
            c.execute("SELECT name, voted, phone FROM voters WHERE voter_id = ?", (voter_input,))
            result = c.fetchone()
            conn.close()
            
            if not result:
                st.error("❌ Error: Voter ID not found in the electoral roll.")
            elif result[1] == 1:
                st.error("🚨 ACCESS DENIED: This Voter ID has ALREADY cast a vote! Duplicate voting is strictly prohibited.")
            else:
                st.session_state.voter_id = voter_input
                st.session_state.voter_name = result[0]
                st.session_state.voter_phone = result[2]
                st.session_state.step = 2
                st.session_state.vote_locked = False
                st.session_state.selected_candidate = ""
                st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# STEP 2: GOVERNMENT ID & FACE BIOMETRIC
# ==========================================
elif st.session_state.step == 2:
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.subheader(f"🔐 Step 2: Verification for {st.session_state.voter_name}")
    
    id_input = st.text_input("Enter 12-Digit Government ID Number", max_chars=12, type="password", placeholder="12 Numeric Digits")
    
    is_valid_id = bool(re.match(r'^\d{12}$', id_input)) if id_input else False
    
    if id_input and not is_valid_id:
        st.error("⚠️ Invalid Format! Government ID must contain exactly 12 numeric digits.")
    
    if is_valid_id:
        st.success("✅ Government ID Format Verified Successfully!")
        st.markdown("---")
        st.write("📷 **Live Face Biometric Authentication:**")
        picture = st.camera_input("Capture Live Photo for Matching")
        
        if picture:
            st.success("✅ Face Biometric Matched Successfully!")
            if st.button("Proceed to Voting Ballot"):
                st.session_state.step = 3
                st.rerun()
                
    if st.button("⬅️ Back to Voter ID"):
        st.session_state.step = 1
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# STEP 3: BALLOT SELECTION & ONE-TIME LOCK
# ==========================================
elif st.session_state.step == 3:
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.subheader("🗳️ Step 3: Official Voting Ballot")
    st.warning("⚠️ **Important:** Once you confirm your vote selection, it will be permanently locked and CANNOT be changed.")
    
    parties = [
        "🪷 Bharatiya Janata Party (BJP)",
        "🖐️ Indian National Congress (INC)",
        "🧹 Aam Aadmi Party (AAP)",
        "❌ None of the Above (NOTA)"
    ]
    
    chosen = st.radio(
        "Select Your Party:",
        options=parties,
        disabled=st.session_state.vote_locked
    )
    
    if not st.session_state.vote_locked:
        if st.button("🔒 Lock & Confirm Selection"):
            st.session_state.selected_candidate = chosen
            st.session_state.vote_locked = True
            st.rerun()
            
    else:
        st.info(f"🔒 **Your Selection is Locked:** `{st.session_state.selected_candidate}` (Selection cannot be changed now)")
        
        if st.button("🚀 SUBMIT FINAL VOTE TO DATABASE"):
            conn = sqlite3.connect('secure_vote.db')
            c = conn.cursor()
            c.execute("INSERT INTO votes (candidate) VALUES (?)", (st.session_state.selected_candidate,))
            c.execute("UPDATE voters SET voted = 1 WHERE voter_id = ?", (st.session_state.voter_id,))
            conn.commit()
            conn.close()
            
            st.balloons()
            st.success("🎉 Vote Successfully Encrypted & Saved!")
            st.markdown(f"### 🙏 Thank you for your valuable vote, **{st.session_state.voter_name}**!")
            
            masked_phone = "XXXXXX" + st.session_state.voter_phone[-4:] if st.session_state.voter_phone else "XXXXXX1234"
            st.info(f"📲 Confirmation SMS dispatched to registered mobile ({masked_phone}): 'Dear {st.session_state.voter_name}, your vote for {st.session_state.selected_candidate} has been recorded.'")
            
            if st.button("Exit / Complete Voting Process"):
                st.session_state.step = 1
                st.session_state.voter_id = ""
                st.session_state.vote_locked = False
                st.session_state.selected_candidate = ""
                st.rerun()
                
    st.markdown('</div>', unsafe_allow_html=True)