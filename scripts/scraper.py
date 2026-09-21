import json
import os
from datetime import datetime
import requests
from bs4 import BeautifulSoup

def fetch_arknights_events():
    """以明日方舟 PRTS Wiki 或社群資料為例 (示意邏輯)"""
    # 實作時可利用 PRTS MediaWiki API 或解析頁面表格
    return [
        {
            "id": "ak_event_01",
            "title": "生息演算：沙洲遺聞",
            "type": "major",
            "endTime": "2026-10-05T03:59:59+08:00",
            "totalStages": 5,
            "rewards": "限定幹部、尋訪憑證"
        }
    ]

def fetch_hsr_events():
    """以星穹鐵道資料為例"""
    return [
        {
            "id": "hsr_event_01",
            "title": "銀河巡禮演武",
            "type": "major",
            "endTime": "2026-09-28T03:59:59+08:00",
            "totalStages": 4,
            "rewards": "星瓊 x1000、命運的足跡"
        }
    ]

def main():
    # 組合四款遊戲的資料
    all_data = [
        {
            "gameId": "hsr",
            "gameName": "崩壞：星穹鐵道",
            "updatedAt": datetime.now().isoformat(),
            "events": fetch_hsr_events()
        },
        {
            "gameId": "arknights",
            "gameName": "明日方舟",
            "updatedAt": datetime.now().isoformat(),
            "events": fetch_arknights_events()
        }
    ]

    # 確保輸出目錄存在
    os.makedirs("data", exist_ok=True)
    
    # 寫入 JSON
    output_path = os.path.join("data", "events.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(all_data, f, ensure_ascii=False, indent=2)
        
    print(f"資料更新成功，已寫入 {output_path}")

if __name__ == "__main__":
    main()
