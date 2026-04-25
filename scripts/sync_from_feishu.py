import json
import subprocess
import os

LARK_CLI = os.path.expanduser("~/.npm-global/bin/lark-cli")
BASE_TOKEN = "PS56bPhyNaWXRdsJX78cxyIOnJb"
TABLE_ID = "tbl1903VNTRjEJc3"

def run_command(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout.strip()

cmd = f"{LARK_CLI} base +record-list --base-token {BASE_TOKEN} --table-id {TABLE_ID}"
out = run_command(cmd)

try:
    res = json.loads(out)
    data_list = res.get("data", {}).get("data", [])
    fields_list = res.get("data", {}).get("fields", [])
    
    # 构建索引
    field_idx = {name: i for i, name in enumerate(fields_list)}
    
    new_items = []
    for r in data_list:
        def get_val(name):
            if name in field_idx and field_idx[name] < len(r):
                return r[field_idx[name]]
            return None

        # 辅助函数：处理可能为 list 的情况
        def get_str(val):
            if isinstance(val, list) and len(val) > 0: return str(val[0])
            return str(val) if val else "未知"
            
        def get_list(val):
            if isinstance(val, list): return [str(x) for x in val]
            return [str(val)] if val else []

        new_item = {
            "id": get_str(get_val("单品编号")),
            "name": get_str(get_val("单品名称")),
            "category": get_str(get_val("品类")),
            "warmth": int(float(get_str(get_val("保暖度分值")))) if get_str(get_val("保暖度分值")).replace('.','',1).isdigit() else 1,
            "color": get_str(get_val("颜色")),
            "style": get_str(get_val("风格")),
            "tags": get_list(get_val("适用场景/标签")),
            "brand": get_str(get_val("品牌")),
            "status": get_str(get_val("状态")),
            "image_path": f"assets/images/{get_str(get_val('单品编号'))}.jpg"
        }
        new_items.append(new_item)
        
    if new_items:
        with open('data/items.json', 'r') as f:
            old_data = json.load(f)
            
        old_data["items"] = new_items
        
        with open('data/items.json', 'w') as f:
            json.dump(old_data, f, indent=2, ensure_ascii=False)
            
        print(f"✅ 成功从飞书全量拉取 {len(new_items)} 条记录并更新到 data/items.json")
    else:
        print("Warning: 飞书中未找到数据")
except Exception as e:
    print(f"Error parsing JSON: {e}")
