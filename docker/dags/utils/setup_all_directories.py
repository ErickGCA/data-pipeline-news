import os

def setup_all_directories(base_dir=None):
    if base_dir is None:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    data_dir = os.path.join(base_dir, "data")
    raw_data_dir = os.path.join(data_dir, "raw")
    processed_data_dir = os.path.join(data_dir, "processed")
    mock_data_dir = os.path.join(data_dir, "mock_data")

    os.makedirs(data_dir, exist_ok=True)
    os.makedirs(raw_data_dir, exist_ok=True)
    os.makedirs(processed_data_dir, exist_ok=True)
    os.makedirs(mock_data_dir, exist_ok=True)

    return {
        "base_dir": base_dir,
        "data_dir": data_dir,
        "raw_data_dir": raw_data_dir,
        "processed_data_dir": processed_data_dir,
        "mock_data_dir": mock_data_dir,
    }
