import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = Flask(__name__)
CORS(app)

LOG_FILE = "urls.txt"

@app.route("/check", methods=["POST"])
def check_url():
    payload = request.get_json()
    if not payload or "url" not in payload:
        return jsonify({"error": "Missing 'url' in request"}), 400

    url = payload["url"]

    # 1. 將收到的 URL 寫入 log 檔
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(url + "\n")
    except Exception as e:
        print("寫入 URL log 檔時發生錯誤：", e)
        # 這裡不當作 fatal error，只是打印訊息

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

    user_message = {
        "role": "user",
        "content": f"URL: {url}\nAnswer only 'Y', 'N', or 'U'."
    }

    try:
        response = client.chat.completions.create(
            model="gpt-4.1-nano",
            temperature=0.0,
            top_p=1.0,
            messages=[system_message, user_message]
        )
    except Exception as e:
        print("OpenAI API 發生錯誤：", e)
        return jsonify({"error": str(e)}), 500

    try:
        reply = response.choices[0].message.content.strip().upper()
        label = "phishing" if reply == "Y" or reply == "U"else "legitimate"
    except Exception as e:
        print("解析 OpenAI 回傳內容時發生錯誤：", e)
        return jsonify({"error": str(e)}), 500
    
    # 寫入 URL 和 GPT 回應到檔案
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(url + "\n")
            f.write(reply + "\n")  # 或改成 label + "\n" 也可以
    except Exception as e:
        print("寫入 URL/GPT 回應時發生錯誤：", e)
    
    return jsonify({"label": label}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

