BANNED_WORDS = [
    "discover", "explore", "embrace", "immerse",
    "timeless", "elegance", "luxury", "opulence", "wrap", "celebrate", "effortless"
]

def build_prompt(data: dict) -> str:
    """Enhanced prompts for human-like, expert marketer quality copy generation."""

    # 1. EMAIL SUBJECT LINES - Enhanced for human-like, expert quality
    if data['category'] == "Email Subject Lines":
        return f"""You are a professional email copywriter for premium fashion brands. Create one email hero section with these three parts written in a human daily conversation and expert marketer style and don't use robotic symbols eg '-' or '!':

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
        
        return f"""You're a professional content creator writing Google Ads copy for a premium fashion brand. Write like you're chatting with friends who totally get style, but keep it conversion-focused and don't use robotic symbols eg '-' or '!'. 

    Format EXACTLY as shown:

    Headlines (max {headline_limit} characters each)
    [Create 15 headlines, each max {headline_limit} chars, mixing brand-specific and product-focused lines]

    Description (max {description_limit} characters each)
    [Create 5 descriptions, each max {description_limit} chars, written like you're personally recommending this to a style-savvy friend]

    Long Headlines (max {long_headline_limit} characters each)
    [Create 5 long headlines, each max {long_headline_limit} chars, telling the story like you're genuinely excited to share]

    Work these in naturally like you're having a conversation:
    • What we're talking about: {data['product']}
    • The Brand Name: {data['brand']}
    • Why it's amazing: {data['usp']}
    • What it's made from: {data['fabric']}
    • Perfect for: {data['festival']}
    • Special deal: {data['discount']}% off (mention in 2-3 places only if >0)
    • The feels: {data.get('emotion', 'Premium quality')}

    Headlines should feel like:
    - "Brand Name Festival Edit" (lead with brand + collection)
    - "Festival Styles by Brand Name" (mix it up)
    - Natural mentions of the occasion and product fabric
    - Conversational but premium product mentions
    - Like something you'd actually say to recommend a brand

    Descriptions should sound like you're texting a friend use below examples as inspiration and write in a friendly, everyday human voice:
    "You HAVE to see Brand's new collection—anarkalis, lehengas, the whole deal for [occasion]"
    "Just discovered Brand's [fabric] pieces and they're perfect for [festival]"
    "Brand just dropped their [collection] and honestly, it's everything"

    Long Headlines tell the full story use below examples as inspiration and write in a friendly, everyday human voice:
    "Honestly obsessed with Brand's new [occasion] edit—anarkalis, lehengas & more"
    "Brand's [fabric] collection just landed and it's perfect for [occasion] season"

    Skip these overused words: {', '.join(BANNED_WORDS)}

    Write in the exact format shown above. Make it sound like a content creator who genuinely loves fashion talking to their audience—professional but real."""


    # 2. LONG CONTENT  ──────────────────────────────────────────────
    if data['category'] == "Long Content":
        return f"""You are a professional copywriter for premium fashion brands and site banners. Create three parts in a warm, human daily conversational tone and don't use robotic symbols eg '-' or '!':

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
        return f"""You are a professional scroll-stopping captions writer for premium fashion brands. Give me three lines in a friendly, everyday human voice and don't use robotic symbols eg '-' or '!':

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
    4. Keep it under {data['char_limit']} characters total.

    Write ONLY the requested copy—nothing extra."""


    # 5. WHATSAPP BROADCAST - Enhanced for personal feel
    if data['category'] == "WhatsApp Broadcast":
        return f"""Write a WhatsApp message that feels like a personal recommendation from a stylish friend, not a brand broadcast and don't use robotic symbols eg '-' or '!'.

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
    - Share excitement genuinely for the product
    - Mention the occasion casually 
    - Mention specific benefits, Brand they'd care about
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