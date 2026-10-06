import streamlit as st
from pathlib import Path
from PIL import Image
from database import init_db, add_item, get_items, mark_worn, delete_item
from ai_model import classify_image

st.set_page_config(page_title="ReWear AI", page_icon="♻️", layout="wide")

init_db()

# ---------- Styling ----------
st.markdown("""
<style>

.stApp {
    background-color: #F7F4EC;
    color: #252822;
}

[data-testid="stHeader"] {
    background-color: transparent;
}

.block-container {
    max-width: 1180px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

/* Main hero */
.hero {
    padding: 42px 46px;
    border-radius: 26px;
    margin-bottom: 28px;
    background: linear-gradient(
        135deg,
        #E8EEE2 0%,
        #F8F3E8 55%,
        #ECE6D7 100%
    );
    border: 1px solid #D9DFD1;
    box-shadow: 0 10px 35px rgba(63,81,57,0.08);
}

.hero h1 {
    color: #26351f !important;
    font-size: 3rem;
    font-weight: 800;
    margin: 0 0 8px 0;
    letter-spacing: -1.5px;
    display: block !important;
}

.hero p {
    color: #596054;
}

/* Dashboard cards */
.metric-card {
    padding: 20px 14px;
    border-radius: 18px;
    background: #FFFDF8;
    border: 1px solid #E4E0D5;
    text-align: center;
    box-shadow: 0 5px 20px rgba(37,40,34,0.04);
}

.metric-card h2 {
    color: #3F5139;
}

.small {
    color: #70766D;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #E9EEE3 !important;
}

section[data-testid="stSidebar"] > div {
    background: #E9EEE3 !important;
}

section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] span {
    color: #26351F !important;
}

/* Buttons */
.stButton > button {
    border-radius: 12px;
    border: 1px solid #CBD5C3;
    background: #F7FAF4;
    color: #3F5139;
    font-weight: 600;
}

.stButton > button:hover {
    background: #E6EEE0;
    border-color: #667C5C;
}

.stButton > button[kind="primary"] {
    background: #526947;
    color: white;
    border: none;
}

.stButton > button[kind="primary"]:hover {
    background: #3F5139;
}

/* Input boxes */
.stTextInput input,
.stTextArea textarea {
    background: #FFFDF8;
    border-radius: 10px;
}

/* Headings */
h1, h2, h3 {
    color: #35432F;
}

hr {
    border-color: #DE DACF;

}

</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
    <h1>♻️ ReWear AI</h1>
    <p>
        Smart Wardrobe Reuse Platform —
        organize your wardrobe, discover outfit possibilities,
        and make smarter sustainable choices.
    </p>
</div>
""", unsafe_allow_html=True)

# ---------- Sidebar ----------
with st.sidebar:
    st.header("Navigation")
    page = st.radio("Go to", ["Dashboard", "Add Clothing", "Wardrobe", "Outfit Advisor", "Sustainability"])
    st.divider()
    st.caption("ReWear AI • AIML Project")
    st.caption("Built with Python, Streamlit, SQLite & CLIP")

items = get_items()

# ---------- Dashboard ----------
if page == "Dashboard":
    total = len(items)
    worn = sum(i["wear_count"] for i in items)
    never = sum(1 for i in items if i["wear_count"] == 0)
    reuse_score = round((worn / max(total, 1)) * 100, 1)

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f'<div class="metric-card"><h2>{total}</h2><div class="small">Wardrobe Items</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="metric-card"><h2>{worn}</h2><div class="small">Total Wears</div></div>', unsafe_allow_html=True)
    with c3:
        st.markdown(f'<div class="metric-card"><h2>{never}</h2><div class="small">Never Worn</div></div>', unsafe_allow_html=True)
    with c4:
        st.markdown(f'<div class="metric-card"><h2>{reuse_score}%</h2><div class="small">Reuse Activity</div></div>', unsafe_allow_html=True)

    st.subheader("✨ Quick Actions")
    a, b, c = st.columns(3)
    with a:
        st.info("👕 Add clothing\n\nUpload an image and let AI suggest a category.")
    with b:
        st.info("👗 Build outfits\n\nChoose weather, occasion and style for recommendations.")
    with c:
        st.info("🌱 Track reuse\n\nRecord wears and identify neglected clothes.")

    st.subheader("How ReWear AI works")
    st.markdown("""
    1. **Upload** a clothing photo.
    2. **AI classification** predicts a useful clothing category.
    3. **Wardrobe storage** keeps your item, color, occasion and wear count.
    4. **Outfit Advisor** filters clothes according to weather, occasion and style.
    5. **Sustainability dashboard** highlights reuse activity and least-worn items.
    """)

