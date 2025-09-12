import os
import streamlit as st
import requests
import json
from dotenv import load_dotenv
from prompt_builder import build_prompt, BANNED_WORDS

load_dotenv()

class GroqContentGenerator:
    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")
        self.base_url = "https://api.groq.com/openai/v1/chat/completions"
        
        # Validate API key
        if not self.api_key:
            st.error("❌ GROQ_API_KEY not found in environment variables. Please set it in your .env file.")
            st.stop()
        
        if not self.api_key.startswith("gsk_"):
            st.error("❌ Invalid GROQ_API_KEY format. It should start with 'gsk_'")
            st.stop()
        
        # Different creative approaches for variations
        self.variation_styles = {
            "Email Subject Lines": [
                "curiosity_hook", "urgency_driven", "benefit_focused"
            ],
            "WhatsApp Broadcast": [
                "friend_recommendation", "personal_stylist", "exclusive_insider"
            ],
            "Concise Content": [
                "lifestyle_moment", "product_spotlight", "emotion_first"
            ],
            "Long Content": [
                "storytelling_approach", "feature_benefits", "aspirational_lifestyle"
            ],
            "PMAX": [
                "brand_focused", "product_driven", "occasion_centered"
            ]
        }
    
    def test_api_connection(self):
        """Test if the API key works"""
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            # Simple test payload
            payload = {
                "model": "llama-3.1-70b-versatile",
                "messages": [{"role": "user", "content": "Hello"}],
                "max_tokens": 5
            }
            
            response = requests.post(self.base_url, headers=headers, json=payload, timeout=10)
            return response.status_code == 200
            
        except Exception:
            return False
    
    def generate_variations(self, data: dict, content_type: str) -> list:
        """Generate 3 different variations using different creative approaches"""
        # Test API connection first
        if not self.test_api_connection():
            st.error("❌ Cannot connect to Groq API. Please check your API key.")
            return [{"variation": 1, "content": "API connection failed", "char_count": 0}]
        
        styles = self.variation_styles.get(content_type, ["standard", "creative", "premium"])
        variations = []
        
        for i, style in enumerate(styles):
            try:
                # Create style-specific prompt
                enhanced_prompt = self._enhance_prompt_with_style(data, content_type, style)
                
                # Generate with Groq
                response = self._call_groq_api(enhanced_prompt)
                
                if response:
                    content = response.strip()
                    
                    # Apply character limits
                    if content_type not in ["PMAX", "Long Content", "Email Subject Lines"]:
                        char_limit = data.get('char_limit', 150)
                        if len(content) > char_limit:
                            content = content[:char_limit-3] + "..."
                    
                    # Remove banned words
                    for word in BANNED_WORDS:
                        content = content.replace(word, "").replace(word.capitalize(), "")
                    
                    variations.append({
                        "variation": i + 1,
                        "style": style.replace('_', ' ').title(),
                        "content": content,
                        "char_count": len(content),
                        "word_count": len(content.split())
                    })
                
            except Exception as e:
                st.error(f"Error generating variation {i+1}: {str(e)}")
                
        return variations if variations else [{"variation": 1, "content": "Generation failed", "char_count": 0}]
    
    def _enhance_prompt_with_style(self, data: dict, content_type: str, style: str) -> str:
        """Enhance the base prompt with specific creative style instructions"""
        
        base_prompt = build_prompt(data)
        
        style_instructions = {
            # Email styles
            "curiosity_hook": "\n\nSTYLE: Create intrigue and mystery. Make them wonder 'what's inside?' Use incomplete thoughts or questions.",
            "urgency_driven": "\n\nSTYLE: Build time pressure. Use words like 'ending soon', 'final hours', 'limited pieces'.",
            "benefit_focused": "\n\nSTYLE: Lead with transformation. How will they feel wearing this? What's the emotional payoff?",
            
            # WhatsApp styles
            "friend_recommendation": "\n\nSTYLE: Write like an excited friend sharing an amazing fashion find. Casual, genuine enthusiasm.",
            "personal_stylist": "\n\nSTYLE: Professional stylist giving insider advice. Confident and authoritative tone.",
            "exclusive_insider": "\n\nSTYLE: VIP treatment. Make them feel chosen and special. Exclusive language.",
            
            # Social content styles
            "lifestyle_moment": "\n\nSTYLE: Paint the scene. Where are they wearing this? What's the moment? Create aspiration.",
            "product_spotlight": "\n\nSTYLE: Hero the craftsmanship and details. Focus on what makes this piece special.",
            "emotion_first": "\n\nSTYLE: Start with feeling. How does this piece make them feel? Connect emotionally first.",
            
            # Long content styles
            "storytelling_approach": "\n\nSTYLE: Tell a story. Create a narrative around the collection or occasion.",
            "feature_benefits": "\n\nSTYLE: Focus on practical benefits and features. What problems does this solve?",
            "aspirational_lifestyle": "\n\nSTYLE: Paint the premium lifestyle. Who do they become wearing this?",
            
            # PMAX styles
            "brand_focused": "\n\nSTYLE: Lead with brand name and reputation. Build brand recognition.",
            "product_driven": "\n\nSTYLE: Hero the specific products and their unique features.",
            "occasion_centered": "\n\nSTYLE: Focus on the event/festival. Make the timing feel perfect."
        }
        
        enhanced_prompt = base_prompt + style_instructions.get(style, "")
        enhanced_prompt += f"\n\nIMPORTANT: Generate fresh, non-robotic copy that sounds human and conversational. Avoid marketing clichés. Temperature: HIGH creativity."
        
        return enhanced_prompt
    
    def _call_groq_api(self, prompt: str) -> str:
        """Make API call to Groq with proper error handling"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "llama-3.1-70b-versatile",
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.8,  # Higher creativity
            "max_tokens": 400,
            "top_p": 0.9
        }
        
        try:
            response = requests.post(self.base_url, headers=headers, json=payload, timeout=30)
            
            if response.status_code == 401:
                raise Exception("Invalid API key. Please check your GROQ_API_KEY in the .env file.")
            elif response.status_code == 429:
                raise Exception("Rate limit exceeded. Please try again in a few minutes.")
            elif response.status_code == 400:
                raise Exception("Bad request. Please check your input parameters.")
            
            response.raise_for_status()
            
            data = response.json()
            if 'choices' not in data or not data['choices']:
                raise Exception("No response generated from API")
                
            return data['choices'][0]['message']['content']
            
        except requests.exceptions.Timeout:
            raise Exception("Request timed out. Please try again.")
        except requests.exceptions.RequestException as e:
            if "401" in str(e):
                raise Exception("Unauthorized: Invalid API key")
            elif "429" in str(e):
                raise Exception("Rate limit exceeded")
            else:
                raise Exception(f"Network error: {str(e)}")
        except KeyError as e:
            raise Exception(f"Unexpected API response format: {str(e)}")

# Initialize Groq generator with validation
@st.cache_resource
def init_groq_generator():
    return GroqContentGenerator()

# Add API key setup instructions at the top
st.set_page_config(
    page_title="AI Ad Text Generator", 
    page_icon="🛍️", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Check for API key before initializing
if not os.getenv("GROQ_API_KEY"):
    st.error("❌ GROQ_API_KEY not found!")
    st.markdown("""
    ### How to fix:
    1. Create a `.env` file in your project root
    2. Add this line: `GROQ_API_KEY=your_actual_groq_api_key_here`
    3. Get your API key from: https://console.groq.com/keys
    4. Restart the application
    """)
    st.stop()

groq_generator = init_groq_generator()

# Rest of your existing Streamlit code stays the same until the generation part
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
    
    .variation-card {
        background: linear-gradient(135deg, #e3f2fd 0%, #f3e5f5 100%);
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        border-left: 4px solid #2196f3;
    }
</style>
""", unsafe_allow_html=True)

