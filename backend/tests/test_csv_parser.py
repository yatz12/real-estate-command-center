import pytest
from fastapi import HTTPException
from app.services.csv_parser import parse_instagram_csv
import os

def test_parse_valid_csv():
    # Path to the valid.csv created previously
    path = "tests/data/valid.csv"
    # We need to be in the backend dir for this path to work if running from there
    # but we'll use absolute path or assume test runs from /backend
    data = parse_instagram_csv(path)
    assert len(data) == 3
    assert data[0]['post_type'] == "REEL"
    assert data[1]['reach'] == 8500

def test_parse_missing_columns():
    path = "tests/data/missing_cols.csv"
    with pytest.raises(HTTPException) as exc:
        parse_instagram_csv(path)
    assert exc.value.status_code == 400
    assert "Missing required columns" in exc.value.detail

def test_parse_negative_metrics():
    path = "tests/data/negative_metrics.csv"
    with pytest.raises(HTTPException) as exc:
        parse_instagram_csv(path)
    assert exc.value.status_code == 400
    assert "contains negative values" in exc.value.detail

def test_parse_empty_csv():
    path = "tests/data/empty.csv"
    with pytest.raises(HTTPException) as exc:
        parse_instagram_csv(path)
    assert exc.value.status_code == 400
    assert "CSV file is empty" in exc.value.detail
