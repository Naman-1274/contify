BANNED_WORDS = [
    "discover", "explore", "embrace", "immerse",
    "timeless", "elegance", "luxury", "opulence", "wrap", "celebrate"
]

def build_prompt(data: dict) -> str:
    """Enhanced prompts for human-like, expert marketer quality copy generation."""

    # 1. EMAIL SUBJECT LINES - Enhanced for human-like, expert quality
    if data['category'] == "Email Subject Lines":
        return f"""You are an expert fashion brand copywriter creating email subject lines that sound completely human and aspirational. Write like the most successful luxury fashion marketers.

Create 8-10 email subject lines in this EXACT format, each separated by a line break:

Study these reference examples for tone and style:
- "Made for Moments That Can't Repeat"
- "Effortless Glamour for Every Occasion — The Wedding Edit by Dolly J"
- "Introducing Kami, the dresses you'll fall in love with 🌸"
- "Freesia Dreams for Festive Evenings 💖"
- "Celebrate Bonds: Up to 10% Off Our Rakhi Collection"

Your lines should:
• Mix poetic headlines with product introductions
• Include the brand/collection name naturally: "{data['product']}"
• Use emotional storytelling like "Celebrate Bonds" or "Made for Moments"
• IMPORTANT: If discount is {data['discount']}% and greater than 0, include it naturally in 2-3 subject lines
• Reference occasion: {data['festival']}
• Add urgency when relevant: {data['timing']}
• Use 1-2 emojis ONLY when they enhance the premium feel
• Sound like something a human brand expert would write, not AI
• Keep each line under {data['char_limit']} characters

Avoid these words completely: {', '.join(BANNED_WORDS)}

Create lines that:
1. Start with aspirational emotion or moment
2. Introduce collection/product name
3. Highlight craft or benefit
4. Connect to occasion or urgency
5. Mix short punchy lines with longer storytelling ones

Each line should feel premium, human, and designed to make someone want to open the email.

Write ONLY the subject lines, one per line, and make sure they build emotional flow across multiple ideas. Vary the structure, but keep the human storytelling natural and non-repetitive.
"""

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

    # 3. LONG CONTENT - Enhanced for storytelling
    if data['category'] == "Long Content":
        return f"""Write premium fashion ad copy that tells a story like an expert brand copywriter. Each line should flow naturally into the next, creating an emotional journey.

Create exactly 5 lines that flow like this:

Line 1: An aspirational headline that captures a moment or feeling
Line 2: Introduce the product/collection with its key benefit
Line 3: Highlight the craft, material, or special quality that makes it premium
Line 4: Connect to the occasion or create gentle urgency with the offer
Line 5: Warm, inviting call-to-action

Use these elements naturally:
• Brand/Product: {data['product']}
• Core promise: {data['usp']}
• Premium materials: {data['fabric']}
• Special qualities: {data['attributes']}
• Occasion: {data['festival']}
• Offer: {data['discount']}% off (if {data['discount']} > 0) (if {data['discount']} > 0) (if {data['discount']} > 0)
• Timing: {data['timing']}
• Emotional hook: {data['emotion']}

Write like these examples (for style reference only):
Summer Sale
Made for Sunny Days  
Slip into light layers, soft textures, and silhouettes that keep things cool
Your season of easygoing style begins with our summer-ready picks
Shop Now

OR:

Raksha Bandhan Ready
The Premium Collection
Crafted in premium materials for comfort that lasts through every celebration
Perfect for gifting the ones who matter most
Shop the festive edit now

Each line should:
- Sound completely natural and human
- Build emotional connection
- Feel premium but warm
- Flow seamlessly to the next line
- IMPORTANT: If discount is {data['discount']}% (greater than 0), include it naturally in line 4
- End with a clear but friendly action

Never use: {', '.join(BANNED_WORDS)}
Keep under {data['char_limit']} characters total.

Write ONLY the 5 lines, no bullets or formatting:"""

    # 4. CONCISE CONTENT - Enhanced
    if data['category'] == "Concise Content":
        return f"""Write a short, impactful fashion ad that sounds like expert human copywriting. Create 2-3 lines that pack maximum emotional punch in minimum words.

Structure:
Line 1: Emotional hook or occasion-based opener
Line 2: Product benefit with premium positioning  
Line 3: Gentle urgency with warm call-to-action

Use naturally:
• Product: {data['product']}
• Key benefit: {data['usp']}
• Materials: {data['fabric']}
• Occasion: {data['festival']}
• Offer: {data['discount']}% off
• Timing: {data['timing']}
• Emotion: {data['emotion']}

Examples of the human style to match:
Rakhi ready? Gift your brother our softest, freshest cotton-silk shirts.
They're wrinkle-free, breezy, and made for festive comfort.
Limited time only—shop the Raksha Bandhan edit now!

OR:

Weekend mood: effortless style
Introducing premium comfort - sophistication in every stitch
Don't wait, these won't last long

Write copy that:
- Sounds conversational and warm
- Builds desire quickly
- Feels premium but accessible
- IMPORTANT: If discount is {data['discount']}% (greater than 0), include it naturally
- Creates gentle urgency
- Ends with clear next step

Never use: {', '.join(BANNED_WORDS)}
Keep under {data['char_limit']} characters.

Write ONLY the 2-3 lines, no formatting:"""

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

Example style (don't copy):
Hey, Raksha Bandhan's here! 🎁
Just saw the new collection and had to share - they're absolutely beautiful
The materials feel amazing and they're perfect for gifting (or keeping for yourself!)
Love, Team [Brand Name]

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