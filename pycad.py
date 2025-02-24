from pyautocad import Autocad, APoint

# 初始化 AutoCAD 接口
acad = Autocad(create_if_not_exists=True)


# 加载模板路径
template_path = r"F:\repo\Python_CAD\resources\KLCOB.dwg"  # 替换为实际模板路径


# 插入模板的函数
def insert_box_template(x, y):
    acad.model.InsertBlock(APoint(x, y), template_path, 1, 1, 1, 0)


# 根据参数拼接显示屏图纸
def generate_display_screen(rows, cols, box_width, box_height):
    start_x, start_y = 0, 0  # 起始位置

    for row in range(rows):
        for col in range(cols):
            x_pos = start_x + col * box_width
            y_pos = start_y + row * box_height
            insert_box_template(x_pos, y_pos)


# 示例：生成10行4列的显示屏，每个箱体的尺寸为300x200单位
generate_display_screen(10, 4, 600, 337.5)
acad.quit()
# 完成后保存图纸
acad.doc.SaveAs("Generated_Display_Screen.dwg")
acad.Application.Quit()