# Your existing constants
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

st.markdown('<h1 class="main-title">🛍️ AI Ad Text Generator with Groq</h1>', unsafe_allow_html=True)
st.markdown("### Create human-like, expert marketer quality ad copy with multiple variations")

# Mode selection
mode = st.radio(
    "Choose your generation mode:",
    ["🎯 Easy Mode - Quick Setup", "⚙️ Flexible Mode - Full Control"],
    horizontal=True
)

def display_variations(variations, data, mode_prefix=""):
    """Display multiple variations in an organized way"""
    
    st.markdown("---")
    
    # Metrics row
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f'<div class="metric-card"><b>{data["category"]}</b></div>', unsafe_allow_html=True)
    with col2:
        avg_chars = sum(v['char_count'] for v in variations) // len(variations)
        st.markdown(f'<div class="metric-card"><b>{avg_chars} avg chars</b></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="metric-card"><b>{data["discount"]}% OFF</b></div>', unsafe_allow_html=True)
    with col4:
        st.markdown(f'<div class="metric-card"><b>{len(variations)} Variations</b></div>', unsafe_allow_html=True)
    
    st.markdown("### 🎯 Generated Variations")
    
    # Display variations in tabs
    tabs = st.tabs([f"Option {v['variation']} - {v['style']}" for v in variations])
    
    for i, (tab, variation) in enumerate(zip(tabs, variations)):
        with tab:
            st.markdown(f'<div class="variation-card">{variation["content"]}</div>', unsafe_allow_html=True)
            
            col1, col2 = st.columns([3, 1])
            with col1:
                st.code(variation["content"], language="text")
            with col2:
                st.metric("Characters", variation["char_count"])
                st.metric("Words", variation.get("word_count", len(variation["content"].split())))
                
                # Download button for each variation
                st.download_button(
                    "📥 Download", 
                    variation["content"], 
                    f"{data['brand']}_{data['category']}_v{variation['variation']}.txt",
                    use_container_width=True,
                    key=f"download_{mode_prefix}_{i}"
                )

