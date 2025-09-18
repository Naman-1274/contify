BANNED_WORDS = [
    "discover", "explore", "embrace", "immerse",
    "timeless", "elegance", "luxury", "opulence", "wrap", "celebrate", "effortless"
]

def build_prompt(data: dict) -> str:
    """Ultra-aggressive structure enforcement prompts."""
    
    product = data.get('product', '').strip()
    brand = data.get('brand', '').strip()
    fabric = data.get('fabric', '').strip()
    festival = data.get('festival', '').strip()
    discount = data.get('discount', 0)
    char_limit = data.get('char_limit', 300)
    banned = ', '.join(BANNED_WORDS)

    if data['category'] == "Email Subject Lines":
        return f"""you are a expert Marketing email writer and is very creative and catchy for
        {product} and {brand} with fabric {fabric} for {festival} festival with {discount}% discount if discount > 0
        and utilize the unique selling point {data.get('usp','')} if exists and blend everything seamlessly.Avoid banned words : {banned}
        and use human symbols like , and . instead of ! or - .

ENFORCE: Output MUST have EXACTLY these lines with blank lines in between, if format is not followed, regenerate internally until correct.
[Single line headline - complete sentence]
[blank line]
[Single line description - complete sentence about {festival} or {discount}% or {product}, {brand}, {fabric}] use storytelling if possible
[blank line]
[2-3 word CTA]

STRICT RULES:
- EXACTLY 3 lines separated by blank lines
- NO labels like "Headline:" or "Subject:"  
- NO bullet points, NO numbering, NO quotes
- Each line must be complete and make sense alone
- equal to {char_limit} characters
- Avoid: {banned}

Use: {product}, {brand}, {fabric}, {festival}, {discount}% discount

Example format:
Weekend Style Refresh

New silk pieces perfect for Diwali celebrations

Shop Now

Generate complete set as asked above Asked ads copy with character limit = {char_limit}:"""

    elif data['category'] == "WhatsApp Broadcast":
        return f"""you are a expert marketing senior human and is very creative and catchy for
        {product} and {brand} with fabric {fabric} for {festival} festival with {discount}% discount if discount > 0
        and utilize the unique selling point {data.get('usp','')} if exists and blend everything seamlessly.Avoid banned words : {banned}
        and use human symbols like , and . instead of ! or - .

ENFORCE: Output MUST have EXACTLY these lines with blank lines in between, if format is not followed, regenerate internally until correct.
[Single line headline]
[blank line]
[First description line - storytelling] use the blend of {festival}, {product}, {brand}, {fabric} if possible
[Second description line - continues story] continue from first line
[Optional third description line] end with a soft nudge to check it out
[blank line]
[2-3 word CTA]

Example:
Found your Raksha Bandhan look

Spotted this gorgeous silk kurta that flows beautifully
Perfect for those long family celebration nights

Check it out

Generate complete set as asked above Asked ads copy with character limit = {char_limit}:"""

    elif data['category'] == "Concise Content":
        return f"""you are a expert marketing senior human and is very creative and catchy for
        {product} and {brand} with fabric {fabric} for {festival} festival with {discount}% discount if discount > 0
        and utilize the unique selling point {data.get('usp','')} if exists and blend everything seamlessly.Avoid banned words : {banned}
        and use human symbols like , and . instead of ! or - .

Must follow this EXACT format with NO deviations:
[Single headline line]
[blank line]
[Single description line - storytelling focused] blend {festival}, {product}, {brand}, {fabric} if possible
[blank line]
[2-4 word CTA]

Example:
Weekend wardrobe sorted

New linen pieces perfect for breezy festivities

Shop Now

Generate complete set as asked above Asked ads copy with character limit = {char_limit}::"""

    elif data['category'] == "Long Content":
        return f"""you are a expert marketing senior human and is very creative and catchy for
        {product} and {brand} with fabric {fabric} for {festival} festival with {discount}% discount if discount > 0
        and utilize the unique selling point {data.get('usp','')} if exists and blend everything seamlessly.Avoid banned words : {banned}
        and use human symbols like , and . instead of ! or - .

ENFORCE: Output MUST have EXACTLY these lines with blank lines in between, if format is not followed, regenerate internally until correct.
[Single headline]
[blank line]
[First description line - sets scene] use {festival} if possible and {discount}%
[Second description line - explains benefit] use {product}, {brand}, {fabric} if possible
[blank line]
[3-5 word CTA]

Example:
Festive Season Perfection

Our silk collection captures every special moment beautifully
Designed for celebrations that deserve nothing but the finest

Shop Collection

Generate complete set as asked above Asked ads copy with character limit = {char_limit}:"""

    elif data['category'] == "PMAX":
        return f"""Generate a Google Ads PMAX copy like you are a expert marketing senior human and is very creative and catchy for 
            {product} and {brand} with fabric {fabric} for {festival} festival with {discount}% discount if discount > 0 
            and utilize the unique selling point {data.get('usp','')} if exists and blend everything seamlessly.Avoid banned words : {banned} and use human symbols like , and . instead of ! or - .

ENFORCE: Output MUST have EXACTLY these lines with blank lines in between, if format is not followed, regenerate internally until correct.
Headlines:
[15 short headlines under 30 chars each]
[Blank line]
Descriptions:  
[5 descriptions under 90 chars each]
[Blank line]
Long Headlines:
[5 long headlines under 120 chars each]


Generate complete set as asked above Asked ads copy with character limit = {char_limit}:"""