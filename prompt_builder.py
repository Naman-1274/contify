BANNED_WORDS = [
    "discover", "explore", "embrace", "immerse",
    "timeless", "elegance", "luxury", "opulence", "wrap", "celebrate"
]

def build_prompt(data: dict) -> str:
    """Strictly enforce format per real category; guide Gemini with explicit templates."""

    # 1. PMAX (Separate category)
    if data['category'] == "PMAX":
        return f"""Write Google Ads (PMAX) creative in this format:

Headlines
[5 short, punchy headlines (max 40 characters each); each on its own line, using product, fabric, benefit, festive/occasion, or gift context.]

Description
[5 lines (max 90 chars each): poetic and sensory, mentioning comfort, fit, feel, utility, emotion, and festival.]

Long Headlines
[2 sentences, each under 120 characters, focused on story or collection/occasion.]

Use this structure:
Headlines
Headline 1
Headline 2
Headline 3
Headline 4
Headline 5

Description
Description 1
Description 2
Description 3
Description 4
Description 5

Long Headlines
Long Headline 1
Long Headline 2

Do not add any sentences before or after these blocks. Use festive and craft cues, and avoid these words: {', '.join(BANNED_WORDS)}.
Brand/Product: {data['product']}
USP: {data['usp']}
Fabric: {data['fabric']}
Festival: {data['festival']}
Attributes: {data['attributes']}
"""

    if data['category'] == "Long Content":
        return f"""Write a premium ad, each line natural and human's daily spoken words only, flowing like a conversation.

    Line 1: Bold headline (occasion, product, or sale) — must stand alone, no brackets or formatting.
    Line 2: Benefit or feature, use USP/fabric/attribute, written as a natural sentence that connects to the headline.
    Line 3: Emotional or gifting/festival connection, written as a continuation (not a list) of the story.
    Line 4: Urgency or exclusivity—offer or timing, as a continuation.
    Line 5: Clear call to action: Shop Now!, Shop Soon!, etc.
    Each line should flow naturally to the next, as if written by a human brand copywriter.

    Inputs to use:
    Product: {data['product']}
    USP: {data['usp']}
    Fabric: {data['fabric']}
    Attributes: {data['attributes']}
    Festival: {data['festival']}
    Timing/Urgency: {data['timing']}

    Do NOT use: {', '.join(BANNED_WORDS)}.

    EXAMPLE:
    Summer Sale
    Made for Sunny Days
    Slip into light layers, soft textures, and silhouettes that keep things cool.
    Your season of easygoing style begins with our summer-ready picks.
    Shop Now

    Return ONLY the five lines, each on its own line, with no brackets, no bullets, no lists, and no extra formatting.
    """


    # 3. Concise Content (short summary version)
    if data['category'] == "Concise Content":
        return f"""Write a concise festive ad (80–140 characters, 2–3 lines) that is a compressed version of a long-form festive ad and Use this structure:
[Festival or Sale Name]
[Discount/Offer, e.g. Flat 25% Off]
[Core product benefit, mention fabric or comfort]
[Emotional/gift line if festival present]
[CTA/urgency if possible]

Base it on:
Product: {data['product']}
USP: {data['usp']}
Fabric: {data['fabric']}
Attributes: {data['attributes']}
Festival: {data['festival']}
Timing/Urgency: {data['timing']}
Make it short, natural, and punchy. Do not use these words: {', '.join(BANNED_WORDS)}.
"""

    # 4. WhatsApp Broadcast
    if data['category'] == "WhatsApp Broadcast":
        return f"""Write a WhatsApp broadcast ad in this format and structure:
[Short event/product hook—emojis allowed]
[Lifestyle/benefit or shopping context—use fabric/festival/USP]
[Optional: gifting or special message]
[Sign-off: e.g., Love, Team {data['product']}]

Use 1–2 emojis if natural.
Product: {data['product']}
USP: {data['usp']}
Fabric: {data['fabric']}
Festival: {data['festival']}
Timing/Urgency: {data['timing']}
Keep it human, brief, and as per real WhatsApp marketing. Avoid: {', '.join(BANNED_WORDS)}.
"""

    # 5. Email Subject/Emailer (as previous)
    if data['category'] == "Email Subject":
        return f"""Compose an email campaign creative and use this structure:
[Poetic/aspirational headline]
[Brand/collection/product—1 line]
[Benefit/heritage/craft—1 line]
[Meaningful gift/story context using festival/attributes]
[Single strong CTA: Shop Now, Launching Soon, etc.]

Headline: {data['usp']}
Brand/Collection: {data['product']}
Benefits: {data['attributes']}
Fabric: {data['fabric']}
Festival/Event: {data['festival']}
Do not exceed 200–250 characters. Stick to the structure, lines, and human tone. Banned: {', '.join(BANNED_WORDS)}.
"""

    # Fallback: Like long content
    return f"""Write a festive ad in poetic, multi-line format (200–300 characters), honoring line breaks and structure. {data['product']} | {data['usp']} | {data['fabric']} | {data['festival']}. Avoid: {', '.join(BANNED_WORDS)}.
"""
