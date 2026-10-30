import pytest
from src.shopflow.extract import data_extraction

def test_data_extraction_returns_valid_list_of_dictionaries():
    assert data_extraction("data/raw/custom.csv") == [{"customer_id":"1","full_name" : "Tshireletso Seodigeng","email":"tshireseodigeng@gmail.com","created_at":"12/10/2026 14:00:00"},
                                        {"customer_id":"2","full_name" : "Sipho Dlamini","email":"siphodlamini@gmail.com","created_at":"2026-09-03 11:30:00"},
                                        {"customer_id":"3","full_name" : "Lerato Nkosi","email":"leratonkosi@gmail.com","created_at":"2026-09-05 14:20:00"}
    ]

def test_data_extraction_file_nonexsistent():
    assert data_extraction("data/raw/tshire.csv") == "This csv file does not exist"

def test_data_extraction_empty_columns(): 
    #test should add NONE values to empty columns within a row
    assert data_extraction("data/raw/orderss.csv") ==  [{'customer_id': '1', 'order_date': '2026-10-01', 'order_id': '1001', 'status': 'completed'},
                                                         {'customer_id': '2', 'order_date': '2026-10-02', 'order_id': '1002', 'status': None}]
def test_data_extraction_empty_file():
    assert data_extraction("data/raw/empty_file.csv")   == "This csv file is empty"

def test_data_extraction_empty_rows():
    #test: empty rows should be skipped and cause no errors
    assert data_extraction("data/raw/custom.csv") ==      [{'customer_id': '1', 'full_name': 'Tshireletso Seodigeng', 'email': 'tshireseodigeng@gmail.com', 'created_at': '12/10/2026 14:00:00'}, 
                                                         {'customer_id': '2', 'full_name': 'Sipho Dlamini', 'email': 'siphodlamini@gmail.com', 'created_at': '2026-09-03 11:30:00'}, 
                                                         {'customer_id': '3', 'full_name': 'Lerato Nkosi', 'email': 'leratonkosi@gmail.com', 'created_at': '2026-09-05 14:20:00'}]
    assert len(data_extraction("data/raw/custom.csv")) == 3
    assert all(None not in row for row in data_extraction("data/raw/custom.csv"))
                                               