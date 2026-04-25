import json
import subprocess
import os

LARK_CLI = os.path.expanduser("~/.npm-global/bin/lark-cli")
BASE_TOKEN = "PS56bPhyNaWXRdsJX78cxyIOnJb"
TABLE_ID = "tbl1903VNTRjEJc3"
FIELD_NAME = "单品图片"

# 手动映射名称到真实图片文件
REAL_IMAGE_MAP = {
    "PRBLMS 白色立领羽绒服": "assets/images/white_puffer_jacket.jpg",
    "灰紫色圆领短袖 T 恤": "assets/images/purple_tshirt.jpg",
    "卡其色圆领短袖 T 恤": "assets/images/khaki_tshirt.jpg",
    "Cabbeen 蓝灰色圆领针织毛衣": "assets/images/grey_sweater.jpg",
    "CEC 灰色圆领卫衣": "assets/images/grey_sweatshirt.jpg"
}

def run_command(cmd):
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.stdout.strip()
    except Exception as e:
        return str(e)

print("Fetching records to get record IDs...")
list_cmd = f"{LARK_CLI} base +record-list --base-token {BASE_TOKEN} --table-id {TABLE_ID}"
list_out = run_command(list_cmd)

try:
    data = json.loads(list_out)
    records_data = data.get("data", {}).get("data", [])
    fields_names = data.get("data", {}).get("fields", [])
    record_ids = data.get("data", {}).get("record_id_list", [])
    
    name_index = fields_names.index("单品名称") if "单品名称" in fields_names else -1
    
    name_to_id = {}
    if name_index != -1:
        for idx, row in enumerate(records_data):
            name = row[name_index]
            rec_id = record_ids[idx]
            name_to_id[name] = rec_id
            
except Exception as e:
    print("Failed to parse list output:", e)
    exit(1)

for name, rel_path in REAL_IMAGE_MAP.items():
    record_id = name_to_id.get(name)
    if not record_id:
        print(f"Skip {name}: record ID not found in Feishu.")
        continue
        
    # 直接使用相对路径
    if not os.path.exists(rel_path):
        print(f"Skip {name}: file {rel_path} does not exist.")
        continue
        
    print(f"Uploading {rel_path} for {name} ({record_id})...")
    cmd = f"{LARK_CLI} base +record-upload-attachment --base-token {BASE_TOKEN} --table-id {TABLE_ID} --record-id {record_id} --field-id '{FIELD_NAME}' --file '{rel_path}'"
    out = run_command(cmd)
    
    if '"ok": true' in out.lower():
        print("Success.")
    else:
        print(f"Failed: {out}")

