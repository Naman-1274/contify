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
    [5 short, punchy headlines (max 40 characters each); each on its own line, using product, fabric, discount, benefit, festive/occasion, or gift context.]

    Description
    [5 lines (max 90 chars each): poetic and sensory, mentioning comfort, fit, feel, utility, emotion, discount and festival.]

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
    discount: {data['discount']}
    Attributes: {data['attributes']}
    Please ensure the total copy does not exceed {data['char_limit']} characters.
    """

    if data['category'] == "Long Content":
        return f"""Write a premium ad, each line natural and human's daily spoken words only, flowing like a conversation.

    Line 1: Bold headline (occasion, product, or sale) — must stand alone, no brackets or formatting.
    Line 2: Benefit or feature, use USP, fabric, attribute, or discount, written as a natural sentence that connects to the headline.
    Line 3: Emotional or gifting/festival connection, written as a continuation (not a list) of the story.
    Line 4: Urgency or exclusivity—offer or timing, discount, as a continuation.
    Line 5: Clear call to action: Shop Now!, Shop Soon!, etc.
    Each line should flow naturally to the next, as if written by a human brand copywriter.

    Inputs to use:
    Product: {data['product']}
    USP: {data['usp']}
    Fabric: {data['fabric']}
    Attributes: {data['attributes']}
    discount: {data['discount']}
    Festival: {data['festival']}
    Timing/Urgency: {data['timing']}

    Do NOT use: {', '.join(BANNED_WORDS)}.

    just for reference generate new messages each time:
    Summer Sale
    Made for Sunny Days
    Slip into light layers, soft textures, and silhouettes that keep things cool.
    Your season of easygoing style begins with our summer-ready picks.
    Shop Now

    Return ONLY the five lines, each on its own line, with no brackets, no bullets, no lists, and no extra formatting.
    Please keep the total ad copy under {data['char_limit']} characters.
    """


    # 3. Concise Content (short summary version)
    if data['category'] == "Concise Content":
        return f"""Write a concise festive ad, 2–3 **natural flowing lines** (total under {data['char_limit']} characters), like something a real person would say to a friend, not a robot. The ad should feel like a compressed, meaningful story that could actually persuade.

    Structure:
    Line 1: An inviting headline or occasion (festival/sale/product) — must stand alone, stated conversationally.
    Line 2: The core product benefit—use USP, fabric, comfort or stand-out attribute, discount. Tie this to the context set above, not just a generic product line.
    Line 3: If a festival or gifting theme is present, weave it in emotionally and naturally—otherwise, use gentle urgency (timing/offer - discount/season). End with a friendly invitation to act (e.g., Shop Now, Treat them, Don’t miss out).

    Base your lines on:
    Product: {data['product']}
    USP: {data['usp']}
    Fabric: {data['fabric']}
    Attributes: {data['attributes']}
    discount: {data['discount']}
    Festival: {data['festival']}
    Timing/Urgency: {data['timing']}

    **Write as if for a premium brand, but keep the flow and word choices as humans actually speak. Never use: {', '.join(BANNED_WORDS)}.**

    just for reference generate new messages each time, (compressed but natural, not a list):
    Rakhi ready? Gift your brother our softest, freshest cotton-silk shirts.
    They’re wrinkle-free, breezy, and made for festive comfort.
    Limited time only—shop the Raksha Bandhan edit now!

    or :
    Summer Sale just got sunnier!
    Light cotton shirts for easy days and better getaways—your next favorite’s waiting.
    Hurry, special prices won’t last long.

    **Return ONLY the 2–3 ad lines, each on its own line, no bullets or lists. They must read as naturally and smoothly as the examples.**
    """

    # 4. WhatsApp Broadcast
    if data['category'] == "WhatsApp Broadcast":
        return f"""Write a WhatsApp marketing message just like a friendly personal recommendation.
    • Use 3–4 natural, connected lines—each easily sent as a broadcast, not a list.
    • Open with a conversational hook about the event or product (emojis allowed, but only where they sound real).
    • Follow with a benefit or shopping context using the product, fabric, USP, discount, festival, or timing fields—but always connected with simple, human phrasing.
    • Naturally add a gifting message or special occasion note if applicable—don’t force it as a bullet point.
    • Sign off warmly with something like: Love, Team {data['product']} (on its own line).

    Use 1–2 emojis if it feels natural—never more and only if they fit the tone.
    Product: {data['product']}
    USP: {data['usp']}
    Fabric: {data['fabric']}
    Festival: {data['festival']}
    discount: {data['discount']}
    Timing/Urgency: {data['timing']}

    just for reference generate new messages each time:
    Hey, Raksha Bandhan’s here! 🎁
    Check out our new wrinkle-free cotton shirts—super comfy, perfect for gifting your brother (or just treating yourself).
    Don’t wait—shop the freshest arrivals now.
    Love, Team [Brand]

    Or:
    Sunny days, softer shirts!
    Cotton & silk blends just landed—easy, breezy, and ready for all your weekend plans ☀️
    Make Rakhi gifting easy this year.
    Cheers, Team {data['product']}

    Write each line naturally, as if you’d send it on WhatsApp, not as slogans, not as a list.
    Never use: {', '.join(BANNED_WORDS)}.
    OUTPUT: Just the message lines—no extra formatting or summaries.
    Please make sure the total message is not longer than {data['char_limit']} characters.
    """


    # 5. Email Subject/Emailer (as previous)
    if data['category'] == "Email Subject":
        return f"""Compose a marketing email for a premium fashion brand, each line flowing like a personal and using daily spoken language, aspirational message. DO NOT use brackets, bullets, or list formatting—each line must sound human and effortlessly connected, not like a generic summary.

    Line 1: An evocative or poetic headline—set the mood or promise (occasion, feeling, or aspiration).
    Line 2: The brand, collection, or product name—one clean line, discount, no extra description.
    Line 3: Benefit, craft, or heritage line—show the special quality or value of the product, discount, using fabric, benefits, or craftsmanship.
    Line 4: Gifting, story, or festival context—a line that anchors this offer in a real moment (e.g., "a thoughtful gift for festival," or "woven for cherished memories").
    Line 5: Short, clear CTA ("Shop Now", "Launching Soon", etc.).

    Draw only from these fields:
    Headline/Theme: {data['usp']}
    Brand/Collection: {data['product']}
    Benefit/Craft: {data['attributes']}
    Fabric: {data['fabric']}
    discount: {data['discount']}
    Festival/Event: {data['festival']}
    Do not exceed {data['char_limit']} characters in total. Each line must build on the last—no abrupt topic jumps or fragments. All phrases must sound like natural, brand-quality daily English. DO NOT use these words anywhere: {', '.join(BANNED_WORDS)}.

    just for reference generate new messages each time (for flow and tone):
    Couture Meets Culture
    Gazal Gupta Brides
    Graceful Silhouettes blending contemporary aesthetics with classic heritage
    Rooted in craft, layered with meaning—each look is a canvas of memories in the making
    Shop Now

    Return ONLY the email lines, in order, with no extra formatting or summaries.
    """
    
    # Fallback: Like long content
    return f"""Write a festive ad in poetic, multi-line format (200–300 characters), honoring line breaks and structure. {data['product']} | {data['usp']} | {data['fabric']} | {data['festival']}. Avoid: {', '.join(BANNED_WORDS)}.
"""
