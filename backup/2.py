import requests
import pandas as pd
import time
import os
import logging
from datetime import datetime
import shutil


# NPI API endpoint
API_URL = "https://npiregistry.cms.hhs.gov/api/?version=2.1"
#example=>https://npiregistry.cms.hhs.gov/provider-view/1063112373

# Dentist taxonomy code (Taxonomy Code)
# 122300000X = Dentist (General)
# 1223G0001X = General Practice
# You can use "Dentist" as description or use specific code
TAXONOMY_DESC = "Dentist"

# Connecticut major cities list (to bypass quantity limits, we need to search by city)
# You can add more small cities here
# CT_CITIES = [
#     "Hartford", "New Haven", "Stamford", "Bridgeport", "Waterbury", "Norwalk", 
#     "Danbury", "New Britain", "West Hartford", "Greenwich", "Hamden", "Meriden",
#     "Manchester", "West Haven", "Milford", "Stratford", "Enfield", "Middletown",
#     "Wallingford", "Southington", "Shelton", "Groton", "Torrington", "Trumbull",
#     "Glastonbury", "Bristol", "Fairfield"
# ]

#Testing city
CT_CITIES = [
    "New Haven"
]


def is_running_in_colab():
    """Detect if code is running in Google Colab environment"""
    try:
        import google.colab
        return True
    except ImportError:
        return False

def get_dentists_by_city(city):
    params = {
        'state': 'CT',
        'city': city,
        'taxonomy_description': TAXONOMY_DESC,
        'limit': 200,  # Number per request
        'pretty_print': 'off'
    }
    
    all_results = []
    skip = 0
    
    logging.info(f"Starting to crawl: {city}...")
    print(f"🔍 正在抓取: {city} ...")
    
    while True:
        params['skip'] = skip
        try:
            response = requests.get(API_URL, params=params, timeout=10)
            data = response.json()
            
            if 'results' not in data:
                break
                
            results = data['results']
            if not results:
                break
                
            for item in results:
                basic = item.get('basic', {})
                addresses = item.get('addresses', [])
                
                # Find primary practice location phone
                phone = "N/A"
                address_line = "N/A"
                for addr in addresses:
                    if addr.get('address_purpose') == 'LOCATION':
                        phone = addr.get('telephone_number', "N/A")
                        address_line = f"{addr.get('address_1', '')} {addr.get('city', '')}"
                        break
                
                dentist_info = {
                    "NPI": item.get('number'),
                    "First Name": basic.get('first_name'),
                    "Last Name": basic.get('last_name'),
                    "Credential": basic.get('credential', ''), # e.g. DDS, DMD
                    "Organization Name": basic.get('organization_name', 'Individual'), # If clinic name
                    "Phone": phone,
                    "Address": address_line,
                    "City": city,
                    "Taxonomy": TAXONOMY_DESC,
                    "Enumeration Date": basic.get('enumeration_date', 'N/A'),
                    "Last Updated": basic.get('last_updated', 'N/A'),
                    "Certification Date": basic.get('certification_date', 'N/A')
                }
                all_results.append(dentist_info)
            
            # If returned results less than limit, it's the last page
            if len(results) < params['limit']:
                break
                
            skip += 200 # Pagination
            time.sleep(0.5) # Polite delay
            
        except Exception as e:
            logging.error(f"Error in {city}: {e}")
            print(f"❌ Error in {city}: {e}")
            break
            
    logging.info(f"{city} found {len(all_results)} dentists")
    print(f"✅ {city} found {len(all_results)} dentists")
    return all_results

# Main program
# Create timestamped folder
script_dir = os.path.dirname(os.path.abspath(__file__))
timestamp = datetime.now().strftime('%Y-%m-%d %H-%M-%S')
run_folder = os.path.join(script_dir, '..', 'data', f'NPI-Result-{timestamp}')
os.makedirs(run_folder, exist_ok=True)

# Setup logging
log_file = os.path.join(run_folder, 'crawler.log')
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file, encoding='utf-8'),
        logging.StreamHandler()
    ]
)

