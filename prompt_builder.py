import random

class ImprovedPromptBuilder:
    def __init__(self):
        self.banned_words = [
            "discover", "explore", "embrace", "immerse", "timeless", 
            "elegance", "luxury", "opulence", "wrap", "celebrate", "effortless"
        ]
        
        # Diverse greetings for different contexts
        self.greetings = [
            "Hey gorgeous", "Style lovers", "Fashion friends", "Beautiful souls",
            "Trendsetters", "Style mavens", "Fashion enthusiasts", "Darling",
            "Style icons", "Fashion family", "Lovely ladies", "Style queens",
            "Fashion lovers", "Hey beautiful", "Style stars", "Gorgeous girls",
            "Fashion tribe", "Style sisters", "Hey stunning", "Fashion forward"
        ]
        
        # Varied call-to-actions
        self.ctas = [
            "Shop Now", "Get Yours", "Order Today", "Buy Now", "Grab It",
            "Shop Today", "Get Started", "Find Yours", "Explore Now", "See More",
            "Shop Collection", "View All", "Check Out", "Browse Now", "Get This",
            "Shop Style", "Pick Yours", "Add to Cart", "See Collection", "Shop Here"
        ]
        
        # Opening hooks for variety
        self.opening_hooks = [
            "New arrivals alert", "Fresh styles just in", "Perfect timing",
            "Your wardrobe upgrade", "Style update incoming", "Fashion finds",
            "Something special arrived", "Ready for compliments", "Style goals unlocked",
            "Wardrobe refresh time", "Fashion alert", "Style inspiration",
            "New obsession incoming", "Perfect pieces found", "Style moment ready"
        ]
        
        # Emotional connectors
        self.emotional_connectors = [
            "designed for your special moments", "crafted for memorable occasions",
            "perfect for your celebrations", "made for standout moments",
            "created for your confidence", "tailored for your lifestyle",
            "styled for your success", "curated for your comfort",
            "chosen for your elegance", "selected for your grace",
            "picked for your personality", "matched to your vibe"
        ]
        
        # Expanded focus options for better targeting
        self.focus_types = [
            "direct_benefits", "emotional_connection", "aspirational_lifestyle",
            "problem_solution", "social_proof", "exclusivity_scarcity", 
            "transformation_story", "comfort_convenience", "quality_craftsmanship",
            "seasonal_relevance", "versatility_styling", "confidence_empowerment"
        ]
        
        # Expanded tone varieties for diverse voice
        self.tone_types = [
            "confident_clear", "warm_personal", "sophisticated_bold",
            "playful_fun", "intimate_conversational", "authoritative_expert",
            "friendly_approachable", "luxurious_premium", "casual_relatable",
            "inspiring_motivational", "elegant_refined", "trendy_youthful"
        ]
        
        # Expanded approach strategies for content structure
        self.approach_types = [
            "feature_benefit_action", "story_emotion_cta", "vision_product_urgency",
            "problem_solution_relief", "before_after_transformation", "social_proof_validation",
            "question_answer_action", "curiosity_reveal_close", "comparison_advantage_buy",
            "lifestyle_integration_cta", "trend_forecast_join", "expert_recommendation_trust"
        ]
        
        # Dynamic strategy assignment - randomly selects from expanded options
        self.strategies = {
            1: {
                "focus": random.choice(self.focus_types[:4]),  # First 4 for variation 1
                "tone": random.choice(self.tone_types[:4]),    # First 4 for variation 1
                "approach": random.choice(self.approach_types[:4])  # First 4 for variation 1
            },
            2: {
                "focus": random.choice(self.focus_types[4:8]),  # Middle 4 for variation 2
                "tone": random.choice(self.tone_types[4:8]),    # Middle 4 for variation 2
                "approach": random.choice(self.approach_types[4:8])  # Middle 4 for variation 2
            },
            3: {
                "focus": random.choice(self.focus_types[8:]),   # Last 4+ for variation 3
                "tone": random.choice(self.tone_types[8:]),     # Last 4+ for variation 3
                "approach": random.choice(self.approach_types[8:])  # Last 4+ for variation 3
            }
        }

    def _get_random_strategy(self, variation_number: int) -> dict:
        """Generate random strategy for each variation with different pools"""
        if variation_number == 1:
            # Business-focused strategies
            return {
                "focus": random.choice(self.focus_types[:4]),
                "tone": random.choice(self.tone_types[:4]), 
                "approach": random.choice(self.approach_types[:4])
            }
        elif variation_number == 2:
            # Emotional and social strategies  
            return {
                "focus": random.choice(self.focus_types[4:8]),
                "tone": random.choice(self.tone_types[4:8]),
                "approach": random.choice(self.approach_types[4:8])
            }
        else:
            # Lifestyle and aspiration strategies
            return {
                "focus": random.choice(self.focus_types[8:]),
                "tone": random.choice(self.tone_types[8:]),
                "approach": random.choice(self.approach_types[8:])
            }
    
    def get_strategy_options(self) -> dict:
        """Return available strategy options for UI selection"""
        return {
            "focus_types": self.focus_types,
            "tone_types": self.tone_types, 
            "approach_types": self.approach_types
        }
    
    def build_focused_prompt(self, data: dict, variation_number: int, content_type: str) -> str:
        """Build focused, strategy-based prompts with enhanced randomness"""
        
        # Regenerate strategy for each call to ensure randomness
        strategy = self._get_random_strategy(variation_number)
        
        # Select random elements
        greeting = random.choice(self.greetings)
        cta = random.choice(self.ctas)
        hook = random.choice(self.opening_hooks)
        connector = random.choice(self.emotional_connectors)
        
        # Extract data
        product = data.get('product', 'Premium Collection')
        brand = data.get('brand', 'Our Brand')
        fabric = data.get('fabric', 'Quality Materials')
        festival = data.get('festival', 'Special Occasions')
        discount = data.get('discount', 0)
        char_limit = data.get('char_limit', 300)
        tone = data.get('tone', 'Premium & Aspirational')
        
        base_prompt = f"""
Create fashion marketing copy variation #{variation_number}.

BRAND: {brand}
PRODUCT: {product} in {fabric}
OCCASION: {festival}
DISCOUNT: {discount}% {"(highlight this)" if discount > 0 else "(ignore)"}

STRATEGY: 
- Focus: {strategy['focus']} (what to emphasize)
- Tone: {strategy['tone']} (how to sound)
- Approach: {strategy['approach']} (content structure)

RANDOM ELEMENTS TO INCORPORATE:
- Greeting style: "{greeting}"
- Call-to-action: "{cta}" 
- Opening hook: "{hook}"
- Emotional connector: "{connector}"

RULES:
1. NO banned words: {', '.join(self.banned_words)}
2. Use periods and commas only - NO exclamation marks
3. No labels like "Headline:" or "Description:"
4. Character limit: {char_limit}
5. Make each line complete and natural

{self._get_format_instructions(content_type, strategy, greeting, cta, hook, connector)}
"""
        return base_prompt
    
    def _get_format_instructions(self, content_type: str, strategy: dict, greeting: str, cta: str, hook: str, connector: str) -> str:
        """Get format-specific instructions with random elements"""
        
        if content_type == "Email Subject Lines":
            return f"""
CREATE EMAIL (2 lines):
Line 1: **Bold subject** - use "{hook}" concept
Line 2: Email body - weave in "{connector}" naturally
Line 3: End with strong "{cta}" call-to-action

Write like a fashion brand email that gets opened.
"""
        
        elif content_type == "WhatsApp Broadcast":
            return f"""
CREATE WHATSAPP (3 lines):
Line 1: Start with "{greeting}" vibe - casual and friendly
Line 2: Develop the story with product details and connect emotionally - use "{connector}" idea and in at least 3-4 sentences.
Line 3: End with "{cta}" or similar

Write like texting a fashion-loving friend.
"""
        
        elif content_type == "PMAX":
            return f"""
CREATE GOOGLE ADS - 3 sections:

Headlines: (15 items, max 30 chars each)
Descriptions: (5 items, max 90 chars each)  
Long Headlines: (5 items, max 120 chars each)

Use variety - mix formal, casual, urgent, emotional tones.
Include "{cta}" in some headlines.
CHARACTER LIMITS ARE STRICT.
"""
        
        elif content_type == "Long Content":
            return f"""
CREATE STORY (4 lines):
Line 1: Open with "{hook}" energy
Line 2: Develop the story with product details
Line 3: Connect emotionally - use "{connector}" idea
Line 4: Close with "{cta}" power

Flow like a mini-story that sells.
"""
        
        else:  # Concise Content
            return f"""
CREATE CONCISE (3 lines):
Line 1: Punchy headline with "{hook}" feel
Line 2: Smart description with key benefits
Line 3: Strong "{cta}" finish

Make every word count.
"""
    
    def create_fallback_content(self, data: dict, content_type: str, variation_number: int) -> str:
        """Create reliable fallback content with enhanced randomness"""
        product = data.get('product', 'Premium Collection')
        brand = data.get('brand', 'Our Brand')
        fabric = data.get('fabric', 'Quality Materials')
        festival = data.get('festival', 'Special Occasions')
        discount = data.get('discount', 0)
        
        # Random selections for fallback with strategy influence
        strategy = self._get_random_strategy(variation_number)
        greeting = random.choice(self.greetings)
        cta = random.choice(self.ctas)
        hook = random.choice(self.opening_hooks)
        
        # Strategy-influenced templates
        if "direct_benefits" in strategy['focus']:
            templates = {
                1: {
                    "line1": f"{hook} - new {product} benefits",
                    "line2": f"Premium {fabric} delivers comfort and style for {festival}",
                    "line3": cta
                }
            }
        elif "emotional_connection" in strategy['focus']:
            templates = {
                2: {
                    "line1": f"{greeting}, feel amazing for {festival}",
                    "line2": f"Beautiful {product} in {fabric} connects to your heart",
                    "line3": cta
                }
            }
        else:  # aspirational/lifestyle
            templates = {
                3: {
                    "line1": f"Elevate your {festival} style with {brand}",
                    "line2": f"Stunning {fabric} {product} transforms your wardrobe",
                    "line3": cta
                }
            }
        
        # Default fallback structure
        default_template = {
            "line1": f"{hook} - new {product}",
            "line2": f"Premium {fabric} perfect for {festival}",
            "line3": cta
        }
        
        template = templates.get(variation_number, default_template)
        
        # Add discount if present
        if discount > 0:
            template["line2"] = f"{discount}% off {template['line2'].lower()}"
        
        if content_type == "PMAX":
            return self._create_pmax_fallback(product, brand, fabric, festival, discount, strategy)
        elif content_type == "Email Subject Lines":
            subjects = [
                f"{hook} - new {product}",
                f"Perfect for {festival} - {brand}",
                f"{discount}% off {product}" if discount > 0 else f"{brand} exclusive {product}"
            ]
            bodies = [
                f"Stunning {fabric} pieces designed for memorable moments.",
                f"Beautiful {product} crafted for your special celebrations.", 
                f"Premium {fabric} {product} ready for your wardrobe."
            ]
            
            template_idx = (variation_number - 1) % len(subjects)
            return f"**{subjects[template_idx]}**\n{bodies[template_idx]}"
            
        elif content_type == "WhatsApp Broadcast":
            whatsapp_templates = [
                f"{greeting}\n{template['line2']}\n{template['line3']}",
                f"{hook}\n{fabric} {product} perfect for {festival}\n{cta}",
                f"Perfect timing\n{template['line2']}\n{random.choice(self.ctas)}"
            ]
            return whatsapp_templates[(variation_number - 1) % len(whatsapp_templates)]
        else:
            return f"{template['line1']}\n\n{template['line2']}\n\n{template['line3']}"
    
    def _create_pmax_fallback(self, product: str, brand: str, fabric: str, festival: str, discount: int, strategy: dict = None) -> str:
        """Enhanced PMAX fallback with strategy-based randomness"""
        
        # Strategy-influenced headline generation
        if strategy and "quality_craftsmanship" in strategy['focus']:
            focus_headlines = [f"Handcrafted {product}", f"Artisan {fabric}", "Premium Made", "Quality Crafted", "Expert Design"]
        elif strategy and "exclusivity_scarcity" in strategy['focus']:
            focus_headlines = ["Limited Edition", "Exclusive Drop", "Rare Find", "Members Only", "Select Few"]
        elif strategy and "transformation_story" in strategy['focus']:
            focus_headlines = ["Transform Style", "New You", "Style Evolution", "Wardrobe Upgrade", "Fresh Look"]
        else:
            focus_headlines = [f"New {product}", f"{brand} Style", f"Premium {fabric}", "Perfect Fit", "Quality First"]
        
        # Dynamic headline mixing
        action_headlines = random.sample(self.ctas, 5)
        trend_headlines = ["Trending Now", "Must Have", "Best Choice", "Modern Look", "Classic Style"]
        seasonal_headlines = [f"Perfect for {festival}", "Season Ready", "Occasion Perfect", "Celebration Style", "Festive Ready"]
        
        # Combine and shuffle
        all_headlines = focus_headlines + action_headlines + trend_headlines + seasonal_headlines
        random.shuffle(all_headlines)
        headlines = all_headlines[:15]
        
        # Strategy-influenced descriptions
        if strategy and "comfort_convenience" in strategy['focus']:
            descriptions = [
                f"Comfortable {fabric} {product} for all-day wear during {festival}",
                f"Easy-care {product} that looks great and feels amazing",
                f"Hassle-free {fabric} pieces perfect for busy lifestyles",
                f"{brand} comfort meets style in every {product}",
                f"Effortless elegance in premium {fabric} collection"
            ]
        elif strategy and "social_proof" in strategy['focus']:
            descriptions = [
                f"Loved by thousands - premium {fabric} {product} for {festival}",
                f"Bestselling {product} collection trusted by style experts",
                f"Join the {brand} family with our top-rated {fabric} pieces",
                f"Customer favorite {product} perfect for special occasions",
                f"Highly recommended {fabric} collection for discerning taste"
            ]
        else:
            descriptions = [
                f"Premium {fabric} {product} for {festival}",
                f"{brand} quality craftsmanship in every piece",
                f"Perfect {product} {random.choice(self.emotional_connectors)}", 
                f"Handpicked {fabric} designs for discerning taste",
                f"New {product} collection now available online"
            ]
        
        # Enhanced long headlines with strategy
        if strategy and "aspirational_lifestyle" in strategy['focus']:
            long_headlines = [
                f"Elevate Your Style with {brand} Premium {product} Collection",
                f"Luxury {fabric} {product} for the Modern Fashion Enthusiast",
                f"Transform Your Wardrobe with {brand} Exclusive {product} Line",
                f"Sophisticated {fabric} {product} for Discerning Fashion Lovers",
                f"Premium Lifestyle Begins with {brand} {product} Collection"
            ]
        else:
            long_headlines = [
                f"{brand} Premium {product} - Quality {fabric} Collection",
                f"Perfect {fabric} {product} for {festival} Celebrations",
                f"New {product} Collection - Handcrafted {fabric} Pieces", 
                f"{brand} {fabric} {product} - Modern Style Statement",
                f"Premium {product} in {fabric} - {random.choice(self.ctas)} Collection"
            ]
        
        # Add discount elements if present
        if discount > 0:
            descriptions[0] = f"{discount}% off premium {fabric} {product}"
            headlines.append(f"{discount}% Off")
            long_headlines.append(f"Save {discount}% on Premium {product} Collection")
        
        result = "Headlines:\n" + '\n'.join(headlines[:15])
        result += "\n\nDescriptions:\n" + '\n'.join(descriptions[:5])
        result += "\n\nLong Headlines:\n" + '\n'.join(long_headlines[:5])
        return result