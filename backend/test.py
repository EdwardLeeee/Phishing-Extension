import os
import pandas as pd
import random
import time
from sklearn.metrics import classification_report
from dotenv import load_dotenv
from openai import OpenAI

start_time = time.time()
# -----------------------------
# 1. 載入 API 金鑰
# -----------------------------
load_dotenv()  # 會自動從 .env 讀取環境變數
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# -----------------------------
# 2. 讀取 CSV 並隨機抽樣
# -----------------------------
df = pd.read_csv("test.csv")  # 假設檔案跟此腳本在同一個目錄

# 隨機抽 40,000 筆
sample_df = df.sample(n=40000)

urls = sample_df["URL"].tolist()
labels = sample_df["Label"].tolist()

# -----------------------------
# 3. 將真實標籤轉成二元：bad → 1, good → 0
# -----------------------------
true_binary = [1 if lbl == "bad" else 0 for lbl in labels]

# 預測結果暫存（0 或 1）
pred_binary = []

# -----------------------------
# 4. 定義 system_message
# -----------------------------
system_message = {
    "role": "system",
    "content": (
        "You are a cybersecurity expert. When given a URL, your task is to determine whether it is likely to be a phishing website. "
        "Base your decision only on the domain name and URL pattern, and do NOT hallucinate.\n\n"
        "Respond with:\n"
        "Y — if it is suspicious and likely a phishing website.\n"
        "N — if it is a legitimate, safe website.\n"
        "U — if you're unsure and cannot make a reliable judgment.\n\n"
        "Do NOT assume any website is phishing unless there are clear signals like misspellings, misleading subdomains, strange TLDs, or unusual paths."
    )
}

# -----------------------------
# 5. 逐一呼叫 GPT-4.1 nano，並將 Y/U 視為 bad(1)、N 視為 good(0)
# -----------------------------
for idx, url in enumerate(urls):
    user_message = {
        "role": "user",
        "content": f"URL: {url}\nAnswer only 'Y', 'N', or 'U'."
    }

    try:
        # 使用 OpenAI client 呼叫 chat completion
        response = client.chat.completions.create(
            model="gpt-4.1-nano",
            temperature=0.0,
            top_p=1.0,
            messages=[system_message, user_message]
        )
        answer = response.choices[0].message.content.strip().upper()

        # 確保只取 Y、N、U，其他視作 U
        if answer not in ["Y", "N", "U"]:
            answer = "U"

        # Y 或 U → 1；N → 0
        if answer in ["Y", "U"]:
            pred_binary.append(1)
        else:
            pred_binary.append(0)

    except Exception as e:
        print(f"[Error at index {idx}]: {e}")
        # 發生例外也當作 bad(1)
        pred_binary.append(1)


# -----------------------------
# 6. 計算 Precision/Recall/F1-score
# -----------------------------
print(classification_report(true_binary, pred_binary, target_names=["Good (0)", "Bad (1)"]))

# 結束計時並印出總花費時間（秒）
end_time = time.time()
print(f"\n✅ 總執行時間：{end_time - start_time:.2f} 秒")

