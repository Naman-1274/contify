import os
import streamlit as st
import re
from groq import Groq
from dotenv import load_dotenv
from prompt_builder import PromptBuilder, BANNED_WORDS

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
        
        # Initialize Groq client and prompt builder
        self.client = Groq(api_key=self.api_key)
        self.prompt_builder = PromptBuilder()
        
        # Track generated content for uniqueness
        self.generated_hooks = set()
        self.generated_phrases = set()
    
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
    
    def generate_single_variation(self, data: dict, variation_number: int, content_type: str, 
                                model: str = "llama-3.1-8b-instant", streaming: bool = False, 
                                placeholder=None, max_retries: int = 3):
        """Generate single variation with enhanced uniqueness"""
        
        for attempt in range(max_retries):
            try:
                # Get unique prompt from prompt builder
                prompt = self.prompt_builder.build_unique_prompt(
                    data, variation_number, content_type, 
                    previous_hooks=list(self.generated_hooks),
                    previous_phrases=list(self.generated_phrases)
                )
                
                # Enhanced parameters for uniqueness per variation
                temperature = 0.7 + (variation_number * 0.2) + (attempt * 0.1)
                top_p = 0.8 + (variation_number * 0.1)
                
                params = {
                    "model": model,
                    "messages": [
                        {"role": "system", "content": f"You are creating variation #{variation_number}. Make it completely unique."},
                        {"role": "user", "content": prompt}
                    ],
                    "temperature": min(temperature, 1.5),  # Cap at 1.5
                    "max_completion_tokens": 1024,
                    "top_p": min(top_p, 1.0),  # Cap at 1.0
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
                            placeholder.markdown(f"**Generating Variation {variation_number} (Attempt {attempt+1})...**\n\n```\n{full_content}\n```")
                    result = full_content
                else:
                    result = completion.choices[0].message.content
                
                # Validate and clean result
                if self._validate_content(result, content_type):
                    cleaned_result = self._clean_and_format_content(result, data, content_type)
                    
                    # Check uniqueness against previous generations
                    if self._is_unique_content(cleaned_result, variation_number):
                        # Store hooks and phrases for future uniqueness checks
                        self._extract_and_store_elements(cleaned_result)
                        return cleaned_result
                    elif attempt < max_retries - 1:
                        continue  # Try again with different parameters
                    else:
                        # Last attempt - accept but mark as less unique
                        return self._create_fallback_content(data, content_type, variation_number)
                else:
                    if attempt < max_retries - 1:
                        continue
                    else:
                        return self._create_fallback_content(data, content_type, variation_number)
                        
            except Exception as e:
                if attempt == max_retries - 1:
                    if "authentication" in str(e).lower():
                        raise Exception("Invalid API key. Check your GROQ_API_KEY.")
                    elif "rate limit" in str(e).lower():
                        raise Exception("Rate limit exceeded. Try again in a few minutes.")
                    elif "quota" in str(e).lower():
                        raise Exception("API quota exceeded. Check your Groq billing.")
                    else:
                        raise Exception(f"Groq API error: {str(e)}")
                continue
        
        return self._create_fallback_content(data, content_type, variation_number)
    
    def _validate_content(self, content: str, content_type: str) -> bool:
        """Validate content structure and quality"""
        if not content or len(content.strip()) < 10:
            return False
        
        content = content.strip()
        lines = [line.strip() for line in content.split('\n') if line.strip()]
        
        if content_type == "PMAX":
            required_sections = ["Headlines:", "Descriptions:", "Long Headlines:"]
            return all(section in content for section in required_sections)
        else:
            # Should have at least 3 meaningful lines for other formats
            if len(lines) < 3:
                return False
            
            # Check for unwanted labels in first few lines
            unwanted_labels = ['headline:', 'subject:', 'description:', 'cta:', 'title:']
            for line in lines[:3]:
                if any(label in line.lower() for label in unwanted_labels):
                    return False
        
        return True
    
    def _is_unique_content(self, content: str, variation_number: int) -> bool:
        """Check if content is unique compared to previous variations"""
        if variation_number == 1:
            return True  # First variation is always unique
        
        lines = content.split('\n\n')
        if not lines:
            return False
        
        # Check first line (headline) uniqueness
        first_line = lines[0].strip().lower()
        first_words = ' '.join(first_line.split()[:3])
        
        # If first 3 words already used, it's not unique enough
        if first_words in self.generated_phrases:
            return False
        
        return True
    
    def _extract_and_store_elements(self, content: str):
        """Extract and store hooks and phrases for uniqueness tracking"""
        lines = content.split('\n\n')
        for line in lines:
            if line.strip():
                # Store first 3 words as key phrase
                first_words = ' '.join(line.strip().lower().split()[:3])
                self.generated_phrases.add(first_words)
                
                # Store first word as hook
                first_word = line.strip().split()[0].lower() if line.strip() else ""
                if first_word:
                    self.generated_hooks.add(first_word)
    
    def _clean_and_format_content(self, content: str, data: dict, content_type: str) -> str:
        """Clean and format content according to requirements"""
        # Remove labels and unwanted formatting
        content = re.sub(r'^(headline|subject|description|cta):\s*', '', content, flags=re.IGNORECASE | re.MULTILINE)
        content = re.sub(r'^[•\-\*]\s*', '', content, flags=re.MULTILINE)
        content = re.sub(r'^[0-9]+\.\s*', '', content, flags=re.MULTILINE)
        
        # Remove banned words
        for word in BANNED_WORDS:
            pattern = r'\b' + re.escape(word) + r'\b'
            content = re.sub(pattern, '', content, flags=re.IGNORECASE)
        
        # Clean up spaces
        content = re.sub(r'\s+', ' ', content).strip()
        
        if content_type == "PMAX":
            return self._format_pmax_content(content, data)
        else:
            return self._format_standard_content(content, data, content_type)
    
    def _format_pmax_content(self, content: str, data: dict) -> str:
        """Format PMAX content with proper structure"""
        # Implementation for PMAX formatting
        lines = [line.strip() for line in content.split('\n') if line.strip()]
        
        headlines = []
        descriptions = []
        long_headlines = []
        
        current_section = None
        for line in lines:
            if 'headline' in line.lower() and 'long' not in line.lower():
                current_section = 'headlines'
                continue
            elif 'description' in line.lower():
                current_section = 'descriptions'
                continue
            elif 'long headline' in line.lower():
                current_section = 'long_headlines'
                continue
            
            if current_section == 'headlines' and len(headlines) < 15:
                headlines.append(line[:30])
            elif current_section == 'descriptions' and len(descriptions) < 5:
                descriptions.append(line[:90])
            elif current_section == 'long_headlines' and len(long_headlines) < 5:
                long_headlines.append(line[:120])
        
        # Build formatted result
        result = "Headlines:\n"
        for h in headlines[:15]:
            result += f"{h}\n"
        result += "\nDescriptions:\n"
        for d in descriptions[:5]:
            result += f"{d}\n"
        result += "\nLong Headlines:\n"
        for lh in long_headlines[:5]:
            result += f"{lh}\n"
        
        return result.strip()
    
    def _format_standard_content(self, content: str, data: dict, content_type: str) -> str:
        """Format standard 3-line content"""
        lines = [line.strip() for line in content.split('\n') if line.strip()]
        filtered_lines = []
        
        for line in lines:
            if len(line) > 2 and not re.match(r'^[-=_]{3,}$', line):
                if not any(label in line.lower() for label in ['headline:', 'subject:', 'description:', 'cta:']):
                    filtered_lines.append(line)
        
        if len(filtered_lines) < 3:
            return self._create_fallback_content(data, content_type, 1)
        
        headline = filtered_lines[0]
        description = filtered_lines[1]
        cta = filtered_lines[2] if len(filtered_lines) > 2 else "Shop Now"
        
        # Apply character limits
        char_limit = data.get('char_limit', 300)
        if isinstance(char_limit, int) and content_type == "Email Subject Lines":
            headline = headline[:char_limit]
        
        return f"{headline}\n\n{description}\n\n{cta}"
    
    def _create_fallback_content(self, data: dict, content_type: str, variation_number: int) -> str:
        """Create fallback content when generation fails"""
        return self.prompt_builder.create_fallback_content(data, content_type, variation_number)
    
    def generate_variations(self, data: dict, content_type: str, model: str, streaming: bool = False):
        """Generate 3 unique variations"""
        
        if not self.test_connection():
            st.warning("Connection test failed, but continuing with generation...")
        
        # Reset uniqueness tracking for new generation
        self.generated_hooks.clear()
        self.generated_phrases.clear()
        
        variations = []
        
        # Create streaming placeholders if needed
        placeholders = []
        if streaming:
            st.markdown("### 🎬 Live Generation")
            for i in range(3):
                st.markdown(f"**Variation {i+1}:**")
                placeholders.append(st.empty())
                st.markdown("---")
        
        # Generate 3 variations with different approaches
        for i in range(3):
            try:
                placeholder = placeholders[i] if streaming and i < len(placeholders) else None
                
                response = self.generate_single_variation(
                    data, i + 1, content_type, model, streaming, placeholder, max_retries=3
                )
                
                if response and len(response.strip()) > 10:
                    variations.append({
                        "variation": i + 1,
                        "style": self._get_variation_style_name(i + 1),
                        "content": response,
                        "char_count": len(response),
                        "word_count": len(response.split()) if response else 0,
                        "model_used": model
                    })
                else:
                    # Create fallback variation
                    fallback_content = self._create_fallback_content(data, content_type, i + 1)
                    variations.append({
                        "variation": i + 1,
                        "style": f"Fallback {i + 1}",
                        "content": fallback_content,
                        "char_count": len(fallback_content),
                        "word_count": len(fallback_content.split()),
                        "model_used": model
                    })
                    
            except Exception as e:
                st.error(f"Error in variation {i+1}: {str(e)}")
                error_content = self._create_fallback_content(data, content_type, i + 1)
                variations.append({
                    "variation": i + 1,
                    "style": f"Error - Variation {i + 1}",
                    "content": error_content,
                    "char_count": len(error_content),
                    "word_count": len(error_content.split()),
                    "model_used": model
                })
        
        return self._ensure_valid_variations(variations, model)
    
    def _get_variation_style_name(self, variation_number: int) -> str:
        """Get descriptive style name for variation"""
        styles = {
            1: "Direct & Feature-Focused",
            2: "Emotional & Question-Based", 
            3: "Storytelling & Aspirational"
        }
        return styles.get(variation_number, f"Variation {variation_number}")
    
    def _ensure_valid_variations(self, variations, model):
        """Ensure all variations have required keys and valid content"""
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

# Rest of your Streamlit UI code remains the same...
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

def display_variations(variations, data):
    """Display variations in a structured format with enhanced readability"""
    if not variations or not variations[0].get('content'):
        st.error("No variations generated")
        return
    
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
            formatted_content = variation.get("content", "No content").replace("\n", "<br>")
            st.markdown(f'<div class="variation-card">{formatted_content}</div>', unsafe_allow_html=True)
            
            col1, col2 = st.columns([2, 1])
            with col1:
                st.code(variation.get("content", "No content"), language="text")
            with col2:
                st.caption(f"🤖 {variation.get('model_used', 'Unknown')}")
                st.download_button(
                    "📥 Download",
                    variation.get("content", "No content"),
                    f"{data.get('brand', 'content')}_{data['category']}_v{variation.get('variation', i+1)}.txt",
                    key=f"download_{i}"
                )

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
st.markdown("✨ **Powered by Groq & Enhanced Prompt Builder** • Made for Premium Fashion Brands")