# ---------- Add Clothing ----------
elif page == "Add Clothing":
    st.header("👕 Add Clothing")
    uploaded = st.file_uploader("Upload a clothing image", type=["jpg", "jpeg", "png", "webp"])

    if uploaded:
        image = Image.open(uploaded).convert("RGB")
        st.image(image, width=350, caption="Uploaded item")

        st.divider()
        st.subheader("1. AI category detection")
        if st.button("🧠 Analyze with AI", type="primary"):
            with st.spinner("Analyzing image..."):
                result = classify_image(image)
            st.session_state["ai_result"] = result
            st.success(f"Detected: {result['label']} ({result['score']:.1f}% confidence)")

        ai = st.session_state.get("ai_result", {})
        categories = ["Shirt", "T-Shirt", "Jeans", "Trousers", "Dress", "Skirt", "Jacket", "Sweater", "Hoodie", "Shoes", "Other"]
        default_idx = 0
        if ai:
            found = next((i for i, x in enumerate(categories) if x.lower() in ai["label"].lower()), 0)
            default_idx = found

        st.subheader("2. Save wardrobe details")
        with st.form("save_item"):
            category = st.selectbox("Category", categories, index=default_idx)
            color = st.selectbox("Main color", ["Black", "White", "Blue", "Red", "Green", "Yellow", "Pink", "Brown", "Grey", "Other"])
            occasion = st.multiselect("Suitable occasions", ["Casual", "College", "Work", "Party", "Sports", "Travel", "Traditional"], default=["Casual"])
            season = st.multiselect("Best season", ["Summer", "Winter", "Monsoon", "All Season"], default=["All Season"])
            style = st.selectbox("Style", ["Casual", "Formal", "Sporty", "Traditional", "Streetwear", "Party"])
            notes = st.text_area("Notes (optional)", placeholder="Brand, fabric, pairing ideas...")
            submitted = st.form_submit_button("💾 Add to Wardrobe", type="primary")
            if submitted:
                safe_name = Path(uploaded.name).name
                save_path = Path("data") / safe_name
                save_path.parent.mkdir(exist_ok=True)
                with open(save_path, "wb") as f:
                    f.write(uploaded.getbuffer())
                add_item(safe_name, category, color, ", ".join(occasion), ", ".join(season), style, notes)
                st.success("Added to your wardrobe! ♻️")
                st.session_state.pop("ai_result", None)

# ---------- Wardrobe ----------
elif page == "Wardrobe":
    st.header("👚 My Wardrobe")
    if not items:
        st.info("Your wardrobe is empty. Go to 'Add Clothing' to add your first item.")
    else:
        q = st.text_input("🔎 Search by category, color or style")
        filtered = [x for x in items if not q or q.lower() in str(x).lower()]
        cols = st.columns(3)
        for idx, item in enumerate(filtered):
            with cols[idx % 3]:
                path = Path("data") / item["image_path"]
                if path.exists():
                    st.image(str(path), use_container_width=True)
                st.markdown(f"**{item['category']}**")
                st.caption(f"{item['color']} • {item['style']}")
                st.write(f"Worn: **{item['wear_count']}** times")
                if st.button("👟 Mark as worn", key=f"w{item['id']}"):
                    mark_worn(item["id"])
                    st.rerun()
                if st.button("🗑️ Delete", key=f"d{item['id']}"):
                    delete_item(item["id"])
                    st.rerun()

# ---------- Outfit Advisor ----------
elif page == "Outfit Advisor":
    st.header("✨ Outfit Advisor")
    weather = st.selectbox("Weather", ["Sunny / Hot", "Cloudy", "Rainy", "Cold"])
    occasion = st.selectbox("Occasion", ["Casual", "College", "Work", "Party", "Sports", "Travel", "Traditional"])
    style = st.selectbox("Preferred style", ["Any", "Casual", "Formal", "Sporty", "Traditional", "Streetwear", "Party"])

    if st.button("✨ Generate Outfit", type="primary"):
        suitable = []
        for item in items:
            occ = item["occasion"].lower()
            sty = item["style"].lower()
            season = item["season"].lower()
            occ_ok = occasion.lower() in occ or not occ
            style_ok = style == "Any" or style.lower() == sty
            weather_word = {"Sunny / Hot":"summer", "Cloudy":"all season", "Rainy":"monsoon", "Cold":"winter"}[weather]
            weather_ok = weather_word in season or "all season" in season
            if occ_ok and style_ok and weather_ok:
                suitable.append(item)

        if not suitable:
            suitable = [x for x in items if occasion.lower() in x["occasion"].lower()] or items

        if suitable:
            st.success(f"Found {len(suitable)} suitable wardrobe item(s).")
            cols = st.columns(min(3, len(suitable)))
            for i, item in enumerate(suitable[:6]):
                with cols[i % len(cols)]:
                    p = Path("data") / item["image_path"]
                    if p.exists():
                        st.image(str(p), use_container_width=True)
                    st.markdown(f"**{item['category']}**")
                    st.caption(f"{item['color']} • {item['style']}")
        else:
            st.warning("Add a few wardrobe items first.")

# ---------- Sustainability ----------
else:
    st.header("🌱 Sustainability Dashboard")
    if not items:
        st.info("Add clothing items to start tracking reuse.")
    else:
        least = sorted(items, key=lambda x: x["wear_count"])[:5]
        most = sorted(items, key=lambda x: x["wear_count"], reverse=True)[:5]

        st.subheader("⚠️ Least-worn items")
        for item in least:
            st.write(f"**{item['category']} — {item['color']}** | worn {item['wear_count']} time(s)")
        st.subheader("🏆 Most-worn items")
        for item in most:
            st.write(f"**{item['category']} — {item['color']}** | worn {item['wear_count']} time(s)")

        avg = sum(x["wear_count"] for x in items) / len(items)
        st.metric("Average wears per item", f"{avg:.1f}")
        st.success("💚 Reuse more of the clothes you already own before buying new ones.")
