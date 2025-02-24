from pyautocad import Autocad, APoint
import pythoncom


class CADManager:
    def __init__(self, template_path):
        self._acad = None
        self.template_path = template_path

    @property
    def acad(self):
        """延迟初始化AutoCAD连接"""
        if not self._acad:
            pythoncom.CoInitialize()
            self._acad = Autocad(create_if_not_exists=True)
        return self._acad

    def insert_block(self, x, y):
        """在指定坐标插入块"""
        try:
            self.acad.model.InsertBlock(APoint(x, y), self.template_path, 1, 1, 1, 0)
        except Exception as e:
            print(f"插入块失败 @ ({x}, {y}): {str(e)}")

    def save_drawing(self, filepath):
        """保存图纸"""
        self.acad.doc.SaveAs(filepath)
        print(f"图纸已保存至: {filepath}")
