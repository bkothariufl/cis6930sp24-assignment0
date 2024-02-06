# README

## NAME: Abhishek Kothari
## UFID: 35641285


## Assignment Description:
Extract incident information from the Norman Police Department website. The incident files are to be downloaded, data needs to be extracted, parsed and inserted into a sqllite database. Once the data is available in the database, return all the natures of the incidents along with their respective incident counts. The assignment needs to be developed using python while adhering to industry development standards. A documentation, demo, setup files and collabarator information is to be provided. 

## How to install
On an ubuntu server: 
'sudo apt install zlib1g zlib1g-dev libssl-dev libbz2-dev libsqlite3-dev libncurses5-dev libssl-dev liblzma-dev libffi-dev libreadline-dev'
curl https://pyenv.run | bash
pyenv install 3.11
pyenv global 3.11
pipenv install pypdf 
pipenv install --dev pytest
pipenv install requests pysqlite3 pypdf


## How to run
pipenv run python assignment0/main.py --incidents <url>

## main.py Function Descriptions
### `extract_date_from_url(url: str) -> str`
This function extracts the date from the provided URL. If the date is not found or not in the format of yyyy-mm-dd, it retrieves the name of the file.

### `download_pdf(url: str) -> str`
Downloads a PDF file from the specified URL, saves it to a temporary folder, and returns the path to the downloaded file. If an error occurs during the download, it prints an error message.

### `parse_pdf(filePath: str) -> List[Tuple[str, str, str, str, str]]`
Parses the content of a PDF file specified by the file path and returns a list of tuples containing incident data such as incident time, incident number, incident location, nature, and incident origin.

### `createDb()`
Creates a SQLite database named `normanpd.db` with an 'incidents' table, if it doesn't exist. The table structure includes columns for incident time, incident number, incident location, nature, and incident origin.

### `insertIntoDb(parse_pdf: List[Tuple[str, str, str, str, str]])`
Inserts the parsed incident data into the SQLite database. Expects a list of tuples representing incident details.

### `connectToDb() -> sqlite3.Connection`
Establishes a connection to the SQLite database and returns the connection object.

### `generate_report() -> str`
Generates a report based on the data in the 'incidents' table. The report includes the count of incidents grouped by nature and is ordered by count in descending order.

### `destroyFile(pdf_location: str)`
Deletes the specified file. Used to clean up temporary PDF files after processing.

### `destroy_db()`
Deletes the SQLite database file named `normanpd.db`. Used to reset the database. This function is not called internally. It was used for testing purposes.

### `getSummary(pdf_url: str)`
Downloads a PDF file from the specified URL, parses it, inserts the data into the database, generates a report, prints the report, and deletes the temporary PDF file. If any errors occur during the process, it prints an error message.

### `main()`
The main function responsible for parsing command-line arguments, calling `getSummary()`, and handling user input errors.



## Tests

# README - Tests

This document provides descriptions for the test functions included in the testing suite for the `assignment0` Python script.

### Test Functions

#### `test_extract_date_from_url()`
Verifies the correct extraction of the date from a URL in the format 'yyyy-mm-dd'. 

#### `test_extract_name_from_url()`
Verifies the correct extraction of the file name from a URL.

#### `test_correct_pdf()`
Checks if the PDF file is successfully downloaded from the specified URL.

#### `test_parse_pdf_size()`
Ensures that the size of the parsed data array matches the expected size.

#### `test_db_creation()`
Verifies the creation of the SQLite database file.

#### `test_db_insertion()`
Tests the insertion of parsed data into the SQLite database.

#### `test_db_data()`
Validates the correctness of data stored in the database.

#### `test_destroy_db()`
Checks if the database file is successfully deleted.

#### `test_destroy_temp_file()`
Verifies the deletion of a temporary PDF file.

### Additional Notes
- Some tests are commented out in the `main` function at the end of the script. They can be uncommented and run as needed. 

