BANNED_WORDS = [
    "discover", "explore", "embrace", "immerse",
    "timeless", "elegance", "luxury", "opulence", "wrap", "celebrate", "effortless"
]

def build_prompt(data: dict) -> str:
    """Enhanced prompts for human-like, expert marketer quality copy generation."""

    # 1. EMAIL SUBJECT LINES - Enhanced for human-like, expert quality
    if data['category'] == "Email Subject Lines":
        return f"""You write email copy for premium fashion brands. Create one email hero section with these three parts written in a human daily conversation and expert marketer style:

    STEP 1 – HEADLINE  
    Write ONE new catchy line that sounds like something you'd actually say to a friend:
    From "I Do" to After-Party – We've Got You  
    Sister of the Bride? Dress Like It 💖  
    Bridesmaid Looks You'll Love Forever  
    Not the Bride, Still the Showstopper ✨  

    Make it fresh, conversational, and real. Skip these overused words: {', '.join(BANNED_WORDS)}. 
    Use emojis sparingly—only when they feel natural.

    STEP 2 – DESCRIPTION  
    Write a flowing paragraph that tells the story naturally. Work in these details like you're having a conversation:
    – What we're talking about: {data['product']}  
    – Why it's special: {data['usp']}  
    – What it's made from: {data['fabric']}  
    – Perfect timing for: {data['festival']}  
    – Special deal: {data['discount']}% off (mention only if there's actually a discount)  
    – Why act now: {data['timing']}  

    Keep the tone {data['tone']}—like you're genuinely excited to share this with someone who gets fashion. Write it as one smooth paragraph, not choppy sentences.

    STEP 3 – CALL TO ACTION  
    End with a simple, compelling phrase (2-5 words): "Shop Now", "Get Yours Today", "See the Collection" 

    FORMAT REQUIREMENTS  
    1. Output exactly three blocks in this order: Headline, *blank line*, Description, *blank line*, CTA.  
    2. Do **NOT** label the blocks (“Step 1”, “Headline”, etc.).  
    3. Preserve line breaks exactly as instructed so the consuming app can split on blank lines.
    4. Keep the total character count under {data['char_limit']} characters.

    Write ONLY the requested copy—nothing extra."""

    # 2. PMAX - Enhanced with specific character limits
    if data['category'] == "PMAX":
        headline_limit = data['char_limit']['headlines']
        description_limit = data['char_limit']['description']
        long_headline_limit = data['char_limit']['long_headlines']
        
        return f"""Create Google Ads PMAX copy that sounds human and converts. Write like an expert performance marketer who understands premium fashion.

    Format EXACTLY as shown:

    Headlines (max {headline_limit} characters each)
    [Create 5 headlines, each max {headline_limit} chars, punchy and human-sounding]

    Description (max {description_limit} characters each)
    [Create 5 descriptions, each max {description_limit} chars, focusing on emotion and benefit]

    Long Headlines (max {long_headline_limit} characters each)
    [Create 2 long headlines, each max {long_headline_limit} chars, more descriptive and story-driven]

    Use these inputs naturally:
    • Product: {data['product']}
    • Key benefit: {data['usp']}
    • Materials: {data['fabric']}
    • Occasion: {data['festival']}
    • Discount: {data['discount']}% (if {data['discount']} > 0)
    • Emotional hook: {data.get('emotion', 'Premium quality')}

    Write headlines that:
    - Sound conversational, not robotic
    - Focus on outcomes and feelings
    - Include specific product benefits
    - IMPORTANT: If discount is {data['discount']}% (greater than 0), include it in 2-3 headlines
    - Create urgency when appropriate
    - Feel premium but approachable

    Never use: {', '.join(BANNED_WORDS)}

    Example style (don't copy exactly):
    Headlines
    Perfect for special moments
    Premium comfort collection
    Festival ready styles
    Up to 20% off today
    Handcrafted with love

    Write in the exact format shown above with strict character limits."""

    # 2. LONG CONTENT  ──────────────────────────────────────────────
    if data['category'] == "Long Content":
        return f"""You are a expert copywriter for premium fashion brands and site banners. Create three parts in a warm, human daily conversational tone:

    STEP 1 – HEADLINE  
    • ONE punchy new headline that blends the moment and the offer, e.g.  
    COMING SOON End of Season Sale is Almost Here!  
    Teej Sale Up to 50% Off  
    Summer Sale Made for Sunny Days  
    • Keep it fresh, conversational, and skip these words: {', '.join(BANNED_WORDS)}.  
    • 0-1 emoji only if it feels natural.

    STEP 2 – DESCRIPTION  
    • ONE smooth paragraph, line breaks only if words exceed 30 characters.  
    • Work in:  
    – Product/collection: {data['product']}  
    – Why it matters: {data['usp']} and {data['attributes']}  
    – Materials: {data['fabric']}  
    – Occasion: {data['festival']}  
    – Deal: {data['discount']}% off (mention only if >0)  
    – Urgency: {data['timing']}  
    • Keep the tone {data['tone']}—like you're genuinely excited to share this with someone who gets fashion. Write it as one smooth paragraph, not choppy sentences, no bullet points, no clichés.

    STEP 3 – CTA  
    • A random eye-catching word or phrase (2-5 words) to close, e.g. “Shop Now”, “Get Yours Today”, “Shop Soon”.

    FORMAT  
    1. Output exactly three blocks in this order: Headline, *blank line*, Description, *blank line*, CTA.  
    2. Do **NOT** label the blocks.  
    3. Preserve the blank lines exactly so the app can split them.
    4. Keep it under {data['char_limit']} characters total.

    Write ONLY the requested copy—nothing extra."""

    # 3. CONCISE CONTENT ───────────────────────────────────────────
    if data['category'] == "Concise Content":
        return f"""You are a expert scroll-stopping captions writer for premium fashion brands. Give me three lines in a friendly, everyday human voice:

    STEP 1 – HEADLINE  
    • ONE fresh opener that sparks curiosity or names the moment.  
    Example vibes: “Bridesmaid Glow-Up ✨” / “Weekend Wardrobe Sorted”.  
    • Avoid these words: {', '.join(BANNED_WORDS)}.  

    STEP 2 – DESCRIPTION
    • ONE line weaving in:  
    – {data['product']}  
    – {data['usp']} / {data['attributes']}  
    – {data['fabric']}  
    – {data['discount']}% off if >0  
    – Occasion cue: {data['festival']}  
    • Keep the tone {data['tone']}—like you're genuinely excited to share this with someone who gets fashion. Write it as one smooth paragraph, not choppy sentences.


    STEP 3 – CTA  
    • A random eye-catching punchy 2-4-word closer such as “Shop Now”, “Grab Yours”, “Try It On”.

    FORMAT  
    1. Output exactly three text blocks in order: HEADLINE, *blank line*, DESCRIPTION, *blank line*, CTA.  
    2. Do **NOT** label the blocks.  
    3. Preserve the blank lines so the app can split them.

    Write ONLY the requested copy—nothing extra."""


    # 5. WHATSAPP BROADCAST - Enhanced for personal feel
    if data['category'] == "WhatsApp Broadcast":
        return f"""Write a WhatsApp message that feels like a personal recommendation from a stylish friend, not a brand broadcast.

    Create 3-4 lines that feel warm and personal:

    Line 1: Friendly opener with occasion/excitement (1 emoji max)
    Line 2: Product recommendation with personal touch
    Line 3: Why it's special (benefit/craft/occasion fit)
    Line 4: Sign off with brand warmth

    Use these elements naturally:
    • Product: {data['product']}
    • Why it's special: {data['usp']}
    • Materials: {data['fabric']}
    • Occasion: {data['festival']}
    • Offer: {data['discount']}% off
    • Personal emotion: {data.get('emotion', 'Premium quality')}
    • Keep the tone {data['tone']}—like you're genuinely excited to share this with someone who gets fashion. Write it as one smooth paragraph, not choppy sentences.
    

    Example style (don't copy just use as inspiration):
    Hey, Raksha Bandhan's here! 🎁
    Just saw the new collection and had to share - they're absolutely beautiful
    The materials feel amazing and they're perfect for gifting (or keeping for yourself!)
    Love, Team [Brand Name]
    or 
    Sharp Hues, Sharper Moves 👖✨
    Denim, Done Right
    Your go-to essential, reimagined. Clean cuts, bold fits, and tailored edge—these denims are made to move with you from work to weekend, AM to PM.
    Find your perfect fit today.

    With love,
    Team Notebook


    Write like you're texting a friend who loves fashion:
    - Use "you" and "your" naturally
    - Share excitement genuinely  
    - Mention specific benefits they'd care about
    - IMPORTANT: If discount is {data['discount']}% (greater than 0), mention it naturally
    - Add one emoji only if it feels natural
    - Sign off warmly with team name

    Never use: {', '.join(BANNED_WORDS)}
    Keep under {data['char_limit']} characters.

    Write ONLY the message lines, no extra formatting:"""
    
    # Fallback for any other category
    return f"""Write premium fashion copy that sounds completely human and expert-crafted. 

Use: {data['product']} | {data['usp']} | {data['fabric']} | {data['festival']} | {data['discount']}% off | {data.get('emotion', 'Premium quality')}

Create copy that:
- Sounds like an expert marketer wrote it
- Builds emotional connection
- Feels premium but warm
- Includes clear value proposition
- Ends with compelling action

Never use: {', '.join(BANNED_WORDS)}
Keep under {data['char_limit']} characters."""