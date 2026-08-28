import os
import re
from datetime import datetime
from zoneinfo import ZoneInfo
from google import genai
from google.genai import types

jst_now = datetime.now(ZoneInfo("Asia/Tokyo")).strftime("%Y年%m月%d日 %H:%M")

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

prompt = f"""
あなたは企業向けの先端AIリサーチエンジニアです。
主要な生成AIプラットフォーム（ChatGPT / OpenAI、Gemini / Google、Claude / Anthropicなど）の最新アップデート動向と、それらを企業業務（営業、開発、バックオフィスなど）へどう活かせるかの具体例を網羅的にまとめてください。

出力はブラウザでそのまま閲覧できる完成したモダンなHTML形式（CSS込み、UTF-8）のみを出力してください。

【出力要件】
1. 完全なHTML（<!DOCTYPE html>〜</html>）として出力すること。
2. タイトル「AI Trends & Business Use Cases」と「最終更新日時: {jst_now} JST」を見やすく配置。
3. Tailwind CSS（CDN）を利用し、見やすいカード型UIとカラータグでデザインすること。
4. サービス別（ChatGPT, Gemini, Claude 等）に「新機能・アップデート要約」「業務活用ユースケース」「推奨アクション」を掲載すること。
5. マークダウン記号（```html など）は一切含めず、純粋なHTMLコードのみを出力すること。
"""

try:
    # まずは検索機能付きで実行
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            tools=[types.Tool(google_search=types.GoogleSearch())],
            temperature=0.3,
        ),
    )
except Exception as e:
    print(f"Search tool failed, retrying standard generation: {e}")
    # クォータエラー等が発生した場合はツールなしで生成
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0.3,
        ),
    )

# HTMLクリーンアップ
html_content = re.sub(r"^```html\s*", "", response.text.strip(), flags=re.IGNORECASE)
html_content = re.sub(r"```$", "", html_content.strip()).strip()

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"[{jst_now}] index.html generated successfully.")
