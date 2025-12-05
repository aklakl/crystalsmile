import asyncio
import re
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import pandas as pd
import os

# 1. 读取 Dentist-website-list.txt 文件中的每一行作为 URLs
script_dir = os.path.dirname(os.path.abspath(__file__))
data_file = os.path.join(script_dir, '..', 'data', 'Dentist-website-list.txt')

with open(data_file, 'r', encoding='utf-8') as f:
    urls = [line.strip() for line in f if line.strip()]

print(f"📋 Loaded {len(urls)} URLs from Dentist-website-list.txt")

async def extract_info(page, url):
    data = {
        "url": url,
        "clinic_name": "",
        "emails": [],
        "phones": [],
        "owner_names": []
    }
    
    try:
        # 访问网站，超时设置为 15 秒
        await page.goto(url, timeout=15000, wait_until='domcontentloaded')
        await page.wait_for_timeout(2000)  # 等待2秒让页面加载完成
        content = await page.content()
        soup = BeautifulSoup(content, 'html.parser')
        text_content = soup.get_text(separator=' ', strip=True)

        # --- A. 提取诊所名字 ---
        # 尝试从 title, h1, 或 meta 标签提取
        clinic_name = ""
        
        # 优先从 title 标签
        if soup.title and soup.title.string:
            clinic_name = soup.title.string.strip()
            # 清理常见的后缀
            clinic_name = re.sub(r'\s*[\|\-]\s*(Home|Dentist|Dental|CT|Connecticut).*$', '', clinic_name, flags=re.IGNORECASE)
        
        # 如果 title 为空，尝试 h1
        if not clinic_name:
            h1 = soup.find('h1')
            if h1:
                clinic_name = h1.get_text(strip=True)
        
        # 如果还是空，尝试从 URL 推断
        if not clinic_name:
            from urllib.parse import urlparse
            domain = urlparse(url).netloc
            clinic_name = domain.replace('www.', '').replace('.com', '').replace('.net', '').replace('-', ' ').title()
        
        data["clinic_name"] = clinic_name

        # --- B. 提取 Email (正则匹配) ---
        # 寻找 mailto: 链接或者文本中的邮箱格式
        email_pattern = r'\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b'
        emails = set(re.findall(email_pattern, content, re.IGNORECASE))
        
        # 过滤掉常见的无效邮箱
        filtered_emails = [e for e in emails if not any(x in e.lower() for x in ['example', 'test', 'domain', 'email', 'wix', 'placeholder'])]
        data["emails"] = filtered_emails[:5]  # 最多保留5个

        # --- C. 提取电话 ---
        # 匹配美国电话格式
        phone_patterns = [
            r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',  # (203) 555-1234 或 203-555-1234
            r'\d{3}[-.\s]\d{3}[-.\s]\d{4}',          # 203.555.1234
            r'\(\d{3}\)\s?\d{3}-\d{4}'                # (203)555-1234
        ]
        
        phones = set()
        for pattern in phone_patterns:
            found = re.findall(pattern, text_content)
            phones.update(found)
        
        # 清理和标准化电话号码
        cleaned_phones = []
        for phone in phones:
            # 只保留数字
            digits = re.sub(r'\D', '', phone)
            if len(digits) == 10:  # 美国电话号码10位
    # 保存结果
    df_result = pd.DataFrame(results)
    
    # 保存到 data 目录
    output_file = os.path.join(script_dir, '..', 'data', 'ct_dentist_leads.csv')
    df_result.to_csv(output_file, index=False, encoding='utf-8-sig')
    
    # 打印统计信息
    print("\n" + "="*50)
    print("🎉 Done! Data saved to ../data/ct_dentist_leads.csv")
    print(f"📊 Total URLs processed: {len(results)}")
    print(f"📧 Clinics with emails: {len([r for r in results if r['emails']])}")
    print(f"📞 Clinics with phones: {len([r for r in results if r['phones']])}")
    print(f"👨‍⚕️ Clinics with doctor names: {len([r for r in results if r['owner_names']])}")
    print("="*50)
        # --- D. 提取 Owner / 医生名字 ---
        # 策略：寻找 "Dr." 开头的名字，以及 DDS, DMD 等专业头衔
        
        # 匹配 Dr. + 名字 (可能有中间名)
        doctor_patterns = [
            r'Dr\.?\s+([A-Z][a-z]+(?:\s+[A-Z]\.?)?\s+[A-Z][a-z]+)',  # Dr. First M. Last 或 Dr. First Last
            r'Doctor\s+([A-Z][a-z]+(?:\s+[A-Z]\.?)?\s+[A-Z][a-z]+)',  # Doctor First Last
            r'([A-Z][a-z]+(?:\s+[A-Z]\.?)?\s+[A-Z][a-z]+),?\s+(?:DDS|DMD|D\.D\.S|D\.M\.D)',  # First Last, DDS
        ]
        
        doctors = set()
        for pattern in doctor_patterns:
            found = re.findall(pattern, text_content)
            doctors.update(found)
        
        # 清理重复和无效的名字
        cleaned_doctors = []
        for doc in doctors:
            doc = doc.strip()
            # 过滤掉太短或太长的名字
            if 5 <= len(doc) <= 50 and not any(x in doc.lower() for x in ['copyright', 'reserved', 'appointment']):
                cleaned_doctors.append(doc)
        
        data["owner_names"] = list(set(cleaned_doctors))[:5]  # 去重并最多保留5个

        print(f"✅ Success: {url}")
        print(f"   Clinic: {data['clinic_name']}")
        print(f"   Emails: {data['emails']}")
        print(f"   Phones: {data['phones']}")
        print(f"   Doctors: {data['owner_names']}")
        
    except Exception as e:
        print(f"❌ Failed: {url} - {str(e)}")
    
    return data

async def main():
    results = []
    async with async_playwright() as p:
        # 启动浏览器 (headless=True 无头模式更快)
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        )
        
        # 限制并发数量，防止被封 IP
        semaphore = asyncio.Semaphore(5) 

        async def worker(url):
            async with semaphore:
                page = await context.new_page()
                info = await extract_info(page, url)
                await page.close()
                results.append(info)

        # 创建任务列表
        tasks = [worker(url) for url in urls]
        await asyncio.gather(*tasks)
        
        await browser.close()

    # 保存结果
    df_result = pd.DataFrame(results)
    df_result.to_csv('ct_dentist_leads.csv', index=False)
    print("🎉 Done! Data saved to ct_dentist_leads.csv")

if __name__ == "__main__":
    asyncio.run(main())