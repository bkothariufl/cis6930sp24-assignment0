import os
import re
import requests
from pypdf import PdfReader
import sqlite3

## Fetch the file and put into the tempFiles directory

## Extract data from the file and put it into lists 

## Create a sqlLite database

def extract_date_from_url(url):
    # Assuming the date is in the format YYYY-MM-DD in the URL
    match = re.search(r'(\d{4}-\d{2}-\d{2})', url)
    if match:
        return match.group(1)
    else:
        return None

def download_pdf(url, destination_folder):
    response = requests.get(url)
    if response.status_code == 200:
        date=f"{extract_date_from_url(url)}"
        filename = date+".pdf"
        # Ensure the destination folder exists
        os.makedirs(destination_folder, exist_ok=True)
        
        # Construct the full file path
        dest_path = os.path.join(destination_folder, filename)

        with open(dest_path, 'wb') as pdf_file:
            pdf_file.write(response.content)
        # print(f"PDF downloaded successfully to {dest_path}")
        return dest_path
        
        
    else:
        print(f"Failed to download PDF. Status code: {response.status_code}")

def parse_pdf(filePath):
    # Initialize a list to store extracted information
    parsed_data = []
    global pdf_data
    pdf_data=""
    
    reader = PdfReader(filePath)
    for page_num in range(len(reader.pages)):
        page = reader.pages[page_num]
        temp_data=page.extract_text(extraction_mode="layout")
        pdf_data+=temp_data+"\n"

    # Split the PDF data into lines and process each line
    lines = pdf_data.split('\n')
    parent_array = []  # Create an empty parent array
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
    con = sqlite3.connect("resources/normanpd.db")
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
    con.commit()  # Commit the changes to the database
    con.close()  # Close the database connection
    
def insertIntoDb(parse_pdf):
    conn = sqlite3.connect("resources/normanpd.db")
    c = conn.cursor()

    for row in parse_pdf:
        # Insert each row into the incidents table
        c.execute("INSERT INTO incidents VALUES (?, ?, ?, ?, ?)", row)

    conn.commit()  # Commit the changes to the database
    conn.close()  # Close the database connection

def generate_report():
    # Connect to the SQLite database
    connection = sqlite3.connect("resources/normanpd.db")
    cursor = connection.cursor()

    # Execute the query to get the count of each nature of incidents
    query = """
        SELECT nature, COUNT(*) as count
        FROM incidents
        GROUP BY nature
        ORDER BY count DESC, nature
    """
    cursor.execute(query)
    results = cursor.fetchall()

    # Generate the report
    report = ""
    for row in results:
        nature, count = row
        report += f"{nature}|{count}\n"

    # Close the database connection
    connection.close()

    return report

def destroyFile(pdf_location):
   
    temp_files_path = pdf_location
    # print(pdf_location)

    if os.path.exists(temp_files_path):
        os.remove(temp_files_path)
        # print("temp_files_path file deleted successfully.")
    else:
        print("temp_files_path file not found.")



def destroyDatabase():

    db_file_path = "resources/normanpd.db"

    if os.path.exists(db_file_path):
        os.remove(db_file_path)
        # print("Database file deleted successfully.")
    else:
        print("Database file not found.")



destination_folder = 'assignment0/tempFiles'
pdf_url='https://www.normanok.gov/sites/default/files/documents/2023-12/2023-12-02_daily_incident_summary.pdf'
pdf_location=download_pdf(pdf_url, destination_folder)
parsed_data=parse_pdf(pdf_location)
createDb()
insertIntoDb(parsed_data)
report=generate_report()
print(report)
# destroyFile(pdf_location)
destroyDatabase()
