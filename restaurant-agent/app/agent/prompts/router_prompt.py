"""
Router prompt - single LLM call that classifies intent AND pulls out any
slot values mentioned in the same message. Uses trimmed history +
already-known slots (context engineering) so the model isn't re-fed
stale info or re-asking for what it already has.
"""

CLASSIFY_AND_EXTRACT_PROMPT = """You are the intent classifier for a restaurant assistant.

Given the user's message, return ONLY a JSON object (no markdown, no explanation) with this exact shape:

{{
  "intent": "faq" | "menu" | "availability_check" | "reservation_create" | "unknown",
  "slots": {{
    "customer_name": string or null,
    "phone": string or null,
    "reservation_date": string or null,   // ISO format YYYY-MM-DD, or null if not mentioned
    "reservation_time": string or null,   // 24hr HH:MM, or null if not mentioned
    "party_size": integer or null
  }}
}}

Rules:
- "faq": questions about hours, location, policies, refunds, contact info.
- "menu": questions about food items, prices, categories.
- "availability_check": asking if a table is free, without confirming a booking.
- "reservation_create": explicitly wants to book/reserve a table.
- "unknown": greetings, small talk, or anything unrelated.
- Only fill a slot if the user's message OR the "Already known" section below states it.
- Do not guess or invent values.
- If a slot is in "Already known", carry it forward as-is unless the user's latest message clearly changes it.
- If today's date is needed to resolve "tomorrow"/"tonight", use: {current_date}

Already known slots:
{known_slots}

Still needed:
{missing_slots}

Recent conversation (last few turns only):
{recent_history}

User's latest message:
{user_message}

Return ONLY the JSON object.
"""