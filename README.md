##伺服器

```bash
cd backend
python3 -m venv venv
source venv/bin/activate         # Linux/macOS
pip install -r requirements.txt
uvicorn main:app --reload
```
## 插鍵
1.打開 Chrome 瀏覽器

2.前往 chrome://extensions/

3.開啟右上角「開發人員模式」

4.點選「載入已解壓縮的擴充功能」，選擇 extension/ 資料夾
