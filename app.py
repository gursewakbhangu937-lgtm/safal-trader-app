import streamlit as st

# Page Setup
st.set_page_config(page_title="Smart Daily Tools", page_icon="📱", layout="centered")

# Sidebar navigation
page = st.sidebar.radio("Navigation", ["📝 Reminder App", "🧮 Smart Calculator"])

if page == "📝 Reminder App":
    st.title("📝 Reminder & Task Manager")
    st.write("Yahan aap apne roz-marra ke kaam save kar sakte hain.")

    # Memory me tasks save karne ke liye session_state ka use
    if 'tasks' not in st.session_state:
        st.session_state.tasks = []

    # Naya task add karne ka input
    new_task = st.text_input("Naya kaam add karein:", placeholder="Jaise: Bijli ka bill bharna hai...")
    
    if st.button("Add Task"):
        if new_task:
            st.session_state.tasks.append(new_task)
            st.success("Kaam add ho gaya!")
            st.rerun()
        else:
            st.warning("Pehle koi kaam likhein!")

    st.markdown("---")
    st.subheader("Aapke Pending Kaam:")
    
    # Tasks ki list dikhana aur delete karne ka option
    if len(st.session_state.tasks) == 0:
        st.info("Abhi koi kaam pending nahi hai.")
    else:
        for i, task in enumerate(st.session_state.tasks):
            cols = st.columns([0.8, 0.2])
            with cols[0]:
                st.write(f"**{i+1}.** {task}")
            with cols[1]:
                if st.button("❌ Done", key=f"del_{i}"):
                    st.session_state.tasks.pop(i)
                    st.rerun()

elif page == "🧮 Smart Calculator":
    st.title("🧮 Smart Shopping Calculator")
    st.write("Mall ki shopping aur sabji mandi ke hisaab ke liye aasan tool.")

    # 2 Tabs banaye hain alag alag calculation ke liye
    tab1, tab2 = st.tabs(["👕 Mall Calculator (Discount)", "🧅 Mandi Calculator (Sabji/Ration)"])

    with tab1:
        st.subheader("Discount Check Karein")
        st.write("Agar kisi item par discount likha hai, toh final price pata karein.")
        
        orig_price = st.number_input("Item ka Original Price (₹):", min_value=0.0, value=3670.0, step=10.0)
        discount = st.number_input("Discount Kitne % hai?:", min_value=0.0, max_value=100.0, value=30.0, step=1.0)

        if st.button("Final Price Banao"):
            saved_amount = (orig_price * discount) / 100
            final_price = orig_price - saved_amount
            
            st.success(f"**Aapko Dena Hai:** ₹ {final_price:.2f}")
            st.info(f"**Aapki Bachat Hui:** ₹ {saved_amount:.2f}")

    with tab2:
        st.subheader("Sabji/Ration Quantity Check")
        st.write("Agar aapko 1 KG ka rate pata hai, toh check karein aapke paison me kitna aayega.")
        
        price_per_kg = st.number_input("1 KG ka Price (₹):", min_value=1.0, value=40.0, step=5.0)
        amount_paid = st.number_input("Aap kitne ₹ ki cheez le rahe hain?:", min_value=1.0, value=20.0, step=5.0)

        if st.button("Quantity Check Karein"):
            # 1 KG = 1000 Grams
            # Grams nikalne ka formula: (Diy Gaye Paise / 1 KG ka Rate) * 1000
            grams = (amount_paid / price_per_kg) * 1000
            
            if grams >= 1000:
                kg = grams / 1000
                st.success(f"**Aapko milega:** {kg:.2f} KG")
            else:
                st.success(f"**Aapko milega:** {grams:.0f} Grams")
