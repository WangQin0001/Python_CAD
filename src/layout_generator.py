from dataclasses import dataclass


@dataclass
class LayoutParams:
    rows: int
    cols: int
    box_width: float
    box_height: float
    spacing_x: float = 0
    spacing_y: float = 0
    start_x: float = 0
    start_y: float = 0


class LayoutGenerator:
    def __init__(self, cad_manager):
        self.cad = cad_manager

    def generate_grid(self, params: LayoutParams):
        """生成网格布局"""
        for row in range(params.rows):
            for col in range(params.cols):
                x = params.start_x + col * (params.box_width + params.spacing_x)
                y = params.start_y + row * (params.box_height + params.spacing_y)
                self.cad.insert_block(x, y)

        print(f"已生成 {params.rows}x{params.cols} 布局，总计 {params.rows*params.cols} 个箱体")