# EASY MODE
if mode == "🎯 Easy Mode - Quick Setup":
    
    with st.sidebar:
        st.markdown("## 🎯 Easy Mode Setup")
        
        # Your existing sidebar code for Easy Mode
        with st.expander("🏷️ Product Details", expanded=True):
            garment_type = st.selectbox("Garment Type", GARMENT_TYPES)
            brand_name = st.text_input("Brand Name", placeholder="e.g., Dolly J, Safaa, Kaveri")
            usp_easy = st.text_input("Unique Selling Point", placeholder="e.g., Effortless Glamour")

        with st.expander("🎨 Style Details", expanded=True):
            fabric_easy = st.multiselect("Fabric Type", FABRIC_TYPES[:10])
            festival_easy = st.selectbox("Occasion", FESTIVALS_OCCASIONS)

        with st.expander("⚙️ Campaign Settings", expanded=True):
            category_easy = st.selectbox("Content Type", ["Email Subject Lines", "Long Content", "Concise Content", "PMAX", "WhatsApp Broadcast"])
            tone_easy = st.selectbox("Brand Voice", ["Premium & Aspirational", "Warm & Personal", "Playful & Fun", "Sophisticated", "Friendly & Approachable", "Luxury & Exclusive"])
            discount_easy = st.number_input("Discount %", min_value=0, max_value=100, step=5, value=0)

            if category_easy == "PMAX":
                char_limit_easy = {'headlines': 30, 'description': 90, 'long_headlines': 120}
                st.info("PMAX: Headlines=30, Description=90, Long Headlines=120")
            else:
                char_limit_easy = st.selectbox("Character Limit", [30, 50, 70, 90, 120, 200, 300, 500, 1000], index=1)

        generate_btn_easy = st.button("✨ Generate Multiple Variations (Easy)", type="primary")

    if generate_btn_easy:
        if not brand_name or not garment_type:
            st.error("⚠️ Please fill Brand Name and Garment Type")
            st.stop()

        data_easy = {
            'category': category_easy,
            'tone': tone_easy, 
            'product': garment_type,
            'brand': brand_name,
            'usp': usp_easy or "Premium Quality",
            'attributes': "Expertly crafted",
            'fabric': ", ".join(fabric_easy) if fabric_easy else "Premium materials",
            'festival': festival_easy,
            'discount': discount_easy,
            'timing': "Limited time",
            'char_limit': char_limit_easy,
            'emotion': "Special moments"
        }

        with st.spinner("✨ Generating multiple variations with Groq..."):
            try:
                variations = groq_generator.generate_variations(data_easy, category_easy)
                display_variations(variations, data_easy, "easy")
                
                # Action buttons
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("🔄 Generate New Set", use_container_width=True):
                        st.rerun()
                with col2:
                    # Download all variations as one file
                    all_content = "\n\n--- VARIATION SEPARATOR ---\n\n".join([v["content"] for v in variations])
                    st.download_button("📦 Download All", all_content, f"{brand_name}_all_variations.txt", use_container_width=True)
                
            except Exception as e:
                st.error(f"⚠️ Generation failed: {str(e)}")

