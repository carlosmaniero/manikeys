import pytest
from core.dependencies import DependencyManager, MagicDependencyMap


def test_dependency_manager_resolve_and_usage():
    loaded_batch = []

    def mock_load_many(paths: list[str]) -> list[str]:
        loaded_batch.append(paths)
        return [f"mock_obj_{p}" for p in paths]

    deps = ["file1.stl", "file2.stl"]
    manager: DependencyManager[str] = DependencyManager(
        load_fn=mock_load_many, deps=deps
    )

    assert loaded_batch == [["file1.stl", "file2.stl"]]

    magic_map: MagicDependencyMap[str] = manager.stls
    assert isinstance(magic_map, MagicDependencyMap)

    # Access file1 and file2
    assert magic_map["file1.stl"] == "mock_obj_file1.stl"
    assert magic_map["file2.stl"] == "mock_obj_file2.stl"

    # Verify all used should pass
    manager.verify_all_used()


def test_dependency_manager_unused_dependency_raises_error():
    def mock_load_many(paths: list[str]) -> list[str]:
        return [f"mock_obj_{p}" for p in paths]

    deps = ["file1.stl", "file2.stl"]
    manager: DependencyManager[str] = DependencyManager(
        load_fn=mock_load_many, deps=deps
    )
    magic_map = manager.resolve()

    # Only access file1
    _ = magic_map["file1.stl"]

    with pytest.raises(
        RuntimeError,
        match="The following dependencies passed in --deps were not used: \\['file2.stl'\\]",
    ):
        manager.verify_all_used()


def test_dependency_manager_unprovided_dependency_raises_key_error():
    def mock_load_many(paths: list[str]) -> list[str]:
        return [f"mock_obj_{p}" for p in paths]

    deps = ["file1.stl"]
    manager: DependencyManager[str] = DependencyManager(
        load_fn=mock_load_many, deps=deps
    )
    magic_map = manager.resolve()

    with pytest.raises(KeyError, match="not provided in --stls list"):
        _ = magic_map["file2.stl"]
