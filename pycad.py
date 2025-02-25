from pyautocad import Autocad, APoint
import pythoncom
import os
import time

# 初始化COM库
pythoncom.CoInitialize()

try:
    # 显式创建AutoCAD实例
    acad = Autocad(create_if_not_exists=True)
    acad.app.Visible = True
    time.sleep(3)  # 等待AutoCAD启动

    # 验证模板路径
    template_path = r"F:\repo\Python_CAD\resources\KLCOB.dwg"
    if not os.path.exists(template_path):
        raise FileNotFoundError(f"模板文件不存在于：{template_path}")

    # 带重试的插入函数
    def insert_box_template(x, y, retries=3):
        for attempt in range(retries):
            try:
                acad.model.InsertBlock(APoint(x, y), template_path, 1, 1, 1, 0)
                return
            except pythoncom.com_error as e:
                if attempt == retries - 1:
                    raise
                print(f"插入fail，正在重试 ({attempt+1}/{retries})")
                time.sleep(1)

    # 生成显示矩阵
    def generate_display_screen(rows, cols, box_width, box_height):
        start_x, start_y = 0, 0
        for row in range(rows):
            y_pos = start_y + row * box_height
            for col in range(cols):
                x_pos = start_x + col * box_width
                insert_box_template(x_pos, y_pos)
                time.sleep(0.1)  # 降低调用频率

    # 执行生成
    generate_display_screen(4, 4, 600, 337.5)

    # 保存文档
    acad.doc.SaveAs("Correct_Display_Screen.dwg")

finally:
    # 清理COM资源
    pythoncom.CoUninitialize()
