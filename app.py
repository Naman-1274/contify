import os
import streamlit as st
import time
import pandas as pd
from groq import Groq
from dotenv import load_dotenv
from prompt_builder import ImprovedPromptBuilder

load_dotenv()

class GroqContentGenerator:
    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")
        if not self.api_key or not self.api_key.startswith("gsk_"):
            st.error("Invalid GROQ_API_KEY. Please check your .env file.")
            st.stop()
        
        self.client = Groq(api_key=self.api_key)
        self.prompt_builder = ImprovedPromptBuilder()
    
    def test_connection(self):
        try:
            self.client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role": "user", "content": "Test"}],
                max_completion_tokens=5
            )
            return True
        except Exception as e:
            st.error(f"Connection failed: {self._handle_error(e)}")
            return False
    
    def generate_single_variation(self, data: dict, variation_number: int, content_type: str, 
                                model: str, streaming: bool = False, placeholder=None):
        try:
            prompt = self.prompt_builder.build_focused_prompt(data, variation_number, content_type)
            
            # Simple parameter variation
            temperature = 0.7 + (variation_number * 0.1)
            top_p = 0.85 + (variation_number * 0.05)
            
            params = {
                "model": model,
                "messages": [
                    {"role": "system", "content": f"You are a professional fashion copywriter creating variation {variation_number}."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": temperature,
                "max_completion_tokens": 800,
                "top_p": top_p,
                "stream": streaming
            }
            
            completion = self.client.chat.completions.create(**params)
            
            if streaming and placeholder:
                full_content = ""
                for chunk in completion:
                    if chunk.choices[0].delta.content:
                        full_content += chunk.choices[0].delta.content
                        placeholder.markdown(f"**Variation {variation_number}**\n\n{full_content}")
                return self._clean_content(full_content, data, content_type)
            else:
                result = completion.choices[0].message.content
                return self._clean_content(result, data, content_type)
                
        except Exception as e:
            st.error(f"Generation error: {self._handle_error(e)}")
            return self.prompt_builder.create_fallback_content(data, content_type, variation_number)
    
    def generate_variations(self, data: dict, content_type: str, model: str, streaming: bool = False):
        if not self.test_connection():
            return []
        
        # Reset session state for new generation
        self._reset_session_state()
        
        variations = []
        progress_bar = st.progress(0, text="Starting generation...")
        
        for i in range(3):
            progress_bar.progress(i / 3, text=f"Generating variation {i+1}/3...")
            
            placeholder = st.empty() if streaming else None
            if streaming:
                st.markdown(f"### Variation {i+1}")
                placeholder = st.empty()
            
            response = self.generate_single_variation(
                data, i + 1, content_type, model, streaming, placeholder
            )
            
            if response:
                variations.append({
                    "variation": i + 1,
                    "style": self._get_style_name(i + 1),
                    "content": response,
                    "char_count": len(response),
                    "word_count": len(response.split()),
                    "model_used": model,
                    "generation_time": time.strftime("%H:%M:%S")
                })
                
                # Store for uniqueness tracking
                self._store_content(response)
        
        progress_bar.progress(1.0, text="Generation complete!")
        time.sleep(0.5)
        progress_bar.empty()
        
        return variations
    
    def _clean_content(self, content: str, data: dict, content_type: str) -> str:
        if not content:
            return self.prompt_builder.create_fallback_content(data, content_type, 1)
        
        # Remove unwanted labels and formatting
        lines = []
        for line in content.split('\n'):
            line = line.strip()
            if line and not any(label in line.lower() for label in 
                              ['headline:', 'subject:', 'description:', 'cta:', 'variation', 'format:', 'line 1:', 'line 2:']):
                lines.append(line)
        
        # Handle PMAX format specifically
        if content_type == "PMAX":
            return self._format_pmax_content(content, data)
        
        # Handle Email format (subject + body + cta)
        if content_type == "Email Subject Lines":
            return self._format_email_content(lines, data)
        
        # WhatsApp format (5 lines for storytelling)
        if content_type == "WhatsApp Broadcast":
            return self._format_whatsapp_content(lines, data)
        
        # Concise Content (3 lines: headline + 1 description + cta)
        if content_type == "Concise Content":
            return self._format_concise_content(lines, data)
        
        # Long Content (4 lines: headline + 2 description + cta)  
        if content_type == "Long Content":
            return self._format_long_content(lines, data)
        
        # Standard format fallback
        filtered_lines = [line for line in lines if len(line) > 3][:3]
        while len(filtered_lines) < 3:
            filtered_lines.append("Shop Now")
        
        return '\n\n'.join(filtered_lines)
    
    def _format_email_content(self, lines: list, data: dict) -> str:
        """Format email: subject + body + cta (3 lines)"""
        subject_line = ""
        body_line = ""
        cta_line = ""
        
        for line in lines:
            if len(line) > 5:  # Substantial content
                if not subject_line:
                    subject_line = line.replace('**', '').strip()
                elif not body_line and line != subject_line and len(line) > 20:
                    body_line = line.strip()
                elif not cta_line and len(line.split()) <= 4 and line != subject_line and line != body_line:
                    cta_line = line.strip()
                    break
        
        # Fallbacks
        if not subject_line:
            subject_line = f"New {data.get('product', 'Collection')} Perfect for {data.get('festival', 'You')}"
        if not body_line:
            body_line = f"Stunning {data.get('fabric', 'premium')} pieces designed for memorable moments."
        if not cta_line:
            cta_line = "Shop Now"
        
        return f"**{subject_line}**\n{body_line}\n{cta_line}"
    
    def _format_whatsapp_content(self, lines: list, data: dict) -> str:
        """Format WhatsApp: headline + 3 story lines + cta (5 lines)"""
        filtered_lines = [line for line in lines if len(line) > 5]
        
        if len(filtered_lines) >= 5:
            return '\n'.join(filtered_lines[:5])
        
        # Build from available lines
        headline = filtered_lines[0] if filtered_lines else f"Style Speaks Softly"
        story_lines = filtered_lines[1:4] if len(filtered_lines) > 3 else []
        cta = filtered_lines[-1] if filtered_lines and len(filtered_lines[-1].split()) <= 4 else "Shop Now"
        
        # Fill missing story lines
        default_stories = [
            f"New {data.get('product', 'collection')} arrives where style meets comfort.",
            f"Designed for seamless transitions from day to {data.get('festival', 'evening')}.",
            f"These pieces effortlessly adapt to your unique style story."
        ]
        
        while len(story_lines) < 3:
            story_lines.append(default_stories[len(story_lines)])
        
        return f"{headline}\n{story_lines[0]}\n{story_lines[1]}\n{story_lines[2]}\n{cta}"
    
    def _format_concise_content(self, lines: list, data: dict) -> str:
        """Format Concise: headline + 1 description + cta (3 lines)"""
        filtered_lines = [line for line in lines if len(line) > 5]
        
        headline = filtered_lines[0] if filtered_lines else f"New {data.get('product', 'Collection')}"
        description = ""
        cta = "Shop Now"
        
        # Find description and CTA
        for line in filtered_lines[1:]:
            if len(line.split()) > 4 and not description:
                description = line
            elif len(line.split()) <= 4 and line != headline:
                cta = line
                break
        
        if not description:
            description = f"Premium {data.get('fabric', 'quality')} pieces for your {data.get('festival', 'style')} wardrobe."
        
        return f"{headline}\n{description}\n{cta}"
    
    def _format_long_content(self, lines: list, data: dict) -> str:
        """Format Long: headline + 2 descriptions + cta (4 lines)"""
        filtered_lines = [line for line in lines if len(line) > 5]
        
        headline = filtered_lines[0] if filtered_lines else f"New {data.get('product', 'Collection')}"
        descriptions = []
        cta = "Shop Now"
        
        # Extract descriptions and CTA
        for line in filtered_lines[1:]:
            if len(line.split()) > 4 and len(descriptions) < 2:
                descriptions.append(line)
            elif len(line.split()) <= 4 and line != headline:
                cta = line
                break
        
        # Fill missing descriptions
        default_descriptions = [
            f"Premium {data.get('fabric', 'quality')} pieces crafted for discerning taste.",
            f"Perfect for your {data.get('festival', 'special')} wardrobe and beyond."
        ]
        
        while len(descriptions) < 2:
            descriptions.append(default_descriptions[len(descriptions)])
        
        return f"{headline}\n{descriptions[0]}\n{descriptions[1]}\n{cta}"
    
    def _format_pmax_content(self, content: str, data: dict) -> str:
        """Improved PMAX formatting with proper parsing"""
        lines = [line.strip() for line in content.split('\n') if line.strip()]
        
        headlines = []
        descriptions = []
        long_headlines = []
        
        current_section = None
        
        for line in lines:
            line_lower = line.lower()
            
            # Detect section headers
            if 'headlines:' in line_lower and 'long' not in line_lower:
                current_section = 'headlines'
                continue
            elif 'descriptions:' in line_lower:
                current_section = 'descriptions'
                continue
            elif 'long headlines:' in line_lower or 'long-headlines:' in line_lower:
                current_section = 'long_headlines'
                continue
            
            # Skip empty lines and section headers
            if not line or line_lower in ['headlines:', 'descriptions:', 'long headlines:']:
                continue
            
            # Add content to appropriate section with character limits
            if current_section == 'headlines' and len(headlines) < 15:
                headlines.append(line[:30])
            elif current_section == 'descriptions' and len(descriptions) < 5:
                descriptions.append(line[:90])
            elif current_section == 'long_headlines' and len(long_headlines) < 5:
                long_headlines.append(line[:120])
        
        # Fill missing content with templates
        product = data.get('product', 'Collection')
        brand = data.get('brand', 'Premium')
        fabric = data.get('fabric', 'Quality')
        festival = data.get('festival', 'Special')
        
        # Fill headlines (need 15)
        headline_templates = [
            f"New {product}", f"{brand} Style", f"Premium {fabric}", 
            f"Perfect for {festival}", "Quality First", "Shop Now", "Get Yours",
            "Trending Style", "Must Have", "Best Choice", "Modern Look",
            "Classic Style", "Fresh Design", "Top Quality", "Great Value"
        ]
        
        while len(headlines) < 15:
            template = headline_templates[len(headlines) % len(headline_templates)]
            if template[:30] not in [h[:30] for h in headlines]:
                headlines.append(template[:30])
            else:
                headlines.append(f"Style {len(headlines) + 1}")
        
        # Fill descriptions (need 5)
        desc_templates = [
            f"Premium {fabric} {product} for {festival} celebrations",
            f"{brand} quality craftsmanship in every piece",
            f"Perfect {product} designed for your special moments",
            f"Handpicked {fabric} pieces for discerning taste",
            f"New {product} collection now available"
        ]
        
        while len(descriptions) < 5:
            template = desc_templates[len(descriptions) % len(desc_templates)]
            descriptions.append(template[:90])
        
        # Fill long headlines (need 5)
        long_templates = [
            f"{brand} Premium {product} - Quality {fabric} Collection",
            f"Perfect {fabric} {product} for {festival} Celebrations", 
            f"New {product} Collection - Handcrafted {fabric} Pieces",
            f"{brand} {fabric} {product} - Modern Style Statement",
            f"Premium {product} in {fabric} - Shop the Collection"
        ]
        
        while len(long_headlines) < 5:
            template = long_templates[len(long_headlines) % len(long_templates)]
            long_headlines.append(template[:120])
        
        # Build final result
        result = "Headlines:\n" + '\n'.join(headlines[:15])
        result += "\n\nDescriptions:\n" + '\n'.join(descriptions[:5])
        result += "\n\nLong Headlines:\n" + '\n'.join(long_headlines[:5])
        
        return result
    
    def _handle_error(self, error: Exception) -> str:
        error_str = str(error).lower()
        if "authentication" in error_str:
            return "Invalid API key"
        elif "rate limit" in error_str:
            return "Rate limit exceeded - wait a moment"
        elif "quota" in error_str:
            return "API quota exceeded"
        else:
            return "API error - please try again"
    
    def _reset_session_state(self):
        for key in ['previous_content', 'generation_counter']:
            if key in st.session_state:
                del st.session_state[key]
    
    def _store_content(self, content: str):
        if 'previous_content' not in st.session_state:
            st.session_state.previous_content = []
        st.session_state.previous_content.append(content)
        if len(st.session_state.previous_content) > 10:
            st.session_state.previous_content = st.session_state.previous_content[-10:]
    
    def _get_style_name(self, variation: int) -> str:
        styles = {1: "Direct & Clear", 2: "Personal & Warm", 3: "Aspirational & Bold"}
        return styles.get(variation, f"Style {variation}")

# Streamlit UI
st.set_page_config(page_title="AI Fashion Copywriter", page_icon="✨", layout="wide")

# Styling
st.markdown("""
<style>
.main-title { text-align: center; color: #1f77b4; font-size: 2.5rem; margin-bottom: 1rem; }
.stButton > button { width: 100%; height: 3rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                     color: white; border: none; border-radius: 12px; font-weight: 600; }
.variation-card { background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                  padding: 1.5rem; border-radius: 12px; color: white; margin: 1rem 0; }
</style>
""", unsafe_allow_html=True)

# Check API key
if not os.getenv("GROQ_API_KEY"):
    st.error("Missing GROQ_API_KEY! Add it to your .env file.")
    st.stop()

# Initialize generator
@st.cache_resource
def init_generator():
    return GroqContentGenerator()

generator = init_generator()

# Header
st.markdown('<h1 class="main-title">✨ AI Fashion Copywriter</h1>', unsafe_allow_html=True)
st.markdown("### Professional ad copy with maximum creative diversity")

# Model and settings selection
col1, col2, col3 = st.columns([2, 1, 1])
with col1:
    model_options = {
        "💡 Gemma2 9B (Recommended)": "gemma2-9b-it",
        "⚡ Llama 3.1 8B (Fastest)": "llama-3.1-8b-instant"
    }
    selected_model = model_options[st.selectbox("🤖 AI Model", list(model_options.keys()))]
with col2:
    streaming = st.toggle("🎬 Live Streaming", help="Watch generation in real-time")
with col3:
    if st.button("🔄 Reset Session"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.success("Session reset!")

# Mode selection
mode = st.radio(
    "Generation Mode:",
    ["🎯 Easy Mode", "⚙️ Advanced Mode"],
    horizontal=True
)

# Constants
GARMENT_TYPES = [
    "Anarkali Palazzo Set", "Anarkali Set", "Kurta Set", "Kurta Palazzo Set", 
    "Lehenga Set", "Saree Set", "Sharara Set", "Gharara Set", "Co-Ord Set", 
    "Dress", "Kaftan", "Blazer Set", "Palazzo Set", "Suit Set"
]

FESTIVALS_OCCASIONS = [
    "Diwali", "Holi", "Raksha Bandhan", "Karva Chauth", "Navratri", "Durga Puja", 
    "Eid", "Christmas", "New Year", "Wedding Season", "Festive Season", 
    "Summer Collection", "Winter Collection", "New Launch", "Anniversary Sale"
]

FABRIC_TYPES = [
    "Cotton", "Linen", "Silk", "Chanderi", "Banarasi Silk", "Georgette", 
    "Crepe", "Velvet", "Satin", "Muslin", "Chiffon", "Organza", "Net"
]

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
            content_type = st.selectbox("Content Type", 
                ["Email Subject Lines", "Long Content", "Concise Content", "PMAX", "WhatsApp Broadcast"])
            tone = st.selectbox("Brand Voice", 
                ["Premium & Aspirational", "Warm & Personal", "Playful & Fun", "Sophisticated", "Friendly & Approachable"])
            discount = st.number_input("Discount %", min_value=0, max_value=100, step=5, value=0)
            
            if content_type == "PMAX":
                char_limit = {'headlines': 30, 'description': 90, 'long_headlines': 120}
                st.info("PMAX: Headlines=30, Descriptions=90, Long Headlines=120")
            elif content_type == "Email Subject Lines":
                char_limit = st.selectbox("Character Limit", [200, 250, 300], index=0)
            elif content_type == "WhatsApp Broadcast":
                char_limit = st.selectbox("Character Limit", [400, 450, 500], index=0)
            elif content_type == "Concise Content":
                char_limit = st.selectbox("Character Limit", [120, 200, 300], index=0)
            elif content_type == "Long Content":
                char_limit = st.selectbox("Character Limit", [300, 500, 1000], index=0)
        
        generate_btn = st.button("✨ Generate Variations", type="primary")

elif mode == "⚙️ Advanced Mode":
    with st.sidebar:
        st.markdown("## ⚙️ Advanced Mode")
        
        with st.expander("🏷️ Product Information", expanded=True):
            product = st.text_input("Product Name", placeholder="e.g., Wedding Collection")
            brand_name = st.text_input("Brand Name", placeholder="e.g., Dolly J")
            usp = st.text_input("Unique Selling Point", placeholder="e.g., Effortless Glamour")
            attributes = st.text_area("Product Attributes", placeholder="e.g., Handcrafted, Premium comfort")
            fabric = st.multiselect("Fabric Types", FABRIC_TYPES)
            emotion = st.text_input("Emotional Hook", placeholder="e.g., Celebrate Bonds")
        
        with st.expander("⚙️ Content Settings", expanded=True):
            content_type = st.selectbox("Content Type", 
                ["Email Subject Lines", "Long Content", "Concise Content", "PMAX", "WhatsApp Broadcast"])
            tone = st.selectbox("Brand Voice", 
                ["Premium & Aspirational", "Warm & Personal", "Playful & Fun", "Sophisticated", "Friendly & Approachable"])
        
        with st.expander("🎯 Marketing Details", expanded=True):
            discount = st.number_input("Discount %", min_value=0, max_value=100, step=5, value=0)
            
            if content_type == "PMAX":
                char_limit = {'headlines': 30, 'description': 90, 'long_headlines': 120}
                st.info("PMAX: Headlines=30, Descriptions=90, Long Headlines=120")
            elif content_type == "Email Subject Lines":
                char_limit = st.selectbox("Character Limit", [200, 250, 300], index=0)
            elif content_type == "WhatsApp Broadcast":
                char_limit = st.selectbox("Character Limit", [400, 450, 500], index=0)
            elif content_type == "Concise Content":
                char_limit = st.selectbox("Character Limit", [120, 200, 300], index=0)
            elif content_type == "Long Content":
                char_limit = st.selectbox("Character Limit", [300, 500, 1000], index=0)
            
            festival = st.text_input("Festival/Occasion", placeholder="e.g., Raksha Bandhan")
            timing = st.text_input("Urgency Element", placeholder="e.g., 48 Hours Left")
        
        generate_btn = st.button("✨ Generate Variations", type="primary")

# Generation
if generate_btn:
    # Validation based on mode
    if mode == "🎯 Easy Mode":
        if not brand_name or not garment_type:
            st.error("Please fill Brand Name and Garment Type")
            st.stop()
        
        data = {
            'category': content_type,
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
    else:  # Advanced Mode
        if not product:
            st.error("Product name is required")
            st.stop()
        
        data = {
            'brand': brand_name or "Premium Brand",
            'category': content_type,
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
    
    with st.spinner("Generating variations..."):
        variations = generator.generate_variations(data, content_type, selected_model, streaming)
    
    if variations:
        # Generation info
        st.markdown("### 🎯 Generated Variations")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f'<div style="background: linear-gradient(135deg, #ffeaa7 0%, #fab1a0 100%); padding: 0.5rem; border-radius: 8px; font-size: 0.9rem;">Generated at: {time.strftime("%H:%M:%S")}</div>', unsafe_allow_html=True)
        with col2:
            st.markdown(f'<div style="background: linear-gradient(135deg, #ffeaa7 0%, #fab1a0 100%); padding: 0.5rem; border-radius: 8px; font-size: 0.9rem;">Total Variations: {len(variations)}</div>', unsafe_allow_html=True)
        with col3:
            st.markdown(f'<div style="background: linear-gradient(135deg, #ffeaa7 0%, #fab1a0 100%); padding: 0.5rem; border-radius: 8px; font-size: 0.9rem;">Model: {variations[0].get("model_used", "Unknown")}</div>', unsafe_allow_html=True)
        
        # Display table
        df = pd.DataFrame([{
            "Variation": f"#{v['variation']}",
            "Style": v['style'],
            "Content": v['content'][:100] + "..." if len(v['content']) > 100 else v['content'],
            "Characters": v['char_count'],
            "Words": v['word_count'],
            "Time": v['generation_time']
        } for v in variations])
        
        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Variation": st.column_config.TextColumn("Var", width="small"),
                "Style": st.column_config.TextColumn("Style", width="medium"),
                "Content": st.column_config.TextColumn("Preview", width="large"),
                "Characters": st.column_config.NumberColumn("Chars", width="small"),
                "Words": st.column_config.NumberColumn("Words", width="small"),
                "Time": st.column_config.TextColumn("Time", width="small")
            }
        )
        
        # Individual variation cards for better readability
        st.markdown("### 📄 Detailed View")
        for i, var in enumerate(variations):
            with st.expander(f"Variation {var['variation']} - {var['style']} ({var['char_count']} chars)"):
                # Display content in card format
                formatted_content = var["content"].replace("\n", "<br>")
                st.markdown(f'<div class="variation-card">{formatted_content}</div>', unsafe_allow_html=True)
                
                col1, col2 = st.columns([2, 1])
                with col1:
                    st.code(var["content"], language="text")
                with col2:
                    st.caption(f"🤖 {var.get('model_used', 'Unknown')}")
                    st.caption(f"⏰ {var.get('generation_time', 'Unknown')}")
                    st.download_button(
                        "📥 Download",
                        var["content"],
                        f"{data.get('brand', 'content')}_{content_type}_v{var['variation']}.txt",
                        key=f"download_{i}"
                    )
        
        # Action buttons
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Generate New Set"):
                st.rerun()
        with col2:
            all_content = "\n\n--- VARIATION ---\n\n".join([v["content"] for v in variations])
            st.download_button("📦 Download All", all_content, f"{data.get('brand', 'content')}_variations.txt")
    else:
        st.error("Failed to generate variations. Please try again.")

st.markdown("---")
st.markdown("✨ **Powered by Groq AI** • Optimized for Fashion Marketing")