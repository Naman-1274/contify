import os
import streamlit as st
import re
from groq import Groq
from dotenv import load_dotenv
from prompt_builder import build_prompt, BANNED_WORDS

load_dotenv()

class GroqContentGenerator:
    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")
        
        # Validate API key
        if not self.api_key:
            st.error("⚠️ GROQ_API_KEY not found in environment variables. Please set it in your .env file.")
            st.stop()
        
        if not self.api_key.startswith("gsk_"):
            st.error("⚠️ Invalid GROQ_API_KEY format. It should start with 'gsk_'")
            st.stop()
        
        # Initialize Groq client
        self.client = Groq(api_key=self.api_key)
        
        # Style variations for different creative approaches
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
    
    def test_connection(self):
        """Test API connection"""
        try:
            completion = self.client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role": "user", "content": "Hello"}],
                temperature=1,
                max_completion_tokens=5,
                top_p=1,
                stream=False,
                stop=None
            )
            return True
        except Exception as e:
            st.warning(f"Connection test failed: {str(e)}")
            return False
    
    def generate_single_variation(self, prompt: str, model: str = "llama-3.1-8b-instant", streaming: bool = False, placeholder=None):
        """Generate single variation using standard Groq models"""
        try:
            # Standard parameters for all models
            params = {
                "model": model,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.8,
                "max_completion_tokens": 1024,
                "top_p": 0.9,
                "stream": streaming,
                "stop": None
            }
            
            completion = self.client.chat.completions.create(**params)
            
            if streaming and placeholder:
                full_content = ""
                for chunk in completion:
                    if chunk.choices[0].delta.content:
                        content_chunk = chunk.choices[0].delta.content
                        full_content += content_chunk
                        placeholder.markdown(f"**Generating...**\n\n```\n{full_content}\n```")
                return full_content
            else:
                return completion.choices[0].message.content
                
        except Exception as e:
            if "authentication" in str(e).lower():
                raise Exception("Invalid API key. Check your GROQ_API_KEY.")
            elif "rate limit" in str(e).lower():
                raise Exception("Rate limit exceeded. Try again in a few minutes.")
            elif "quota" in str(e).lower():
                raise Exception("API quota exceeded. Check your Groq billing.")
            else:
                raise Exception(f"Groq API error: {str(e)}")
    
    def generate_variations(self, data: dict, content_type: str, model: str, streaming: bool = False):
        """Generate 3 variations with different styles"""
        
        if not self.test_connection():
            st.warning("Connection test failed, but continuing with generation...")
            # Don't return error, continue with generation attempt
        
        styles = self.variation_styles.get(content_type, ["standard", "creative", "premium"])
        variations = []
        
        # Create streaming placeholders if needed
        placeholders = []
        if streaming:
            st.markdown("### 🎬 Live Generation")
            for i, style in enumerate(styles):
                st.markdown(f"**Variation {i+1} - {style.replace('_', ' ').title()}:**")
                placeholders.append(st.empty())
                st.markdown("---")
        
        for i, style in enumerate(styles):
            try:
                # Enhance data with style-specific elements
                enhanced_data = self._enhance_data_for_style(data, style)
                
                # Build prompt using your prompt_builder
                base_prompt = build_prompt(enhanced_data)
                
                # Add style-specific creative direction
                final_prompt = self._add_style_instructions(base_prompt, style)
                
                # Generate content
                placeholder = placeholders[i] if streaming and i < len(placeholders) else None
                response = self.generate_single_variation(
                    final_prompt, 
                    model, 
                    streaming, 
                    placeholder
                )
                
                if response:
                    # Clean and process content
                    clean_content = self._clean_content(response, enhanced_data, content_type)
                    structured = self._enforce_structure(clean_content, content_type)
                    variations.append({
                        "variation": i + 1,
                        "style": style.replace('_', ' ').title(),
                        "content": clean_content,
                        "char_count": len(clean_content),
                        "word_count": len(clean_content.split()) if clean_content else 0,
                        "model_used": model
                    })
                else:
                    # Handle empty response
                    variations.append({
                        "variation": i + 1,
                        "style": f"Error - {style.replace('_', ' ').title()}",
                        "content": "No content generated",
                        "char_count": 0,
                        "word_count": 0,
                        "model_used": model
                    })
                    
            except Exception as e:
                st.error(f"Error in variation {i+1}: {str(e)}")
                # Add error variation with style key to prevent KeyError
                variations.append({
                    "variation": i + 1,
                    "style": f"Error - {style.replace('_', ' ').title()}",
                    "content": f"Generation failed: {str(e)}",
                    "char_count": 0,
                    "word_count": 0,
                    "model_used": model
                })
        
        # Ensure we always return variations with all required keys
        if not variations:
            variations = [{
                "variation": 1, 
                "style": "Default", 
                "content": "Generation failed - please try again", 
                "char_count": 0,
                "word_count": 0,
                "model_used": model
            }]
        
        # Validate all variations have required keys
        for i, var in enumerate(variations):
            if not isinstance(var, dict):
                variations[i] = {
                    "variation": i + 1,
                    "style": "Error",
                    "content": "Invalid response format",
                    "char_count": 0,
                    "word_count": 0,
                    "model_used": model
                }
            else:
                # Ensure all required keys exist
                required_keys = ["variation", "style", "content", "char_count", "word_count", "model_used"]
                for key in required_keys:
                    if key not in var:
                        if key == "variation":
                            var[key] = i + 1
                        elif key == "style":
                            var[key] = "Unknown"
                        elif key == "content":
                            var[key] = "No content"
                        elif key == "char_count":
                            var[key] = len(var.get("content", ""))
                        elif key == "word_count":
                            var[key] = len(var.get("content", "").split()) if var.get("content") else 0
                        elif key == "model_used":
                            var[key] = model
            
        return variations
    
    def _enhance_data_for_style(self, data: dict, style: str) -> dict:
        """Enhance data based on creative style"""
        enhanced = data.copy()
        
        style_enhancements = {
            "curiosity_hook": {"emotion": "Mystery & anticipation", "tone": "Intriguing"},
            "urgency_driven": {"emotion": "FOMO urgency", "timing": "Ending soon", "tone": "Time-sensitive"},
            "benefit_focused": {"emotion": "Transformation confidence", "tone": "Benefit-driven"},
            "friend_recommendation": {"emotion": "Excited discovery", "tone": "Friend sharing"},
            "personal_stylist": {"emotion": "Expert confidence", "tone": "Professional advice"},
            "exclusive_insider": {"emotion": "VIP special", "tone": "Exclusive access"},
            "lifestyle_moment": {"emotion": "Aspirational living", "tone": "Scene-setting"},
            "product_spotlight": {"emotion": "Quality appreciation", "tone": "Craftsmanship focus"},
            "emotion_first": {"emotion": "Deep connection", "tone": "Feeling-centered"},
            "storytelling_approach": {"emotion": "Narrative engagement", "tone": "Story-driven"},
            "feature_benefits": {"emotion": "Smart confidence", "tone": "Informative"},
            "aspirational_lifestyle": {"emotion": "Premium elevation", "tone": "Luxury lifestyle"},
            "brand_focused": {"emotion": "Brand trust", "tone": "Authority"},
            "product_driven": {"emotion": "Product excitement", "tone": "Feature hero"},
            "occasion_centered": {"emotion": "Perfect timing", "tone": "Occasion-perfect"}
        }
        
        if style in style_enhancements:
            enhanced.update(style_enhancements[style])
            
        return enhanced
    
    def _add_style_instructions(self, base_prompt: str, style: str) -> str:
        """Add creative style instructions to prompt. Style hints must NOT break required format."""
        style_instructions = {
            "curiosity_hook": "\n\nSTYLE: Use curiosity and intrigue while remaining fully complete. Do NOT use ellipses '...' or incomplete fragments. Follow the required output format exactly.",
            "urgency_driven": "\n\nSTYLE: Build clear time pressure in a human voice (e.g., 'Last chance', 'Ends tonight') but keep all lines complete and within char limits. Follow the required output format exactly.",
            "benefit_focused": "\n\nSTYLE: Lead with transformation and benefits — complete, human sentences. Keep it concise and within char limits. Follow the required output format exactly.",
            "friend_recommendation": "\n\nSTYLE: Write like you're texting a close friend — warm, short, and conversational. Keep the format exact.",
            "personal_stylist": "\n\nSTYLE: Professional but friendly styling note. Complete sentences only. Follow the required format exactly.",
            "exclusive_insider": "\n\nSTYLE: VIP tone but still human and direct. No extra commentary. Follow the required format exactly.",
            "lifestyle_moment": "\n\nSTYLE: Paint a brief scene or moment — complete sentences only. Follow the required format exactly.",
            "product_spotlight": "\n\nSTYLE: Focus on product details in a human voice. Keep all lines complete and within char limits. Follow the required format exactly.",
            "emotion_first": "\n\nSTYLE: Start with feeling and connect to product. Full sentences only. Follow the required format exactly.",
            "storytelling_approach": "\n\nSTYLE: Tell a short, complete micro-story (if allowed by format). Keep to the required output structure and char limits.",
            "feature_benefits": "\n\nSTYLE: Highlight features and benefits in short complete lines. Keep the required format and char limits.",
            "aspirational_lifestyle": "\n\nSTYLE: Paint an aspirational moment in human language but keep concise and within char limits.",
            "brand_focused": "\n\nSTYLE: Lead with brand/collection tone in a human way. Keep outputs complete and in required format.",
            "product_driven": "\n\nSTYLE: Make the product the hero while staying conversational and within the required format.",
            "occasion_centered": "\n\nSTYLE: Make the occasion central, keep lines complete, follow the exact format."
        }

        instruction = style_instructions.get(style, "\n\nSTYLE: Generate natural, conversational copy. Follow the required output format exactly.")
        # Ensure the style instruction ends with an explicit requirement
        instruction += "\n\nENFORCE: Output ONLY the required 3-line format. No extra text."
        return base_prompt + instruction

    
    def _clean_content(self, content: str, data: dict, content_type: str) -> str:
        """Clean content according to requirements"""
        
        # Remove extra whitespace
        cleaned = re.sub(r'\s+', ' ', content.strip())
        
        # Remove banned words (whole words only)
        for word in BANNED_WORDS:
            pattern = r'\b' + re.escape(word) + r'\b'
            cleaned = re.sub(pattern, '', cleaned, flags=re.IGNORECASE)
        
        # Clean up spaces
        cleaned = re.sub(r'\s+', ' ', cleaned).strip()
        
        # Apply character limits (except PMAX which has its own structure)
        if content_type != "PMAX":
            char_limit = data.get('char_limit', 300)
            if isinstance(char_limit, int) and len(cleaned) > char_limit:
                # Try to cut at sentence boundary
                sentences = cleaned.split('. ')
                truncated = sentences[0]
                for sentence in sentences[1:]:
                    if len(truncated + '. ' + sentence) <= char_limit - 3:
                        truncated += '. ' + sentence
                    else:
                        break
                if len(truncated) < len(cleaned):
                    cleaned = truncated + "..."
        
        return cleaned

    def _enforce_structure(self, text: str, content_type: str) -> str:
        text = text.strip()
        parts = [p.strip() for p in re.split(r'\n\s*\n', text) if p.strip()]
        if len(parts) >= 3:
            return parts[0] + "\n\n" + parts[1] + "\n\n" + parts[2]
        sentences = [s.strip() for s in re.split(r'(?<=[\.\?\!])\s+', text) if s.strip()]
        if len(sentences) >= 3:
            return sentences[0] + "\n\n" + sentences[1] + "\n\n" + sentences[2]
        cta_match = re.search(r'(Shop Now|Explore Now|See Collection|Get Yours|Buy Now|Check it out|Check it out now|Take a look|Shop curated looks)', text, flags=re.I)
        if cta_match:
            cta = cta_match.group(0).strip()
            body = re.sub(re.escape(cta), '', text, flags=re.I).strip()
            parts2 = re.split(r'[-–—:]\s*', body, maxsplit=1)
            if len(parts2) == 2:
                headline = parts2[0].strip()
                desc = parts2[1].strip()
            else:
                words = body.split()
                headline = ' '.join(words[:min(7, len(words))]).strip()
                desc = ' '.join(words[min(7, len(words)):]).strip()
            if not desc:
                desc = headline
            return headline + "\n\n" + desc + "\n\n" + cta

        # 4) last resort: split by word count
        words = text.split()
        if len(words) <= 10:
            return text + "\n\n" + "" + "\n\n" + "Explore Now"
        headline = ' '.join(words[:7])
        desc = ' '.join(words[7:22])
        return headline.strip() + "\n\n" + desc.strip() + "\n\n" + "Shop Now"

