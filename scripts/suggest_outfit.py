import json
import sys

def calculate_required_warmth(current_temp, target_temp=26):
    return target_temp - current_temp

def get_recommendation(temp_min, temp_max, items, outfits):
    temp_diff = temp_max - temp_min
    avg_temp = (temp_min + temp_max) / 2
    required_warmth = calculate_required_warmth(avg_temp)
    
    # 逻辑：如果温差大，强制开启叠穿模式
    is_layering_needed = temp_diff > 8
    
    recommendation = {
        "is_layering": is_layering_needed,
        "required_warmth": required_warmth,
        "advice": "",
        "selected_items": []
    }
    
    if is_layering_needed:
        recommendation["advice"] = f"今日温差高达 {temp_diff}℃，建议采用「洋葱穿衣法」。内层吸汗，外层防风，方便随气温穿脱。"
    else:
        recommendation["advice"] = f"今日气温较平稳，目标保暖度约为 {required_warmth}℃。"
        
    return recommendation

if __name__ == "__main__":
    # 示例调用逻辑
    t_min = float(sys.argv[1]) if len(sys.argv) > 1 else 15
    t_max = float(sys.argv[2]) if len(sys.argv) > 2 else 25
    print(json.dumps(get_recommendation(t_min, t_max, [], []), ensure_ascii=False, indent=2))
