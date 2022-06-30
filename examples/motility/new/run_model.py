from pathlib import Path

from physicool import optimization as opt


def prepare_environment():
    opt.compile_project()
    if Path("temp").is_dir():
        Path("temp").rmdir()

    black_box = opt.PhysiCellBlackBox()

    return black_box


def main():
    box = prepare_environment()
    box.run()


if __name__ == "__main__":
    main()