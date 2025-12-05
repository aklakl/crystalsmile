#scrape dental-website from google_maps
from playwright.sync_api import sync_playwright
import pandas as pd
import time
import random

# List of all zip codes in Connecticut (must be split for queries, as Google may limit results)
ZIP_CODES = [
    "06810", "06516", "06478", "06070", "06756", "06782", "06461", "06249", "06374", "06387", 
    "06812", "06001", "06786", "06708", "06811", "06410", "06379", "06339", "06269", "06606", 
    "06784", "06019", "06085", "06851", "06033", "06752", "06488", "06518", "06763", "06790", 
    "06024", "06512", "06279", "06373", "06470", "06854", "06856", "06438", "06472", "06473", 
    "06770", "06405", "06604", "06804", "06880", "06840", "06106", "06479", "06793", "06460", 
    "06706", "06492", "06514", "06517", "06226", "06231", "06277", "06897", "06903", "06614", 
    "06091", "06020", "06791", "06057", "06469", "06457", "06513", "06032", "06084", "06255", 
    "06040", "06787", "06511", "06704", "06333", "06608", "06468", "06089", "06254", "06820", 
    "06830", "06114", "06710", "06105", "06360", "06384", "06051", "06095", "06088", "06096", 
    "06081", "06160", "06118", "06389", "06357", "06234", "06278", "06260", "06264", "06610", 
    "06877", "06906", "06798", "06751", "06758", "06475", "06243", "06481", "06332", "06525", 
    "06712", "06524", "06350", "06248", "06282", "06262", "06807", "06801", "06120", "06103", 
    "06878", "06905", "06883", "06111", "06074", "06783", "06779", "06426", "06420", "06418", 
    "06401", "06359", "06331", "06247", "06377", "06013", "06082", "06607", "06053", "06052", 
    "06023", "06060", "06021", "06058", "06108", "06061", "06480", "06498", "06412", "06414", 
    "06471", "06519", "06510", "06371", "06403", "06334", "06029", "06071", "06266", "06320", 
    "06890", "06896", "06853", "06107", "06090", "06073", "06042", "06442", "06409", "06416", 
    "06702", "06263", "06112", "06489", "06235", "06907", "06615", "06117", "06016", "06092", 
    "06467", "06067", "06477", "06450", "06762", "06437", "06901", "06850", "06335", "06376", 
    "06043", "06110", "06451", "06605", "06484", "06010", "06035", "06447", "06444", "06002", 
    "06026", "06059", "06441", "06455", "06483", "06515", "06705", "06340", "06353", "06232", 
    "06855", "06066", "06870", "06119", "06716", "06037", "06256", "06027", "06062", "06109"
]

#ZIP_CODES = ["06810", "06516", "06478", "06070", "06756", "06782", "06461", "06249", "06374", "06387", "06812", "06001", "06786", "06708", "06811", "06410", "06379", "06339", "06269", "06606", "06784", "06019", "06085", "06851", "06033", "06752", "06488", "06518", "06763", "06790", "06024", "06512", "06279", "06373", "06470", "06854", "06856", "06438", "06472", "06473", "06770", "06405", "06604", "06804", "06880", "06840", "06106", "06479", "06793", "06460", "06706", "06492", "06514", "06517", "06226", "06231", "06277", "06897", "06903", "06614", "06091", "06020", "06791", "06057", "06469", "06457", "06513", "06032", "06084", "06255", "06040", "06787", "06511", "06704", "06333", "06608", "06468", "06089", "06254", "06820", "06830", "06114", "06710", "06105", "06360", "06384", "06051", "06095", "06088", "06096", "06081", "06160", "06118", "06389", "06357", "06234", "06278", "06260", "06264", "06610", "06877", "06906", "06798", "06751", "06758", "06475", "06243", "06481", "06332", "06525", "06712", "06524", "06350", "06248", "06282", "06262", "06807", "06801", "06120", "06103", "06878", "06905", "06883", "06111", "06074", "06783", "06779", "06426", "06420", "06418", "06401", "06359", "06331", "06247", "06377", "06013", "06082", "06607", "06053", "06052", "06023", "06060", "06021", "06058", "06108", "06061", "06480", "06498", "06412", "06414", "06471", "06519", "06510", "06371", "06403", "06334", "06029", "06071", "06266", "06320", "06890", "06896", "06853", "06107", "06090", "06073", "06042", "06442", "06409", "06416", "06702", "06263", "06112", "06489", "06235", "06907", "06615", "06117", "06016", "06092", "06467", "06067", "06477", "06450", "06762", "06437", "06901", "06850", "06335", "06376", "06043", "06110", "06451", "06605", "06484", "06010", "06035", "06447", "06444", "06002", "06026", "06059", "06441", "06455", "06483", "06515", "06705", "06340", "06353", "06232", "06855", "06066", "06870", "06119", "06716", "06037", "06256", "06027", "06062", "06109", "06022", "06422", "06413", "06417", "06456", "06380", "06336", "06365"]


