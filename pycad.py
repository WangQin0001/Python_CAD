from pyautocad import Autocad, APoint
import pythoncom
import os
import time


def initialize_autocad():
    """初始化AutoCAD实例并显示界面"""
    pythoncom.CoInitialize()
    acad = Autocad(create_if_not_exists=True)
    acad.app.Visible = True
    time.sleep(5)  # 增加等待时间，确保AutoCAD完全启动
    return acad


def validate_template_path(template_path):
    """验证模板文件是否存在"""
    if not os.path.exists(template_path):
        raise FileNotFoundError(f"模板文件不存在于：{template_path}")
    print(f"模板路径验证成功: {template_path}")
    return template_path


def insert_block_with_retry(acad, template_path, x, y, retries=3):
    """带重试机制的块插入函数"""
    for attempt in range(retries):
        try:
            print(f"尝试插入块，坐标: ({x}, {y})")
            acad.model.InsertBlock(APoint(x, y), template_path, 1, 1, 1, 0)
            print(f"插入成功，坐标: ({x}, {y})")
            return
        except pythoncom.com_error as e:
            if attempt == retries - 1:
                print(f"插入失败，坐标({x},{y})，错误详情: {e}")
                raise RuntimeError(f"插入失败，坐标({x},{y})") from e
            print(f"插入失败，正在重试 ({attempt + 1}/{retries})")
            time.sleep(1)


def generate_display_matrix(
    acad, template_path, rows, cols, screen_width, screen_height, start_x, start_y
):
    """生成屏幕矩阵"""
    for row in range(rows):
        current_y = start_y + row * screen_height
        for col in range(cols):
            current_x = start_x + col * screen_width
            insert_block_with_retry(acad, template_path, current_x, current_y)
            time.sleep(0.1)  # 降低操作频率


def save_document(acad, output_filename):
    """保存AutoCAD文档"""
    try:
        acad.doc.SaveAs(output_filename)
        print(f"文件已成功保存至：{os.path.abspath(output_filename)}")
    except pythoncom.com_error as e:
        print(f"保存文件失败，错误详情: {e}")
        raise


def cleanup_com():
    """清理COM资源"""
    pythoncom.CoUninitialize()


def get_user_input():
    """获取用户输入参数"""
    user_rows = int(input("请输入矩阵行数（默认：4）：") or 4)
    user_cols = int(input("请输入矩阵列数（默认：4）：") or 4)
    user_width = 600
    user_height = 337.5
    user_output = "Display_Screen.dwg"
    return user_rows, user_cols, user_width, user_height, user_output


def main():
    """主函数"""
    # 写死模板路径
    template_path = r"F:\repo\Python_CAD\resources\KLCOB.dwg"
    start_x = 0
    start_y = 0
    try:
        # 获取用户输入
        rows, cols, screen_width, screen_height, output_filename = get_user_input()

        # 初始化AutoCAD
        acad = initialize_autocad()

        # 验证模板路径
        validate_template_path(template_path)

        # 生成屏幕矩阵
        generate_display_matrix(
            acad,
            template_path,
            rows,
            cols,
            screen_width,
            screen_height,
            start_x,
            start_y,
        )

        # 保存文档
        save_document(acad, output_filename)

    except Exception as e:
        print(f"程序执行出错：{str(e)}")
    finally:
        # 清理COM资源
        cleanup_com()


if __name__ == "__main__":
    main()
