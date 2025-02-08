import boto3
import os
import json
import tempfile
import pytest

from pathlib import Path

try:
    from moto import mock_aws
except:
    from moto import mock_s3 as mock_aws

from s3localkit.utils import (
    copy_file,
    remove_file,
    read_json,
    file_exists,
    upload_file,
    download_file,
    listfiles
)

@pytest.fixture
def s3_setup():
    with mock_aws():
        s3 = boto3.client('s3', region_name='us-east-1')
        s3.create_bucket(Bucket='my-test-bucket')
        yield s3

def test_copy_file_local2local():
    with tempfile.NamedTemporaryFile(delete=False) as src_file:
        src_file.write(b"Test content")
        src_file_path = src_file.name

    with tempfile.NamedTemporaryFile(delete=False) as dst_file:
        dst_file_path = dst_file.name

    try:
        copy_file(src_file_path, dst_file_path)
        assert os.path.exists(dst_file_path)
        with open(dst_file_path, 'rb') as f:
            content = f.read()
        assert content == b"Test content"
    finally:
        os.remove(src_file_path)
        os.remove(dst_file_path)

def test_remove_file_local():
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file_path = temp_file.name

    assert os.path.exists(temp_file_path)
    remove_file(temp_file_path)
    assert not os.path.exists(temp_file_path)

def test_read_json_local():
    data = {"key": "value"}
    with tempfile.NamedTemporaryFile(delete=False, mode='w', encoding='utf-8') as temp_file:
        json.dump(data, temp_file)
        temp_file_path = temp_file.name

    try:
        result = read_json(temp_file_path)
        assert result == data
    finally:
        os.remove(temp_file_path)

def test_file_exists_local():
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file_path = temp_file.name

    try:
        assert file_exists(temp_file_path)
        os.remove(temp_file_path)
        assert not file_exists(temp_file_path)
    finally:
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)

def test_listfiles_local():
    with tempfile.TemporaryDirectory() as temp_dir:
        file1 = Path(temp_dir) / "file1.txt"
        file2 = Path(temp_dir) / "file2.log"
        file1.write_text("Content of file1")
        file2.write_text("Content of file2")

        # Create a subdirectory with another file
        sub_dir = Path(temp_dir) / "subdir"
        sub_dir.mkdir()
        file3 = sub_dir / "file3.txt"
        file3.write_text("Content of file3")

        # Test listfiles without glob filter
        all_files = listfiles(temp_dir)
        expected_files = {str(file1), str(file2), str(file3), str(sub_dir)}
        assert set(all_files) == expected_files

        # Test listfiles with glob filter
        txt_files = listfiles(temp_dir, "*.txt")
        expected_txt_files = {str(file1), str(file3)}
        assert set(txt_files) == expected_txt_files

def test_upload_file(s3_setup, tmp_path):
    local_file = tmp_path / "test.txt"
    local_file.write_text("Hello, world!")
    upload_file(str(local_file), "s3://my-test-bucket/test.txt")
    response = s3_setup.list_objects_v2(Bucket='my-test-bucket')
    assert 'Contents' in response
    assert any(obj['Key'] == 'test.txt' for obj in response['Contents'])

def test_download_file(s3_setup, tmp_path):
    s3_setup.put_object(Bucket='my-test-bucket', Key='test.txt', Body='Hello, world!')
    local_file = tmp_path / "downloaded_test.txt"
    download_file("s3://my-test-bucket/test.txt", str(local_file))
    assert local_file.read_text() == "Hello, world!"

def test_file_exists_s3(s3_setup):
    s3_setup.put_object(Bucket='my-test-bucket', Key='test.txt', Body='Hello, world!')
    assert file_exists("s3://my-test-bucket/test.txt") is True
    assert file_exists("s3://my-test-bucket/non_existent.txt") is False

def test_listfiles_s3(s3_setup):
    s3_setup.put_object(Bucket='my-test-bucket', Key='file1.txt', Body='Content of file1')
    s3_setup.put_object(Bucket='my-test-bucket', Key='file2.log', Body='Content of file2')
    s3_setup.put_object(Bucket='my-test-bucket', Key='subdir/file3.txt', Body='Content of file3')

    all_files = listfiles("s3://my-test-bucket/")
    assert set(all_files) == {
        "s3://my-test-bucket/file1.txt",
        "s3://my-test-bucket/file2.log",
        "s3://my-test-bucket/subdir/file3.txt"
    }

    txt_files = listfiles("s3://my-test-bucket/", "*.txt")
    assert set(txt_files) == {
        "s3://my-test-bucket/file1.txt",
        "s3://my-test-bucket/subdir/file3.txt"
    }


if __name__ == "__main__":
    pytest.main()