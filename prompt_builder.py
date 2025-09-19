BANNED_WORDS = [
    "discover", "explore", "embrace", "immerse",
    "timeless", "elegance", "luxury", "opulence", "wrap", "celebrate", "effortless"
]

class PromptBuilder:
    def __init__(self):
        # Unique hook libraries for different variations
        self.variation_hooks = {
            1: {  # Direct & Feature-Focused
                "openers": ["Introducing", "Meet your new", "New arrival", "Perfect for", "Premium"],
                "emotions": ["confidence", "sophistication", "quality"],
                "benefits": ["premium craftsmanship", "superior comfort", "perfect fit"],
                "sentence_style": "direct statements",
                "approach": "product features first"
            },
            2: {  # Emotional & Question-Based  
                "openers": ["What if you could", "Imagine wearing", "How would you feel", "Ever dreamed of", "Picture yourself"],
                "emotions": ["transformation", "joy", "empowerment"],
                "benefits": ["feel confident", "express yourself", "shine brightly"],
                "sentence_style": "questions and conditionals",
                "approach": "emotional connection first"
            },
            3: {  # Storytelling & Aspirational
                "openers": ["Every woman deserves", "Step into a world", "Your story begins", "When elegance meets", "Special moments call"],
                "emotions": ["aspiration", "dreams", "lifestyle"],
                "benefits": ["elevated style", "memorable moments", "personal expression"],
                "sentence_style": "narrative and aspirational",
                "approach": "lifestyle and story first"
            }
        }
        
        # CTA variations for each approach
        self.cta_variations = {
            1: ["Shop Now", "Get Yours", "Order Today", "Buy Now", "Secure Yours"],
            2: ["Discover More", "Feel The Difference", "Experience Magic", "Find Your Perfect", "See The Beauty"],
            3: ["Begin Your Journey", "Live Your Story", "Embrace Your Style", "Create Memories", "Step Into Luxury"]
        }
        
        # Benefit angles to ensure variety
        self.benefit_angles = {
            1: ["material quality", "craftsmanship", "durability", "comfort", "fit"],
            2: ["emotional impact", "confidence boost", "self-expression", "transformation", "empowerment"], 
            3: ["lifestyle elevation", "memorable experiences", "personal story", "aspirational living", "dream fulfillment"]
        }
        
    def build_unique_prompt(self, data: dict, variation_number: int, content_type: str, 
                           previous_hooks: list = None, previous_phrases: list = None) -> str:
        """Build completely unique prompts for each variation"""
        
        if previous_hooks is None:
            previous_hooks = []
        if previous_phrases is None:
            previous_phrases = []
        
        # Get variation-specific elements
        var_elements = self.variation_hooks.get(variation_number, self.variation_hooks[1])
        
        # Select unique opener not used before
        available_openers = [op for op in var_elements["openers"] if op.lower() not in [h.lower() for h in previous_hooks]]
        unique_opener = available_openers[0] if available_openers else f"Style Moment {variation_number}"
        
        # Select unique CTA
        unique_cta = self.cta_variations[variation_number][0]
        
        # Build base requirements
        base_requirements = self._build_base_requirements(data, unique_opener, unique_cta, var_elements)
        
        # Build format-specific prompt
        if content_type == "Email Subject Lines":
            return self._build_email_prompt(base_requirements, data, variation_number, previous_phrases)
        elif content_type == "WhatsApp Broadcast":
            return self._build_whatsapp_prompt(base_requirements, data, variation_number, previous_phrases)
        elif content_type == "Concise Content":
            return self._build_concise_prompt(base_requirements, data, variation_number, previous_phrases)
        elif content_type == "Long Content":
            return self._build_long_prompt(base_requirements, data, variation_number, previous_phrases)
        elif content_type == "PMAX":
            return self._build_pmax_prompt(base_requirements, data, variation_number, previous_phrases)
        else:
            return self._build_general_prompt(base_requirements, data, variation_number, previous_phrases)
    
    def _build_base_requirements(self, data: dict, unique_opener: str, unique_cta: str, var_elements: dict) -> str:
        """Build base requirements section"""
        product = data.get('product', '').strip()
        brand = data.get('brand', '').strip()
        fabric = data.get('fabric', '').strip()
        festival = data.get('festival', '').strip()
        discount = data.get('discount', 0)
        char_limit = data.get('char_limit', 300)
        tone = data.get('tone', 'casual').strip().lower()
        banned = ', '.join(BANNED_WORDS)
        
        return f"""
CORE REQUIREMENTS:
- Product: {product}
- Brand: {brand} 
- Fabric: {fabric}
- Occasion: {festival}
- Discount: {discount}% {'(highlight if > 0)' if discount > 0 else '(ignore)'}
- USP: {data.get('usp', 'Premium Quality')}
- Tone: {tone}
- Character Limit: {char_limit}

VARIATION-SPECIFIC CREATIVE DIRECTION:
- Approach: {var_elements['approach']}
- Opening Style: Use "{unique_opener}" or similar
- Emotion Focus: {var_elements['emotions'][0]}
- Benefit Angle: {var_elements['benefits'][0]}
- Sentence Style: {var_elements['sentence_style']}
- CTA Style: {unique_cta}

BANNED WORDS (never use): {banned}
PUNCTUATION: Only periods (.) and commas (,) - NO exclamation marks (!) or dashes (-)"""

    def _build_email_prompt(self, base_requirements: str, data: dict, variation_number: int, previous_phrases: list) -> str:
        """Build email subject line prompt"""
        forbidden_phrases = ', '.join(previous_phrases) if previous_phrases else "none"
        
        return f"""{base_requirements}

EMAIL SUBJECT LINE FORMAT - VARIATION #{variation_number} REQUIREMENTS:

FORBIDDEN PHRASES (from previous variations): {forbidden_phrases}

FORMAT STRUCTURE - FOLLOW EXACTLY:
[Single line headline - complete sentence]

[Single line description - complete sentence about occasion/product]  

[2-3 word CTA]

VARIATION #{variation_number} SPECIFIC RULES:
- Start with completely different words than previous variations
- Use {self.variation_hooks[variation_number]['sentence_style']} 
- Focus on {self.benefit_angles[variation_number][0]}
- Character limit: {data.get('char_limit', 200)} total
- NO labels like "Headline:" "Subject:" "Description:" "CTA:"
- NO bullet points, numbering, or quotes
- Each line must be complete and meaningful

EXAMPLE STRUCTURE (create something completely different):
Perfect weekend style sorted

New silk pieces ideal for Diwali nights

Shop Now

CRITICAL: Output ONLY the 3 lines with blank lines between. No explanations."""

    def _build_whatsapp_prompt(self, base_requirements: str, data: dict, variation_number: int, previous_phrases: list) -> str:
        """Build WhatsApp broadcast prompt"""
        forbidden_phrases = ', '.join(previous_phrases) if previous_phrases else "none"
        
        return f"""{base_requirements}

WHATSAPP BROADCAST FORMAT - VARIATION #{variation_number} REQUIREMENTS:

FORBIDDEN PHRASES (from previous variations): {forbidden_phrases}

FORMAT STRUCTURE - FOLLOW EXACTLY:
[Single line headline]

[Multi-line description - 2-3 lines that flow as one story]
[Each line continues the narrative naturally]

[2-3 word CTA]

VARIATION #{variation_number} SPECIFIC RULES:
- Use {self.variation_hooks[variation_number]['sentence_style']}
- Focus on {self.variation_hooks[variation_number]['approach']}
- Emotion: {self.variation_hooks[variation_number]['emotions'][0]}
- Character limit: {data.get('char_limit', 400)} total
- NO labels or bullet points
- Description flows as natural conversation
- Start with unique opening words

CRITICAL: Output ONLY in the exact format. No labels or explanations."""

    def _build_concise_prompt(self, base_requirements: str, data: dict, variation_number: int, previous_phrases: list) -> str:
        """Build concise content prompt"""
        forbidden_phrases = ', '.join(previous_phrases) if previous_phrases else "none"
        
        return f"""{base_requirements}

CONCISE CONTENT FORMAT - VARIATION #{variation_number} REQUIREMENTS:

FORBIDDEN PHRASES (from previous variations): {forbidden_phrases}

FORMAT STRUCTURE - FOLLOW EXACTLY:
[Single headline line]

[Single description line - storytelling focused]

[2-4 word CTA]

VARIATION #{variation_number} SPECIFIC RULES:
- Approach: {self.variation_hooks[variation_number]['approach']}
- Sentence Style: {self.variation_hooks[variation_number]['sentence_style']}
- Benefit Focus: {self.benefit_angles[variation_number][0]}
- Character limit: {data.get('char_limit', 200)} total
- EXACTLY 3 lines with blank lines between
- NO labels, bullets, or quotes
- Each line complete and meaningful

CRITICAL: Output ONLY the 3 lines with proper spacing. No explanations."""

    def _build_long_prompt(self, base_requirements: str, data: dict, variation_number: int, previous_phrases: list) -> str:
        """Build long content prompt"""
        forbidden_phrases = ', '.join(previous_phrases) if previous_phrases else "none"
        
        return f"""{base_requirements}

LONG CONTENT FORMAT - VARIATION #{variation_number} REQUIREMENTS:

FORBIDDEN PHRASES (from previous variations): {forbidden_phrases}

FORMAT STRUCTURE - FOLLOW EXACTLY:
[Single headline]

[First description line - sets scene/emotion]
[Second description line - explains benefit/product]

[3-5 word CTA]

VARIATION #{variation_number} SPECIFIC RULES:
- Approach: {self.variation_hooks[variation_number]['approach']}
- Emotion: {self.variation_hooks[variation_number]['emotions'][0]}
- Benefit Angle: {self.benefit_angles[variation_number][1]}
- Character limit: {data.get('char_limit', 500)} total
- Description lines flow together as one story
- Use {self.variation_hooks[variation_number]['sentence_style']}
- NO labels or formatting markers

CRITICAL: Output ONLY the 4 lines with blank lines between. No explanations."""

    def _build_pmax_prompt(self, base_requirements: str, data: dict, variation_number: int, previous_phrases: list) -> str:
        """Build PMAX ads prompt"""
        forbidden_phrases = ', '.join(previous_phrases) if previous_phrases else "none"
        
        return f"""{base_requirements}

GOOGLE ADS PMAX FORMAT - VARIATION #{variation_number} REQUIREMENTS:

FORBIDDEN PHRASES (from previous variations): {forbidden_phrases}

FORMAT STRUCTURE - FOLLOW EXACTLY:
Headlines:
[15 headlines under 30 characters each - vary approaches]

Descriptions:  
[5 descriptions under 90 characters each - different angles]

Long Headlines:
[5 long headlines under 120 characters each - mix of styles]

VARIATION #{variation_number} SPECIFIC RULES:
- Headlines: Mix of {self.variation_hooks[variation_number]['approach']} approach
- Use different emotional angles: {', '.join(self.variation_hooks[variation_number]['emotions'])}
- Vary benefit focus across items
- Each section should have diversity in approach
- Character limits: Headlines=30, Descriptions=90, Long Headlines=120
- Use EXACTLY the section labels shown
- NO bullet points within sections

CRITICAL: Follow exact 3-section format with proper labels and character limits."""

    def _build_general_prompt(self, base_requirements: str, data: dict, variation_number: int, previous_phrases: list) -> str:
        """Build general marketing copy prompt"""
        forbidden_phrases = ', '.join(previous_phrases) if previous_phrases else "none"
        
        return f"""{base_requirements}

GENERAL MARKETING COPY FORMAT - VARIATION #{variation_number} REQUIREMENTS:

FORBIDDEN PHRASES (from previous variations): {forbidden_phrases}

FORMAT STRUCTURE - FOLLOW EXACTLY:
[Single headline - unique opening]

[Single description line - blend occasion/product/brand]

[CTA - action-focused]

VARIATION #{variation_number} SPECIFIC RULES:
- Use {self.variation_hooks[variation_number]['sentence_style']}
- Focus on {self.variation_hooks[variation_number]['approach']}
- Character limit: {data.get('char_limit', 300)} total
- EXACTLY 3 lines with blank lines between
- NO labels or formatting

CRITICAL: Output ONLY the 3 lines with blank lines. No explanations."""

    def create_fallback_content(self, data: dict, content_type: str, variation_number: int) -> str:
        """Create fallback content when generation fails"""
        product = data.get('product', 'Fashion Collection')
        brand = data.get('brand', 'Brand')
        fabric = data.get('fabric', 'Premium')
        festival = data.get('festival', 'Special Occasion')
        discount = data.get('discount', 0)
        
        # Variation-specific fallback templates
        templates = {
            1: {  # Direct & Feature-Focused
                "headline": f"New {product} Collection",
                "description": f"Premium {fabric} pieces perfect for {festival}",
                "cta": "Shop Now"
            },
            2: {  # Emotional & Question-Based
                "headline": f"What if you could transform your {festival} look",
                "description": f"Imagine wearing {fabric} that makes you feel confident",
                "cta": "Discover More"
            },
            3: {  # Storytelling & Aspirational
                "headline": f"Every {festival} deserves something special",
                "description": f"Your story begins with {fabric} that speaks to your soul",
                "cta": "Begin Journey"
            }
        }
        
        template = templates.get(variation_number, templates[1])
        
        # Add discount if present
        if discount > 0:
            template["description"] = f"{discount}% off {template['description'].lower()}"
        
        if content_type == "PMAX":
            return self._create_pmax_fallback(product, brand, fabric, festival, discount)
        else:
            return f"{template['headline']}\n\n{template['description']}\n\n{template['cta']}"
    
    def _create_pmax_fallback(self, product: str, brand: str, fabric: str, festival: str, discount: int) -> str:
        """Create PMAX fallback content"""
        headlines = [
            f"{product} Collection", f"{brand} {fabric}", f"New Arrivals",
            f"Premium {fabric}", f"{product} Sale", f"{festival} Special",
            f"{brand} Quality", f"Handcrafted {fabric}", f"Perfect Fit",
            f"Style Update", f"{fabric} Comfort", f"Fashion Forward",
            f"Quality Craft", f"Modern Style", f"Premium Choice"
        ]
        
        descriptions = [
            f"Discover {product} in {fabric} - perfect for {festival}",
            f"{brand}'s premium {fabric} collection now available",
            f"Handcrafted {product} pieces for special moments",
            f"Premium {fabric} {product} - comfort meets style",
            f"New {product} arrivals in luxurious {fabric}"
        ]
        
        long_headlines = [
            f"{brand} Premium {fabric} {product} Collection - Handcrafted Excellence",
            f"Discover Luxury {product} in {fabric} - Perfect for {festival}",
            f"New {fabric} {product} Arrivals - Premium Quality Guaranteed",
            f"{brand} {product} Collection - Where Style Meets Comfort",
            f"Handcrafted {fabric} {product} - Traditional Meets Modern"
        ]
        
        result = "Headlines:\n"
        for h in headlines[:15]:
            result += f"{h[:30]}\n"
        result += "\nDescriptions:\n"  
        for d in descriptions[:5]:
            result += f"{d[:90]}\n"
        result += "\nLong Headlines:\n"
        for lh in long_headlines[:5]:
            result += f"{lh[:120]}\n"
            
        return result.strip()

def build_prompt(data: dict) -> str:
    """Legacy function for backward compatibility - redirects to PromptBuilder"""
    builder = PromptBuilder()
    return builder.build_unique_prompt(data, 1, "General")  # Default to variation 1, General type