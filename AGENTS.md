# Project Guidelines

- **Code Comments**: Do NOT add code comments unless explicitly asked by the user.
- **Dataclasses**: Prefer using `@dataclass` for data-holding classes to reduce boilerplate (like `__init__` and `__repr__`).
- **Factory Methods**: When complex initialization is required, prefer using `@classmethod` factory methods (e.g., `from_x`) to keep the primary constructor simple and the class's purpose clear.

# Operational Requirements

Before performing any change in the code:
1.  **Sync**: Read the file again to ensure you have the latest version, as it may have been edited manually.
2.  **Confirm**: Always show a diff of the proposed changes and ask for confirmation before performing the changes.

After completing any code modifications:
1.  **Format**: Run `uv run ruff format .` to ensure consistent styling.
2.  **Verify**: Run `uv run pytest` to ensure no regressions were introduced.

# CAD File Generation

The `STL`, `3MF`, and `WRL` files in the `build/` directory are generated from Python source files located in `src/`. The generation process is managed by the `Makefile`.

There are two primary methods for generating CAD models in this project:

1.  **Direct Mesh Generation with PyVista**: Some models are created directly as meshes using the `pyvista` library. These scripts calculate vertices and faces to construct a `pyvista.PolyData` object. An example of this is `src/cad/body.py`, which generates the main body of the keyboard. The key function used is `create_full_surface(x, y, top_z, bottom_z)`, which builds a solid 3D object from top and bottom surfaces defined on a grid.

    Example of creating inputs for `create_full_surface`:
    ```python
    import numpy as np
    from pyvista_ext import create_full_surface

    # Create a grid of points
    x_coords = np.linspace(-10, 10, 50)
    y_coords = np.linspace(-10, 10, 50)
    x, y = np.meshgrid(x_coords, y_coords)

    # Define the top surface (e.g., a wavy surface)
    top_z = np.sin(x) * np.cos(y)

    # Define the bottom surface (e.g., a flat plane)
    bottom_z = np.full_like(x, -2)

    # Create the solid object
    surface = create_full_surface(x, y, top_z, bottom_z)
    ```

2.  **CSG with Manifold3D and OpenSCAD**: Most components and assemblies are built using Constructive Solid Geometry (CSG) via `manifold3d` directly or the `openscad` Python library with the Manifold backend. These scripts define geometric shapes and combine them with boolean operations (union, difference, intersection). `src/cad/body_bottom.py` and `src/components/oled_096/cad/oled.py` are good examples.

    When using boolean operations in `manifold3d.Manifold`, prefer `+` for union and `-` for difference.

    When using boolean operations, **prefer the `|` operator for union** instead of the `+` operator.

    A key feature of this approach is the ability to import existing models using `load_stl("path/to/model.stl")`. This returns an `openscad` object that can be manipulated, allowing for a hybrid workflow where generated and pre-existing parts can be combined.

All generated STL files are post-processed with `simplify.py` to reduce complexity and file size.

## Creating a New CAD File

To create a new CAD component:

1.  **Follow the Component Pattern**: Always separate data, logic, and geometry. Create a new folder (e.g., `src/components/my_part/`) and inside it create:
    - `parameters.py`: A `@dataclass` holding physical dimensions (e.g., `MyPartParameters`).
    - `model.py`: A `@dataclass` that injects the parameters and calculates bounding boxes, coordinates, and spacing (e.g., `MyPartModel`).
    - `cad/my_part.py`: The actual CAD generation file.

2.  **Implement the CAD Class**: Inside `cad/my_part.py`, define a class that generates your 3D object.
    - For `manifold3d`-based models (recommended for CSG), the `assemble` method should return a `manifold3d.Manifold` object.
    - Ensure your CAD class is injectable (using `@inject` and `@singleton`) and inherits from `ManifoldObject` (or `VistaObject` for PyVista points, `OSCObject` for raw OpenSCAD), which provides a `program` method to handle command-line execution.

3.  **Add Main Execution Block**: Add the following boilerplate to the end of your file to make it executable. Make sure to import `sys`, `injector`, and your new class.

    ```python
    if __name__ == "__main__":
        my_part = injector.get(MyPartCAD)
        my_part.program(sys.argv)
    ```

4.  **Update Makefile**: You need to tell `make` how to build your file.
    - For simple cases where `src/cad/foo.py` generates `build/cad/foo.stl`, the existing generic rules might be sufficient.
    - If your script depends on other generated files (e.g., it uses `load_stl("build/cad/dependency.stl")`), you **must** declare this dependency in the `Makefile`:
      ```makefile
      build/cad/my_new_part.stl: src/cad/my_new_part.py build/cad/dependency.stl
      ```
      This ensures `make` builds the dependency first.

5.  **Build the File**: Run `make` with the path to the desired output file in the `build/` directory. For example:

    ```sh
    make build/cad/my_new_part.stl
    ```

The `Makefile` contains generic rules that will find your script (`src/cad/my_new_part.py`), execute it, and save the output file. For STLs, it will also run the simplification script.
