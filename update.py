import os
import re
from datetime import datetime
from zoneinfo import ZoneInfo
from google import genai
from google.genai import types

# JST現在日時の取得
jst_now = datetime.now(ZoneInfo("Asia/Tokyo")).strftime("%Y年%m月%d日 %H:%M")

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

prompt = f"""
あなたは企業向けの先端AIリサーチエンジニアです。
主要な生成AIプラットフォーム（ChatGPT / OpenAI、Gemini / Google、Claude / Anthropic、その他オープンソースモデル等）の直近の公式アップデート・重要リリース情報をWeb検索で調査してください。

調査結果をもとに、ビジネスパーソンが業務にどう活かせるかを分かりやすく整理した、完成した1枚のHTMLページ（CSS内蔵・レスポンシブデザイン）を出力してください。

【出力要件】
1. 完全なHTML（<!DOCTYPE html>〜</html>）として出力すること。
2. ヘッダーにタイトル「AI Trends & Business Use Cases」と「最終更新日時: {jst_now} JST」を表示。
3. サービスごとのセクション（ChatGPT、Gemini、Claudeなど）をカード形式またはタブ形式で配置。
4. 各項目には以下を含めること：
   - アップデート概要（簡潔な要約）
   - 具体的な業務活用例（営業・マーケティング、開発・エンジニアリング、総務・バックオフィスなどの対象部門とユースケース）
   - おすすめのアクション / 試す手順
5. デザインはモダンで洗練されたUI（Tailwind CSSのCDN読み込みまたはインラインCSS、見やすいフォント、適切な余白、タグ配色）にすること。
6. マークダウン（```html や ```）は含めず、純粋なHTML文字列のみを出力すること。
"""

response = client.models.generate_content(
    model="gemini-3.6-flash",
    contents=prompt,
    config=types.GenerateContentConfig(
        tools=[types.Tool(google_search=types.GoogleSearch())],
        temperature=0.2,
    ),
)

# 余分なマークダウン装飾が残った場合のクリーンアップ
html_content = re.sub(r"^```html\s*", "", response.text.strip(), flags=re.IGNORECASE)
html_content = re.sub(r"```$", "", html_content.strip()).strip()

# index.html として書き出し
with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"[{jst_now}] index.html updated successfully.")
