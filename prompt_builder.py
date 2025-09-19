import random
import time

BANNED_WORDS = [
    "discover", "explore", "embrace", "immerse",
    "timeless", "elegance", "luxury", "opulence", "wrap", "celebrate", "effortless"
]

class PromptBuilder:
    def __init__(self):
        # Expanded creative hooks for maximum diversity
        self.creative_hooks = {
            "openers": [
                # Direct starters
                "Introducing", "Meet your new", "New arrival", "Perfect for", "Premium", "Handpicked",
                "Fresh drop", "Just landed", "Now available", "Unveiling", "Presenting", "Ready to wear",
                
                # Question starters  
                "What if you could", "Imagine wearing", "How would you feel", "Ever dreamed of", 
                "Picture yourself", "Ready for", "Looking for", "Want to feel", "Need something",
                
                # Story starters
                "Every woman deserves", "Step into a world", "Your story begins", "When style meets",
                "Special moments call", "The perfect choice", "Made for moments", "Designed for you",
                "Crafted with care", "Born from tradition", "Modern meets classic", "Style redefined"
            ],
            
            "emotions": [
                "confidence", "sophistication", "quality", "transformation", "joy", "empowerment",
                "aspiration", "dreams", "lifestyle", "comfort", "beauty", "grace", "charm",
                "radiance", "allure", "poise", "strength", "individuality", "freedom", "warmth"
            ],
            
            "benefits": [
                "premium craftsmanship", "superior comfort", "perfect fit", "feel confident", 
                "express yourself", "shine brightly", "elevated style", "memorable moments",
                "personal expression", "authentic style", "unique design", "modern comfort",
                "traditional artistry", "contemporary flair", "versatile wear", "statement making"
            ],
            
            "descriptors": [
                "stunning", "beautiful", "gorgeous", "chic", "stylish", "trendy", "fashionable",
                "sophisticated", "refined", "polished", "striking", "captivating", "alluring",
                "graceful", "vibrant", "bold", "contemporary", "classic", "modern", "artistic"
            ],
            
            "occasions": [
                "special occasions", "festive moments", "celebrations", "gatherings", "parties",
                "weddings", "festivals", "ceremonies", "events", "outings", "dates", "meetings",
                "casual wear", "office wear", "weekend style", "evening wear", "daytime charm"
            ]
        }
        
        # Diverse CTA options
        self.cta_library = [
            "Shop Now", "Get Yours", "Order Today", "Buy Now", "Secure Yours",
            "Discover More", "Feel The Difference", "Experience Magic", "Find Your Perfect", 
            "See The Beauty", "Begin Your Journey", "Live Your Story", "Embrace Your Style",
            "Create Memories", "Step Into Luxury", "Add To Cart", "View Collection",
            "Browse Now", "Start Shopping", "Claim Yours", "Make It Yours", "Try Today"
        ]
        
        # Dynamic sentence structures for variety
        self.sentence_structures = [
            "{opener} {product} in {fabric}",
            "{product} crafted in {fabric} for {occasion}",
            "{fabric} {product} that {benefit}",
            "Perfect {product} featuring {fabric}",
            "{brand} presents {product} in {fabric}",
            "Stunning {product} made from {fabric}",
            "Your new favorite {product} in {fabric}",
            "{occasion} calls for {fabric} {product}"
        ]
        
        # Time-based randomization seed
        self.session_seed = int(time.time() * 1000000) % 999999
        
    def build_unique_prompt(self, data: dict, variation_number: int, content_type: str, 
                           previous_hooks: list = None, previous_phrases: list = None) -> str:
        """Build completely unique prompts with dynamic randomization"""
        
        # Create unique seed for this specific generation
        unique_seed = self.session_seed + variation_number * 1000 + hash(str(data)) % 1000
        random.seed(unique_seed)
        
        # Get diverse creative elements
        opener = random.choice([h for h in self.creative_hooks["openers"] 
                              if h.lower() not in [p.lower() for p in (previous_hooks or [])]])
        emotion = random.choice(self.creative_hooks["emotions"])
        benefit = random.choice(self.creative_hooks["benefits"])
        descriptor = random.choice(self.creative_hooks["descriptors"])
        occasion = random.choice(self.creative_hooks["occasions"])
        
        # Dynamic approach based on variation
        approaches = [
            "feature-first with product benefits",
            "emotion-driven with lifestyle focus", 
            "storytelling with aspirational tone",
            "question-based with engagement focus",
            "benefit-focused with practical appeal"
        ]
        approach = approaches[variation_number % len(approaches)]
        
        # Build creative direction
        creative_direction = f"""
CREATIVE VARIATION #{variation_number} UNIQUE APPROACH:
- Opening Hook: "{opener}" (never used before)
- Emotional Core: {emotion}
- Key Benefit: {benefit}
- Style Descriptor: {descriptor}
- Occasion Context: {occasion}
- Writing Approach: {approach}
- Randomization Seed: {unique_seed}
"""
        
        # Base requirements with dynamic elements
        base_requirements = self._build_enhanced_base_requirements(data, creative_direction)
        
        # Format-specific prompts with enhanced creativity
        if content_type == "Email Subject Lines":
            return self._build_email_prompt(base_requirements, data, variation_number, opener, unique_seed)
        elif content_type == "WhatsApp Broadcast":
            return self._build_whatsapp_prompt(base_requirements, data, variation_number, opener, unique_seed)
        elif content_type == "Concise Content":
            return self._build_concise_prompt(base_requirements, data, variation_number, opener, unique_seed)
        elif content_type == "Long Content":
            return self._build_long_prompt(base_requirements, data, variation_number, opener, unique_seed)
        elif content_type == "PMAX":
            return self._build_pmax_prompt(base_requirements, data, variation_number, opener, unique_seed)
        else:
            return self._build_general_prompt(base_requirements, data, variation_number, opener, unique_seed)
    
    def _build_enhanced_base_requirements(self, data: dict, creative_direction: str) -> str:
        """Enhanced base requirements with more context"""
        product = data.get('product', '').strip()
        brand = data.get('brand', '').strip()
        fabric = data.get('fabric', '').strip()
        festival = data.get('festival', '').strip()
        discount = data.get('discount', 0)
        char_limit = data.get('char_limit', 300)
        tone = data.get('tone', 'casual').strip()
        usp = data.get('usp', 'Premium Quality').strip()
        attributes = data.get('attributes', 'Expertly crafted').strip()
        
        return f"""
PRODUCT CONTEXT:
- Product: {product}
- Brand: {brand} 
- Fabric/Material: {fabric}
- Occasion/Festival: {festival}
- Discount: {discount}% {'(prominently feature)' if discount > 0 else '(ignore discount)'}
- USP: {usp}
- Key Attributes: {attributes}
- Brand Tone: {tone}
- Character Limit: {char_limit}

{creative_direction}

CONTENT RULES:
- BANNED WORDS (absolutely avoid): {', '.join(BANNED_WORDS)}
- Use only periods (.) and commas (,) - NO exclamation marks (!) or dashes (-)
- Create genuinely different content from previous variations
- Focus on unique angles and perspectives
- Make each line meaningful and complete
"""

    def _build_email_prompt(self, base_requirements: str, data: dict, variation_number: int, opener: str, seed: int) -> str:
        """Enhanced email subject line prompt with more variety"""
        random.seed(seed)
        structure = random.choice([
            "statement + benefit + action",
            "question + solution + cta", 
            "problem + solution + urgency",
            "feature + emotion + action",
            "story + benefit + cta"
        ])
        
        return f"""{base_requirements}

EMAIL SUBJECT LINE - VARIATION #{variation_number}:

UNIQUE CREATIVE APPROACH:
- Structure Pattern: {structure}
- Opening Style: Start with "{opener}" concept
- Variation Focus: Make this completely different from any previous attempts
- Randomization: Using seed {seed} for uniqueness

FORMAT REQUIREMENTS - FOLLOW EXACTLY:
Line 1: [Complete headline sentence - unique opening]
[blank line]
Line 2: [Complete description sentence - connects product to occasion] 
[blank line]
Line 3: [2-3 word action CTA]

CRITICAL GENERATION RULES:
- NO labels like "Headline:" "Subject:" "Description:" "CTA:"
- NO bullet points, numbering, quotes, or formatting
- Each line must be complete, meaningful, and grammatically correct
- Character limit: {data.get('char_limit', 200)} total across all lines
- Start with completely different words than any previous variation
- Use natural, conversational language

EXAMPLE STRUCTURE (create something entirely different):
{opener} {data.get('product', 'collection')} pieces arriving now

Premium {data.get('fabric', 'fabric')} perfect for {data.get('festival', 'occasions')} celebrations

Shop Today

OUTPUT ONLY the 3 lines with blank lines between. No explanations or additional text."""

    def _build_whatsapp_prompt(self, base_requirements: str, data: dict, variation_number: int, opener: str, seed: int) -> str:
        """Enhanced WhatsApp prompt with conversational variety"""
        random.seed(seed)
        conversation_style = random.choice([
            "friendly and personal",
            "exciting and energetic",
            "warm and inviting", 
            "sophisticated and refined",
            "casual and relatable"
        ])
        
        return f"""{base_requirements}

WHATSAPP BROADCAST - VARIATION #{variation_number}:

CONVERSATION STYLE: {conversation_style}
OPENING APPROACH: Use "{opener}" concept creatively
RANDOMIZATION: Seed {seed} for unique generation

FORMAT REQUIREMENTS:
Line 1: [Engaging headline - conversation starter]
[blank line]
Line 2: [Story continuation - product details naturally woven in]
Line 3: [Emotional connection - why this matters now]
[blank line] 
Line 4: [Clear, friendly CTA]

WHATSAPP-SPECIFIC RULES:
- Write like you're texting a friend about something exciting
- Use {conversation_style} tone throughout
- Character limit: {data.get('char_limit', 400)} total
- Make it feel personal and immediate
- NO formal business language
- Connect {data.get('festival', 'occasion')} to personal moments

OUTPUT ONLY the 4 lines with proper blank line spacing. No labels or explanations."""

    def _build_concise_prompt(self, base_requirements: str, data: dict, variation_number: int, opener: str, seed: int) -> str:
        """Enhanced concise content with punchy variety"""
        random.seed(seed)
        energy_level = random.choice(["high-energy", "calm confidence", "warm enthusiasm", "sophisticated charm"])
        
        return f"""{base_requirements}

CONCISE CONTENT - VARIATION #{variation_number}:

ENERGY STYLE: {energy_level}
OPENING HOOK: "{opener}" approach
UNIQUE SEED: {seed}

FORMAT STRUCTURE:
Line 1: [Punchy headline - grab attention immediately]
[blank line]
Line 2: [Smart description - pack maximum value in minimum words]
[blank line]
Line 3: [Power CTA - 2-4 words that drive action]

CONCISE-SPECIFIC RULES:
- Every word must earn its place
- {energy_level} tone throughout
- Character limit: {data.get('char_limit', 200)} total
- Make each line independently powerful
- Focus on immediate impact
- No filler words or phrases

INSPIRATION (create something completely different):
Transform your {data.get('festival', 'style')} wardrobe

{data.get('fabric', 'Premium')} {data.get('product', 'pieces')} that speak your language

Get Yours

OUTPUT ONLY the 3 lines with blank lines. No explanations."""

    def _build_long_prompt(self, base_requirements: str, data: dict, variation_number: int, opener: str, seed: int) -> str:
        """Enhanced long content with narrative variety"""
        random.seed(seed)
        narrative_style = random.choice([
            "storytelling journey",
            "lifestyle transformation", 
            "emotional journey",
            "behind-the-scenes craft",
            "personal connection"
        ])
        
        return f"""{base_requirements}

LONG CONTENT - VARIATION #{variation_number}:

NARRATIVE APPROACH: {narrative_style}
OPENING TECHNIQUE: "{opener}" style
GENERATION SEED: {seed}

FORMAT STRUCTURE:
Line 1: [Compelling headline - sets the stage]
[blank line]
Line 2: [Scene setting - paint the picture]
Line 3: [Product integration - naturally weave in details]
[blank line]
Line 4: [Motivating CTA - 3-5 words]

LONG-FORM SPECIFIC RULES:
- Use {narrative_style} approach throughout
- Character limit: {data.get('char_limit', 500)} total
- Create a mini-story that flows naturally
- Make the reader visualize themselves in the scenario
- Seamlessly blend {data.get('festival', 'occasion')} context
- End with compelling reason to act now

OUTPUT ONLY the 4 lines with proper spacing. No labels or extra text."""

    def _build_pmax_prompt(self, base_requirements: str, data: dict, variation_number: int, opener: str, seed: int) -> str:
        """Enhanced PMAX with diverse ad approaches"""
        random.seed(seed)
        ad_strategy = random.choice([
            "benefit-focused variety",
            "emotion-driven mix",
            "feature-benefit blend",
            "lifestyle-aspiration combo",
            "problem-solution approach"
        ])
        
        return f"""{base_requirements}

GOOGLE ADS PMAX - VARIATION #{variation_number}:

AD STRATEGY MIX: {ad_strategy}
CREATIVE DIRECTION: "{opener}" family of approaches
RANDOMIZATION: Seed {seed} for maximum variety

REQUIRED FORMAT:
Headlines:
[15 different headlines under 30 chars each - mix approaches]

Descriptions:
[5 varied descriptions under 90 chars each - different angles]  

Long Headlines:
[5 diverse long headlines under 120 chars each - story variety]

PMAX DIVERSITY RULES:
- Use {ad_strategy} as primary strategy
- Within each section, vary the approach significantly
- Headlines: Mix direct, emotional, and benefit-focused
- Descriptions: Tell different mini-stories
- Long Headlines: Use various narrative techniques
- Character limits: Headlines=30, Descriptions=90, Long Headlines=120
- Each item should feel fresh and unique

GENERATION APPROACH:
- Start headlines with different word patterns
- Vary emotional triggers across descriptions
- Use different fabric/festival combinations
- Mix urgent and aspirational tones
- Include variety of CTAs naturally

OUTPUT EXACTLY in the 3-section format shown above. No additional formatting."""

    def _build_general_prompt(self, base_requirements: str, data: dict, variation_number: int, opener: str, seed: int) -> str:
        """Enhanced general prompt with flexible creativity"""
        random.seed(seed)
        creative_angle = random.choice([
            "lifestyle integration",
            "personal transformation",
            "social connection", 
            "self-expression",
            "quality craftsmanship",
            "cultural celebration"
        ])
        
        return f"""{base_requirements}

GENERAL MARKETING COPY - VARIATION #{variation_number}:

CREATIVE ANGLE: {creative_angle}
OPENING STRATEGY: "{opener}" approach
UNIQUE SEED: {seed}

FLEXIBLE FORMAT:
Line 1: [Strong headline - {creative_angle} focus]
[blank line]
Line 2: [Rich description - blend all key elements naturally]
[blank line]
Line 3: [Action CTA - motivating and clear]

GENERAL COPY RULES:
- Focus on {creative_angle} throughout
- Character limit: {data.get('char_limit', 300)} total
- Make it feel authentic and relatable
- Blend {data.get('festival', 'occasion')} context naturally
- Highlight {data.get('fabric', 'quality')} appropriately
- End with clear next step

OUTPUT ONLY the 3 lines with blank lines between. No labels."""

    def create_fallback_content(self, data: dict, content_type: str, variation_number: int) -> str:
        """Enhanced fallback with more variety"""
        # Use time-based randomization for fallback too
        fallback_seed = int(time.time() * 1000) % 10000 + variation_number
        random.seed(fallback_seed)
        
        product = data.get('product', 'Fashion Collection')
        brand = data.get('brand', 'Premium Brand')
        fabric = data.get('fabric', 'Quality Fabric')
        festival = data.get('festival', 'Special Occasions')
        discount = data.get('discount', 0)
        
        # More diverse fallback templates
        fallback_options = [
            {
                "headline": f"New {product} arrivals just dropped",
                "description": f"Stunning {fabric} pieces perfect for your {festival} moments",
                "cta": random.choice(["Shop Now", "Browse Collection", "View Styles"])
            },
            {
                "headline": f"Your perfect {festival} outfit awaits",
                "description": f"Beautiful {product} crafted in premium {fabric}",
                "cta": random.choice(["Discover More", "Find Yours", "Explore Now"])
            },
            {
                "headline": f"{brand} presents {product} magic",
                "description": f"Handpicked {fabric} designs for memorable {festival} celebrations",
                "cta": random.choice(["Get Started", "See Collection", "Shop Today"])
            },
            {
                "headline": f"Transform your {festival} style story",
                "description": f"Premium {fabric} {product} that speaks to your soul",
                "cta": random.choice(["Start Journey", "Create Magic", "Make Memories"])
            }
        ]
        
        template = random.choice(fallback_options)
        
        # Add discount naturally if present
        if discount > 0:
            template["description"] = f"{discount}% off {template['description'].lower()}"
        
        if content_type == "PMAX":
            return self._create_enhanced_pmax_fallback(product, brand, fabric, festival, discount, fallback_seed)
        else:
            return f"{template['headline']}\n\n{template['description']}\n\n{template['cta']}"
    
    def _create_enhanced_pmax_fallback(self, product: str, brand: str, fabric: str, festival: str, discount: int, seed: int) -> str:
        """Enhanced PMAX fallback with more variety"""
        random.seed(seed)
        
        headline_starters = ["New", "Premium", "Perfect", "Stunning", "Beautiful", "Handcrafted", "Quality", 
                           "Modern", "Classic", "Stylish", "Trendy", "Chic", "Sophisticated", "Unique", "Special"]
        random.shuffle(headline_starters)
        
        headlines = []
        for i, starter in enumerate(headline_starters[:15]):
            if i % 3 == 0:
                headlines.append(f"{starter} {product}"[:30])
            elif i % 3 == 1:
                headlines.append(f"{starter} {fabric}"[:30])
            else:
                headlines.append(f"{brand} {starter}"[:30])
        
        desc_templates = [
            f"Discover {product} in {fabric} for {festival}",
            f"{brand} premium {fabric} now available",
            f"Handcrafted {product} for special moments",
            f"Your perfect {fabric} {product} awaits",
            f"New {product} collection in {fabric}"
        ]
        
        long_headline_templates = [
            f"{brand} Premium {fabric} {product} - Handcrafted Excellence",
            f"Discover {product} Magic in {fabric} - Perfect for {festival}",
            f"New {fabric} {product} Collection - Quality Guaranteed",
            f"{brand} {product} - Where Tradition Meets Modern Style",
            f"Premium {fabric} {product} - Made for Special Moments"
        ]
        
        result = "Headlines:\n"
        for h in headlines:
            result += f"{h}\n"
        result += "\nDescriptions:\n"
        for d in desc_templates:
            result += f"{d[:90]}\n"
        result += "\nLong Headlines:\n"
        for lh in long_headline_templates:
            result += f"{lh[:120]}\n"
            
        return result.strip()

# Legacy compatibility function
def build_prompt(data: dict) -> str:
    """Legacy function for backward compatibility"""
    builder = PromptBuilder()
    # Add randomization to legacy calls too
    variation = random.randint(1, 3)
    return builder.build_unique_prompt(data, variation, "General")