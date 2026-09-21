import os
import json
import smtplib
from email.mime.text import MIMEText
from email.header import Header

# 模擬爬蟲監聽到的最新官方公告網址（實作時可替換為爬取到的真實動態網址）
LATEST_ANNOUNCEMENTS = [
    {
        "game": "崩壞：星穹鐵道",
        "title": "全新版本活動快訊公告",
        "url": "https://www.hoyolab.com/circles/6"
    },
    {
        "game": "鳴潮",
        "title": "限時活動時程預告",
        "url": "https://kurobbs.com"
    }
]

HISTORY_FILE = "data/notified_history.json"

def send_notification_email(new_items):
    sender = os.environ.get("MAIL_USERNAME")
    password = os.environ.get("MAIL_PASSWORD")
    receiver = os.environ.get("RECEIVER_EMAIL")

    if not sender or not password or not receiver:
        print("未設定 Email 環境變數，略過發信。")
        return

    # 組合信件內容
    content = "你好！二遊爬蟲偵測到以下可能的新活動情報：\n\n"
    for item in new_items:
        content += f"【{item['game']}】{item['title']}\n"
        content += f"情報網址：{item['url']}\n\n"
    content += "--------------------------------------\n"
    content += "請將上述活動文字或網址直接貼給 AI，AI 會幫你整理出更新代碼！"

    msg = MIMEText(content, 'plain', 'utf-8')
    msg['From'] = Header(f"二遊情報機器人 <{sender}>", 'utf-8')
    msg['To'] = Header(receiver, 'utf-8')
    msg['Subject'] = Header(f"🚨 發現 {len(new_items)} 則新二遊活動公告！", 'utf-8')

    try:
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login(sender, password)
        server.sendmail(sender, [receiver], msg.as_string())
        server.quit()
        print("✅ 通知信件寄送成功！")
    except Exception as e:
        print(f"❌ 寄信失敗: {e}")

def main():
    os.makedirs("data", exist_ok=True)
    
    # 讀取以前通知過的歷史紀錄，避免重複發信
    notified_urls = []
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            notified_urls = json.load(f)

    # 比對是否有新情報
    new_items = [item for item in LATEST_ANNOUNCEMENTS if item['url'] not in notified_urls]

    if new_items:
        print(f"發現 {len(new_items)} 則新情報，準備發送郵件通知...")
        send_notification_email(new_items)
        
        # 紀錄已通知過
        notified_urls.extend([item['url'] for item in new_items])
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(notified_urls, f, ensure_ascii=False, indent=2)
    else:
        print("沒有新的公告情報。")

if __name__ == "__main__":
    main()
