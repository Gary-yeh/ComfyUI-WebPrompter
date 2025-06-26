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
            "required": {
                # 為了讓 UI 返回值能更新這個控件，它必須存在於 INPUT_TYPES 中
                "prompt": ("STRING", {"multiline": True, "dynamicPrompts": False, "default": ""}),
            },
            "optional": {
                # 我們用一個隱藏的輸入來接收上游數據，避免衝突
                "text_input": ("STRING", {"forceInput": True, "widget": "hide"}),
            }
        }

    # 注意：RETURN_TYPES 現在只包含給下游節點的數據
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("final_prompt",)
    FUNCTION = "finalize"
    CATEGORY = "WebPrompter"

    def finalize(self, prompt, text_input=None):
        # 決定最終的文本內容，優先使用來自上游連線的數據
        # 如果沒有連線，則使用用戶在文本框中輸入的內容
        final_text = text_input if text_input is not None else prompt

        # ======================================================================
        # V V V 這是解決問題的關鍵所在 V V V
        # ======================================================================
        # 我們返回一個元組，其中第二個元素是一個特殊的 "ui" 字典。
        # 這個字典會告訴前端去更新名為 "prompt" 的控件（widget），
        # 將其內容設置為我們處理好的 final_text。
        return {
            "ui": {
                "prompt": [final_text] # 將 'prompt' 文本框的內容更新為 final_text
            },
            "result": (final_text,) # 'result' 鍵包含了要傳遞給下游節點的數據
        }
