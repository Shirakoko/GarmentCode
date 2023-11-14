import json

# 把garmentcode的json格式转换成我们需要的panels.json的格式
def convert_form(filepath):
    json_str = ""
    with open(filepath, 'r') as f_json:
        json_str = json.load(f_json) # 得到json字符串
    # 获取原始的板片和缝纫线数据
    panels = json_str["pattern"]["panels"]
    stitches = json_str["pattern"]["stitches"]
    # 创建一个空的字典，用于存储目标的板片和缝纫线数据
    result = {}

    # 创建一个空的列表，用于存储目标的板片数据
    result["panels"] = []
    # 遍历原始的板片数据
    for key, panel_data in panels.items():
        # 创建一个空的字典，用于存储目标板片数据
        panel = {}
        # 设置板片的id，先用板片名称即key代替
        panel["id"] = key
        # 设置板片的label，也先用key代替，后面再做字符串mapping
        panel["label"] = key
        # 设置板片的左右配偶和前后配偶先为空
        panel["xSpouse"] = None
        panel["ySpouse"] = None
        # 设置板片的顶点，先用原始的顶点数据代替
        panel["vertices"] = panel_data["vertices"]
        # 设置板片的边，先用原始的边数据代替
        panel["edges"] = panel_data["edges"]
        # 设置板片的bbox中心，用原始的平移数据
        panel["center"] = panel_data["translation"]
        panel["center"][2] = 0 # 压平z坐标
        # 计算板片的顶点的x和y坐标的最小值和最大值，得到板片的2D包围盒的边界
        x_coords = [vertex[0] for vertex in panel["vertices"]]
        y_coords = [vertex[1] for vertex in panel["vertices"]]
        bbox_left = min(x_coords)
        bbox_right = max(x_coords)
        bbox_bottom = min(y_coords)
        bbox_top = max(y_coords)
        # 设置板片的bbox字段，用一个列表来表示
        panel["bbox"] = [bbox_left, bbox_right, bbox_bottom, bbox_top]
        # 将板片数据添加到列表中
        result["panels"].append(panel)

    # 创建一个空的列表，用于存储目标的缝纫线数据
    result["stitches"] = []
    # 遍历原始的缝纫线数据
    for stitch in stitches:
        # 创建一个空的列表，用于存储目标的缝纫线数据
        stitch_result = []
        # 遍历缝纫线的每一段
        for segment in stitch:
            # 创建一个空的字典，用于存储目标的缝纫线数据
            segment_result = {}
            # 设置缝纫线的起点
            segment_result["start"] = {
            "clothPieceId": segment["panel"], # 这里是板片名称而不是uuid
            "edgeId": segment["edge"], # 这里是板片边的index而不是uuid
            "param": 0 # param先设置为0，我也不清楚param是啥
            }
            # 设置缝纫线的终点
            segment_result["end"] = {
            "clothPieceId": segment["panel"],
            "edgeId": segment["edge"],
            "param": 0
            }
            # 设置缝纫线的遍历顺序，默认设置成false
            segment_result["isCounterClockWise"] = False 
            # 将缝纫线数据添加到列表中
            stitch_result.append(segment_result)
        # 将缝纫线数据添加到列表中
        result["stitches"].append(stitch_result)
    
    # 最后将对象转换成json字符串
    result_json = json.dumps(result, indent=4)
    # 返回json字符串
    # print(result_json)
    with open('output.json', 'w', encoding='utf-8') as f:
        # 用json.dump()函数把json字符串写入文件
        f.write(result_json)
        f.close()
    return

if __name__ == '__main__':
    convert_form("panels copy.json")