st.set_page_config(
    page_title="AI Fashion Copywriter", 
    page_icon="✨", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Check API key
if not os.getenv("GROQ_API_KEY"):
    st.error("⚠️ GROQ_API_KEY not found!")
    st.markdown("""
    ### Setup Instructions:
    1. Install: `pip install groq`
    2. Create `.env` file with: `GROQ_API_KEY=gsk_your_key_here`
    3. Get key from: https://console.groq.com/keys
    4. Restart app
    """)
    st.stop()

# Initialize generator
@st.cache_resource
def init_generator():
    return GroqContentGenerator()

generator = init_generator()

# Styling
st.markdown("""
<style>
    .main-title {
        text-align: center;
        color: #1f77b4;
        font-size: 2.8rem;
        font-weight: 700;
        margin-bottom: 1rem;
    }
    
    .stButton > button {
        width: 100%;
        height: 3rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 12px;
        font-size: 1.1rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .variation-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 1.8rem;
        border-radius: 12px;
        margin: 1rem 0;
        color: white;
        font-size: 1.1rem;
        line-height: 1.6;
        box-shadow: 0 6px 20px rgba(0,0,0,0.15);
    }
    
    .metric-card {
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Constants
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

# Header
st.markdown('<h1 class="main-title">✨ AI Fashion Copywriter</h1>', unsafe_allow_html=True)
st.markdown("### Professional ad copy with multiple creative variations")

# Model and streaming selection
col1, col2, col3 = st.columns([2, 1, 1])
with col1:
    model_options = {
        "💡 Gemma2 9B": "gemma2-9b-it",
        "⚡ Llama 3.1 8B (Fastest)": "llama-3.1-8b-instant"
    }
    selected_model_name = st.selectbox("🤖 AI Model", list(model_options.keys()))
    selected_model = model_options[selected_model_name]

with col2:
    enable_streaming = st.toggle("🎬 Live Streaming", help="Watch generation in real-time")

# Mode selection
mode = st.radio(
    "Generation Mode:",
    ["🎯 Easy Mode", "⚙️ Advanced Mode"],
    horizontal=True
)

def display_variations(variations, data):
    """Display generated variations in a single table"""
    
    if not variations or not variations[0].get('content'):
        st.error("No variations generated")
        return
    
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f'<div class="metric-card"><b>{data["category"]}</b></div>', unsafe_allow_html=True)
    with col2:
        avg_chars = sum(v['char_count'] for v in variations) // len(variations)
        st.markdown(f'<div class="metric-card"><b>{avg_chars} avg chars</b></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="metric-card"><b>{data.get("discount", 0)}% OFF</b></div>', unsafe_allow_html=True)
    with col4:
        st.markdown(f'<div class="metric-card"><b>{len(variations)} Variations</b></div>', unsafe_allow_html=True)
    
    # Single table with all variations
    st.markdown("### 🎯 Generated Variations")
    
    # Create table data
    table_data = []
    for i, variation in enumerate(variations):
        table_data.append({
            "Variation": f"#{variation.get('variation', i+1)}",
            "Style": variation.get('style', 'Default'),
            "Content": variation.get('content', 'No content'),
            "Characters": variation.get('char_count', 0),
            "Words": variation.get('word_count', 0),
            "Model": variation.get('model_used', 'Unknown')
        })
    
    # Display as dataframe
    import pandas as pd
    df = pd.DataFrame(table_data)
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Variation": st.column_config.TextColumn("Variation", width="small"),
            "Style": st.column_config.TextColumn("Style", width="medium"),
            "Content": st.column_config.TextColumn("Content", width="large"),
            "Characters": st.column_config.NumberColumn("Chars", width="small"),
            "Words": st.column_config.NumberColumn("Words", width="small"),
            "Model": st.column_config.TextColumn("Model", width="medium")
        }
    )
    
    # Individual variation cards for better readability
    st.markdown("### 📝 Detailed View")
    for i, variation in enumerate(variations):
        with st.expander(f"Variation {variation.get('variation', i+1)} - {variation.get('style', 'Default')} ({variation.get('char_count', 0)} chars)"):
            # Display content in card format
            st.markdown(f'<div class="variation-card">{variation.get("content", "No content")}</div>', unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns([2, 1, 1])
            with col1:
                st.code(variation.get("content", "No content"), language="text")
            with col2:
                st.metric("Characters", variation.get("char_count", 0))
                st.metric("Words", variation.get("word_count", 0))
            with col3:
                st.caption(f"🤖 {variation.get('model_used', 'Unknown')}")
                st.download_button(
                    "📥 Download",
                    variation.get("content", "No content"),
                    f"{data.get('brand', 'content')}_{data['category']}_v{variation.get('variation', i+1)}.txt",
                    key=f"download_{i}"
                )

# EASY MODE
if mode == "🎯 Easy Mode":
    
    with st.sidebar:
        st.markdown("## 🎯 Easy Mode")
        
        with st.expander("🏷️ Product Details", expanded=True):
            garment_type = st.selectbox("Garment Type", GARMENT_TYPES)
            brand_name = st.text_input("Brand Name", placeholder="e.g., Dolly J, Safaa")
            usp = st.text_input("Unique Selling Point", placeholder="e.g., Effortless Glamour")
        
        with st.expander("🎨 Style Details", expanded=True):
            fabric = st.multiselect("Fabric Types", FABRIC_TYPES[:10])
            festival = st.selectbox("Occasion", FESTIVALS_OCCASIONS)
        
        with st.expander("⚙️ Campaign Settings", expanded=True):
            category = st.selectbox("Content Type", 
                ["Email Subject Lines", "Long Content", "Concise Content", "PMAX", "WhatsApp Broadcast"])
            tone = st.selectbox("Brand Voice", 
                ["Premium & Aspirational", "Warm & Personal", "Playful & Fun", "Sophisticated", "Friendly & Approachable", "Luxury & Exclusive"])
            discount = st.number_input("Discount %", min_value=0, max_value=100, step=5, value=0)
            
            if category == "PMAX":
                char_limit = {'headlines': 30, 'description': 90, 'long_headlines': 120}
                st.info("PMAX: Headlines=30, Descriptions=90, Long Headlines=120")
            elif category == "Email Subject Lines":
                char_limit = st.selectbox("Character Limit", [200, 250, 300], index=0)
            elif category == "WhatsApp Broadcast":
                char_limit = st.selectbox("Character Limit", [400, 450, 500], index=0)
            elif category == "Concise Content":
                char_limit = st.selectbox("Character Limit", [120, 200, 300], index=0)
            elif category == "Long Content":
                char_limit = st.selectbox("Character Limit", [300, 500, 1000], index=0)
            else:
                char_limit = st.selectbox("Character Limit", [300], index=0)
        
        generate_btn = st.button("✨ Generate Variations", type="primary")
    
    if generate_btn:
        if not brand_name or not garment_type:
            st.error("Please fill Brand Name and Garment Type")
            st.stop()
        
        data = {
            'category': category,
            'tone': tone,
            'product': garment_type,
            'brand': brand_name,
            'usp': usp or "Premium Quality",
            'attributes': "Expertly crafted",
            'fabric': ", ".join(fabric) if fabric else "Premium materials",
            'festival': festival,
            'discount': discount,
            'timing': "Limited time",
            'char_limit': char_limit,
            'emotion': "Special moments"
        }
        
        with st.spinner("✨ Generating variations..."):
            try:
                variations = generator.generate_variations(
                    data, category, selected_model, enable_streaming
                )
                
                if not enable_streaming:
                    display_variations(variations, data)
                else:
                    st.markdown("### 📊 Final Results")
                    display_variations(variations, data)
                
                # Action buttons
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("🔄 Generate New Set"):
                        st.rerun()
                with col2:
                    all_content = "\n\n--- VARIATION ---\n\n".join([v["content"] for v in variations])
                    st.download_button("📦 Download All", all_content, f"{brand_name}_variations.txt")
                    
            except Exception as e:
                st.error(f"Generation failed: {str(e)}")

elif mode == "⚙️ Advanced Mode":
    
    with st.sidebar:
        st.markdown("## ⚙️ Advanced Mode")
        
        with st.expander("🏷️ Product Information", expanded=True):
            product = st.text_input("Product Name", placeholder="e.g., Wedding Collection")
            brand = st.text_input("Brand Name", placeholder="e.g., Dolly J")
            usp = st.text_input("Unique Selling Point", placeholder="e.g., Effortless Glamour")
            attributes = st.text_area("Product Attributes", placeholder="e.g., Handcrafted, Premium comfort")
            fabric = st.multiselect("Fabric Types", FABRIC_TYPES)
            emotion = st.text_input("Emotional Hook", placeholder="e.g., Celebrate Bonds")
        
        with st.expander("⚙️ Content Settings", expanded=True):
            category = st.selectbox("Content Type", 
                ["Email Subject Lines", "Long Content", "Concise Content", "PMAX", "WhatsApp Broadcast"])
            tone = st.selectbox("Brand Voice", 
                ["Premium & Aspirational", "Warm & Personal", "Playful & Fun", "Sophisticated", "Friendly & Approachable", "Luxury & Exclusive"])
        
        with st.expander("🎯 Marketing Details", expanded=True):
            discount = st.number_input("Discount %", min_value=0, max_value=100, step=5, value=0)
            
            if category == "PMAX":
                char_limit = {'headlines': 30, 'description': 90, 'long_headlines': 120}
                st.info("PMAX: Headlines=30, Descriptions=90, Long Headlines=120")

            elif category == "Email Subject Lines":
                char_limit = st.selectbox("Character Limit", [30, 50, 70], index=0)

            elif category == "WhatsApp Broadcast":
                char_limit = st.selectbox("Character Limit", [90, 120, 200], index=0)

            elif category == "Concise Content":
                char_limit = st.selectbox("Character Limit", [120, 200, 300], index=0)

            elif category == "Long Content":
                char_limit = st.selectbox("Character Limit", [300, 500, 1000], index=0)

            else:
                # fallback for unexpected categories
                char_limit = st.selectbox("Character Limit", [300], index=0)
            
            festival = st.text_input("Festival/Occasion", placeholder="e.g., Raksha Bandhan")
            timing = st.text_input("Urgency Element", placeholder="e.g., 48 Hours Left")
        
        generate_btn = st.button("✨ Generate Variations", type="primary")
    
    if generate_btn:
        if not product:
            st.error("Product name is required")
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
        
        with st.spinner("✨ Generating variations..."):
            try:
                variations = generator.generate_variations(
                    data, category, selected_model, enable_streaming
                )
                
                if not enable_streaming:
                    display_variations(variations, data)
                else:
                    st.markdown("### 📊 Final Results")
                    display_variations(variations, data)
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("🔄 Generate New Set"):
                        st.rerun()
                with col2:
                    all_content = "\n\n--- VARIATION ---\n\n".join([v["content"] for v in variations])
                    st.download_button("📦 Download All", all_content, f"{product}_variations.txt")
                    
            except Exception as e:
                st.error(f"Generation failed: {str(e)}")

# Footer
st.markdown("---")
st.markdown("✨ **Powered by Groq & Your Sophisticated Prompt Builder** • Made for Premium Fashion Brands")