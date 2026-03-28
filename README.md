# Manikeys Keyboard

[3D Model (STL)](https://raw.githubusercontent.com/carlosmaniero/manikey/assets/main.stl)

## Views

| Perspective | Back View |
| :---: | :---: |
| ![Perspective](https://raw.githubusercontent.com/carlosmaniero/manikey/assets/main.png) | ![Back View](https://raw.githubusercontent.com/carlosmaniero/manikey/assets/main_back.png) |

| Top View | Side View | Side View (Inverse) |
| :---: | :---: | :---: |
| ![Top View](https://raw.githubusercontent.com/carlosmaniero/manikey/assets/main_top.png) | ![Side View](https://raw.githubusercontent.com/carlosmaniero/manikey/assets/main_side.png) | ![Side View (Inverse)](https://raw.githubusercontent.com/carlosmaniero/manikey/assets/main_side_inv.png) |

## All Angles (45° steps)

| 45° (Perspective) | 90° | 135° | 180° |
| :---: | :---: | :---: | :---: |
| ![45°](https://raw.githubusercontent.com/carlosmaniero/manikey/assets/main_angle45.png) | ![90°](https://raw.githubusercontent.com/carlosmaniero/manikey/assets/main_angle90.png) | ![135°](https://raw.githubusercontent.com/carlosmaniero/manikey/assets/main_angle135.png) | ![180°](https://raw.githubusercontent.com/carlosmaniero/manikey/assets/main_angle180.png) |

| 225° (Back View) | 270° | 315° | 0° |
| :---: | :---: | :---: | :---: |
| ![225°](https://raw.githubusercontent.com/carlosmaniero/manikey/assets/main_angle225.png) | ![270°](https://raw.githubusercontent.com/carlosmaniero/manikey/assets/main_angle270.png) | ![315°](https://raw.githubusercontent.com/carlosmaniero/manikey/assets/main_angle315.png) | ![0°](https://raw.githubusercontent.com/carlosmaniero/manikey/assets/main_angle0.png) |

This project uses [PythonSCAD](https://pythonscad.org) to design a custom 3D-printable keyboard based on spherical projections.

## Requirements

- **PythonSCAD**: Required for core CAD operations.
- **F3D**: Required **only** for the `render` step (generating PNGs).

## Development

- `make build`: Generate the STL and 3MF files for `src/main.py`.
- `make render`: Generate PNG renderings (Front, Back, Top, Side) for `src/main.py`.
- `make build/ANY_FILE.stl`: Generate STL file for `src/ANY_FILE.py`.
- `make build/ANY_FILE.3mf`: Generate 3MF file for `src/ANY_FILE.py`.
- `make build/ANY_FILE.png`: Generate PNG rendering for `src/ANY_FILE.py`.
- `make test`: Run tests.
- `make lint`: Check code quality.
