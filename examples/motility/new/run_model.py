from pathlib import Path

from physicool import optimization as opt


def prepare_environment():
    opt.compile_project()
    opt.clean_outputs()
    black_box = opt.PhysiCellBlackBox()

    return black_box


def main():
    box = prepare_environment()
    box.run()


if __name__ == "__main__":
    main()