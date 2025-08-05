import os
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
from prompt_builder import build_prompt, BANNED_WORDS

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash")

st.set_page_config(
    page_title="AI Ad Text Generator", 
    page_icon="🛍️", 
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main-title {
        text-align: center;
        color: #1f77b4;
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    .stButton > button {
        width: 100%;
        height: 3rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 15px;
        font-size: 1.1rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.3);
    }
    
    .result-container {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 2rem;
        border-radius: 15px;
        border-left: 5px solid #e91e63;
        margin: 1.5rem 0;
        font-size: 1.1rem;
        line-height: 1.8;
        color: white;
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }
    
    .metric-card {
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        margin: 0.5rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .mode-selector {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
</style>
""", unsafe_allow_html=True)

GARMENT_TYPES = [
    "Anarkali Palazzo Set", "Anarkali Set", "Angrakha", "Belt", "Bhanvara", "Blazer", 
    "Blazer Set", "Cap", "Choga", "Choga Set", "Co-Ord Set", "Cushion Cover", 
    "Dhoti Set", "Dress", "Dupatta", "Gharara Set", "Gift", "Jacket", "Kaftan", 
    "Kaftan Set", "Kurta", "Kurta Gharara Set", "Kurta Palazzo Set", "Kurta Salwar Set", 
    "Kurta Set", "Kurta Sharara Set", "Lehenga Set", "Lounge Wear", "Only Shawl", 
    "Palazzo", "Palazzo Set", "Pant", "Potli", "Quilt", "Salwar", "Saree Set", 
    "Scarf", "Set of 2", "Sharara Set", "Shawl", "Shirt", "Shirt Kurta Set", 
    "Shirt Set", "Skirt Set", "Suit Set", "Tops/Skirts", "Tote Bag"
]

FESTIVALS_OCCASIONS = [
    "Diwali", "Holi", "Raksha Bandhan", "Karva Chauth", "Navratri", "Durga Puja", 
    "Eid", "Christmas", "New Year", "Valentine's Day", "Mother's Day", "Father's Day",
    "Wedding Season", "Festive Season", "Summer Collection", "Winter Collection",
    "Monsoon Special", "Black Friday", "Cyber Monday", "EOSS (End of Season Sale)",
    "New Launch", "Anniversary Sale", "Flash Sale", "Pre-Diwali Sale", "Post-Diwali Sale",
    "Republic Day", "Independence Day", "Women's Day", "Friendship Day"
]

FABRIC_TYPES = [
    "Cotton", "Linen", "Silk", "Chanderi", "Banarasi Silk", "Tussar Silk", 
    "Organza", "Georgette", "Crepe", "Velvet", "Satin", "Muslin", "Brocade", 
    "Raw Silk", "Moonga Silk", "Net", "Tissue", "Mulberry Silk", "Khadi", 
    "Dupion Silk", "Chiffon", "Denim", "Rayon", "Polyester", "Blend",
    "Modal", "Bamboo", "Handloom", "Kota Cotton", "Malkha Cotton", "Organic Cotton",
    "Jamdani", "Ikat", "Kalamkari", "Block Print", "Hand Embroidered", "Machine Embroidered"
]

st.markdown('<h1 class="main-title">🛍️ AI Ad Text Generator</h1>', unsafe_allow_html=True)
st.markdown("### Create human-like, expert marketer quality ad copy")

st.markdown('<div class="mode-selector">', unsafe_allow_html=True)
st.markdown("### Select Your Mode")

mode = st.radio(
    "Choose your generation mode:",
    ["🎯 Easy Mode - Quick Setup", "⚙️ Flexible Mode - Full Control"],
    horizontal=True,
    help="Easy Mode: Pre-defined options | Flexible Mode: Full customization"
)
st.markdown('</div>', unsafe_allow_html=True)

if mode == "🎯 Easy Mode - Quick Setup":
    
    with st.sidebar:
        st.markdown("## 🎯 Easy Mode Setup")
        
        # Product Selection
        with st.expander("🏷️ Product Details", expanded=True):
            garment_type = st.selectbox(
                "Garment Type",
                GARMENT_TYPES,
                help="Choose your product type"
            )
            
            brand_name = st.text_input(
                "Brand Name", 
                placeholder="e.g., Dolly J, Safaa, Kaveri",
                help="Enter your brand name"
            )
            
            usp_easy = st.text_input(
                "Unique Selling Point", 
                placeholder="e.g., Effortless Glamour, Made for Moments",
                help="Enter your brand's key promise"
            )
        

        with st.expander("🎨 Style Details", expanded=True):
            fabric_easy = st.multiselect(
                "Fabric Type",
                FABRIC_TYPES[:10], 
                help="Select fabric types"
            )
            
            festival_easy = st.selectbox(
                "Occasion",
                FESTIVALS_OCCASIONS,
                help="Choose occasion"
            )
        

        with st.expander("⚙️ Campaign Settings", expanded=True):
            category_easy = st.selectbox(
                "Content Type",
                ["Email Subject Lines", "Long Content", "Concise Content", "PMAX", "WhatsApp Broadcast"],
                help="Choose format"
            )
            
            tone_easy = st.selectbox(
                "Brand Voice",
                ["Premium & Aspirational", "Warm & Personal", "Playful & Fun", 
                 "Sophisticated", "Friendly & Approachable", "Luxury & Exclusive"],
                help="Select tone"
            )
            
            discount_easy = st.number_input(
                "Discount %", 
                min_value=0, 
                max_value=100, 
                step=5,
                value=0,
                help="Discount percentage"
            )

            if category_easy == "PMAX":
                char_limit_easy = {
                    'headlines': 30,
                    'description': 90,
                    'long_headlines': 120
                }
                st.info("PMAX: Headlines=30, Description=90, Long Headlines=120")
            else:
                char_limit_easy = st.selectbox(
                    "Character Limit",
                    [30, 50, 70, 90, 120, 200, 300, 500, 1000],
                    index=1,  # Default to 50
                    help="Select character limit"
                )

        generate_btn_easy = st.button("✨ Generate Copy (Easy Mode)", type="primary")

    if generate_btn_easy:
        if not brand_name or not garment_type:
            st.error("⚠️ Please fill Brand Name and Garment Type")
            st.stop()

        product_name = f"{brand_name} {garment_type}"
        data_easy = {
            'category': category_easy,
            'tone': tone_easy, 
            'product': product_name,
            'usp': usp_easy or "Premium Quality",
            'attributes': "Expertly crafted",
            'fabric': ", ".join(fabric_easy) if fabric_easy else "Premium materials",
            'festival': festival_easy,
            'discount': discount_easy,
            'timing': "Limited time",
            'char_limit': char_limit_easy,
            'emotion': "Special moments"
        }

        prompt_easy = build_prompt(data_easy)
        
        with st.spinner("✨ Generating..."):
            try:
                response = model.generate_content(prompt_easy)
                copy_easy = response.text.strip()
                
                # FIXED CHARACTER LIMIT ENFORCEMENT
                if category_easy != "PMAX" and category_easy not in ["Email Subject Lines", "Long Content"]:
                    if len(copy_easy) > char_limit_easy:
                        # Hard truncate at character limit
                        copy_easy = copy_easy[:char_limit_easy-3] + "..."
                        st.warning(f"⚠️ Copy truncated to {char_limit_easy} characters")
                
                # Remove banned words
                for word in BANNED_WORDS:
                    copy_easy = copy_easy.replace(word, "").replace(word.capitalize(), "")
                
            except Exception as e:
                st.error(f"❌ Error: {e}")
                st.stop()

        # Display Results
        st.markdown("---")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(f'<div class="metric-card"><b>{category_easy}</b></div>', unsafe_allow_html=True)
        with col2:
            if category_easy == "PMAX":
                st.markdown('<div class="metric-card"><b>PMAX Format</b></div>', unsafe_allow_html=True)  
            else:
                char_color = "green" if len(copy_easy) <= char_limit_easy else "red"
                st.markdown(f'<div class="metric-card" style="color: {char_color}"><b>{len(copy_easy)} chars</b><br><small>Limit: {char_limit_easy}</small></div>', unsafe_allow_html=True)
        with col3:
            st.markdown(f'<div class="metric-card"><b>{discount_easy}% OFF</b></div>', unsafe_allow_html=True)
        with col4:
            st.markdown(f'<div class="metric-card"><b>{len(copy_easy.split())} words</b></div>', unsafe_allow_html=True)

        st.markdown("### 🎯 Generated Copy")
        st.markdown(f'<div class="result-container">{copy_easy}</div>', unsafe_allow_html=True)
        st.code(copy_easy)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Generate Another", use_container_width=True):
                st.rerun()
        with col2:
            st.download_button("📥 Download", copy_easy, f"{product_name}.txt", use_container_width=True)

# ─── FLEXIBLE MODE ────────────────────────────────────────────
elif mode == "⚙️ Flexible Mode - Full Control":
    
    with st.sidebar:
        st.markdown("## ⚙️ Flexible Mode")
        
        # Product Information
        with st.expander("🏷️ Product Information", expanded=True):
            product = st.text_input(
                "Product/Brand Name", 
                placeholder="e.g., Dolly J Wedding Collection",
                help="Enter your brand or product name"
            )
            
            usp = st.text_input(
                "Unique Selling Point", 
                placeholder="e.g., Effortless Glamour, Made for Moments",
                help="Your brand's core promise"
            )
            
            attributes = st.text_area(
                "Product Attributes", 
                placeholder="e.g., Handcrafted, Premium comfort, Wedding-ready",
                help="Key features and benefits",
                height=80
            )
            
            fabric = st.multiselect(
                "Fabric Types",
                FABRIC_TYPES,
                help="Select all applicable fabrics"
            )

            emotion = st.text_input(
                "Emotional Hook", 
                placeholder="e.g., Celebrate Bonds, Festive Joy",
                help="Emotion to evoke"
            )
        
        # Content Settings
        with st.expander("⚙️ Content Settings", expanded=True):
            category = st.selectbox(
                "Content Type",
                ["Email Subject Lines", "Long Content", "Concise Content", "PMAX", "WhatsApp Broadcast"],
                help="Choose format"
            )
            
            tone = st.selectbox(
                "Brand Voice",
                ["Premium & Aspirational", "Warm & Personal", "Playful & Fun", 
                 "Sophisticated", "Friendly & Approachable", "Luxury & Exclusive"],
                help="Select tone"
            )
        
        # Marketing Details
        with st.expander("🎯 Marketing Details", expanded=True):
            discount = st.number_input(
                "Discount %", 
                min_value=0, 
                max_value=100, 
                step=5,
                value=0
            )
            
            # FIXED CHARACTER LIMIT LOGIC
            if category == "PMAX":
                char_limit = {
                    'headlines': 30,
                    'description': 90,
                    'long_headlines': 120
                }
                st.info("PMAX: Headlines=30, Description=90, Long Headlines=120")
            else:
                char_limit = st.selectbox(
                    "Character Limit",
                    [30, 50, 70, 90, 120, 200, 300, 500, 1000],
                    index=1,  # Default to 50
                    help="Select character limit"
                )
            
            festival = st.text_input(
                "Festival/Occasion", 
                placeholder="e.g., Raksha Bandhan, Wedding Season",
                help="Seasonal context"
            )
            
            timing = st.text_input(
                "Urgency Element", 
                placeholder="e.g., 48 Hours Left, Flash Sale",
                help="Create urgency"
            )
        
        # Generate Button
        generate_btn = st.button("✨ Generate Copy (Flexible Mode)", type="primary")
    
    # Flexible Mode Generation
    if generate_btn:
        if not product:
            st.error("⚠️ Product/Brand name is required")
            st.stop()

        data = {
            'category': category,
            'tone': tone,
            'product': product,
            'usp': usp or "Premium Quality",
            'attributes': attributes or "Expertly crafted",
            'fabric': ", ".join(fabric) if fabric else "Premium materials",
            'festival': festival or "Special occasion",
            'discount': discount,
            'timing': timing or "Limited time",
            'char_limit': char_limit,
            'emotion': emotion or "Exclusive luxury"
        }

        prompt = build_prompt(data)
        
        with st.spinner("✨ Generating..."):
            try:
                response = model.generate_content(prompt)
                copy = response.text.strip()
                
                # FIXED CHARACTER LIMIT ENFORCEMENT
                if category != "PMAX" and category not in ["Email Subject Lines", "Long Content"]:
                    if len(copy) > char_limit:
                        # Hard truncate at character limit
                        copy = copy[:char_limit-3] + "..."
                        st.warning(f"⚠️ Copy truncated to {char_limit} characters")
                
                # Remove banned words
                for word in BANNED_WORDS:
                    copy = copy.replace(word, "").replace(word.capitalize(), "")
                
            except Exception as e:
                st.error(f"❌ Error: {e}")
                st.stop()

        # Display Results
        st.markdown("---")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(f'<div class="metric-card"><b>{category}</b></div>', unsafe_allow_html=True)
        with col2:
            if category == "PMAX":
                st.markdown('<div class="metric-card"><b>PMAX Format</b></div>', unsafe_allow_html=True)
            else:
                char_color = "green" if len(copy) <= char_limit else "red"
                st.markdown(f'<div class="metric-card" style="color: {char_color}"><b>{len(copy)} chars</b><br><small>Limit: {char_limit}</small></div>', unsafe_allow_html=True)
        with col3:
            st.markdown(f'<div class="metric-card"><b>{discount}% OFF</b></div>', unsafe_allow_html=True)
        with col4:
            st.markdown(f'<div class="metric-card"><b>{len(copy.split())} words</b></div>', unsafe_allow_html=True)

        st.markdown("### 🎯 Generated Copy")
        st.markdown(f'<div class="result-container">{copy}</div>', unsafe_allow_html=True)
        st.code(copy)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Generate Another", use_container_width=True):
                st.rerun()
        with col2:
            st.download_button("📥 Download", copy, f"{product.replace(' ', '_')}.txt", use_container_width=True)

# ─── Footer ──────────────────────────────────────────────────
st.markdown("---")
st.markdown('<div style="text-align: center; color: #6c757d;">✨ Powered by AI • Made for Premium Brands</div>', unsafe_allow_html=True)