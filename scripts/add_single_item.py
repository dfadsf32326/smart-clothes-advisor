import json
import subprocess
import sys
import os
import argparse

LARK_CLI = os.path.expanduser("~/.npm-global/bin/lark-cli")
BASE_TOKEN = "PS56bPhyNaWXRdsJX78cxyIOnJb"
TABLE_ID = "tbl1903VNTRjEJc3"

def run_command(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout.strip()

def main():
    parser = argparse.ArgumentParser(description="Add a single new clothes item to Feishu.")
    parser.add_argument("--name", required=True)
    parser.add_argument("--category", required=True)
    parser.add_argument("--color", required=True)
    parser.add_argument("--warmth", type=int, required=True)
    parser.add_argument("--style", required=True)
    parser.add_argument("--tags", required=True, help="Comma separated tags")
    parser.add_argument("--brand", default="")
    parser.add_argument("--status", default="in_stock")
    parser.add_argument("--image", help="Relative path to image file", default="")

    args = parser.parse_args()

    fields = {
        "单品名称": args.name,
        "品类": args.category,
        "颜色": args.color,
        "保暖度分值": args.warmth,
        "风格": args.style,
        "适用场景/标签": [t.strip() for t in args.tags.split(",") if t.strip()],
        "品牌": args.brand,
        "状态": args.status
    }

    print(f"1. Creating record in Feishu for: {args.name}")
    upsert_cmd = f"{LARK_CLI} base +record-upsert --base-token {BASE_TOKEN} --table-id {TABLE_ID} --json '{json.dumps(fields, ensure_ascii=False)}'"
    upsert_out = run_command(upsert_cmd)
    
    try:
        res_data = json.loads(upsert_out)
        record_id = res_data.get("data", {}).get("record", {}).get("record_id_list", [])[0]
        print(f"✅ Record created successfully. Record ID: {record_id}")
    except Exception as e:
        print("Failed to create record or parse output:")
        print(upsert_out)
        sys.exit(1)

    if args.image and os.path.exists(args.image):
        print(f"2. Uploading image attachment: {args.image}")
        img_dir = os.path.dirname(os.path.abspath(args.image))
        img_name = os.path.basename(args.image)
        upload_cmd = f"cd '{img_dir}' && {LARK_CLI} base +record-upload-attachment --base-token {BASE_TOKEN} --table-id {TABLE_ID} --record-id {record_id} --field-id 'fld3xOg2p9' --file './{img_name}'"
        upload_out = run_command(upload_cmd)
        if '"ok": true' in upload_out.lower():
            print("✅ Image uploaded successfully.")
        else:
            print(f"⚠️ Image upload failed: {upload_out}")
    elif args.image:
        print(f"⚠️ Image file {args.image} not found, skipped upload.")

    print("Done! You may want to run sync_from_feishu.py to update local JSON database.")

if __name__ == "__main__":
    main()
