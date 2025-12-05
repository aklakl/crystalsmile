import asyncio
import re
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import pandas as pd
import os
from urllib.parse import urlparse
from datetime import datetime
import logging

# 1. Read each line from Dentist-website-list.txt as URLs
script_dir = os.path.dirname(os.path.abspath(__file__))
data_file = os.path.join(script_dir, '..', 'data', 'Dentist-website-list.txt')

with open(data_file, 'r', encoding='utf-8') as f:
    urls = [line.strip() for line in f if line.strip()]

# Create timestamped folder for this run
timestamp = datetime.now().strftime('%Y-%m-%d %H-%M-%S')
run_folder = os.path.join(script_dir, '..', 'data', f'run_{timestamp}')
os.makedirs(run_folder, exist_ok=True)

# Setup logging
log_file = os.path.join(run_folder, f'scraper_{timestamp}.log')
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file, encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

logger.info(f"📋 Loaded {len(urls)} URLs from Dentist-website-list.txt")
logger.info(f"📁 Run folder: {run_folder}")
print(f"📋 Loaded {len(urls)} URLs from Dentist-website-list.txt\n")

async def extract_info(page, url):
    """
    Extract information from dental clinic websites:
    - clinic_name: Clinic name
    - emails: Email address list
    - phones: Phone number list
    - owner_names: Clinic owner/doctor name list
    """
    data = {
        "url": url,
        "clinic_name": "",
        "emails": [],
        "phones": [],
        "owner_names": []
    }
    
    try:
        # Visit website with 15-second timeout
        await page.goto(url, timeout=15000, wait_until='domcontentloaded')
        await page.wait_for_timeout(2000)  # Wait 2 seconds for page to load
        content = await page.content()
        soup = BeautifulSoup(content, 'html.parser')
        text_content = soup.get_text(separator=' ', strip=True)

        # --- A. Extract Clinic Name ---
        clinic_name = ""
        
        # Priority: extract from title tag
        if soup.title and soup.title.string:
            clinic_name = soup.title.string.strip()
            # Clean common suffixes (like "| Home", "- Dentist", etc.)
            clinic_name = re.sub(r'\s*[\|\-]\s*(Home|Dentist|Dental|CT|Connecticut).*$', '', clinic_name, flags=re.IGNORECASE)
        
        # If title is empty, try h1 tag
        if not clinic_name:
            h1 = soup.find('h1')
            if h1:
                clinic_name = h1.get_text(strip=True)
        
        # If still empty, infer from URL
        if not clinic_name:
            domain = urlparse(url).netloc
            clinic_name = domain.replace('www.', '').replace('.com', '').replace('.net', '').replace('-', ' ').title()
        
        data["clinic_name"] = clinic_name

        # --- B. Extract Email ---
        email_pattern = r'\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b'
        emails = set(re.findall(email_pattern, content, re.IGNORECASE))
        
        # Filter out common invalid emails
        filtered_emails = [
            e for e in emails 
            if not any(x in e.lower() for x in ['example', 'test', 'domain', 'email', 'wix', 'placeholder', 'sampleemail'])
        ]
        data["emails"] = filtered_emails[:5]  # Keep maximum of 5

        # --- C. Extract Phone Numbers ---
        # Match US phone formats
        phone_patterns = [
            r'\(?\d{3}\)?[-. \s]?\d{3}[-. \s]?\d{4}',  # (203) 555-1234 or 203-555-1234
            r'\d{3}[-. \s]\d{3}[-. \s]\d{4}',          # 203.555.1234
            r'\(\d{3}\)\s?\d{3}-\d{4}'                # (203)555-1234
        ]
        
        phones = set()
        for pattern in phone_patterns:
            found = re.findall(pattern, text_content)
            phones.update(found)
        
        # Clean and standardize phone numbers
        cleaned_phones = []
        for phone in phones:
            # Keep only digits
            digits = re.sub(r'\D', '', phone)
            if len(digits) == 10:  # US phone numbers are 10 digits
                cleaned_phones.append(phone)
        
        data["phones"] = list(set(cleaned_phones))[:5]  # Deduplicate and keep max 5

        # --- D. Extract Owner / Doctor Names ---
        # Strategy: Look for names starting with "Dr." and professional titles like DDS, DMD
        
        # Match Dr. + Name (may include middle name)
        doctor_patterns = [
            r'Dr\.?\s+([A-Z][a-z]+(?:\s+[A-Z]\.?)?\s+[A-Z][a-z]+)',  # Dr. First M. Last or Dr. First Last
            r'Doctor\s+([A-Z][a-z]+(?:\s+[A-Z]\.?)?\s+[A-Z][a-z]+)',  # Doctor First Last
            r'([A-Z][a-z]+(?:\s+[A-Z]\.?)?\s+[A-Z][a-z]+),?\s+(?:DDS|DMD|D\.D\.S\.|D\.M\.D\.)',  # First Last, DDS
        ]
        
        doctors = set()
        for pattern in doctor_patterns:
            found = re.findall(pattern, text_content)
            doctors.update(found)
        
        # Clean duplicates and invalid names
        cleaned_doctors = []
        for doc in doctors:
            doc = doc.strip()
            # Filter out names that are too short/long or contain irrelevant words
            if 5 <= len(doc) <= 50 and not any(x in doc.lower() for x in ['copyright', 'reserved', 'appointment', 'contact', 'dental']):
                cleaned_doctors.append(doc)
        
        data["owner_names"] = list(set(cleaned_doctors))[:5]  # Deduplicate and keep max 5

        logger.info(f"✅ Success: {url} | Clinic: {data['clinic_name']} | Emails: {len(data['emails'])} | Phones: {len(data['phones'])} | Doctors: {len(data['owner_names'])}")
        print(f"✅ Success: {url}")
        print(f"   Clinic: {data['clinic_name']}")
        print(f"   Emails: {data['emails'] if data['emails'] else '❌ None found'}")
        print(f"   Phones: {data['phones'] if data['phones'] else '❌ None found'}")
        print(f"   Doctors: {data['owner_names'] if data['owner_names'] else '❌ None found'}\n")
        
    except Exception as e:
        logger.error(f"❌ Failed: {url} - {str(e)}")
        print(f"❌ Failed: {url} - {str(e)}\n")
    
    return data

