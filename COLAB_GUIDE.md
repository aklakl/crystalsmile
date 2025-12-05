# Google Colab Running Guide

## Running Scraper on Google Colab

This project is hosted on GitHub: **https://github.com/aklakl/crystalsmile.git**

**📦 Project includes complete data directory with 924 dental clinic website list!**

---

## 🚀 Quick Start (Recommended Method)

### One-Click Complete Code Block

Copy the following code to a Colab code cell and execute all at once:

```python
# 1. Clone project
!git clone https://github.com/aklakl/crystalsmile.git
%cd crystalsmile

# 2. Mount Google Drive (Recommended! Enables automatic backup)
from google.colab import files, drive
drive.mount('/content/drive')

# 3. Install dependencies
%cd scraper
#!pip install -r  requirements.txt
!pip install !pip install playwright beautifulsoup4 pandas requests pandas openpyxl
!playwright install chromium && playwright install-deps chromium

# 4. Check data files (data directory already included in GitHub repo)
!ls -la /content/crystalsmile/data/

# 5. Run scraper (will auto-save to Drive)
!python crawler.py
#!python crawler-from-NPI.py

# 6. Download results (optional, already saved to Drive)
# files.download('/content/crystalsmile/data/ct_dentist_leads.csv')
```

---



#### Step 5: Download Results
```python
from google.colab import files

# Download generated CSV file
files.download('/content/crystalsmile/data/ct_dentist_leads.csv')
```

---

## Colab Environment Considerations

### ✅ Advantages
1. **Free GPU/CPU resources**
2. **Python and common libraries pre-installed**
3. **No local environment setup needed**
4. **Can run for extended periods (up to 12 hours)**

### ⚠️ Important Notes

1. **Reduce Concurrency**
   - Colab has limited resources, recommend reducing from 5 to 3
   - Modify code: `semaphore = asyncio.Semaphore(3)`

2. **Adjust Timeout**
   - Colab network may be slower, increase timeout if needed
   - Modify: `timeout=20000` (20 seconds)

3. **Session Limits**
   - Free tier: Maximum 12-hour runtime
   - Need to keep browser window open (or use Colab Pro)

4. **File Saving**
   - Colab files are deleted after session ends
   - Remember to download results locally
   - Or save to Google Drive

5. **Dependency Installation Time**
   - First installation of Playwright + Chromium takes 5-10 minutes
   - Downloads approximately 300MB of data

---

## Recommended: Save to Google Drive

```python
# Mount Google Drive
from google.colab import drive
drive.mount('/content/drive')

# Modify output path
output_file = '/content/drive/MyDrive/ct_dentist_leads.csv'
df_result.to_csv(output_file, index=False, encoding='utf-8-sig')
```

---

## Performance Comparison

| Environment | Concurrency | Estimated Time (924 URLs) |
|------|--------|---------------------------|
| Local PC | 5 | ~30-45 minutes |
| Google Colab Free | 3 | ~45-60 minutes |
| Google Colab Pro | 5 | ~30-40 minutes |
---



**Key Advantages:**
1. ✅ Code uses `headless=True` (headless mode)
2. ✅ Playwright fully supports Linux environment
3. ✅ Clone directly from GitHub, no manual code/data upload needed
4. ✅ data directory includes 924 website URLs, ready to use
5. ✅ Free access to Google's computing resources

**Important Notes:**
1. Recommend reducing concurrency to 3 (`semaphore = asyncio.Semaphore(3)`)
2. Download results promptly or save to Google Drive
3. First dependency installation takes 5-10 minutes
4. Colab free tier has 12-hour maximum runtime

**Use Cases:**
- ✅ Large-scale website scraping (recommended on Colab)
- ✅ Limited local computer resources
- ✅ Long-running tasks needed
- ⚠️ Small sample testing (recommended locally)

---

## 📞 Troubleshooting

Encountered issues? Check the following:

1. **GitHub Clone Failed**
   ```python
   # Check network connection
   !ping -c 3 github.com
   ```

2. **Dependency Installation Failed**
   ```python
   # Reinstall
   !pip install --upgrade playwright beautifulsoup4 pandas
   !playwright install --force chromium
   ```

3. **File Path Error**
   ```python
   # Check current path
   !pwd
   !ls -la
   ```

4. **Out of Memory**
   ```python
   # Check memory usage
   !free -h
   # Consider batch processing URLs
   ```

---

**Project URL:** https://github.com/aklakl/crystalsmile.git

**Recommendation: Run large batch tasks (924 URLs) on Colab, test small samples (10-20 URLs) locally!** 🚀

### Error 2: `TimeoutError`
```python
# Increase timeout
await page.goto(url, timeout=30000)
```

### Error 3: `Too many open files`
```python
# Reduce concurrency
semaphore = asyncio.Semaphore(2)
```

### Error 4: Out of Memory
```python
# Process URLs in batches
batch_size = 100
for i in range(0, len(urls), batch_size):
    batch_urls = urls[i:i+batch_size]
    # Process this batch of URLs
```

---

## Summary

✅ **Your code can run perfectly on Google Colab**

Key points:
1. Uses `headless=True` (headless mode)
2. Playwright fully supports Linux environment
3. Just reduce concurrency to 3
4. Remember to download result files

Recommend running large batch tasks on Colab, test small samples locally!
