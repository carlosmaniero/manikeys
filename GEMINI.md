# Project Guidelines

- **Dataclasses**: Prefer using `@dataclass` for data-holding classes to reduce boilerplate (like `__init__` and `__repr__`).
- **Factory Methods**: When complex initialization is required, prefer using `@classmethod` factory methods (e.g., `from_x`) to keep the primary constructor simple and the class's purpose clear.

# Operational Requirements

Before performing any change in the code:
1.  **Sync**: Read the file again to ensure you have the latest version, as it may have been edited manually.

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

2.  **CSG with `openscad`**: Other models are built using Constructive Solid Geometry (CSG) principles via the `openscad` Python library. These scripts define shapes and combine them with boolean operations (union, difference, intersection). `src/full_keyboard.py` is a good example, as it assembles the final keyboard.

    A key feature of this approach is the ability to import existing models using `load_stl("path/to/model.stl")`. This returns an `openscad` object that can be manipulated, allowing for a hybrid workflow where generated and pre-existing parts can be combined.

All generated STL files are post-processed with `simplify.py` to reduce complexity and file size.

## Creating a New CAD File

To create a new CAD file (e.g., an STL):

1.  **Create a Python Script**: Create a new Python file under the `src/` directory (e.g., `src/cad/my_new_part.py`).

2.  **Implement the Model Class**: Inside the new file, define a class that generates your 3D object.
    - For `pyvista`-based models, the `assemble` method should return a `pyvista.PolyData` object.
    - For `openscad`-based models, the `assemble` method should return an `openscad.PyOpenSCAD` object.
    - Ensure your class is injectable (using `@inject` and `@singleton`) and inherits from `VistaObject` or `OSCObject` which provide a `program` method to handle command-line execution.

3.  **Add Main Execution Block**: Add the following boilerplate to the end of your file to make it executable. Make sure to import `sys`, `injector`, and your new class.

    ```python
    if __name__ == "__main__":
        my_part = injector.get(MyPartCAD) # Replace MyPartCAD with your class name
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
