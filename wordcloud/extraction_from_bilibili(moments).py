import re
import time
import requests
from typing import List, Dict, Any

OUT_TXT = "bilibili_text.txt"
SLEEP = 0.7
TIMEOUT = 10
HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Referer": "https://www.bilibili.com/",
    "Accept-Encoding": "identity", 
    # 请替换为自己的 Cookie
    "Cookie": "buvid3=..."
}

API = "https://api.bilibili.com/x/polymer/web-dynamic/v1/feed/space"

# 正则预编译
re_url = re.compile(r'https?://\S+')
re_square = re.compile(r'\[[^\]]+\]')
re_topic = re.compile(r'#.*?#')
re_at = re.compile(r'@[\w\u4e00-\u9fff_-]+')
# 只保留：中文、数字、常见中文标点和空白
re_keep = re.compile(r'[^\u4e00-\u9fff0-9，。！？；：“”‘’、……—（）《》\s]')

FIELDS = ["title", "desc", "description", "content", "dynamic", "text"]

def pick_text(d: Dict[str, Any], fields=FIELDS) -> List[str]:
    out = []
    for k in fields:
        v = d.get(k)
        if v:
            out.append(str(v))
    return out

def extract_text_from_item(item: Dict[str, Any]) -> str:
    texts: List[str] = []
    modules = item.get("modules", {})

    md = modules.get("module_dynamic", {})
    if "desc" in md:
        desc_obj = md["desc"]
        if isinstance(desc_obj, dict):
            texts.append(desc_obj.get("text", ""))
        elif isinstance(desc_obj, str):
            texts.append(desc_obj)

    major = md.get("major")
    if isinstance(major, dict):
        texts += pick_text(major)

    texts += pick_text(md)
    mm = modules.get("module_more", {})
    texts += pick_text(mm)
    texts += pick_text(item)

    if "orig" in item and isinstance(item["orig"], dict):
        texts += pick_text(item["orig"])
        modules_o = item["orig"].get("modules", {})
        md_o = modules_o.get("module_dynamic", {})
        if "desc" in md_o and isinstance(md_o["desc"], dict):
            texts.append(md_o["desc"].get("text", ""))

    return "\n".join(t for t in texts if t)

def clean_text(s: str) -> str:
    # 1. 去 URL
    s = re_url.sub('', s)
    # 2. 去 [xxx]
    s = re_square.sub('', s)
    # 3. 去 #话题#
    s = re_topic.sub('', s)
    # 4. 去 @xxx
    s = re_at.sub('', s)
    # 5. 删掉其他英文/符号，仅保留中文、数字、中文标点
    s = re_keep.sub('', s)
    # 6. 合并多余空白
    s = re.sub(r'\s+\n', '\n', s)
    s = re.sub(r'\n+', '\n', s).strip()
    return s

def crawl(uid: int):
    offset = ""
    total = 0
    with open(OUT_TXT, "w", encoding="utf-8") as fp:
        while True:
            params = {"offset": offset, "host_mid": uid}
            try:
                r = requests.get(API, params=params, headers=HEADERS, timeout=TIMEOUT)
                r.raise_for_status()
            except Exception as e:
                print(f"[ERROR] 请求失败：{e}")
                break

            data = r.json()
            if data.get("code") != 0:
                print(f"[ERROR] 接口返回错误：{data.get('message')}")
                break

            items = data.get("data", {}).get("items", [])
            if not items:
                print("没有更多动态。")
                break

            for it in items:
                raw_txt = extract_text_from_item(it)
                cleaned = clean_text(raw_txt)
                if cleaned:
                    fp.write(cleaned + "\n")
                    total += 1

            if not data.get("data", {}).get("has_more"):
                break
            offset = data.get("data", {}).get("offset")
            time.sleep(SLEEP)

    print("\n-------- 完成！---------")
    print(f"共写入 {total} 条动态文本 -> {OUT_TXT}")

def main():
    uid_str = input("请输入要抓取的 B 站 UID：").strip()
    if not uid_str.isdigit():
        print("UID 必须为数字")
        return
    crawl(int(uid_str))

if __name__ == "__main__":
    main()