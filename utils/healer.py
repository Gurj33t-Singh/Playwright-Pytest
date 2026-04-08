import requests, pytest
from playwright.sync_api import Page, Locator

class SmartHealer:
    def __init__(self, page: Page, model= "qwen3.5:4b"):
        self.page = page
        self.model = model
        self.ollama_url = "http://localhost:11434/api/generate"

    def get_locator(self, selector: str, description: str) -> Locator:
        """Returns a Playwright Locator. Heals automatically if the initial selector fails."""
        try:
            # Check if the element is visible/present within 3 seconds
            element = self.page.locator(selector)
            element.wait_for(state="attached", timeout=3000)
            return element
        except Exception:
            print(f"⚠️ [Healer] '{selector}' failed. Consulting ollama for: '{description}'...")
            return self._heal(description)

    def _heal(self, description: str) -> Locator:
        # 1. Capture a compact DOM snapshot
        # We target interactive elements to keep the prompt small
        html_snapshot = self.page.evaluate("""
            () => {
                const elements = document.querySelectorAll('button, input, a, [role="button"], select');
                return Array.from(elements).map(el => el.outerHTML).join('\\n').substring(0, 8000);
            }
        """)
        
        # 2. Build the AI Prompt
        prompt = f"""
        Find the CSS selector for: "{description}"
        HTML: {html_snapshot}
        
        CRITICAL: Return ONLY the raw string. 
        Example: input[name="user"]
        DO NOT include the word "css", DO NOT use markdown, DO NOT explain.
        """

        try:
            response = requests.post(self.ollama_url, json={
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "think": False,
                "options": {"temperature": 0}
            }, timeout=30000)
            
            raw_response = response.json()['response'].strip()
            
            # SANITIZATION: Remove AI fluff that causes Playwright to crash
            # Removes "css", markdown backticks, and common labels
            clean_selector = (raw_response
                              .replace("css", "")
                              .replace("Selector:", "")
                              .replace("```css", "")
                              .replace("```", "")
                              .strip())
            
            print(f"✅ [Healer] Cleaned suggested locator: {clean_selector}")
            return self.page.locator(clean_selector).first
            
        except Exception as e:
            print(f"❌ [Healer] Critical Failure: {e}")
            raise
        

@pytest.fixture
def healer(page_chr):
    return SmartHealer(page_chr)