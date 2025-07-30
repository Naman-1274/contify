import os
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
from prompt_builder import build_prompt, BANNED_WORDS

# ─── Load environment variables ────────────────────────────────
load_dotenv()

# ─── Speed-optimized Gemini setup ──────────────────────────────

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash")

# ─── Page Configuration & Minimal CSS ─────────────────────────
st.set_page_config(
    page_title="AI Ad Text Generator", 
    page_icon="🛍️", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Streamlined CSS for faster loading
st.markdown("""
<style>
    .main-title {
        text-align: center;
        color: #1f77b4;
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 1rem;
    }
    
    .stButton > button {
        width: 100%;
        height: 3rem;
        background: linear-gradient(90deg, #28a745, #20c997);
        color: white;
        border: none;
        border-radius: 10px;
        font-size: 1.1rem;
        font-weight: 600;
    }
    
    .result-container {
        background: linear-gradient(90deg, #28a745, #20c997);
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #28a745;
        margin: 1rem 0;
        font-size: 1.1rem;
        line-height: 1.6;
    }
</style>
""", unsafe_allow_html=True)

# ─── Main Title ──────────────────────────────────────────────────
st.markdown('<h1 class="main-title">🛍️ AI Ad Text Generator</h1>', unsafe_allow_html=True)
st.markdown("### Create high-converting ad copy with AI assistance")

# ─── Sidebar Input Panel ────────────────────────────────────────
with st.sidebar:
    st.markdown("## 📝 Input Configuration")
    
    # Product Information Section
    with st.expander("🏷️ Product Information", expanded=True):
        product = st.text_input(
            "Product / Category", 
            placeholder="e.g., Summer Dress, Casual Shirt",
            help="Enter the main product or category you're advertising"
        )
        
        usp = st.text_input(
            "Unique Selling Point", 
            placeholder="e.g., Premium Quality, Comfortable Fit",
            help="What makes your product special?"
        )
        
        attributes = st.text_area(
            "Additional Attributes", 
            placeholder="e.g., Breathable, Wrinkle-free, Machine washable",
            help="Any extra features or benefits",
            height=100
        )
        
        fabric = st.multiselect(
            "Fabric Type",
            ["Cotton", "Linen", "Silk", "Polyester", "Blend", "Denim", "Chiffon", "Georgette"],
            help="Select all applicable fabric types"
        )
        
    # Content Settings Section
    with st.expander("⚙️ Content Settings", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            category = st.selectbox(
                "Content Type",
                ["Long Content", "Concise Content", "PMAX", "WhatsApp Broadcast", "Email Subject"],
                help="Choose the exact format for your ad copy"
            )
        
        with col2:
            tone = st.selectbox(
                "Tone of Voice",
                ["Casual", "Playful", "Friendly", "Professional", "Corporate", "Expert"],
                help="Select the tone that matches your brand"
            )
    
    # Marketing Details Section
    with st.expander("🎯 Marketing Details", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            discount = st.number_input(
                "Discount %", 
                min_value=0, 
                max_value=100, 
                step=5,
                value=0,
                help="Discount percentage (0 for no discount)"
            )
        
        with col2:
            category_char_defaults = {
                "PMAX": 800,
                "Long Content": 450,
                "Concise Content": 150,
                "WhatsApp Broadcast": 300,
                "Email Subject": 220
            }
            
            char_limit = st.slider(
                "Character Limit",
                min_value=50, max_value=800,
                value=category_char_defaults.get(category, 120),
                help=f"Suggested: {category_char_defaults.get(category,120)}"
            )
        
        festival = st.text_input(
            "Festival / Event", 
            placeholder="e.g., Diwali, Christmas, EOSS",
            help="Optional: Seasonal or event-based context"
        )
        
        timing = st.text_input(
            "Timing Hook", 
            placeholder="e.g., New Arrival, Limited Time, Flash Sale",
            help="Create urgency or highlight timing"
        )
        
        st.markdown("---")
    
    # Generate Button
    generate_btn = st.button("⚡ Generate Fast Copy", type="primary", use_container_width=True)
    
    # Quick Tips
    with st.expander("💡 Quick Tips"):
        st.markdown("""
        **For better results:**
        - Be specific about your product
        - Highlight unique benefits
        - Use relevant festivals/events
        - Choose appropriate tone for your audience
        """)

# ─── Fast Generation Logic ──────────────────────────────────────
if generate_btn:
    if not product:
        st.error("⚠️ Product name is required to generate ad copy.")
        st.stop()

    # Prepare optimized data with smart defaults
    data = {
        'category': category,
        'tone': tone,
        'product': product,
        'usp': usp or "Premium quality",
        'attributes': attributes or "Stylish design",
        'fabric': ", ".join(fabric) if fabric else "Premium fabric",
        'festival': festival or "None",
        'discount': discount,
        'timing': timing or "Limited time",
        'char_limit': char_limit
    }

    # Build streamlined prompt
    prompt = build_prompt(data)

    # Fast generation with timeout
    with st.spinner("⚡ Generating your ad copy..."):
        try:
            response = model.generate_content(prompt)
            copy = response.text.strip()
        except Exception as e:
            st.error(f"❌ Error: {e}")
            st.stop()

    # Quick post-processing
    if len(copy) > char_limit and category != "Long Content":
        copy = copy[:char_limit].rstrip(".,!? ") + "..."
    
    # Simple banned word replacement
    for word in BANNED_WORDS:
        if word in copy.lower():
            copy = copy.replace(word, "")

    # ─── Clean Display ──────────────────────────────────────────
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.markdown(f"**{category}** - {tone} tone")
    with col2:
        if category == "Long Content":
            st.markdown(f"**{len(copy)} characters**")
        else:
            st.markdown(f"**{len(copy)}/{char_limit} chars**")
    with col3:
        if discount > 0:
            st.markdown(f"**{discount}% OFF**")

    # Display generated copy
    st.markdown(f'<div class="result-container">{copy}</div>', unsafe_allow_html=True)
    
    # Copy code block
    st.code(copy, language=None)
    
    # Action buttons
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔄 Generate Another", use_container_width=True):
            st.rerun()
    
    with col2:
        st.download_button(
            "📥 Download",
            copy,
            file_name=f"{product.replace(' ', '_')}_ad_copy.txt",
            mime="text/plain",
            use_container_width=True
        )

else:
    # Welcome screen
    st.markdown("## 👋 Welcome to AI Ad Text Generator")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        ### ⚡ Fast & Accurate Generation
        
        1. **📝 Fill in product details** in the sidebar
        2. **🎨 Choose your content type and tone**
        3. **⚡ Get instant ad copy** in 2-3 seconds
        4. **✨ Matches your sample style** exactly
        
        ---
        
        **Ready to create amazing ad copy?** Start by entering your product details in the sidebar! 👆
        """)

# ─── Footer ──────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    '<div style="text-align: center; color: #6c757d;">⚡ Powered by Optimized Gemini AI</div>', 
    unsafe_allow_html=True
)