# FLEXIBLE MODE - Similar structure
elif mode == "⚙️ Flexible Mode - Full Control":
    
    with st.sidebar:
        st.markdown("## ⚙️ Flexible Mode")
        
        with st.expander("🏷️ Product Information", expanded=True):
            product = st.text_input("Product/Brand Name", placeholder="e.g. Wedding Collection")
            brand = st.text_input("Brand Name", placeholder="e.g., Dolly J")
            usp = st.text_input("Unique Selling Point", placeholder="e.g., Effortless Glamour")
            attributes = st.text_area("Product Attributes", placeholder="e.g., Handcrafted, Premium comfort", height=80)
            fabric = st.multiselect("Fabric Types", FABRIC_TYPES)
            emotion = st.text_input("Emotional Hook", placeholder="e.g., Celebrate Bonds")
        
        with st.expander("⚙️ Content Settings", expanded=True):
            category = st.selectbox("Content Type", ["Email Subject Lines", "Long Content", "Concise Content", "PMAX", "WhatsApp Broadcast"])
            tone = st.selectbox("Brand Voice", ["Premium & Aspirational", "Warm & Personal", "Playful & Fun", "Sophisticated", "Friendly & Approachable", "Luxury & Exclusive"])
        
        with st.expander("🎯 Marketing Details", expanded=True):
            discount = st.number_input("Discount %", min_value=0, max_value=100, step=5, value=0)
            
            if category == "PMAX":
                char_limit = {'headlines': 30, 'description': 90, 'long_headlines': 120}
                st.info("PMAX: Headlines=30, Description=90, Long Headlines=120")
            else:
                char_limit = st.selectbox("Character Limit", [30, 50, 70, 90, 120, 200, 300, 500, 1000], index=1)
            
            festival = st.text_input("Festival/Occasion", placeholder="e.g., Raksha Bandhan")
            timing = st.text_input("Urgency Element", placeholder="e.g., 48 Hours Left")
        
        generate_btn = st.button("✨ Generate Multiple Variations (Flexible)", type="primary")
    
    if generate_btn:
        if not product:
            st.error("⚠️ Product/Brand name is required")
            st.stop()

        data = {
            'brand': brand,
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

        with st.spinner("✨ Generating multiple variations with Groq..."):
            try:
                variations = groq_generator.generate_variations(data, category)
                display_variations(variations, data, "flex")
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("🔄 Generate New Set", use_container_width=True, key="regen_flex"):
                        st.rerun()
                with col2:
                    all_content = "\n\n--- VARIATION SEPARATOR ---\n\n".join([v["content"] for v in variations])
                    st.download_button("📦 Download All", all_content, f"{product}_all_variations.txt", use_container_width=True, key="download_all_flex")
                
            except Exception as e:
                st.error(f"⚠️ Generation failed: {str(e)}")

# Footer
st.markdown("---")
st.markdown('<div style="text-align: center; color: #6c757d;">✨ Powered by Groq Llama 3.1 70B • Made for Premium Brands</div>', unsafe_allow_html=True)