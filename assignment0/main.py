import argparse
import os
import re
import requests
from pypdf import PdfReader
import sqlite3


def extract_date_from_url(url):
    match = re.search(r'(\d{4}-\d{2}-\d{2})', url)
    if match:
        return match.group(1)
    else:
        return None

def download_pdf(url):
    response = requests.get(url)
    if response.status_code == 200:
        date = extract_date_from_url(url)
        filename = f"{date}.pdf"
        destination_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tempFiles')
        os.makedirs(destination_folder, exist_ok=True)
        dest_path = os.path.join(destination_folder, filename)

        with open(dest_path, 'wb') as pdf_file:
            pdf_file.write(response.content)
        # print(f"PDF downloaded successfully to {dest_path}")
        return dest_path
        
    else:
        print(f"Failed to download PDF. Status code: {response.status_code}")


def parse_pdf(filePath):
    parsed_data = []
    global pdf_data
    pdf_data=""
    filePath = os.path.abspath(filePath)
    reader = PdfReader(filePath)
    for page_num in range(len(reader.pages)):
        page = reader.pages[page_num]
        temp_data=page.extract_text(extraction_mode="layout")
        pdf_data+=temp_data+"\n"

    lines = pdf_data.split('\n')
    parent_array = [] 
    for line in lines:
        data_array = [e.strip() for e in re.split(r"\s{4,}", line.strip())]
        # print(data_array)
        if len(data_array)<5:
            continue
        else:
            if data_array[0] and data_array[0][0].isdigit():
                parent_array.append(tuple(data_array))
    return parent_array

def createDb():
    resources_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "resources")
    if not os.path.exists(resources_folder):
        os.makedirs(resources_folder)
        # print(f"Created 'resources' folder: {resources_folder}")

    db_path = os.path.abspath(os.path.join("resources", "normanpd.db"))
    if os.path.exists(db_path):
        os.remove(db_path)
        # print(f"Existing database file removed: {db_path}")
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    cur.execute("""
        CREATE TABLE incidents (
            incident_time TEXT,
            incident_number TEXT,
            incident_location TEXT,
            nature TEXT,
            incident_ori TEXT
        )
    """)
    con.commit()  
    con.close() 
    
def insertIntoDb(parse_pdf):
    db_path = os.path.abspath(os.path.join("resources", "normanpd.db"))

    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    for row in parse_pdf:
        
        c.execute("INSERT INTO incidents VALUES (?, ?, ?, ?, ?)", row)

    conn.commit() 
    conn.close()  

def connectToDb():
    db_path = os.path.abspath(os.path.join("resources", "normanpd.db"))

    conn = sqlite3.connect(db_path)
    return conn


def generate_report():

    connection = sqlite3.connect("resources/normanpd.db")
    cursor = connection.cursor()

    query = """
        SELECT nature, COUNT(*) as count
        FROM incidents
        GROUP BY nature
        ORDER BY count DESC, nature
    """
    cursor.execute(query)
    results = cursor.fetchall()
    
    report = ""
    for row in results:
        nature, count = row
        report += f"{nature}|{count}\n"
    connection.close()

    return report

def destroyFile(pdf_location):
   
    temp_files_path = pdf_location

    if os.path.exists(temp_files_path):
        os.remove(temp_files_path)
    else:
        print("temp_files_path file not found.")



def destroy_db():

    db_file_path = "resources/normanpd.db"

    if os.path.exists(db_file_path):
        os.remove(db_file_path)
    else:
        print("Database file not found.")





def getSummary(pdf_url):
    destination_folder = 'assignment0/tempFiles'
    # pdf_url='https://www.normanok.gov/sites/default/files/documents/2023-12/2023-12-04_daily_incident_summary.pdf'
    try:
        pdf_location = download_pdf(pdf_url)
        if not pdf_location:
            return

        parsed_data = parse_pdf(pdf_location)
        print("parsed_data len ", len(parsed_data))
        if not parsed_data:
            print("Error parsing PDF. Exiting.")
            return
        createDb()
        insertIntoDb(parsed_data)
        report = generate_report()
        print(report)
        destroyFile(pdf_location)
        destroy_db()

    except Exception as e:
        print(f"An error occurred: {e}. Exiting.")
        return

def main():
    parser = argparse.ArgumentParser(description='Generate a summary based on a PDF URL.')
    parser.add_argument('--incidents', type=str, help='URL of the PDF containing incidents data')

    args = parser.parse_args()

    if not args.incidents:
        print("Please provide the --incidents option with a PDF URL.")
        return
    
    pdf_url = args.incidents
    # pdf_url='https://www.normanok.gov/sites/default/files/documents/2023-12/2023-12-04_daily_incident_summary.pdf'
    
    getSummary(pdf_url)

if __name__ == '__main__':
    main()