import requests
from playwright.sync_api import Page, Locator

MODEL_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "gemma4:e2b"

class SmartHealer:
    def __init__(self, page: Page, model=MODEL_NAME):
        self.page = page
        self.model = model
        self.ai_url = MODEL_URL

    def get_locator(self, css_selector: str, description: str) -> Locator:
        """Attempts to find an element; heals via Ollama if it fails."""
        try:
            # Short timeout for the initial check to trigger healing quickly
            element = self.page.locator(css_selector)
            element.wait_for(state="attached", timeout=2000)
            return element
        except Exception:
            print(f"[HealerAI] CSS Locator '{css_selector}' failed. AI searching for: '{description}'")
            return self._heal(description)

    def _heal(self, description: str) -> Locator:
        # Extracting a smarter, smaller snapshot of the interactive DOM
        html_snapshot = self.page.evaluate("""
            () => {
                const elements = document.querySelectorAll('button, input, a, select, [role="button"]');
                return Array.from(elements).map(el => {
                    return `<${el.tagName.toLowerCase()} id="${el.id}" name="${el.name}" placeholder="${el.placeholder}" class="${el.className}" aria-label="${el.getAttribute('aria-label')}">${el.innerText}</${el.tagName.toLowerCase()}>`;
                }).join('\\n').substring(0, 5000);
            }
        """)
        
        prompt = f"""
        The user is looking for: "{description}"
        Here is the current simplified HTML:
        {html_snapshot}

        Task: Provide the most accurate CSS selector to find this element.
        Return ONLY the raw CSS selector string. No explanation, no markdown.
        """

        try:
            response = requests.post(self.ai_url, json={
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "think": False,
                "options": {"temperature": 0}
            }, timeout=30)
            
            new_selector = response.json()['response'].strip().replace("`", "").replace("css", "")
            print(f"[HealerAI] Suggested new selector: {new_selector}")
            return self.page.locator(new_selector).first
        except Exception as e:
            print(f"[HealerAI] Healing failed: {e}")
            raise