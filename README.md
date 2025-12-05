# Dental Clinic Website Scraper Project

## Project Features
This scraper can automatically extract the following information from dental clinic websites:
- **Clinic Name**
- **Email Addresses**
- **Phone Numbers**
- **Owner/Doctor Names**

## File Structure
```
crystalsmile/
├── scraper/
│   └── crawler.py           # Main scraper program
├── data/
│   ├── Dentist-website-list.txt   # Input: Website URL list
│   └── ct_dentist_leads.csv       # Output: Extracted information
└── README.md
```

## Usage

### 1. Install Dependencies
```cmd
pip install playwright beautifulsoup4 pandas
playwright install chromium
```

### 2. Prepare URL List
Ensure `data/Dentist-website-list.txt` file exists with one website URL per line.
Example:
```
http://www.example-dental.com/
https://www.another-dentist.com/
```

### 3. Run Scraper
```cmd
cd scraper
python crawler.py
```

### 4. View Results
After completion, results will be saved in `data/ct_dentist_leads.csv` file.

## Output Format
CSV file contains the following columns:
- `url`: Website URL
- `clinic_name`: Clinic name
- `emails`: Email addresses (multiple emails separated by ;)
- `phones`: Phone numbers (multiple numbers separated by ;)
- `owner_names`: Doctor/Owner names (multiple names separated by ;)

## Technical Features

### 1. Clinic Name Extraction
- Priority extraction from `<title>` tag
- If empty, extract from `<h1>` tag
- Finally infer from URL domain
- Auto-clean suffixes like "Home", "Dentist"

### 2. Email Extraction
- Use regex to match standard email format
- Filter out invalid emails like example, test, placeholder
- Keep maximum of 5 email addresses

### 3. Phone Extraction
- Support multiple US phone formats:
  - (203) 555-1234
  - 203-555-1234
  - 203.555.1234
- Validate phone numbers are 10 digits
- Auto-deduplicate

### 4. Doctor Name Extraction
- Recognize "Dr. FirstName LastName" format
- Recognize "FirstName LastName, DDS/DMD" format
- Filter out irrelevant words (copyright, appointment, etc.)
- Keep maximum of 5 names

## Performance Optimization
- Use async concurrent processing for significant speed improvement
- Limit concurrency to 5 to avoid IP blocking
- Headless browser mode to save resources
- 15-second timeout to avoid long waits

## Important Notes
1. First run requires downloading Playwright browser (~100MB)
2. Recommended to run in stable network environment
3. Scraper outputs detailed processing logs for progress tracking
4. Some websites may fail due to anti-scraping mechanisms, which is normal

## Program Logic Verification

### ✅ Path Handling
- Use `os.path` module for relative paths, ensuring cross-platform compatibility
- `script_dir` gets current script directory
- `os.path.join()` correctly concatenates paths

### ✅ File Reading
- Read `Dentist-website-list.txt` with UTF-8 encoding
- Auto-remove empty lines and whitespace
- Print number of loaded URLs

### ✅ Regular Expressions
- Email: `\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b`
- Phone: Multiple format pattern arrays
- Doctor names: 3 patterns matching different formats

### ✅ Async Processing
- Use `async/await` syntax
- `Semaphore(5)` limits concurrency
- `asyncio.gather()` executes all tasks in parallel

### ✅ Error Handling
- `try-except` catches all exceptions
- Single website failure doesn't affect others
- Detailed error log output

### ✅ Data Saving
- Convert lists to strings (separated by ;)
- UTF-8-SIG encoding, Excel compatible
- Auto-save to `data` directory
- Print detailed statistics

## Sample Statistics Output
```
====================================================================
🎉 Scraping completed! Data saved to ../data/ct_dentist_leads.csv
====================================================================
📊 Total URLs processed: 924
📧 Clinics with emails found: 782
📞 Clinics with phones found: 856
👨‍⚕️ Clinics with doctor names found: 654
====================================================================
```

## Troubleshooting
1. **ModuleNotFoundError**: Run `pip install` to install dependencies
2. **Playwright not installed**: Run `playwright install chromium`
3. **File path error**: Ensure running program in `scraper` directory
4. **Website access timeout**: Some websites may be slow or protected, this is normal
