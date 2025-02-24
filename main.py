import argparse
from src.config_loader import load_config
from src.cad_utils import CADManager
from src.layout_generator import LayoutGenerator, LayoutParams


def main():
    # 命令行参数解析
    parser = argparse.ArgumentParser(description="自动化CAD显示屏生成系统")
    parser.add_argument("--rows", type=int, help="行数")
    parser.add_argument("--cols", type=int, help="列数")
    parser.add_argument("--width", type=float, help="箱体宽度")
    parser.add_argument("--height", type=float, help="箱体高度")
    args = parser.parse_args()

    # 加载配置
    config = load_config()

    # 合并配置与命令行参数
    params = LayoutParams(
        rows=args.rows or config["default_params"]["rows"],
        cols=args.cols or config["default_params"]["cols"],
        box_width=args.width or config["default_params"]["box_width"],
        box_height=args.height or config["default_params"]["box_height"],
        spacing_x=config["default_params"]["spacing_x"],
        spacing_y=config["default_params"]["spacing_y"],
    )

    # 初始化CAD系统
    cad = CADManager(config["autocad"]["template_path"])

    # 生成布局
    generator = LayoutGenerator(cad)
    generator.generate_grid(params)

    # 保存图纸
    cad.save_drawing(config["autocad"]["output_file"])


if __name__ == "__main__":
    main()
