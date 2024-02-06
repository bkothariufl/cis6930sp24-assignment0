import os
import pytest
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from assignment0.main import extract_date_from_url, download_pdf,createDb,parse_pdf,insertIntoDb,destroy_db,destroyFile,connectToDb,generate_report,getSummary


test_pdf_url='https://www.normanok.gov/sites/default/files/documents/2023-12/2023-12-04_daily_incident_summary.pdf'


def test_extract_date_from_url():
    url = 'https://www.example.com/2023-12-01_daily_incident_summary.pdf'
    extracted_date = extract_date_from_url(url)
    assert extracted_date == '2023-12-01'

def test_extract_name_from_url():
    url = 'https://www.example.com/test0.pdf'
    extracted_name = extract_date_from_url(url)
    assert extracted_name == 'test0'

def test_correct_pdf():
    pdf_location = download_pdf(test_pdf_url)
    assert os.path.exists(pdf_location), f"PDF file does not exist at {pdf_location}"

def test_parse_pdf_size():
    test_pdf_path = 'testPdfs/2023-12-04.pdf'
    test_dir = os.path.dirname(os.path.abspath(__file__))
    full_pdf_path = os.path.join(test_dir, test_pdf_path)
    parsed_data = parse_pdf(full_pdf_path)
    expected_size = 413  

    assert len(parsed_data) == expected_size, f"Unexpected size of parent array: {len(parsed_data)}"


def test_db_creation():
    temp_db_path = os.path.join('resources', 'normanpd.db')
    createDb()
    assert os.path.exists(temp_db_path), f"Database file does not exist at {temp_db_path}"


def test_db_insertion():
    test_pdf_path = 'testPdfs/2023-12-04.pdf'
    test_dir = os.path.dirname(os.path.abspath(__file__))
    full_pdf_path = os.path.join(test_dir, test_pdf_path)
    parsed_data = parse_pdf(full_pdf_path)
    insertIntoDb(parsed_data)

def test_db_data():
    conn = connectToDb()
    cursor = conn.cursor()
    query = """SELECT
    (SELECT COUNT(*) FROM incidents WHERE nature = 'Breathing Problems') as breathing_problems,
    (SELECT COUNT(*) FROM incidents WHERE nature = 'Falls') as falls,
    (SELECT COUNT(*) FROM incidents WHERE nature = 'Check Area') as check_area,
    (SELECT COUNT(*) FROM incidents WHERE nature = 'Fraud') as fraud;"""
    cursor.execute(query)
    results = cursor.fetchall()
    correct_results=[(12,11,7,6)]
    assert results == correct_results, f"Test failed! Expected: {correct_results}, Actual: {results}"
    conn.close()


def test_destroy_db():
    temp_db_path = os.path.join('resources', 'normanpd.db')
    destroy_db()
    assert not os.path.exists(temp_db_path), f"Database file still exists at {temp_db_path}"

def test_destroy_temp_file():
    temp_files_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../assignment0/tempFiles')
    temp_pdf_path = os.path.join(temp_files_folder, '2023-12-04.pdf')
    destroyFile(temp_pdf_path)
    assert not os.path.exists(temp_pdf_path), f"Temp pdf file still exists at {temp_pdf_path}"

# def test_parsed_data():
#     test_pdf_path = 'testPdfs/blank_nature.pdf'
#     test_dir = os.path.dirname(os.path.abspath(__file__))
#     full_pdf_path = os.path.join(test_dir, test_pdf_path)
#     parsed_data = parse_pdf(full_pdf_path)
#     # temp_db_path = os.path.join('resources', 'normanpd.db')
#     createDb()
#     insertIntoDb(parsed_data)
#     report = generate_report()
#     # print(report)

# def testSummary():
#     getSummary("https://www.normanok.gov/sites/default/files/documents/2024-01/2024-01-04_daily_incident_summary.pdf")
# def main():
#     # test_extract_date_from_url()
#     # test_extract_name_from_url()
#     # test_correct_pdf()
#     # test_destroy_temp_file()
#     # test_parse_pdf_size()
    # test_db_creation()
#     # test_db_insertion()
#     # test_db_data()
#     # test_destroy_db()
#     # test_parsed_data()
#     # test_parsed_data()


# if __name__ == '__main__':
#     main()