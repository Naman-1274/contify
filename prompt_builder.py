class ImprovedPromptBuilder:
    def __init__(self):
        self.banned_words = [
            "discover", "explore", "embrace", "immerse", "timeless", 
            "elegance", "luxury", "opulence", "wrap", "celebrate", "effortless"
        ]
        
        # Clear, focused strategies for each variation
        self.strategies = {
            1: {
                "focus": "direct_benefits",
                "tone": "confident_clear",
                "approach": "feature_benefit_action"
            },
            2: {
                "focus": "emotional_connection", 
                "tone": "warm_personal",
                "approach": "story_emotion_cta"
            },
            3: {
                "focus": "aspirational_lifestyle",
                "tone": "sophisticated_bold", 
                "approach": "vision_product_urgency"
            }
        }
    
    def build_focused_prompt(self, data: dict, variation_number: int, content_type: str) -> str:
        """Build focused, strategy-based prompts"""
        strategy = self.strategies[variation_number]
        
        # Extract data
        product = data.get('product', 'Premium Collection')
        brand = data.get('brand', 'Our Brand')
        fabric = data.get('fabric', 'Quality Materials')
        festival = data.get('festival', 'Special Occasions')
        discount = data.get('discount', 0)
        char_limit = data.get('char_limit', 300)
        tone = data.get('tone', 'Premium & Aspirational')
        
        base_prompt = f"""
You are creating fashion marketing copy variation #{variation_number}.

PRODUCT INFO:
- Brand: {brand}
- Product: {product}
- Fabric: {fabric}
- Occasion: {festival}
- Discount: {discount}% {"(feature prominently)" if discount > 0 else "(ignore)"}
- Brand Voice: {tone}

STRATEGY FOR THIS VARIATION:
- Focus: {strategy['focus']}
- Tone: {strategy['tone']}
- Approach: {strategy['approach']}

STRICT RULES:
1. Never use: {', '.join(self.banned_words)}
2. Use only periods and commas - NO exclamation marks or dashes
3. No labels like "Headline:" "Description:" "CTA:"
4. Character limit: {char_limit}
5. Each line must be complete and grammatically correct

{self._get_format_instructions(content_type, strategy, data)}
"""
        return base_prompt
    
    def _get_format_instructions(self, content_type: str, strategy: dict, data: dict) -> str:
        """Get format-specific instructions"""
        
        if content_type == "Email Subject Lines":
            return f"""
EMAIL FORMAT (exactly 2 lines):
Line 1: **Bold subject line** (30-60 chars) - compelling email header
Line 2: Email body content (1-2 sentences) - engaging description that flows naturally
Line 3: CTA (2-4 words) - clear action prompt

VARIATION {1 if strategy['focus'] == 'direct_benefits' else 2 if strategy['focus'] == 'emotional_connection' else 3} STYLE:
- {strategy['focus']}: Focus on what the customer gains
- {strategy['tone']}: Write in this emotional register
- Create professional email content like fashion brands send

EXAMPLE STRUCTURE (create something different):
**New Arrivals Perfect for {data.get('festival', 'Celebrations')}**
Stunning {data.get('fabric', 'premium')} {data.get('product', 'pieces')} designed for memorable moments.
"""
        
        elif content_type == "WhatsApp Broadcast":
            return f"""
WHATSAPP FORMAT (exactly 3 lines):
Line 1: Casual conversation starter - like texting a friend
Line 2:  WhatsApp body content (2-4 sentences) - engaging description that flows naturally with {data.get('festival', 'occasion')} connection
Line 3: Friendly call-to-action (2-4 words)

Write conversationally like a friend sharing exciting news.
"""
        
        elif content_type == "PMAX":
            return f"""
GOOGLE ADS PMAX FORMAT - Generate exactly these sections:

Headlines: (exactly 15 items, each under 30 characters)
[15 short headlines - mix {strategy['focus']} approach]

Descriptions: (exactly 5 items, each under 90 characters) 
[5 longer descriptions - {strategy['tone']} style]

Long Headlines: (exactly 5 items, each under 120 characters)
[5 extended headlines - {strategy['approach']} pattern]

CHARACTER LIMITS ARE STRICT:
- Headlines: 30 chars max each
- Descriptions: 90 chars max each  
- Long Headlines: 120 chars max each

Each item within a section must be unique and different.
"""
        
        elif content_type == "Long Content":
            return f"""
FORMAT (exactly 4 lines with blank lines between):
Line 1: Strong opening - {strategy['tone']} voice
Line 2: Story development - {strategy['focus']} angle  
Line 3: Product integration - natural weaving
Line 4: Compelling CTA (3-6 words)

Create a mini-narrative that flows naturally.
"""
        
        else:  # Concise Content
            return f"""
FORMAT (exactly 3 lines with blank lines between):
Line 1: Punchy headline - {strategy['focus']} impact
Line 2: Smart description - {strategy['tone']} efficiency
Line 3: Power CTA (2-4 words)

Every word must earn its place.
"""
    
    def create_fallback_content(self, data: dict, content_type: str, variation_number: int) -> str:
        """Create reliable fallback content"""
        product = data.get('product', 'Premium Collection')
        brand = data.get('brand', 'Our Brand')
        fabric = data.get('fabric', 'Quality Materials')
        festival = data.get('festival', 'Special Occasions')
        discount = data.get('discount', 0)
        
        # Simple fallback templates
        templates = {
            1: {
                "line1": f"New {product} now available",
                "line2": f"Premium {fabric} perfect for {festival}",
                "line3": "Shop Now"
            },
            2: {
                "line1": f"Perfect for your {festival} celebrations",
                "line2": f"Beautiful {product} in {fabric} awaits",
                "line3": "Find Yours"
            },
            3: {
                "line1": f"Step into {brand} luxury",
                "line2": f"Stunning {fabric} {product} for memorable moments",
                "line3": "Order Today"
            }
        }
        
        template = templates.get(variation_number, templates[1])
        
        # Add discount if present
        if discount > 0:
            template["line2"] = f"{discount}% off {template['line2'].lower()}"
        
        if content_type == "PMAX":
            return self._create_pmax_fallback(product, brand, fabric, festival, discount)
        elif content_type == "Email Subject Lines":
            # Email format: **Subject** \n Body
            subjects = [
                f"New {product} Perfect for {festival}",
                f"Your {festival} Style Awaits",
                f"Step Into {brand} Luxury"
            ]
            bodies = [
                f"Stunning {fabric} pieces designed for memorable moments.",
                f"Beautiful {product} crafted for your special celebrations.",
                f"Premium {fabric} {product} that speaks to your soul."
            ]
            
            template_idx = (variation_number - 1) % len(subjects)
            subject = subjects[template_idx]
            body = bodies[template_idx]
            
            if discount > 0:
                subject = f"{discount}% Off {subject}"
                
            return f"**{subject}**\n{body}"
        elif content_type == "WhatsApp Broadcast":
            templates = [
                f"{template['line1']}\n\n{template['line2']}\n\n{template['line3']}",
                f"Perfect timing for {festival}\n\n{template['line2']}\n\n{template['line3']}",
                f"Something special just arrived\n\n{template['line2']}\n\n{template['line3']}"
            ]
            return templates[(variation_number - 1) % len(templates)]
        else:
            return f"{template['line1']}\n\n{template['line2']}\n\n{template['line3']}"
    
    def _create_pmax_fallback(self, product: str, brand: str, fabric: str, festival: str, discount: int) -> str:
        """Simple PMAX fallback"""
        
        headlines = [
            f"New {product}", f"{brand} Style", f"Premium {fabric}", f"Perfect Fit", "Quality First",
            "Shop Now", "Get Yours", "Trending", "Must Have", "Best Choice",
            "Modern Style", "Classic Look", "Fresh Design", "Top Quality", "Great Value"
        ]
        
        descriptions = [
            f"Discover premium {fabric} {product} for {festival}",
            f"{brand} quality craftsmanship in every piece",
            f"Perfect {product} for your special moments",
            f"Handpicked {fabric} designs for you",
            f"Premium quality {product} now available"
        ]
        
        long_headlines = [
            f"{brand} Premium {product} - Quality {fabric} Collection",
            f"Perfect {fabric} {product} for {festival} Celebrations",
            f"New {product} Collection - Handcrafted {fabric} Pieces",
            f"{brand} {fabric} {product} - Modern Style Statement",
            f"Premium {product} in {fabric} - Shop the Collection"
        ]
        
        # Add discount to descriptions if present
        if discount > 0:
            descriptions[0] = f"{discount}% off premium {fabric} {product}"
        
        result = "Headlines:\n" + '\n'.join(headlines)
        result += "\n\nDescriptions:\n" + '\n'.join(descriptions)
        result += "\n\nLong Headlines:\n" + '\n'.join(long_headlines)
        return result