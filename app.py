import streamlit as st
import sqlite3

# --- DATABASE SETUP ---
# Yeh function ek local database banayega taaki aapke tasks save rahein
def init_db():
    conn = sqlite3.connect('reminders.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY AUTOINCREMENT, task TEXT)''')
    conn.commit()
    conn.close()

def add_task_to_db(task):
    conn = sqlite3.connect('reminders.db')
    c = conn.cursor()
    c.execute("INSERT INTO tasks (task) VALUES (?)", (task,))
    conn.commit()
    conn.close()

def get_tasks_from_db():
    conn = sqlite3.connect('reminders.db')
    c = conn.cursor()
    c.execute("SELECT * FROM tasks")
    data = c.fetchall()
    conn.close()
    return data

def delete_task_from_db(task_id):
    conn = sqlite3.connect('reminders.db')
    c = conn.cursor()
    c.execute("DELETE FROM tasks WHERE id=?", (task_id,))
    conn.commit()
    conn.close()

# Initialize DB when app starts
init_db()

# --- PAGE SETUP ---
st.set_page_config(page_title="Smart Daily Tools", page_icon="📱", layout="centered")

# --- NAVIGATION ---
page = st.sidebar.radio("Navigation", ["📝 Reminder App (Permanent)", "🧮 Smart Calculator", "🏦 EMI & Loan Calculator"])

# ==========================================
# PAGE 1: REMINDER APP
# ==========================================
if page == "📝 Reminder App (Permanent)":
    st.title("📝 Reminder & Task Manager")
    st.write("Aapke zaroori kaam ab yahan permanently save rahenge.")

    # Naya task add karne ka input
    new_task = st.text_input("Naya kaam add karein:", placeholder="Jaise: Aaj bank jana hai...")
    
    if st.button("Add Task"):
        if new_task:
            add_task_to_db(new_task)
            st.success("Kaam save ho gaya!")
            st.rerun()
        else:
            st.warning("Pehle koi kaam likhein!")

    st.markdown("---")
    st.subheader("Aapke Pending Kaam:")
    
    # Database se tasks nikal kar dikhana
    saved_tasks = get_tasks_from_db()
    
    if len(saved_tasks) == 0:
        st.info("Badhiya! Abhi koi kaam pending nahi hai.")
    else:
        for task_id, task_text in saved_tasks:
            cols = st.columns([0.8, 0.2])
            with cols[0]:
                st.write(f"🔹 {task_text}")
            with cols[1]:
                # Unique key zaroori hai har button ke liye
                if st.button("❌ Done", key=f"del_{task_id}"):
                    delete_task_from_db(task_id)
                    st.rerun()

# ==========================================
# PAGE 2: SMART CALCULATOR
# ==========================================
elif page == "🧮 Smart Calculator":
    st.title("🧮 Smart Shopping Calculator")
    st.write("Mall ki shopping aur sabji mandi ke hisaab ke liye aasan tool.")

    tab1, tab2 = st.tabs(["👕 Mall Calculator (Discount)", "🧅 Mandi Calculator (Sabji/Ration)"])

    with tab1:
        st.subheader("Discount Check Karein")
        orig_price = st.number_input("Item ka Original Price (₹):", min_value=0.0, value=3670.0, step=10.0)
        discount = st.number_input("Discount Kitne % hai?:", min_value=0.0, max_value=100.0, value=30.0, step=1.0)

        if st.button("Final Price Banao"):
            saved_amount = (orig_price * discount) / 100
            final_price = orig_price - saved_amount
            st.success(f"**Aapko Dena Hai:** ₹ {final_price:.2f}")
            st.info(f"**Aapki Bachat Hui:** ₹ {saved_amount:.2f}")

    with tab2:
        st.subheader("Sabji/Ration Quantity Check")
        price_per_kg = st.number_input("1 KG ka Price (₹):", min_value=1.0, value=40.0, step=5.0)
        amount_paid = st.number_input("Aap kitne ₹ ki cheez le rahe hain?:", min_value=1.0, value=20.0, step=5.0)

        if st.button("Quantity Check Karein"):
            grams = (amount_paid / price_per_kg) * 1000
            if grams >= 1000:
                kg = grams / 1000
                st.success(f"**Aapko milega:** {kg:.2f} KG")
            else:
                st.success(f"**Aapko milega:** {grams:.0f} Grams")

# ==========================================
# PAGE 3: EMI CALCULATOR
# ==========================================
elif page == "🏦 EMI & Loan Calculator":
    st.title("🏦 EMI & Loan Calculator")
    st.write("Gaadi (SUV), Ghar, ya Personal loan ki EMI asani se check karein.")

    loan_amount = st.number_input("Loan ka Amount (₹):", min_value=10000, value=1500000, step=50000)
    interest_rate = st.number_input("Saalana Interest Rate (%):", min_value=1.0, value=9.5, step=0.1)
    tenure_years = st.number_input("Loan kitne saal ke liye hai?:", min_value=1, value=5, step=1)

    if st.button("EMI Calculate Karein"):
        # EMI Formula: P x R x (1+R)^N / [(1+R)^N-1]
        # P = Principal, R = Monthly Interest Rate, N = Total Months
        P = loan_amount
        R = interest_rate / 12 / 100
        N = tenure_years * 12

        emi = P * R * ((1 + R)**N) / (((1 + R)**N) - 1)
        total_payment = emi * N
        total_interest = total_payment - P

        st.markdown("---")
        st.subheader("📊 Loan Summary:")
        
        # Displaying results in columns for better look
        col1, col2, col3 = st.columns(3)
        with col1:
            st.info(f"**Har Mahine ki EMI:**\n\n₹ {int(emi):,}")
        with col2:
            st.warning(f"**Total Interest (Biaj):**\n\n₹ {int(total_interest):,}")
        with col3:
            st.success(f"**Total Paise Dene Hain:**\n\n₹ {int(total_payment):,}")
