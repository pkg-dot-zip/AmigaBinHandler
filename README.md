# AmigaBinHandler

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

## Running
> Make sure you have installed the [ADK](https://amiga.farm-ng.com/docs/brain/brain-install/)!

PyCharm automatically uses the correct virtual environment if you have setup
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