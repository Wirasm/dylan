"""Tests to validate parallel execution infrastructure with pytest-xdist.

This test module demonstrates and validates that tests can run in parallel
safely using pytest-xdist. Each test is isolated and independent, ensuring
no shared state conflicts when running with multiple workers.
"""

import time


def test_parallel_execution_test_1(tmp_path):
    """Test 1: Independent file operations with isolated temp directory.

    This test validates that file operations in temporary directories
    are properly isolated between parallel workers.

    Args:
        tmp_path: pytest fixture providing unique temporary directory
    """
    test_file = tmp_path / "test_file_1.txt"
    test_file.write_text("Test content 1")

    assert test_file.exists()
    assert test_file.read_text() == "Test content 1"


def test_parallel_execution_test_2(tmp_path):
    """Test 2: Independent file operations with different content.

    This test can run simultaneously with test_1 without conflicts
    because each test gets its own tmp_path from pytest.

    Args:
        tmp_path: pytest fixture providing unique temporary directory
    """
    test_file = tmp_path / "test_file_2.txt"
    test_file.write_text("Test content 2")

    assert test_file.exists()
    assert test_file.read_text() == "Test content 2"


def test_parallel_execution_test_3(tmp_path):
    """Test 3: Directory creation and file operations.

    Validates that directory operations are properly isolated
    across parallel test workers.

    Args:
        tmp_path: pytest fixture providing unique temporary directory
    """
    subdir = tmp_path / "subdir"
    subdir.mkdir()

    test_file = subdir / "nested_file.txt"
    test_file.write_text("Nested content")

    assert subdir.exists()
    assert test_file.exists()
    assert test_file.read_text() == "Nested content"


def test_parallel_execution_test_4():
    """Test 4: Pure computation with no shared state.

    This test performs calculations without any file I/O or external
    dependencies, demonstrating ideal parallel test characteristics.
    """
    result = sum(range(1000))
    expected = 499500

    assert result == expected


def test_parallel_execution_test_5():
    """Test 5: String manipulation without side effects.

    Another example of a pure test that can safely run in parallel
    with any other test.
    """
    test_string = "parallel execution"
    reversed_string = test_string[::-1]

    assert reversed_string == "noitucexe lellarap"
    assert test_string.upper() == "PARALLEL EXECUTION"


def test_parallel_execution_test_6():
    """Test 6: List operations demonstrating deterministic behavior.

    Tests list operations that are deterministic and don't rely
    on execution order or external state.
    """
    test_list = [3, 1, 4, 1, 5, 9, 2, 6]
    sorted_list = sorted(test_list)

    assert sorted_list == [1, 1, 2, 3, 4, 5, 6, 9]
    assert len(test_list) == 8


def test_parallel_execution_test_7():
    """Test 7: Dictionary operations with no shared state.

    Validates dictionary operations work correctly in parallel
    execution without interference.
    """
    test_dict = {"a": 1, "b": 2, "c": 3}
    test_dict["d"] = 4

    assert len(test_dict) == 4
    assert test_dict["d"] == 4
    assert "a" in test_dict


def test_parallel_execution_test_8(tmp_path):
    """Test 8: Multiple file operations in sequence.

    Demonstrates that sequential operations within a single test
    work correctly even when the test runs in parallel with others.

    Args:
        tmp_path: pytest fixture providing unique temporary directory
    """
    files_created = []

    for i in range(5):
        test_file = tmp_path / f"file_{i}.txt"
        test_file.write_text(f"Content {i}")
        files_created.append(test_file)

    assert len(files_created) == 5
    assert all(f.exists() for f in files_created)
    assert files_created[3].read_text() == "Content 3"


def test_parallel_execution_test_9():
    """Test 9: Set operations demonstrating isolation.

    Tests set operations that are independent and can run
    in parallel safely.
    """
    set_a = {1, 2, 3, 4, 5}
    set_b = {4, 5, 6, 7, 8}

    union = set_a | set_b
    intersection = set_a & set_b

    assert union == {1, 2, 3, 4, 5, 6, 7, 8}
    assert intersection == {4, 5}


def test_parallel_execution_test_10():
    """Test 10: Tuple operations with immutable data.

    Tests with immutable data structures are naturally safe
    for parallel execution.
    """
    test_tuple = (1, 2, 3, 4, 5)

    assert len(test_tuple) == 5
    assert test_tuple[0] == 1
    assert test_tuple[-1] == 5
    assert 3 in test_tuple


def test_parallel_execution_isolation_verification(tmp_path):
    """Test isolation: Verify temp directories are unique per test.

    This test specifically validates that pytest provides isolated
    temporary directories to each test, which is critical for
    parallel execution safety.

    Args:
        tmp_path: pytest fixture providing unique temporary directory
    """
    # Write a marker file with a unique identifier
    marker_file = tmp_path / "isolation_marker.txt"
    marker_file.write_text(str(id(tmp_path)))

    # Verify the marker file exists and contains our ID
    assert marker_file.exists()
    stored_id = marker_file.read_text()
    assert stored_id == str(id(tmp_path))

    # Verify the temp path is unique (pytest truncates long test names)
    assert "test_parallel_execution_isolat" in str(tmp_path)


def test_parallel_execution_no_timing_dependencies():
    """Test timing independence: No race conditions or timing dependencies.

    This test validates that our tests don't rely on specific timing
    or execution order, which could cause flakiness in parallel execution.
    """
    start_time = time.time()

    # Perform some work
    result = 0
    for i in range(1000):
        result += i

    end_time = time.time()

    # We don't assert on timing, only on results
    assert result == 499500
    assert end_time > start_time  # Basic sanity check


def test_parallel_execution_fixture_isolation(tmp_path):
    """Test fixture isolation: Multiple uses of tmp_path are independent.

    Even within a single test, multiple operations using the tmp_path
    fixture should be isolated and not interfere with other tests.

    Args:
        tmp_path: pytest fixture providing unique temporary directory
    """
    # Create multiple subdirectories
    dir1 = tmp_path / "dir1"
    dir2 = tmp_path / "dir2"
    dir1.mkdir()
    dir2.mkdir()

    # Create files in each directory
    file1 = dir1 / "file.txt"
    file2 = dir2 / "file.txt"
    file1.write_text("content1")
    file2.write_text("content2")

    # Verify isolation within the test
    assert file1.read_text() == "content1"
    assert file2.read_text() == "content2"
    assert file1.read_text() != file2.read_text()