def scrape_google_maps(zip_query):
    extracted_data = []
    
    with sync_playwright() as p:
        # Launch browser (headless=False to see browser actions, less likely to be blocked)
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        
        # 1. Visit Google Maps
        search_term = f"Dentist in {zip_query}"
        print(f"🚗 Searching for: {search_term}")
        
        page.goto("https://www.google.com/maps", timeout=60000)
        
        # 2. Enter search term
        page.wait_for_selector("input#searchboxinput")
        page.fill("input#searchboxinput", search_term)
        page.keyboard.press("Enter")
        
        # 3. Wait for the list to load
        # The list container in Google Maps usually has role="feed"
        try:
            page.wait_for_selector('div[role="feed"]', timeout=10000)
        except:
            print(f"❌ No results found for: {zip_query}")
            return []

        # 4. Infinite Scroll
        # We need to keep scrolling the left panel until the "You've reached the end of the list" sign appears
        print("📜 Starting to scroll the list...")
        previous_count = 0
        same_count_attempts = 0
        
        while True:
            # Get all current entries
            # a[href*="/maps/place/"] is the link to the details page
            listings = page.locator('div[role="feed"] > div > div[jsaction]').all()
            current_count = len(listings)
            
            # Scroll operation: select the last element and press PageDown
            page.locator('div[role="feed"]').click()
            page.keyboard.press("End")
            
            time.sleep(random.uniform(2, 4)) # Random wait, like a human
            
            if current_count == previous_count:
                same_count_attempts += 1
                if same_count_attempts > 3: # If the count doesn't change for 3 consecutive times, it means we've reached the bottom
                    # Check if it has really reached the end (there will be a text prompt on the page), or if it's just a network lag
                    end_text = page.locator("text=You've reached the end of the list").count()
                    if end_text > 0 or current_count > 110: # Google's limit is about 120 results
                        break
            else:
                same_count_attempts = 0
            
            previous_count = current_count
            print(f"   Loaded {current_count} clinics...")

        print(f"✅ Scrolling finished, starting to extract {len(listings)} records...")

        # 5. Parse data (scrape directly from the list without clicking into the detail page, which is faster and less likely to be blocked)
        # Note: Without entering the detail page, you might not get the full Website URL, but the Google Maps list page usually contains a website button
        
        # To get the exact Website URL, we need to parse the list's HTML
        # The Class for this part changes frequently, so we use Aria-label or relative positions
        
        # Here we demonstrate a more robust method: iterating through the listings found earlier
        for item in listings:
            try:
                # Extract text, usually in the format: "Name\nRating\nType\nAddress\nOpen status"
                text = item.inner_text()
                lines = text.split('\n')
                
                if len(lines) < 3: continue
                
                name = lines[0]
                
                # Try to get the link (usually in href)
                link_tag = item.locator('a').first
                maps_link = link_tag.get_attribute('href')
                
                extracted_data.append({
                    "Zipcode_Searched": zip_query,
                    "Name": name,
                    "Raw_Text": text.replace('\n', ' | '), # Contains address and phone number
                    "Maps_Link": maps_link
                })
            except:
                continue

        browser.close()
        
    return extracted_data

# Main program
all_results = []
for zipcode in ZIP_CODES:
    data = scrape_google_maps(zipcode)
    all_results.extend(data)
    time.sleep(5) # Rest between zip codes

# Save
df = pd.DataFrame(all_results)
df.to_csv("local_google_maps_results.csv", index=False)
print("🎉 Done!")