logging.info("="*50)
logging.info("NPI Crawler Started")
logging.info(f"Run folder: {run_folder}")
logging.info("="*50)

# Crawl data
all_dentists = []
for city in CT_CITIES:
    city_data = get_dentists_by_city(city)
    all_dentists.extend(city_data)

# Save data
if all_dentists:
    df = pd.DataFrame(all_dentists)
    # Remove duplicates (dentists may be registered in multiple cities)
    df.drop_duplicates(subset=['NPI'], inplace=True)
    
    # Save main results
    csv_filename = os.path.join(run_folder, "CT_Dentists_NPI_Data.csv")
    df.to_csv(csv_filename, index=False, encoding='utf-8-sig')
    
    logging.info(f"Crawling completed! Total unique dentists/clinics: {len(df)}")
    logging.info(f"Main CSV saved: {csv_filename}")
    
    # Check for missing data (empty Phone or missing Name)
    missing_data = []
    for idx, row in df.iterrows():
        missing_fields = []
        
        if pd.isna(row['Phone']) or row['Phone'] == 'N/A' or row['Phone'] == '':
            missing_fields.append('Phone')
        
        if pd.isna(row['First Name']) or row['First Name'] == '':
            missing_fields.append('First Name')
            
        if pd.isna(row['Last Name']) or row['Last Name'] == '':
            missing_fields.append('Last Name')
        
        if missing_fields:
            missing_data.append({
                'NPI': row['NPI'],
                'Organization Name': row['Organization Name'],
                'City': row['City'],
                'Missing Fields': '; '.join(missing_fields)
            })
    
    # Save missing data for rerun
    if missing_data:
        df_missing = pd.DataFrame(missing_data)
        missing_csv = os.path.join(run_folder, 'missing_data_for_rerun.csv')
        df_missing.to_csv(missing_csv, index=False, encoding='utf-8-sig')
        logging.info(f"Found {len(missing_data)} records with missing data")
        logging.info(f"Missing data CSV saved: {missing_csv}")
        print(f"\n⚠️ {len(missing_data)} records with missing data, saved to missing_data_for_rerun.csv")
    else:
        logging.info("All records have complete data")
        print("\n✅ All records have complete data")
    
    # Statistics
    total_with_phone = df[df['Phone'] != 'N/A'].shape[0]
    total_individuals = df[df['Organization Name'] == 'Individual'].shape[0]
    
    logging.info("="*50)
    logging.info("STATISTICS:")
    logging.info(f"Total records: {len(df)}")
    logging.info(f"Records with phone: {total_with_phone}")
    logging.info(f"Individual dentists: {total_individuals}")
    logging.info(f"Organizations: {len(df) - total_individuals}")
    logging.info("="*50)
    
    print(f"\n🎉 Crawling completed! Total unique dentists/clinics: {len(df)}")
    print(f"📊 Statistics: {total_with_phone} with phone, {total_individuals} individual dentists, {len(df) - total_individuals} organizations")
    print(f"Files saved to folder: {run_folder}")
    
    # Backup to Google Drive if running in Colab
    if is_running_in_colab():
        try:
            from google.colab import drive
            drive.mount('/content/drive', force_remount=True)
            
            drive_base_path = '/content/drive/MyDrive/TMP-Share/crystalsmile/data/crawl-running-result'
            os.makedirs(drive_base_path, exist_ok=True)
            
            drive_run_folder = os.path.join(drive_base_path, f'NPI-Result-{timestamp}')
            shutil.copytree(run_folder, drive_run_folder, dirs_exist_ok=True)
            
            logging.info(f"Successfully backed up to Google Drive: {drive_run_folder}")
            print(f"\n☁️ Successfully backed up to Google Drive: {drive_run_folder}")
        except Exception as e:
            logging.error(f"Failed to backup to Google Drive: {e}")
            print(f"\n❌ Google Drive backup failed: {e}")
    
    logging.info("NPI Crawler Finished Successfully")
else:
    logging.warning("No data found")
    print("No data found.")