async def main():
    results = []
    logger.info("🚀 Starting scraper...")
    
    async with async_playwright() as p:
        # Launch browser (headless=True for faster performance)
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        
        logger.info("🌐 Browser launched successfully")
        
        # Limit concurrency to 5 to avoid IP blocking
        semaphore = asyncio.Semaphore(5)

        async def worker(url):
            async with semaphore:
                page = await context.new_page()
                info = await extract_info(page, url)
                await page.close()
                results.append(info)

        # Create task list and execute
        tasks = [worker(url) for url in urls]
        await asyncio.gather(*tasks)
        
        await browser.close()
        logger.info("🔒 Browser closed")

    # Save results to CSV
    df_result = pd.DataFrame(results)
    
    # Convert lists to strings for CSV storage convenience
    df_result['emails'] = df_result['emails'].apply(lambda x: '; '.join(x) if x else '')
    df_result['phones'] = df_result['phones'].apply(lambda x: '; '.join(x) if x else '')
    df_result['owner_names'] = df_result['owner_names'].apply(lambda x: '; '.join(x) if x else '')
    
    # Save main results to timestamped folder
    output_file = os.path.join(run_folder, 'ct_dentist_leads.csv')
    df_result.to_csv(output_file, index=False, encoding='utf-8-sig')
    logger.info(f"💾 Main results saved to: {output_file}")
    
    # Also save to main data directory for backward compatibility
    legacy_output = os.path.join(script_dir, '..', 'data', 'ct_dentist_leads.csv')
    df_result.to_csv(legacy_output, index=False, encoding='utf-8-sig')
    
    # Identify websites missing emails or doctor names
    missing_data = []
    for idx, row in df_result.iterrows():
        missing_fields = []
        if not row['emails'] or row['emails'] == '':
            missing_fields.append('Email')
        if not row['owner_names'] or row['owner_names'] == '':
            missing_fields.append('Doctors')
        
        if missing_fields:
            missing_data.append({
                'url': row['url'],
                'clinic_name': row['clinic_name'],
                'missing_fields': '; '.join(missing_fields),
                'has_phones': 'Yes' if row['phones'] else 'No'
            })
    
    # Save missing data to separate CSV
    if missing_data:
        df_missing = pd.DataFrame(missing_data)
        missing_file = os.path.join(run_folder, 'missing_data_for_rerun.csv')
        df_missing.to_csv(missing_file, index=False, encoding='utf-8-sig')
        logger.info(f"⚠️  Missing data report saved to: {missing_file}")
        logger.info(f"📊 Total websites missing data: {len(missing_data)}")
    else:
        logger.info("✅ All websites have complete email and doctor information!")
    
    # Detect if running in Google Colab environment
    def is_running_in_colab():
        try:
            import google.colab
            return True
        except ImportError:
            return False
    
    # If running in Colab, backup entire run folder to Google Drive
    if is_running_in_colab():
        import shutil
        drive_backup_base = '/content/drive/MyDrive/TMP-Share/crystalsmile/data/crawl-running-result'
        
        # Check if Google Drive is mounted
        if os.path.exists('/content/drive/MyDrive'):
            try:
                # Create backup directory structure
                os.makedirs(drive_backup_base, exist_ok=True)
                
                # Copy entire run folder to Google Drive
                drive_run_folder = os.path.join(drive_backup_base, f'run_{timestamp}')
                shutil.copytree(run_folder, drive_run_folder, dirs_exist_ok=True)
                
                logger.info(f"✅ Run folder backed up to Google Drive: {drive_run_folder}")
                print(f"✅ Run folder backed up to Google Drive: {drive_run_folder}")
            except Exception as e:
                logger.warning(f"⚠️ Unable to backup to Google Drive: {str(e)}")
                print(f"⚠️ Unable to backup to Google Drive: {str(e)}")
        else:
            logger.warning("⚠️ Google Drive not mounted, skipping Drive backup")
            print("⚠️ Google Drive not mounted, skipping Drive backup")
            print("   Tip: Run the following code to mount Google Drive:")
            print("   from google.colab import drive")
            print("   drive.mount('/content/drive')")
    
    # Print statistics
    stats_msg = f"""
{"="*60}
🎉 Scraping completed! Data saved to: {run_folder}
{"="*60}
📊 Total URLs processed: {len(results)}
    logger.info(stats_msg)
    print(stats_msg)

if __name__ == "__main__":
    asyncio.run(main()) URLs processed: {len(results)}")
    print(f"📧 Clinics with emails found: {len([r for r in results if r['emails']])}")
    print(f"📞 Clinics with phones found: {len([r for r in results if r['phones']])}")
    print(f"👨‍⚕️ Clinics with doctor names found: {len([r for r in results if r['owner_names']])}")
    print("="*60)
"""

if __name__ == "__main__":
    asyncio.run(main())