import os
import streamlit as st
import re
import time
import random
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
        
        # Reset tracking for each new instance
        self.reset_generation_state()
    
    def reset_generation_state(self):
        """Reset all generation tracking for fresh content"""
        self.generated_hooks = set()
        self.generated_phrases = set()
        self.generation_timestamp = time.time()
        self.generation_counter = 0
    
    def test_connection(self):
        """Test API connection"""
        try:
            completion = self.client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role": "user", "content": "Test"}],
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
        """Generate single variation with enhanced uniqueness and randomization"""
        
        self.generation_counter += 1
        
        for attempt in range(max_retries):
            try:
                # Create unique timestamp-based seed for this specific generation
                current_time = int(time.time() * 1000000)
                unique_seed = current_time + variation_number * 10000 + attempt * 1000 + self.generation_counter
                
                # Get unique prompt with enhanced randomization
                prompt = self.prompt_builder.build_unique_prompt(
                    data, variation_number, content_type, 
                    previous_hooks=list(self.generated_hooks),
                    previous_phrases=list(self.generated_phrases)
                )
                
                # Dynamic parameters for maximum variety
                base_temp = 0.8 + (variation_number * 0.15) + (attempt * 0.1)
                temperature = min(base_temp + random.uniform(-0.2, 0.3), 1.5)
                
                base_top_p = 0.85 + (variation_number * 0.05) + random.uniform(-0.1, 0.1)
                top_p = min(max(base_top_p, 0.1), 1.0)
                
                # Add randomization to system message
                system_messages = [
                    f"You are creating variation #{variation_number}. Make it completely unique and different from any previous content. Use creative approach {unique_seed % 5 + 1}.",
                    f"Generate variation #{variation_number} with maximum creativity. Avoid repetition. Creative seed: {unique_seed}",
                    f"Create fresh, original variation #{variation_number}. Think outside the box. Randomization: {unique_seed}",
                    f"Variation #{variation_number} needs to be completely different. Use unique perspective {unique_seed % 3 + 1}.",
                    f"Generate diverse variation #{variation_number}. Maximum originality required. Seed: {unique_seed}"
                ]
                
                system_msg = random.choice(system_messages)
                
                params = {
                    "model": model,
                    "messages": [
                        {"role": "system", "content": system_msg},
                        {"role": "user", "content": prompt}
                    ],
                    "temperature": temperature,
                    "max_completion_tokens": 1024,
                    "top_p": top_p,
                    "stream": streaming,
                    "stop": None,
                    "frequency_penalty": 0.8,  # Penalize repetition
                    "presence_penalty": 0.6    # Encourage new topics
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
                
                # Enhanced validation and cleaning
                if self._validate_content(result, content_type):
                    cleaned_result = self._clean_and_format_content(result, data, content_type, variation_number)
                    
                    # Enhanced uniqueness check
                    if self._is_sufficiently_unique(cleaned_result, variation_number, attempt):
                        # Store elements for uniqueness tracking
                        self._extract_and_store_elements(cleaned_result)
                        return cleaned_result
                    elif attempt < max_retries - 1:
                        # Add more randomization for next attempt
                        time.sleep(0.1)  # Small delay to ensure different timestamp
                        continue
                    else:
                        # Accept with modifications on last attempt
                        modified_result = self._add_uniqueness_modifications(cleaned_result, variation_number)
                        self._extract_and_store_elements(modified_result)
                        return modified_result
                else:
                    if attempt < max_retries - 1:
                        continue
                    else:
                        return self._create_emergency_fallback(data, content_type, variation_number)
                        
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
                # Add delay before retry
                time.sleep(0.5)
                continue
        
        return self._create_emergency_fallback(data, content_type, variation_number)
    
    def _validate_content(self, content: str, content_type: str) -> bool:
        """Enhanced content validation"""
        if not content or len(content.strip()) < 10:
            return False
        
        content = content.strip()
        lines = [line.strip() for line in content.split('\n') if line.strip()]
        
        if content_type == "PMAX":
            required_sections = ["Headlines:", "Descriptions:", "Long Headlines:"]
            return all(section in content for section in required_sections)
        else:
            # Check for minimum content requirements
            if len(lines) < 2:
                return False
            
            # Check for unwanted labels in content
            unwanted_patterns = [
                r'^(headline|subject|description|cta|line \d+):\s*',
                r'^(variation|example|template)\s*\d*:?\s*',
                r'^[•\-\*]\s*',
                r'^\d+\.\s*'
            ]
            
            clean_lines = 0
            for line in lines:
                if not any(re.match(pattern, line.lower()) for pattern in unwanted_patterns):
                    clean_lines += 1
            
            return clean_lines >= 2
    
    def _is_sufficiently_unique(self, content: str, variation_number: int, attempt: int) -> bool:
        """Enhanced uniqueness checking"""
        if variation_number == 1 and attempt == 0:
            return True  # First variation is always unique
        
        lines = [line.strip() for line in content.split('\n\n') if line.strip()]
        if not lines:
            return False
        
        # Check first line uniqueness (most important)
        first_line = lines[0].strip().lower()
        first_three_words = ' '.join(first_line.split()[:3])
        first_word = first_line.split()[0] if first_line.split() else ""
        
        # Multiple uniqueness criteria
        uniqueness_checks = [
            first_three_words not in self.generated_phrases,
            first_word not in self.generated_hooks,
            len(set(first_line.split()).intersection(self.generated_hooks)) < 2,
            # Allow some repetition on later attempts
            attempt > 1 or len(lines) > 1
        ]
        
        # Pass if at least 2 uniqueness criteria are met
        return sum(uniqueness_checks) >= 2
    
    def _add_uniqueness_modifications(self, content: str, variation_number: int) -> str:
        """Add modifications to make content more unique"""
        lines = content.split('\n\n')
        if not lines:
            return content
            
        # Modify first line to add uniqueness
        first_line = lines[0].strip()
        if first_line:
            # Add variation-specific modifiers
            modifiers = {
                1: ["Fresh", "New", "Latest", "Premium", "Quality"],
                2: ["Perfect", "Ideal", "Beautiful", "Stunning", "Amazing"], 
                3: ["Special", "Unique", "Exclusive", "Limited", "Custom"]
            }
            
            modifier = random.choice(modifiers.get(variation_number, modifiers[1]))
            if not any(mod.lower() in first_line.lower() for mod in modifiers[variation_number]):
                first_line = f"{modifier} {first_line.lower()}"
                lines[0] = first_line
        
        return '\n\n'.join(lines)
    
    def _extract_and_store_elements(self, content: str):
        """Extract and store hooks and phrases for uniqueness tracking"""
        lines = content.split('\n\n')
        for line in lines:
            if line.strip():
                # Store first 3 words as key phrase
                words = line.strip().lower().split()
                if len(words) >= 3:
                    first_three = ' '.join(words[:3])
                    self.generated_phrases.add(first_three)
                
                # Store first word as hook
                if words:
                    self.generated_hooks.add(words[0])
                    
                # Store second word too for better variety
                if len(words) > 1:
                    self.generated_hooks.add(words[1])
    
    def _clean_and_format_content(self, content: str, data: dict, content_type: str, variation_number: int) -> str:
        """Enhanced cleaning and formatting with variation-specific handling"""
        
        # Remove unwanted labels and formatting
        content = re.sub(r'^(headline|subject|description|cta|line \d+):\s*', '', content, flags=re.IGNORECASE | re.MULTILINE)
        content = re.sub(r'^(variation|example|template)\s*\d*:?\s*', '', content, flags=re.IGNORECASE | re.MULTILINE)
        content = re.sub(r'^[•\-\*]\s*', '', content, flags=re.MULTILINE)
        content = re.sub(r'^[0-9]+\.\s*', '', content, flags=re.MULTILINE)
        content = re.sub(r'^[-=_]{3,}', '', content, flags=re.MULTILINE)
        
        # Remove banned words
        for word in BANNED_WORDS:
            pattern = r'\b' + re.escape(word) + r'\b'
            content = re.sub(pattern, '', content, flags=re.IGNORECASE)
        
        # Clean up multiple spaces and empty lines
        content = re.sub(r'\s+', ' ', content)
        content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)
        content = content.strip()
        
        if content_type == "PMAX":
            return self._format_pmax_content(content, data)
        else:
            return self._format_standard_content(content, data, content_type, variation_number)
    
    def _format_pmax_content(self, content: str, data: dict) -> str:
        """Enhanced PMAX formatting with better parsing"""
        lines = [line.strip() for line in content.split('\n') if line.strip()]
        
        headlines = []
        descriptions = []
        long_headlines = []
        
        current_section = None
        for line in lines:
            line_lower = line.lower()
            if 'headline' in line_lower and 'long' not in line_lower:
                current_section = 'headlines'
                continue
            elif 'description' in line_lower:
                current_section = 'descriptions'  
                continue
            elif 'long headline' in line_lower or 'long-headline' in line_lower:
                current_section = 'long_headlines'
                continue
            
            # Skip section headers and empty lines
            if line in ['Headlines:', 'Descriptions:', 'Long Headlines:'] or not line:
                continue
                
            if current_section == 'headlines' and len(headlines) < 15:
                headlines.append(line[:30])
            elif current_section == 'descriptions' and len(descriptions) < 5:
                descriptions.append(line[:90])
            elif current_section == 'long_headlines' and len(long_headlines) < 5:
                long_headlines.append(line[:120])
        
        # Fill missing content if sections are incomplete
        if len(headlines) < 15:
            self._fill_missing_pmax_headlines(headlines, data)
        if len(descriptions) < 5:
            self._fill_missing_pmax_descriptions(descriptions, data)
        if len(long_headlines) < 5:
            self._fill_missing_pmax_long_headlines(long_headlines, data)
        
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
    
    def _fill_missing_pmax_headlines(self, headlines: list, data: dict):
        """Fill missing PMAX headlines"""
        templates = [
            f"New {data.get('product', 'Collection')}",
            f"{data.get('brand', 'Premium')} Style", 
            f"{data.get('fabric', 'Quality')} Pieces",
            f"{data.get('festival', 'Special')} Ready",
            f"Shop {data.get('product', 'Now')}",
            "Quality Crafted",
            "Modern Design", 
            "Perfect Fit",
            "Premium Choice",
            "Style Update",
            "Fresh Arrivals",
            "Handpicked",
            "Trending Now",
            "Must Have",
            "Best Seller"
        ]
        
        while len(headlines) < 15 and templates:
            template = templates.pop(0)
            if template[:30] not in [h[:30] for h in headlines]:
                headlines.append(template[:30])
    
    def _fill_missing_pmax_descriptions(self, descriptions: list, data: dict):
        """Fill missing PMAX descriptions"""
        templates = [
            f"Discover {data.get('product', 'premium pieces')} in {data.get('fabric', 'quality materials')}",
            f"{data.get('brand', 'Premium brand')} collection for {data.get('festival', 'special moments')}",
            f"Handcrafted {data.get('product', 'designs')} perfect for your style",
            f"Quality {data.get('fabric', 'materials')} meets modern design",
            f"Your perfect {data.get('product', 'outfit')} awaits - shop now"
        ]
        
        while len(descriptions) < 5 and templates:
            template = templates.pop(0)
            if template[:90] not in [d[:90] for d in descriptions]:
                descriptions.append(template[:90])
    
    def _fill_missing_pmax_long_headlines(self, long_headlines: list, data: dict):
        """Fill missing PMAX long headlines"""
        templates = [
            f"{data.get('brand', 'Premium')} {data.get('product', 'Collection')} - Handcrafted in {data.get('fabric', 'Quality Materials')}",
            f"Discover {data.get('product', 'Premium Designs')} Perfect for {data.get('festival', 'Special Occasions')}",
            f"New {data.get('fabric', 'Quality')} {data.get('product', 'Collection')} - Modern Style Meets Tradition",
            f"{data.get('brand', 'Premium')} Quality - {data.get('product', 'Pieces')} That Make a Statement",
            f"Shop {data.get('product', 'Premium Collection')} - {data.get('fabric', 'Quality')} That Speaks to You"
        ]
        
        while len(long_headlines) < 5 and templates:
            template = templates.pop(0)
            if template[:120] not in [lh[:120] for lh in long_headlines]:
                long_headlines.append(template[:120])
    
    def _format_standard_content(self, content: str, data: dict, content_type: str, variation_number: int) -> str:
        """Enhanced standard content formatting"""
        lines = [line.strip() for line in content.split('\n') if line.strip()]
        
        # Filter out unwanted lines more aggressively
        filtered_lines = []
        for line in lines:
            if len(line) > 2 and not re.match(r'^[-=_]{3,}', line):
                # Skip lines with labels
                if not any(label in line.lower() for label in [
                    'headline:', 'subject:', 'description:', 'cta:', 'line 1:', 'line 2:', 'line 3:',
                    'variation', 'example', 'template', 'output', 'format', 'structure'
                ]):
                    filtered_lines.append(line)
        
        if len(filtered_lines) < 2:
            return self._create_emergency_fallback(data, content_type, variation_number)
        
        # Extract components based on content type
        if content_type in ["Email Subject Lines", "Concise Content"]:
            headline = filtered_lines[0]
            description = filtered_lines[1] if len(filtered_lines) > 1 else f"Perfect for {data.get('festival', 'special moments')}"
            cta = filtered_lines[2] if len(filtered_lines) > 2 else random.choice(["Shop Now", "Get Yours", "Discover More"])
        else:
            # Longer formats
            headline = filtered_lines[0]
            description_parts = filtered_lines[1:3] if len(filtered_lines) > 2 else [filtered_lines[1]]
            description = " ".join(description_parts)
            cta = filtered_lines[-1] if len(filtered_lines) > 3 else random.choice(["Shop Today", "Explore Now", "Find Yours"])
        
        # Apply character limits
        char_limit = data.get('char_limit', 300)
        if isinstance(char_limit, int):
            total_content = f"{headline}\n\n{description}\n\n{cta}"
            if len(total_content) > char_limit:
                # Trim description to fit
                available_for_desc = char_limit - len(headline) - len(cta) - 6  # 6 for spacing
                if available_for_desc > 20:
                    description = description[:available_for_desc].rsplit(' ', 1)[0]
        
        return f"{headline}\n\n{description}\n\n{cta}"
    
    def _create_emergency_fallback(self, data: dict, content_type: str, variation_number: int) -> str:
        """Create emergency fallback when all else fails"""
        return self.prompt_builder.create_fallback_content(data, content_type, variation_number)
    
    def generate_variations(self, data: dict, content_type: str, model: str, streaming: bool = False):
        """Generate 3 unique variations with enhanced randomization"""
        
        if not self.test_connection():
            st.warning("Connection test failed, but continuing with generation...")
        
        # Reset state for fresh generation
        self.reset_generation_state()
        
        variations = []
        
        # Create streaming placeholders if needed
        placeholders = []
        if streaming:
            st.markdown("### 🎬 Live Generation")
            for i in range(3):
                st.markdown(f"**Variation {i+1}:**")
                placeholders.append(st.empty())
                st.markdown("---")
        
        # Generate 3 variations with enhanced diversity
        for i in range(3):
            try:
                placeholder = placeholders[i] if streaming and i < len(placeholders) else None
                
                # Add small delay between generations to ensure different timestamps
                if i > 0:
                    time.sleep(0.2)
                
                response = self.generate_single_variation(
                    data, i + 1, content_type, model, streaming, placeholder, max_retries=4
                )
                
                if response and len(response.strip()) > 10:
                    variations.append({
                        "variation": i + 1,
                        "style": self._get_variation_style_name(i + 1),
                        "content": response,
                        "char_count": len(response),
                        "word_count": len(response.split()) if response else 0,
                        "model_used": model,
                        "generation_time": time.strftime("%H:%M:%S")
                    })
                else:
                    # Create enhanced fallback variation
                    fallback_content = self.prompt_builder.create_fallback_content(data, content_type, i + 1)
                    variations.append({
                        "variation": i + 1,
                        "style": f"Fallback Style {i + 1}",
                        "content": fallback_content,
                        "char_count": len(fallback_content),
                        "word_count": len(fallback_content.split()),
                        "model_used": model,
                        "generation_time": time.strftime("%H:%M:%S")
                    })
                    
            except Exception as e:
                st.error(f"Error in variation {i+1}: {str(e)}")
                error_content = self.prompt_builder.create_fallback_content(data, content_type, i + 1)
                variations.append({
                    "variation": i + 1,
                    "style": f"Error Recovery {i + 1}",
                    "content": error_content,
                    "char_count": len(error_content),
                    "word_count": len(error_content.split()),
                    "model_used": model,
                    "generation_time": time.strftime("%H:%M:%S")
                })
        
        return self._ensure_valid_variations(variations, model)
    
    def _get_variation_style_name(self, variation_number: int) -> str:
        """Get descriptive style name for variation with more variety"""
        styles = {
            1: random.choice(["Direct & Bold", "Feature-Focused", "Quality-First", "Premium Approach"]),
            2: random.choice(["Emotional & Personal", "Question-Driven", "Heart-Centered", "Connection-Based"]), 
            3: random.choice(["Storytelling & Dreams", "Aspirational Lifestyle", "Narrative-Rich", "Vision-Focused"])
        }
        return styles.get(variation_number, f"Creative Style {variation_number}")
    
    def _ensure_valid_variations(self, variations, model):
        """Enhanced variation validation and completion"""
        if not variations:
            # Create emergency variations if completely failed
            emergency_data = {"product": "Collection", "brand": "Premium", "fabric": "Quality"}
            variations = []
            for i in range(3):
                content = self.prompt_builder.create_fallback_content(emergency_data, "General", i + 1)
                variations.append({
                    "variation": i + 1,
                    "style": f"Emergency Style {i + 1}",
                    "content": content,
                    "char_count": len(content),
                    "word_count": len(content.split()),
                    "model_used": model,
                    "generation_time": time.strftime("%H:%M:%S")
                })
        
        # Validate and fix each variation
        for i, var in enumerate(variations):
            if not isinstance(var, dict):
                variations[i] = {
                    "variation": i + 1,
                    "style": "Error Recovery",
                    "content": "Generation failed - please try again",
                    "char_count": 0,
                    "word_count": 0,
                    "model_used": model,
                    "generation_time": time.strftime("%H:%M:%S")
                }
            else:
                # Ensure all required keys exist
                required_keys = ["variation", "style", "content", "char_count", "word_count", "model_used", "generation_time"]
                for key in required_keys:
                    if key not in var:
                        if key == "variation":
                            var[key] = i + 1
                        elif key == "style":
                            var[key] = f"Style {i + 1}"
                        elif key == "content":
                            var[key] = "Content generation failed"
                        elif key == "char_count":
                            var[key] = len(var.get("content", ""))
                        elif key == "word_count":
                            var[key] = len(var.get("content", "").split()) if var.get("content") else 0
                        elif key == "model_used":
                            var[key] = model
                        elif key == "generation_time":
                            var[key] = time.strftime("%H:%M:%S")
        
        return variations

