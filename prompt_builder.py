BANNED_WORDS = [
    "discover", "explore", "embrace", "immerse",
    "timeless", "elegance", "luxury", "opulence", "wrap", "celebrate", "effortless"
]

def build_prompt(data: dict) -> str:
    """Enhanced prompts for genuine human-like conversation with strict structure and limits."""

    # Helpful local variables
    product = data.get('product', '').strip()
    brand = data.get('brand', '').strip()
    fabric = data.get('fabric', '').strip()
    festival = data.get('festival', '').strip()
    discount = data.get('discount', 0)
    char_limit = data.get('char_limit', 300)

    # Helper text for banned words
    banned = ', '.join(BANNED_WORDS)

    # Strict instruction prefix used across categories
    strict_prefix = (
        "INSTRUCTIONS (READ CAREFULLY):\n"
        "- OUTPUT EXACTLY the three parts below and NOTHING ELSE.\n"
        "- EXACT FORMAT REQUIRED (no labels, no extra lines, no bullets, no quotes):\n"
        "  Headline\n\n"
        "  Description\n\n"
        "  CTA\n"
        "- Headline must be ONE LINE only. Description must be ONE LINE (or 2 lines where specified). CTA ONE LINE only.\n"
        "- Do NOT include ellipses ('...'), parentheses, or meta commentary.\n"
        f"- TOTAL character count for the entire output must be <= {char_limit} characters. If necessary, shorten the Description first then Headline.\n"
        f"- Avoid these overused words: {banned}.\n"
        "- Sound like a real, warm, fashion-savvy friend (natural, not robotic).\n\n"
    )

    # ---------- EMAIL SUBJECT LINES ----------
    if data['category'] == "Email Subject Lines":
        # examples provided in exact format to teach the model the pattern & variety
        examples = (
            "A New Chapter in Style\n\n"
            "Step into the Jashn new arrivals\n\n"
            "Explore Now\n\n"
            "---\n\n"
            "Red Carpet Ready\n\n"
            "From runway to reality — pieces to turn heads\n\n"
            "Shop Now\n\n"
            "---\n\n"
            "Printed Perfection\n\n"
            "Twirls in print — our newest lehenga edits\n\n"
            "See Collection\n\n"
            "---\n\n"
            "Festive Glow Starts Here\n\n"
            "Timed edits and textured fabrics for every celebration\n\n"
            "Explore Now\n\n"
            "---\n\n"
            "Last Chance: 40% Off Ends Tonight\n\n"
            "Final hours to grab your favourite festive pieces\n\n"
            "Shop Now"
        )

        return (
            strict_prefix +
            "CATEGORY: Email Subject Lines (ONE-LINE headline, ONE-LINE description, ONE-LINE CTA)\n\n"
            "Guidance:\n"
            "- Each variation should choose one primary focus: Festival/Occasion, Discount/Urgency, Brand/Collection.\n"
            "- Headline: 3-8 words, bold, complete and meaningful (editorial-style). Examples below follow the exact required output format.\n"
            "- Description: 10-25 words, single complete line, referencing product/fabric/festival/discount when relevant.\n"
            "- CTA: 2-4 words, natural. Examples: Shop Now, Explore Now, See Collection.\n\n"
            "EXACT EXAMPLES (follow the same format and tone):\n\n"
            f"{examples}\n\n"
            "Now write a single variation (one output) using the data below. Use the chosen focus to guide tone and content.\n\n"
            f"DATA: product={product} | brand={brand} | fabric={fabric} | festival={festival} | discount={discount}%\n\n"
            "OUTPUT:"
        )

    # ---------- PMAX (unchanged structure but keep strict prefix) ----------
    if data['category'] == "PMAX":
        headline_limit = data['char_limit']['headlines']
        description_limit = data['char_limit']['description']
        long_headline_limit = data['char_limit']['long_headlines']
        return (
            strict_prefix +
            f"You're creating Google Ads copy. Follow the exact format below and ensure each item stays within character limits.\n\n"
            f"Headlines (each MAX {headline_limit} chars)\n[Write 15 headlines, each under {headline_limit} chars]\n\n"
            f"Description (each MAX {description_limit} chars)\n[Write 5 descriptions, each under {description_limit} chars]\n\n"
            f"Long Headlines (each MAX {long_headline_limit} chars)\n[Write 5 long headlines, each under {long_headline_limit} chars]\n\n"
            f"Include naturally: {product} | {brand} | {fabric} | {festival} | {discount}% off (if >0)\n"
            f"Skip: {banned}\n\n"
            "OUTPUT: (write only the requested lists in the exact layout)"
        )

    # ---------- WHATSAPP BROADCAST ----------
    if data['category'] == "WhatsApp Broadcast":
        return (
            strict_prefix +
            "CATEGORY: WhatsApp Broadcast (Headline one line, Description 2-3 lines, CTA one line)\n\n"
            "Tone: Storytelling, warm, personal — like texting a close friend about a great find.\n"
            "- Headline: 4-10 words, one line.\n"
            "- Description: 20-50 words total, spread over 2-3 short lines; paint a moment; mention product/usp/fabric/festival naturally.\n"
            "- CTA: 2-5 words, friendly.\n\n"
            f"DATA: product={product} | brand={brand} | fabric={fabric} | festival={festival} | discount={discount}%\n\n"
            "EXAMPLES (exact format):\n\n"
            "Raksha Bandhan outfit sorted!\n\n"
            "Found the softest organza lehenga — lightweight, sparkly, made for long family nights.\n\n"
            "Check it out\n\n"
            "---\n\n"
            "Wedding guest looks, solved\n\n"
            "Picked up a dreamy embroidered saree that will feel custom-made — perfect for sangeet.\n\n"
            "See Collection\n\n\n"
            "OUTPUT:"
        )

    # ---------- CONCISE CONTENT ----------
    if data['category'] == "Concise Content":
        return (
            strict_prefix +
            "CATEGORY: Concise Content (Headline one line, Description one line, CTA one line)\n\n"
            "Tone: quick micro-story that lands in the feed — organic and human.\n"
            "- Headline: 3-8 words.\n"
            "- Description: 8-20 words, one complete line.\n"
            "- CTA: 2-4 words.\n\n"
            f"DATA: product={product} | fabric={fabric} | festival={festival} | discount={discount}%\n\n"
            "EXAMPLES (exact format):\n\n"
            "Weekend wardrobe sorted\n\n"
            "New linen kurtas for breezy daytime festivities\n\n"
            "Shop now\n\n\n"
            "OUTPUT:"
        )

    # ---------- LONG CONTENT ----------
    if data['category'] == "Long Content":
        return (
            strict_prefix +
            "CATEGORY: Long Content (Headline one line, Description two lines, CTA one line)\n\n"
            "Tone: premium storytelling from a fashion expert. Warm and descriptive, not salesy.\n"
            "- Headline: 4-10 words.\n"
            "- Description: 25-60 words total, over exactly 2 lines (Line1: scene; Line2: why it matters).\n"
            "- CTA: 2-5 words.\n\n"
            f"DATA: product={product} | usp={data.get('usp','')} | fabric={fabric} | festival={festival} | discount={discount}% | timing={data.get('timing','')}\n\n"
            "EXAMPLES (exact format):\n\n"
            "Printed Perfection\n\n"
            "Our printed lehengas are perfect for every festive moment — from mehndi to sangeet.\n"
            "Playful, polished and utterly you.\n\n"
            "Shop printed lehengas\n\n\n"
            "OUTPUT:"
        )

    # ---------- FALLBACK ----------
    return (
        strict_prefix +
        f"DATA: {data}\n\n"
        "Write a single 3-line output (Headline / Description / CTA) staying under the given char limit.\n\n"
        "OUTPUT:"
    )
