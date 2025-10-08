# AmigaBinHandler

![GitHub commit activity](https://img.shields.io/github/commit-activity/t/pkg-dot-zip/AmigaBinHandler)
![GitHub Repo stars](https://img.shields.io/github/stars/pkg-dot-zip/AmigaBinHandler)

![](https://github.com/farm-ng/amiga-dev-kit/assets/64480560/18dbebd2-98a1-4c5b-b6b4-2c73093fb7df)

## What is this?
This is a CLI tool written in Python to retrieve usable information
from the .bin files created by the recorder in the [Farm-Ng Amiga](https://farm-ng.com/amiga/) brain.

Instead of having many small scripts to automate this process this is a bundled application
intended to save time for all developers.

Please note that this project was created and maintained by 3rd party developers and that we are not affiliated with Farm-Ng.

## Current features
In this section we describe the features for every extractable service
in the application:

### Camera
- Export all cameras or a selected single one.
- Export rgb, disparity, left and right camera data (or a selected single one) to _.jpg_'s or a _.mp4_ video.
- Merge left and right pictures into a single [.mpo](https://en.wikipedia.org/wiki/JPEG#JPEG_Multi-Picture_Format) file using the --mpo argument.

| Argument Name       | Short Form | Description                                               | Required | Type                  | Default    | Choices                             |
|---------------------|------------|-----------------------------------------------------------|----------|-----------------------|------------|-------------------------------------|
| `--file`            | `-f`       | Specifies the path to the input `.bin` data file.         | **Yes**  | `Path`                | None       | None                                |
| `--ouput_dir`       | `-o`       | Specifies the directory to write the parsed data to.      | **Yes**  | `Path`                | None       | None                                |
| `--camera`          | `-c`       | Specifies the camera to parse data from.                  | No       | `ECamera`             | None (all) | `oak0`, `oak1`, `oak2`, `oak3`      |
| `--view`            | `-v`       | Specifies the view to parse data from.                    | No       | `EView`               | None (all) | `rgb`, `left`, `right`, `disparity` |
| `--method`          | `-m`       | Specifies the export method for the data.                 | No       | `ECameraExportMethod` | `JPG`      | `jpg`, `mp4`                        |
| `--disparity_scale` | `-d`       | Specifies the disparity scale for the data.               | No       | `int`                 | `1`        | None                                |
| `--mpo`             | `-a`       | Combines left and right images into a single `.mpo` file. | No       | `bool`                | `False`    | None                                |


## Running
> Make sure you have installed the [ADK](https://amiga.farm-ng.com/docs/brain/brain-install/)!

First of all, clone the repository and open it in PyCharm.

PyCharm automatically uses the correct virtual environment if you have set up
the project correctly. If you are using the terminal you might have to add
the `src` directory to the `$PYTHONPATH` to avoid `ModuleNotFoundError`s like this:

```bash
export PYTHONPATH="{$PYTHONPATH}:/home/user/PycharmProjects/AmigaBinHandler/src"
```

You can then run the script as follows:
```bash
python3 main.py <component> <args>
```

An example for the camera:
```bash
python3 main.py camera -f "/home/user/Downloads/test_bin.bin" -o "/home/user/Downloads/output/" --mpo
```

## Building
> Note that this project is intended to be run on a developer machine with the IDE open.

If you want to bundle this project into a single executable you can use
[pyinstaller](https://pyinstaller.org/en/stable/). Navigate to the project directory after verifying you can run the project, and run the following in your terminal:

```bash
pip install pyinstaller
pyinstaller --onefile main.py
```