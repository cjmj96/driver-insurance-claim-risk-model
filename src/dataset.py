from data_understanding import data_collection


def main():
    # Specify raw data paths
    train_raw_data_path = "data/raw/train.csv"
    test_raw_data_path = "data/raw/test.csv"

    # Specify converted data paths
    train_parquet_data_path = "data/interim/train.parquet"
    test_parquet_data_path = "data/interim/test.parquet"

    # Convert raw data to parquet format
    data_collection.convert_data(train_raw_data_path, train_parquet_data_path)
    data_collection.convert_data(test_raw_data_path, test_parquet_data_path)


if __name__ == "__main__":
    main()
