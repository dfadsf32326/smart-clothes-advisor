import json

raw_json = """{
  "items": [
    {
      "id": "white_puffer_jacket_001",
      "name": "PRBLMS 白色立领羽绒服",
      "category": "厚羽绒服",
      "color": "白色",
      "warmth": 9,
      "style": "美式",
      "tags": ["街头", "复古", "简约舒适"],
      "image_path": "assets/images/white_puffer_jacket.jpg",
      "brand": "PRBLMS",
      "status": "in_stock"
    },
    {
      "id": "purple_tshirt_001",
      "name": "灰紫色圆领短袖 T 恤",
      "category": "短袖 T 恤",
      "color": "灰紫色",
      "warmth": 1,
      "style": "日系",
      "tags": ["简约舒适", "盐系"],
      "image_path": "assets/images/purple_tshirt.jpg",
      "brand": "未知",
      "status": "in_stock"
    },
    {
      "id": "khaki_tshirt_001",
      "name": "卡其色圆领短袖 T 恤",
      "category": "短袖 T 恤",
      "color": "卡其色",
      "warmth": 1,
      "style": "日系",
      "tags": ["简约舒适", "盐系"],
      "image_path": "assets/images/khaki_tshirt.jpg",
      "brand": "未知",
      "status": "in_stock"
    },
    {
      "id": "grey_sweater_001",
      "name": "Cabbeen 蓝灰色圆领针织毛衣",
      "category": "厚毛衣",
      "color": "蓝灰色",
      "warmth": 5,
      "style": "日系",
      "tags": ["简约舒适", "精致"],
      "image_path": "assets/images/grey_sweater.jpg",
      "brand": "Cabbeen",
      "status": "in_stock"
    },
    {
      "id": "grey_sweatshirt_001",
      "name": "CEC 灰色圆领卫衣",
      "category": "卫衣",
      "color": "灰色",
      "warmth": 3,
      "style": "韩系",
      "tags": ["简约舒适", "休闲", "街头"],
      "image_path": "assets/images/grey_sweatshirt.jpg",
      "brand": "CEC",
      "status": "in_stock"
    }
  ],
  "config": {
    "styles": ["商务", "日系", "韩系", "美式"],
    "tags": ["正式干练", "简约舒适", "复古", "街头", "户外", "运动", "盐系", "精致"]
  }
}"""

with open('data/items.json', 'w') as f:
    json.dump(json.loads(raw_json), f, indent=2, ensure_ascii=False)
