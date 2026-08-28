import os
import re
from datetime import datetime
from zoneinfo import ZoneInfo
from google import genai
from google.genai import types

jst_now = datetime.now(ZoneInfo("Asia/Tokyo")).strftime("%Y年%m月%d日 %H:%M")

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

prompt = f"""
あなたは企業向けAI導入・業務DXのコンサルタントです。
ChatGPT(OpenAI)、Gemini(Google)、Claude(Anthropic)の主要3大AIを中心に、直近の重要アップデート・新機能を調査してください。
非エンジニアのビジネスパーソンが見ても「自社の業務でどう使えるか」が即座に理解・実践できる、極めて実用的で洗練されたWebダッシュボードHTML（CSS内蔵・完全レスポンシブ）を生成してください。

【構成・デザイン要件】
1. 完全なHTML（<!DOCTYPE html>〜</html>）として出力すること。Tailwind CSS (https://cdn.tailwindcss.com) をCDNで読み込むこと。
2. ヘッダー:
   - タイトル: 「主要AIアップデート & 業務活用ガイド」
   - サブタイトル: 「最新機能のビジネス活用シーン・実践プロンプト集」
   - 最終更新日時バッジ: 「最終更新: {jst_now} JST」
3. 「今週の重要ハイライト（3選）」:
   - 画面上部に、全ビジネスパーソンが押さえるべき最重要トピックを3つのカードで要約提示。
4. 主要サービス別セクション（ChatGPT / Gemini / Claude）:
   - ブランドカラーで色分け（ChatGPT: エメラルドグリーン系、Gemini: ブルー/インディゴ系、Claude: アンバー/オレンジ系）
   - 各アップデート項目は以下のフォーマットで記述すること：
     ■ 機能名 & バージョン（例: Claude 3.7 Sonnet / o3-mini / Gemini 2.0 Flash など）
     ■ 何ができるようになった？（専門用語を使わず「Before（以前）→ After（今）」で比較説明）
     ■ 業務での具体的活用シーン（部門別バッジ付き: 【営業・マーケ】【開発・情シス】【バックオフィス・人事・総務】などから該当するもの）
     ■ 【コピペで使える】実践プロンプト例 または 具体的な活用手順（背景付きのコードブロックまたは引用枠で掲載）
5. マークダウン記号（```html や ```）は一切含めず、純粋なHTMLコードのみを出力すること。
"""

try:
    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            tools=[types.Tool(google_search=types.GoogleSearch())],
            temperature=0.3,
        ),
    )
except Exception as e:
    print(f"Retrying without search tool due to: {e}")
    response = client.models.generate_content(
        model="gemini-3.6-flash",
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

print(f"[{jst_now}] index.html updated successfully.")
