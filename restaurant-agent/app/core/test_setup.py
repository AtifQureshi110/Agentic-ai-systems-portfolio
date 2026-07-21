from app.core.config import settings
from app.core.llm import llm

print("Config loaded:", settings.app_name)
print("DB URL:", settings.database_url)

response = llm.invoke("Say hello in five words")
print("Gemini response:", response.content)