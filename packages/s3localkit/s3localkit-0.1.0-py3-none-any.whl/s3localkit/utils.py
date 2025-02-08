import boto3
import os
import shutil
import json
import tempfile
import fnmatch

from pathlib import Path
from typing import Any, Dict, List, Tuple, Union
from botocore.exceptions import ClientError
from contextlib import contextmanager

FILE_TYPE = Union[Path, str]

def _is_s3_path(path: FILE_TYPE) -> bool:
    return str(path).startswith("s3://") or str(path).startswith("s3:/")

def _parse_s3_path(s3_path: FILE_TYPE) -> Tuple[str, str]:
    path = str(s3_path)
    if path.startswith("s3://"):
        path = path.replace("s3://", "")
    elif path.startswith("s3:/"):
        path = path.replace("s3:/", "")
    bucket, key = path.split("/", 1)
    return bucket, key

def upload_file(src: FILE_TYPE, dst: FILE_TYPE) -> None:
    src = Path(src)
    dst = Path(dst)
    if not _is_s3_path(src) and _is_s3_path(dst):
        bucket, key = _parse_s3_path(dst)
        s3 = boto3.client('s3')
        s3.upload_file(str(src), bucket, key)
    else:
        raise ValueError("Source must be a local path and destination must be an S3 path")

def download_file(src: FILE_TYPE, dst: FILE_TYPE) -> None:
    src = Path(src)
    dst = Path(dst)
    if _is_s3_path(src) and not _is_s3_path(dst):
        bucket, key = _parse_s3_path(src)
        s3 = boto3.client('s3')
        s3.download_file(bucket, key, str(dst))
    else:
        raise ValueError("Source must be an S3 path and destination must be a local path")

def file_exists(path: FILE_TYPE) -> bool:
    path = Path(path)
    if _is_s3_path(path):
        bucket, key = _parse_s3_path(path)
        s3 = boto3.client('s3')
        try:
            s3.head_object(Bucket=bucket, Key=key)
            return True
        except ClientError:
            return False
    else:
        return path.exists()

def rename_file(src: FILE_TYPE, dst: FILE_TYPE) -> None:
    copy_file(src, dst)
    remove_file(src)

def move_file(src: FILE_TYPE, dst: FILE_TYPE) -> None:
    copy_file(src, dst)
    remove_file(src)

def copy_file(src: FILE_TYPE, dst: FILE_TYPE) -> None:
    src = Path(src)
    dst = Path(dst)
    if _is_s3_path(src) and _is_s3_path(dst):
        bucket_src, key_src = _parse_s3_path(src)
        bucket_dst, key_dst = _parse_s3_path(dst)
        s3 = boto3.client('s3')
        s3.copy_object(Bucket=bucket_dst, CopySource={'Bucket': bucket_src, 'Key': key_src}, Key=key_dst)
    elif not _is_s3_path(src) and not _is_s3_path(dst):
        shutil.copy(src, dst)
    elif _is_s3_path(src) and not _is_s3_path(dst):
        download_file(src, dst)
    elif not _is_s3_path(src) and _is_s3_path(dst):
        upload_file(src, dst)

def remove_file(path: FILE_TYPE) -> None:
    path = Path(path)
    if _is_s3_path(path):
        bucket, key = _parse_s3_path(path)
        s3 = boto3.client('s3')
        s3.delete_object(Bucket=bucket, Key=key)
    else:
        os.remove(path)

def read_json(path: FILE_TYPE) -> Dict[Any, Any]:
    path = Path(path)
    if _is_s3_path(path):
        bucket, key = _parse_s3_path(path)
        s3 = boto3.client('s3')
        obj = s3.get_object(Bucket=bucket, Key=key)
        data = obj['Body'].read().decode('utf-8')
        return json.loads(data)
    else:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)

def write_json(data: dict, path: FILE_TYPE) -> None:
    path = Path(path)
    if _is_s3_path(path):
        bucket, key = _parse_s3_path(path)
        s3 = boto3.client('s3')
        s3.put_object(Bucket=bucket, Key=key, Body=json.dumps(data).encode('utf-8'))
    else:
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

def listfiles(directory: FILE_TYPE, glob_filter: str = "*") -> List[str]:
    if _is_s3_path(directory):
        bucket, prefix = _parse_s3_path(directory)
        s3 = boto3.client('s3')
        paginator = s3.get_paginator('list_objects_v2')
        files = []
        for page in paginator.paginate(Bucket=bucket, Prefix=prefix):
            for obj in page.get('Contents', []):
                key = obj['Key']
                if fnmatch.fnmatch(key, glob_filter):
                    files.append(f"s3://{bucket}/{key}")
        return files
    else:
        directory = Path(directory)
        return [str(file) for file in directory.rglob(glob_filter)]

def down_maybe(file: FILE_TYPE) -> Path:
    if not _is_s3_path(file):
        return Path(file)
    
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    temp_file.close()
    download_file(file, temp_file.name)
    return Path(temp_file.name)

@contextmanager
def with_down_maybe(file: FILE_TYPE) -> Path:
    if not _is_s3_path(file):
        yield Path(file)
    else:
        temp_file = tempfile.NamedTemporaryFile(delete=False)
        temp_file.close()
        download_file(file, temp_file.name)
        try:
            yield Path(temp_file.name)
        finally:
            os.remove(temp_file.name)