# Enhanced Streamlit UI with better state management
st.set_page_config(
    page_title="AI Fashion Copywriter", 
    page_icon="✨", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state for better state management
if 'generation_count' not in st.session_state:
    st.session_state.generation_count = 0
if 'last_generation_time' not in st.session_state:
    st.session_state.last_generation_time = 0

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

# Initialize generator with state management
@st.cache_resource
def init_generator():
    return GroqContentGenerator()

# Reset cache if needed for fresh generations
def reset_generator():
    st.cache_resource.clear()
    return GroqContentGenerator()

generator = init_generator()

# Enhanced styling
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
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
        transform: translateY(-2px);
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
    
    .generation-info {
        background: linear-gradient(135deg, #ffeaa7 0%, #fab1a0 100%);
        padding: 0.5rem;
        border-radius: 8px;
        font-size: 0.9rem;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Constants (same as before)
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
    """Enhanced variation display with generation info"""
    if not variations or not variations[0].get('content'):
        st.error("No variations generated")
        return
    
    # Generation info
    st.markdown("### 🎯 Generated Variations")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f'<div class="generation-info">Generated at: {time.strftime("%H:%M:%S")}</div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="generation-info">Total Variations: {len(variations)}</div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="generation-info">Model: {variations[0].get("model_used", "Unknown")}</div>', unsafe_allow_html=True)
    
    # Single table with all variations
    import pandas as pd
    table_data = []
    for i, variation in enumerate(variations):
        table_data.append({
            "Variation": f"#{variation.get('variation', i+1)}",
            "Style": variation.get('style', 'Default'),
            "Content": variation.get('content', 'No content'),
            "Characters": variation.get('char_count', 0),
            "Words": variation.get('word_count', 0),
            "Time": variation.get('generation_time', 'Unknown')
        })
    
    df = pd.DataFrame(table_data)
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Variation": st.column_config.TextColumn("Var", width="small"),
            "Style": st.column_config.TextColumn("Style", width="medium"),
            "Content": st.column_config.TextColumn("Content", width="large"),
            "Characters": st.column_config.NumberColumn("Chars", width="small"),
            "Words": st.column_config.NumberColumn("Words", width="small"),
            "Time": st.column_config.TextColumn("Time", width="small")
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
                st.caption(f"⏰ {variation.get('generation_time', 'Unknown')}")
                st.download_button(
                    "📥 Download",
                    variation.get("content", "No content"),
                    f"{data.get('brand', 'content')}_{data['category']}_v{variation.get('variation', i+1)}.txt",
                    key=f"download_{i}_{st.session_state.generation_count}"
                )

# Header
st.markdown('<h1 class="main-title">✨ AI Fashion Copywriter</h1>', unsafe_allow_html=True)
st.markdown("### Professional ad copy with maximum creative diversity")

# Model and streaming selection
col1, col2, col3 = st.columns([2, 1, 1])
with col1:
    model_options = {
        "💡 Gemma2 9B (Recommended)": "gemma2-9b-it",
        "⚡ Llama 3.1 8B (Fastest)": "llama-3.1-8b-instant"
    }
    selected_model_name = st.selectbox("🤖 AI Model", list(model_options.keys()))
    selected_model = model_options[selected_model_name]

with col2:
    enable_streaming = st.toggle("🎬 Live Streaming", help="Watch generation in real-time")

with col3:
    if st.button("🔄 Reset Generator"):
        generator = reset_generator()
        st.success("Generator reset! Fresh content incoming.")

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