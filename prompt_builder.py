BANNED_WORDS = [
    "discover", "explore", "embrace", "immerse",
    "timeless", "elegance", "luxury", "opulence", "wrap", "celebrate", "effortless"
]

def build_prompt(data: dict) -> str:
    """Enhanced structure enforcement prompts with variation uniqueness and better format compliance."""
    
    product = data.get('product', '').strip()
    brand = data.get('brand', '').strip()
    fabric = data.get('fabric', '').strip()
    festival = data.get('festival', '').strip()
    discount = data.get('discount', 0)
    char_limit = data.get('char_limit', 300)
    tone = data.get('tone', 'casual').strip().lower()
    banned = ', '.join(BANNED_WORDS)
    
    # Extract style-specific elements for enhanced variation
    approach = data.get('approach', 'Create engaging content')
    opener = data.get('opener', 'New arrivals')
    cta_style = data.get('cta_style', 'Shop Now')
    emotion = data.get('emotion', 'special moments')
    variation_tone = data.get('tone', 'conversational')
    
    base_requirements = f"""
CORE REQUIREMENTS:
- Product: {product}
- Brand: {brand} 
- Fabric: {fabric}
- Occasion: {festival}
- Discount: {discount}% {'(include if > 0)' if discount > 0 else '(ignore)'}
- USP: {data.get('usp', 'Premium Quality')}
- Tone: {tone}
- Character Limit: {char_limit}
- Emotion: {emotion}

CREATIVE DIRECTION: {approach}
OPENING STYLE: {opener}
CTA PREFERENCE: {cta_style}

BANNED WORDS (avoid completely): {banned}
USE ONLY: Periods (.) and commas (,) for punctuation - NO exclamation marks (!) or dashes (-)

UNIQUENESS REQUIREMENT: This variation must be COMPLETELY different from other variations in:
- Opening words and phrases
- Emotional approach
- Benefit focus
- Sentence structure
- Call-to-action style"""

    if data['category'] == "Email Subject Lines":
        return f"""{base_requirements}

EMAIL SUBJECT LINE FORMAT - FOLLOW EXACTLY:

[Single line headline - complete sentence - USE UNIQUE OPENING: "{opener}" style or similar]

[Single line description - complete sentence about {festival}/{discount}%/{product} - DIFFERENT ANGLE THAN OTHER VARIATIONS]

[2-3 word CTA - USE "{cta_style}" STYLE]

ABSOLUTE STRUCTURE RULES:
- EXACTLY 3 lines with blank lines between them
- NO labels like "Headline:" "Subject:" "Description:" or "CTA:"
- NO bullet points (•), NO numbering (1,2,3), NO quotes ("")
- Each line must be complete and standalone
- Character limit: {char_limit} characters total
- Must blend {product}, {brand}, {fabric}, {festival} naturally
- MUST BE UNIQUE - different opening, different angle, different words

EXAMPLE STRUCTURE (create something completely different):
Weekend Style Refresh

New silk pieces perfect for Diwali celebrations  

Shop Now

CRITICAL: Output ONLY the 3 lines in the exact format shown. No explanations, no extra text, no labels."""

    elif data['category'] == "WhatsApp Broadcast":
        return f"""{base_requirements}

WHATSAPP BROADCAST FORMAT - FOLLOW EXACTLY:

[Single line headline - USE UNIQUE OPENING WORDS: "{opener}" approach]

[First description line - storytelling blend of {festival}, {product}, {brand}, {fabric} - DIFFERENT STORY ANGLE]
[Second description line - continues story - UNIQUE CONTINUATION]
[Optional third description line - soft nudge - DIFFERENT FROM OTHER VARIATIONS]

[2-3 word CTA - USE "{cta_style}" STYLE]

ABSOLUTE STRUCTURE RULES:
- Headline + multi-line description + CTA
- NO labels like "Headline:" or "Description:" or "CTA:"
- NO bullet points, NO numbering, NO quotes
- Description can be 2-3 lines but flows as one story
- Character limit: {char_limit} characters total
- MUST BE UNIQUE story and approach
- Each line meaningful and complete

EXAMPLE STRUCTURE (create something completely different):
Found your Raksha Bandhan look

Spotted this gorgeous silk kurta that flows beautifully
Perfect for those long family celebration nights
Thought you'd love it

Check it out

CRITICAL: Output ONLY in the exact format shown. No labels, no extra text."""

    elif data['category'] == "Concise Content":
        return f"""{base_requirements}

CONCISE CONTENT FORMAT - FOLLOW EXACTLY:

[Single headline line - USE UNIQUE OPENING WORDS: "{opener}" style]

[Single description line - storytelling focused, blend {festival}, {product}, {brand}, {fabric} - DIFFERENT BENEFIT/ANGLE]

[2-4 word CTA - USE "{cta_style}" STYLE]

ABSOLUTE STRUCTURE RULES:
- EXACTLY 3 lines with blank lines between them
- NO labels whatsoever
- NO bullet points, NO numbering, NO quotes
- Each line complete and meaningful
- Character limit: {char_limit} characters total
- MUST BE UNIQUE approach and words
- Focus on {emotion} feeling

EXAMPLE STRUCTURE (create something completely different):
Weekend wardrobe sorted

New linen pieces perfect for breezy festivities

Shop Now

CRITICAL: Output ONLY the 3 lines in exact format. No labels, no explanations."""

    elif data['category'] == "Long Content":
        return f"""{base_requirements}

LONG CONTENT FORMAT - FOLLOW EXACTLY:

[Single headline - USE UNIQUE OPENING WORDS: "{opener}" approach]

[First description line - sets scene, use {festival} and {discount if discount > 0 else 'premium quality'} - DIFFERENT SCENE/ANGLE]
[Second description line - explains benefit, use {product}, {brand}, {fabric} - UNIQUE BENEFIT FOCUS]

[3-5 word CTA - USE "{cta_style}" STYLE]

ABSOLUTE STRUCTURE RULES:
- Headline + 2 description lines + CTA (4 lines total with blank lines between)
- NO labels like "Headline:" or "Description:"
- NO bullet points, NO numbering, NO quotes
- Description lines flow together as one story
- Character limit: {char_limit} characters total
- MUST BE UNIQUE narrative and approach
- Channel {emotion} throughout

EXAMPLE STRUCTURE (create something completely different):
Festive Season Perfection

Our silk collection captures every special moment beautifully
Designed for celebrations that deserve nothing but the finest

Shop Collection

CRITICAL: Output ONLY in the exact format shown. No labels, no extra text."""

    elif data['category'] == "PMAX":
        return f"""{base_requirements}

GOOGLE ADS PMAX FORMAT - FOLLOW EXACTLY:

Headlines:
[15 short headlines under 30 characters each - VARY THE APPROACH: some "{opener}" style, some {emotion}, some product-focused]

Descriptions:  
[5 descriptions under 90 characters each - DIFFERENT ANGLES: benefit, feature, emotion, urgency, lifestyle]

Long Headlines:
[5 long headlines under 120 characters each - MIX OF: storytelling, feature+benefit, seasonal, brand+product, emotional]

ABSOLUTE STRUCTURE RULES:
- Use EXACTLY the labels "Headlines:", "Descriptions:", "Long Headlines:"
- NO bullet points, NO numbering within sections
- Each item on its own line
- Headlines: 30 char max each (aim for 25-30)
- Descriptions: 90 char max each (aim for 80-90)
- Long Headlines: 120 char max each (aim for 100-120)
- Include variations of {product}, {brand}, {fabric}, {festival}
- ENSURE DIVERSITY in approaches and angles
- Use {emotion} and {approach} throughout different items

CRITICAL: Follow the exact 3-section format with proper labels and character limits. Create diverse content across all sections."""

    else:
        # Fallback for any other category
        return f"""{base_requirements}

GENERAL MARKETING COPY FORMAT - FOLLOW EXACTLY:

[Single headline - UNIQUE OPENING: "{opener}" style]

[Single description line - blend {festival}, {product}, {brand}, {fabric} - DIFFERENT ANGLE]

[CTA - USE "{cta_style}" STYLE]

ABSOLUTE STRUCTURE RULES:
- EXACTLY 3 lines with blank lines between them
- NO labels, NO bullet points, NO quotes
- Character limit: {char_limit}
- MUST BE UNIQUE and different from other variations    
- Focus on {emotion}

CRITICAL: Output ONLY the 3 lines with blank lines between them. No explanations."""