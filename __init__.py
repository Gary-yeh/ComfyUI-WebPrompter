# __init__.py
from .web_prompter_nodes import ContentFetcher, LLMNewsScriptGenerator

NODE_CLASS_MAPPINGS = {
    "ContentFetcher (WebPrompter)": ContentFetcher,
    "LLMNewsScriptGenerator (WebPrompter)": LLMNewsScriptGenerator,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ContentFetcher (WebPrompter)": "1. Content Fetcher",
    "LLMNewsScriptGenerator (WebPrompter)": "2. News Script Generator",
}

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']

print("### Loading: WebPrompter Custom Nodes ###") # 加上這行可以在啟動 ComfyUI 時的終端看到加載訊息，方便調試
