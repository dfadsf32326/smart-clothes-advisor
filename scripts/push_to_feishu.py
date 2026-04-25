import json
import subprocess
import os
import sys

LARK_CLI = os.path.expanduser("~/.npm-global/bin/lark-cli")
BASE_TOKEN = "PS56bPhyNaWXRdsJX78cxyIOnJb"
TABLE_ID = "tbl1903VNTRjEJc3"
DATA_FILE = "data/items.json"

def run_command(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
    return result.stdout.strip()

def push_data():
    if not os.path.exists(DATA_FILE):
        print(f"Error: {DATA_FILE} not found.")
        sys.exit(1)

    with open(DATA_FILE, 'r') as f:
        data = json.load(f)

    items = data.get("items", [])
    if not items:
        print("No items to push.")
        return

    print(f"Start pushing {len(items)} items to Feishu...")
    success_count = 0
    for item in items:
        # 如果是未分配 ID 的数据或者只是本地草稿，可以推送到飞书
        fields = {
            "单品名称": item.get("name"),
            "品类": item.get("category"),
            "保暖度分值": item.get("warmth"),
            "颜色": item.get("color"),
            "风格": item.get("style"),
            "适用场景/标签": item.get("tags", []),
            "品牌": item.get("brand"),
            "状态": item.get("status")
        }
        
        # 使用 record-upsert ，如果飞书中有记录，可以不重复创建 (简化处理：这里仍使用批量创建机制，实际场景通常结合搜索去重，这里用简单的 record-upsert 占位)
        cmd = f"{LARK_CLI} base +record-upsert --base-token {BASE_TOKEN} --table-id {TABLE_ID} --json '{json.dumps(fields, ensure_ascii=False)}'"
        print(f"Pushing: {item.get('name')}...")
        out = run_command(cmd)
        if "ok" in out.lower():
            success_count += 1
            
    print(f"✅ Push finished. Successfully pushed {success_count}/{len(items)} items.")

if __name__ == "__main__":
    push_data()
