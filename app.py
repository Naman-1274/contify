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

# Enhanced CSS for better visual appeal
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
    
    .welcome-card {
        background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
        padding: 2rem;
        border-radius: 15px;
        margin: 2rem 0;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# ─── Main Title ──────────────────────────────────────────────────
st.markdown('<h1 class="main-title">🛍️ AI Ad Text Generator</h1>', unsafe_allow_html=True)
st.markdown("### Create human-like, expert marketer quality ad copy")

# ─── Sidebar Input Panel ────────────────────────────────────────
with st.sidebar:
    st.markdown("## 📝 Input Configuration")
    
    # Product Information Section
    with st.expander("🏷️ Product Information", expanded=True):
        product = st.text_input(
            "Product / Brand Name", 
            placeholder="e.g., Dolly J Wedding Edit, Safaa Festive Collection",
            help="Enter your brand or product collection name"
        )
        
        usp = st.text_input(
            "Unique Selling Point", 
            placeholder="e.g., Effortless Glamour, Made for Moments",
            help="What's your brand's core promise or unique angle?"
        )
        
        attributes = st.text_area(
            "Product Attributes", 
            placeholder="e.g., Handcrafted details, Premium comfort, Wedding-ready",
            help="Key features and benefits that matter to customers",
            height=100
        )
        
        fabric = st.multiselect(
            "Fabric Type",
            ["Cotton", "Linen", "Silk", "Chanderi", "Banarasi Silk", "Tussar Silk", 
             "Organza", "Georgette", "Crepe", "Velvet", "Satin", "Muslin", "Brocade", 
             "Raw Silk", "Moonga Silk", "Net", "Tissue", "Mulberry Silk", "Khadi", 
             "Dupion Silk", "Chiffon", "Denim", "Rayon", "Polyester", "Blend"],
            help="Select all applicable fabric types"
        )

        emotion = st.text_input(
            "Emotional Hook", 
            placeholder="e.g., Celebrate Bonds, Sisterhood & Style, Festive Joy",
            help="What emotion should the copy evoke?"
        )
           
        
        
    # Content Settings Section
    with st.expander("⚙️ Content Settings", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            category = st.selectbox(
                "Content Type",
                ["Email Subject Lines", "Long Content", "Concise Content", "PMAX", "WhatsApp Broadcast"],
                help="Choose the format for your ad copy"
            )
        
        with col2:
            tone = st.selectbox(
                "Brand Voice",
                ["Premium & Aspirational", "Warm & Personal", "Playful & Fun", 
                 "Sophisticated", "Friendly & Approachable", "Luxury & Exclusive"],
                help="Select the tone that matches your brand personality"
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
                "Email Subject Lines": 400
            }
            
            char_limit = st.slider(
                "Character Limit",
                min_value=50, max_value=1000,
                value=category_char_defaults.get(category, 400),
                help=f"Suggested: {category_char_defaults.get(category, 400)}"
            )
        
        festival = st.text_input(
            "Festival / Occasion", 
            placeholder="e.g., Raksha Bandhan, Wedding Season, Diwali",
            help="Seasonal context or special occasion"
        )
        
        timing = st.text_input(
            "Urgency Element", 
            placeholder="e.g., 48 Hours Left, Flash Sale, Limited Edition",
            help="Create urgency or scarcity"
        )
        
        st.markdown("---")
    
    # Generate Button
    generate_btn = st.button("✨ Generate Expert Copy", type="primary", use_container_width=True)
    
    # Enhanced Tips
    with st.expander("💡 Pro Tips for Better Copy"):
        st.markdown("""
        **🎯 For Premium Results:**
        - Use specific brand names (e.g., "Dolly J" vs "dress")
        - Include emotional hooks ("Celebrate Bonds")
        - Mention craftsmanship details
        - Reference specific occasions
        
        **📝 Email Subject Lines:**
        - Focus on aspirational headlines
        - Include collection names
        - Add emotional storytelling
        - Use premium language
        """)

# ─── Enhanced Generation Logic ──────────────────────────────────
if generate_btn:
    if not product:
        st.error("⚠️ Product/Brand name is required to generate ad copy.")
        st.stop()

    # Prepare enhanced data with better defaults
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

    # Build enhanced prompt
    prompt = build_prompt(data)
    
    # Define improve_flow before usage
    def improve_flow(text):
        lines = [line.strip().capitalize() for line in text.strip().split("\n") if line.strip()]
        polished_lines = []

        for i, line in enumerate(lines):
            # Remove repeated product mentions
            if i > 0 and any(line.lower().startswith(start) for start in ["introducing", "presenting", "meet"]):
                continue
            # Ensure emotional hook doesn't feel robotic
            if i == 0 and any(line.lower().startswith(w) for w in ["exclusive", "special", "discount"]):
                line = line.replace("exclusive", "crafted for").replace("special", "celebrating")
            polished_lines.append(line)

        return "\n".join(polished_lines)

    # Generate with enhanced error handling
    with st.spinner("✨ Crafting your expert ad copy..."):
        try:
            # Generate content with error handling
            response = model.generate_content(prompt)
            copy = response.text.strip()
            copy = improve_flow(copy)
            
        except Exception as e:
            st.error(f"❌ Generation Error: {e}")
            st.stop()

    # Enhanced post-processing
    if len(copy) > char_limit and category not in ["Long Content", "Email Subject Lines"]:
        # Smart truncation that preserves word boundaries
        copy = copy[:char_limit].rsplit(' ', 1)[0] + "..."
    
    # Simple banned word replacement
    for word in BANNED_WORDS:
        if word.lower() in copy.lower():
            copy = copy.replace(word, "")

    # ─── Enhanced Display ──────────────────────────────────────
    st.markdown("---")
    
    # Metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f'<div class="metric-card"><b>{category}</b><br><small>{tone}</small></div>', 
                   unsafe_allow_html=True)
    with col2:
        char_color = "green" if len(copy) <= char_limit else "orange"
        st.markdown(f'<div class="metric-card" style="color: {char_color}"><b>{len(copy)} chars</b><br><small>Limit: {char_limit}</small></div>', 
                   unsafe_allow_html=True)
    with col3:
        if discount > 0:
            st.markdown(f'<div class="metric-card"><b>{discount}% OFF</b><br><small>Discount</small></div>', 
                       unsafe_allow_html=True)
        else:
            st.markdown('<div class="metric-card"><b>No Discount</b><br><small>Regular Price</small></div>', 
                       unsafe_allow_html=True)
    with col4:
        words = len(copy.split())
        st.markdown(f'<div class="metric-card"><b>{words} words</b><br><small>Word count</small></div>', 
                   unsafe_allow_html=True)

    # Display generated copy with enhanced styling
    st.markdown("### 🎯 Generated Copy")
    st.markdown(f'<div class="result-container">{copy}</div>', unsafe_allow_html=True)
    
    # Copy code block for easy copying
    st.code(copy, language=None)
    
    # Action buttons
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔄 Generate Another Version", use_container_width=True):
            st.rerun()
    
    with col2:
        st.download_button(
            "📥 Download Copy",
            copy,
            file_name=f"{product.replace(' ', '_')}_{category.replace(' ', '_')}.txt",
            mime="text/plain",
            use_container_width=True
        )
    
    with col3:
        # Copy to clipboard functionality
        st.button("📋 Copy to Clipboard", use_container_width=True, 
                 help="Click to copy the generated text")

    # Performance feedback
    st.markdown("---")
    st.markdown("### 📊 Quick Analysis")
    
    analysis_col1, analysis_col2 = st.columns(2)
    
    with analysis_col1:
        # Simple readability check
        sentences = copy.count('.') + copy.count('!') + copy.count('?')
        if sentences > 0:
            avg_sentence_length = len(copy.split()) / sentences
            readability = "Easy" if avg_sentence_length < 15 else "Moderate" if avg_sentence_length < 25 else "Complex"
            st.write(f"**Readability:** {readability}")
        
        # Emotional words check
        emotional_words = ["love", "celebrate", "joy", "beautiful", "perfect", "amazing", "stunning"]
        emotion_count = sum(1 for word in emotional_words if word.lower() in copy.lower())
        st.write(f"**Emotional Appeal:** {emotion_count}/7")
    
    with analysis_col2:
        # Call-to-action check
        cta_words = ["shop", "buy", "get", "order", "discover", "explore"]
        has_cta = any(word.lower() in copy.lower() for word in cta_words)
        st.write(f"**Call-to-Action:** {'✅ Present' if has_cta else '❌ Missing'}")
        
        # Brand mention check
        has_brand = product.lower() in copy.lower()
        st.write(f"**Brand Mention:** {'✅ Included' if has_brand else '⚠️ Consider adding'}")

else:
    # Enhanced welcome screen
    st.markdown('<div class="welcome-card">', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("""
        ## 👋 Welcome to Expert Ad Copy Generator
        
        ### ✨ What Makes This Different?
        
        - **Human-like Writing:** Copy that sounds like an expert marketer wrote it
        - **Brand Voice Matching:** Maintains your premium brand personality  
        - **Format Expertise:** Specialized templates for each content type
        - **Emotional Intelligence:** Incorporates feelings and aspirations
        """)
    
# ─── Enhanced Footer ────────────────────────────────────────────
    st.markdown('</div>', unsafe_allow_html=True)
def improve_flow(text):
    lines = [line.strip().capitalize() for line in text.strip().split("\n") if line.strip()]
    polished_lines = []

    for i, line in enumerate(lines):
        # Remove repeated product mentions
        if i > 0 and any(line.lower().startswith(start) for start in ["introducing", "presenting", "meet"]):
            continue
        # Ensure emotional hook doesn't feel robotic
        if i == 0 and any(line.lower().startswith(w) for w in ["exclusive", "special", "discount"]):
            line = line.replace("exclusive", "crafted for").replace("special", "celebrating")
        polished_lines.append(line)

    return "\n".join(polished_lines)
# ─── Enhanced Footer ────────────────────────────────────────────


st.markdown("---")
st.markdown(
    '<div style="text-align: center; color: #6c757d; font-style: italic;">✨ Powered by Advanced AI • Designed for Premium Brands</div>', 
    unsafe_allow_html=True
)


