# ComfyUI-WebPrompter

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

一個為 ComfyUI 設計的自訂節點套件，旨在自動化「從網頁內容到高品質 AI 提示詞」的完整流程。厭倦了手動複製新聞、總結內容、再轉換為提示詞嗎？WebPrompter 將這一切變為全自動。

This is a custom node suite for ComfyUI that automates the entire workflow from web content to a high-quality AI prompt. Tired of manually copying news, summarizing content, and then converting it into a prompt? WebPrompter automates it all.

---

### ✨ 功能亮點 (Features)

*   **網址直達提示詞**: 直接輸入一個新聞網址，節點會自動抓取主要內容。
*   **LLM 智能轉化**: 利用強大的大語言模型（如 GPT-4o, GPT-4-Turbo）將原始文本轉化為符合事實、適合播報的新聞字幕稿。
*   **完全可控**: LLM 的指導語 (System Prompt) 完全開放，您可以自訂任何轉換風格。
*   **最終審核**: 在將提示詞送入 `CLIP Text Encode` 之前，提供一個可視化的編輯器，讓您擁有人工的最終決定權。
*   **支援手動輸入**: 除了網址，您也可以直接貼上自己的文本作為輸入源。

### 🎨 節點工作流預覽 (Node Workflow)

這是一張展示 WebPrompter 核心節點如何協同工作的範例圖。

<!-- 
重要提示：請截一張您在 ComfyUI 中使用這套節點的圖片，
命名為 workflow_example.png，並將它放在專案的 `assets` 資料夾下。
-->
![WebPrompter Workflow](assets/workflow_example.png)


### 📦 安裝 (Installation)

#### 方法 1: 使用 ComfyUI Manager (推薦)

1.  安裝 [ComfyUI Manager](https://github.com/ltdrdata/ComfyUI-Manager)。
2.  點擊 `Manager` 按鈕 -> `Install Custom Nodes`。
3.  搜尋 `WebPrompter` 並點擊 `Install`。
4.  重啟 ComfyUI。

<!--
開發者提示：在您的專案被 ComfyUI Manager 收錄前，可以先保留這段說明。
這是使用者最喜歡的安裝方式。
-->

#### 方法 2: 手動安裝 (Git Clone)

1.  打開終端 (Terminal)，進入 `ComfyUI/custom_nodes/` 資料夾。
2.  執行以下指令，複製本專案：
    ```bash
    git clone https://github.com/Gary-yeh/ComfyUI-WebPrompter.git
    ```
    <!-- 請確認上面的 GitHub 用戶名 `Gary-yeh` 是否正確 -->

3.  安裝所需的依賴套件：
    ```bash
    cd ComfyUI-WebPrompter
    pip install -r requirements.txt
    ```

4.  重啟 ComfyUI。

### 🚀 使用指南 (Usage)

#### ⚠️ 第一步：設置 API 金鑰

本節點套件中的 `LLM News Script Generator` 節點需要使用 OpenAI 的 API。請務必在使用前設置您的 API 金鑰。

**這是一個秘密金鑰，請勿洩漏或上傳到任何地方！**

您需要將金鑰設置為名為 `OPENAI_API_KEY` 的**環境變數**。

*   **Windows**:
    在命令提示字元 (CMD) 中執行:
    ```cmd
    setx OPENAI_API_KEY "你的sk-開頭的API金鑰"
    ```
    (注意: `setx` 設置後需要重開一個新的終端才會生效)

*   **macOS / Linux**:
    在你的 `.bashrc`, `.zshrc`, 或其他 shell 設定檔中加入這一行：
    ```bash
    export OPENAI_API_KEY="你的sk-開頭的API金鑰"
    ```
    然後執行 `source ~/.zshrc` 或重開終端。

#### 基本工作流程

1.  **新增 `1. Content Fetcher` 節點**:
    *   `mode` 設為 `URL`，然後在 `url` 欄位中貼上您想分析的新聞網址。
    *   或者，`mode` 設為 `Manual`，直接在 `manual_text` 中輸入您的內容。

2.  **新增 `2. News Script Generator` 節點**:
    *   將 `Content Fetcher` 的 `original_text` 輸出接口，連接到本節點的 `original_text` 輸入接口。
    *   檢查 `system_prompt` 是否符合您的需求，可以自由修改它來改變 AI 的行為。
    *   選擇一個合適的 `model`，例如 `gpt-4o`。

3.  **新增 `3. Prompt Finalizer/Editor` 節點**:
    *   將 `News Script Generator` 的 `news_script` 輸出接口，連接到本節點的 `prompt` 輸入接口。
    *   此時，節點的文字框會自動填入由 LLM 生成的新聞稿。您可以在這裡進行**最後的手動修改**。

4.  **連接到下游節點**:
    *   將 `Prompt Finalizer/Editor` 的 `final_prompt` 輸出接口，連接到 `CLIP Text Encode` 節點的 `text` 輸入接口中。

5.  **執行！** 點擊 `Queue Prompt`，享受自動化的成果。

### 🤝 貢獻 (Contributing)

歡迎任何形式的貢獻！如果您發現了 Bug 或有任何功能建議，請隨時在 [GitHub Issues](https://github.com/Gary-yeh/ComfyUI-WebPrompter/issues) 中提出。

<!-- 同樣，請確認上面的 GitHub 用戶名 -->

### 📄 授權 (License)

本專案採用 [MIT License](LICENSE) 授權。

### 🙏 致謝 (Acknowledgements)

*   感謝 [ComfyUI](https://github.com/comfyanonymous/ComfyUI) 的作者 comfyanonymous 創造了這個強大且靈活的平台。
*   本專案使用了 [trafilatura](https://github.com/adbar/trafilatura) 來提取網頁內容。
