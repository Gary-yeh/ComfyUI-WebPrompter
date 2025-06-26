# web_prompter_nodes.py

import os
import requests
from bs4 import BeautifulSoup
import trafilatura
from openai import OpenAI

# =================================================================================
# 節點 1: Content Fetcher
# =================================================================================
class ContentFetcher:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": { "mode": (["URL", "Manual"],) },
            "optional": {
                "url": ("STRING", {"multiline": False, "default": "https://www.bbc.com/news/technology-68523302"}),
                "manual_text": ("STRING", {"multiline": True, "default": "A cat sitting on a mat."}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("original_text",)
    FUNCTION = "fetch_content"
    CATEGORY = "WebPrompter"

    def fetch_content(self, mode, url="", manual_text=""):
        if mode == "Manual":
            print("[ContentFetcher] Using manual text input.")
            return (manual_text,)
        if not url:
            raise ValueError("URL input is required when mode is set to URL.")
        print(f"[ContentFetcher] Fetching content from URL: {url}")
        try:
            downloaded = trafilatura.fetch_url(url)
            content_text = trafilatura.extract(downloaded, include_comments=False, include_tables=False)
            if not content_text:
                print("[ContentFetcher] Warning: trafilatura failed, falling back to raw text.")
                content_text = trafilatura.extract(downloaded, method="raw_text")
            print(f"[ContentFetcher] Extracted text length: {len(content_text)}")
            return (content_text,)
        except Exception as e:
            error_message = f"Failed to fetch or process URL {url}. Error: {e}"
            print(f"[ContentFetcher] {error_message}")
            return (error_message,)


# =================================================================================
# 節點 2: LLM News Script Generator
# =================================================================================
class LLMNewsScriptGenerator:
    def __init__(self):
        api_key = os.environ.get('OPENAI_API_KEY')
        self.client = OpenAI(api_key=api_key) if api_key else None

    @classmethod
    def INPUT_TYPES(cls):
        default_system_prompt = (
            "You are a professional news script editor... (此處省略之前設計的詳細 prompt)"
        )
        return {
            "required": {
                "original_text": ("STRING", {"forceInput": True}),
                "system_prompt": ("STRING", {"multiline": True, "default": default_system_prompt}),
                "model": (["gpt-4-turbo", "gpt-4o", "gpt-3.5-turbo"],),
                "max_tokens": ("INT", {"default": 500, "min": 50, "max": 4096}),
                "temperature": ("FLOAT", {"default": 0.2, "min": 0.0, "max": 1.0, "step": 0.1}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("news_script",)
    FUNCTION = "generate_script"
    CATEGORY = "WebPrompter"

    def generate_script(self, original_text, system_prompt, model, max_tokens, temperature):
        if not self.client:
            return ("ERROR: OpenAI API key is not configured. Please set the OPENAI_API_KEY environment variable.",)
        if not original_text or original_text.isspace():
            return ("Input text is empty. Please provide content to process.",)
        try:
            print(f"[LLMNewsScriptGenerator] Sending request to OpenAI with model {model}...")
            response = self.client.chat.completions.create(
                model=model,
                messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": original_text}],
                max_tokens=max_tokens,
                temperature=temperature,
            )
            news_script = response.choices[0].message.content.strip()
            print(f"[LLMNewsScriptGenerator] Generated news script successfully.")
            return (news_script,)
        except Exception as e:
            error_message = f"OpenAI API call failed: {e}"
            print(f"[LLMNewsScriptGenerator] {error_message}")
            return (error_message,)


# =================================================================================
# 節點 3: Prompt Finalizer
# =================================================================================
class PromptFinalizer:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {}, # 必須項留空
            "optional": {   # 所有輸入都設為可選，以獲得最大靈活性
                "text_input": ("STRING", {"forceInput": True, "widget": "hide"}),
                "text_widget": ("STRING", {"multiline": True, "default": "This is the default text in the widget."}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("final_prompt",)
    FUNCTION = "finalize"
    CATEGORY = "WebPrompter"

    def finalize(self, text_widget=None, text_input=None):
        # ======================================================================
        # V V V 這是我們必須在後端終端看到的「強力偵錯日誌」 V V V
        # ======================================================================
        print("\n\n" + "#"*60)
        print("### INSIDE PromptFinalizer: FINALIZE FUNCTION IS RUNNING! ###")
        print("#"*60)

        # 診斷來自上游連線的數據 (text_input)
        print(f"--- Diagnosing 'text_input' (from upstream link) ---")
        print(f"    Value: {text_input}")
        print(f"    Type: {type(text_input)}")
        print(f"    Is None? {text_input is None}")
        print(f"    Content (repr): {repr(text_input)}") # repr()能區分 ' ' 和 ''

        # 診斷來自界面文本框的數據 (text_widget)
        print(f"\n--- Diagnosing 'text_widget' (from UI textbox) ---")
        print(f"    Value: {text_widget}")
        print(f"    Type: {type(text_widget)}")
        print(f"    Is None? {text_widget is None}")
        print(f"    Content (repr): {repr(text_widget)}")

        # 決定輸出的邏輯
        # 即使 'text_input' 是空字串 ""，我們也優先使用它，只要它不是 None
        if text_input is not None:
            final_text = text_input
            print("\n>>> DECISION: Using 'text_input' from the upstream link.")
        else:
            final_text = text_widget
            print("\n>>> DECISION: No upstream link data. Using 'text_widget' from the UI.")

        print(f"\n--- FINAL OUTPUT ---")
        print(f"    Final text to be returned: {repr(final_text)}")
        print("#"*60 + "\n\n")

        return (final_text,)
