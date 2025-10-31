"""
Selenium Web Scraper for Actuary List Jobs from https://www.actuarylist.com (scrapes and populates db)

Scraping Scope: targets the first 10 pages (est: 300 jobs) from actuarylist.com excluding duplicates
for demonstration purposes as per project requirements
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.chrome.options import Options
import time
import re
from datetime import datetime
import sys
import os

# Get the absolute path to the backend directory
current_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.join(os.path.dirname(current_dir), 'backend')
sys.path.insert(0, backend_dir)

from flask import Flask
from flask_cors import CORS
from config import Config
from db import db
from models.job import Job

def create_app():
    """Create Flask app for database operations"""
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app)
    db.init_app(app)
    return app

class ActuaryListScraper:
    def __init__(self, headless=True):
        """Initialize the scraper with Chrome WebDriver"""
        self.url = "https://www.actuarylist.com/"
        self.driver = None
        self.jobs_data = []
        self.headless = headless
        self.failed_extractions = []
        
    def setup_driver(self):
        """Configure and return Chrome WebDriver"""
        chrome_options = Options()
        
        if self.headless:
            chrome_options.add_argument('--headless=new')
        
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        chrome_options.add_argument('--window-size=1920,1080')
        
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.set_page_load_timeout(30)
        print("✓ WebDriver initialized successfully")
        
    def load_page(self):
        """Load the Actuary List jobs page"""
        try:
            print(f"\nLoading {self.url}...")
            self.driver.get(self.url)
            
            # Wait for job cards to load
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "article"))
            )
            print("Page loaded successfully")
            
            # Wait aa bit for JavaScript to finish rendering
            time.sleep(3)
            
            return True
            
        except TimeoutException:
            print("Error: Page took too long to load")
            return False
        except Exception as e:
            print(f"Error loading page: {str(e)}")
            return False
    
    def scroll_and_load_more(self, target_pages=10):
        """Click the Next button to load more pages and scrape each page"""
        print(f"\nLoading and scraping multiple pages (target: {target_pages} pages)...")
        
        # Scrape the first page
        print(f"\nScraping page 1...")
        self.scrape_current_page()
        pages_loaded = 1
        
        while pages_loaded < target_pages:
            try:
                #Scroll to bottom first to ensure that the pagination is visible
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
                
                # Try multiple selectors for the Next button
                next_button = None
                selectors = [
                    (By.XPATH, "//button[contains(text(), 'Next')]"),
                    (By.CSS_SELECTOR, "button:contains('Next')"),
                    (By.XPATH, "//button[contains(@class, 'relative') and contains(text(), 'Next')]"),
                ]
                
                for selector_type, selector in selectors:
                    try:
                        next_button = self.driver.find_element(selector_type, selector)
                        if next_button.is_displayed():
                            break
                    except:
                        continue
                
                if next_button and next_button.is_displayed() and next_button.is_enabled():
                    # Scroll to button
                    self.driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
                    time.sleep(1)
                    
                    # Click 
                    self.driver.execute_script("arguments[0].click();", next_button)
                    pages_loaded += 1
                    print(f"  Clicked Next - Loading page {pages_loaded}")
                    
                    # Wait for new jobs to load 
                    try:
                        WebDriverWait(self.driver, 10).until(
                            EC.presence_of_element_located((By.TAG_NAME, "article"))
                        )
                        time.sleep(2)  # Small buffer for full render
                    except TimeoutException:
                        time.sleep(4)  # Fallback to fixed wait
                    
                    # Scrape this page
                    print(f"\nScraping page {pages_loaded}...")
                    self.scrape_current_page()
                else:
                    print("  Next button not available reached end")
                    break
                    
            except NoSuchElementException:
                print("  No Next button found reached last page")
                break
            except Exception as e:
                print(f"  Error clicking Next: {str(e)}")
                break
        
        print(f"\nFinished loading and scraping {pages_loaded} pages")
        print(f"Total jobs collected: {len(self.jobs_data)}")
        return pages_loaded
    
    def scrape_current_page(self):
        """Scrape all job listings on the current page"""
        # Find all job article elements on current page
        job_articles = self.driver.find_elements(By.TAG_NAME, "article")
        
        page_jobs_count = 0
        
        for idx, job_article in enumerate(job_articles):
            try:
                job_data = self.extract_job_data(job_article)
                
                if job_data and job_data['title'] and job_data['company']:
                    # Check for if we already have this job to avoid duplicates across the pages
                    job_key = (job_data['title'], job_data['company'])
                    existing_keys = [(j['title'], j['company']) for j in self.jobs_data]
                    
                    if job_key not in existing_keys:
                        self.jobs_data.append(job_data)
                        page_jobs_count += 1
                        
            except Exception as e:
                self.failed_extractions.append({
                    'page_position': idx + 1,
                    'error': str(e)
                })
                continue
        
        print(f"  Scraped {page_jobs_count} jobs from this page (Total: {len(self.jobs_data)})")
    
    def extract_job_data(self, job_element):
        """Extract all relevant data from a single job card element"""
        try:
            job_data = {}
            
            # Extract Company Name from paragraph with specific class
            try:
                company = job_element.find_element(By.CSS_SELECTOR, "p.Job_job-card__company__7T9qY").text.strip()
                job_data['company'] = company if company else "Company Name Not Listed"
            except:
                job_data['company'] = "Company Name Not Listed"
            
            # Extract Job Title/Position from paragraph with specific class
            try:
                title = job_element.find_element(By.CSS_SELECTOR, "p.Job_job-card__position__ic1rc").text.strip()
                job_data['title'] = title if title else "Actuary Position"
            except:
                job_data['title'] = "Actuary Position"
            
            # Extract Location from the locations div (improved with regex)
            try:
                locations_div = job_element.find_element(By.CSS_SELECTOR, "div.Job_job-card__locations__x1exr")
                location_text = locations_div.text.strip()
                lines = location_text.split('\n')
                
                # Filter out lines that start with emojis or contain only emojis/salary info
                # Using regex to match the emoji patterns
                location_parts = []
                for line in lines:
                    line = line.strip()
                    # Skip empty lines + salary lines with the moneybag emoji + emoji-only lines
                    if line and not re.match(r'^[\U0001F300-\U0001F9FF\U0001F600-\U0001F64F\U0001F680-\U0001F6FF]', line):
                        location_parts.append(line)
                
                job_data['location'] = ', '.join(location_parts[:3]) if location_parts else "Not Specified"
            except:
                job_data['location'] = "Remote / Not Specified"
            
            # Extract Posting Date
            try:
                date = job_element.find_element(By.CSS_SELECTOR, "p.Job_job-card__posted-on__NCZaJ").text.strip()
                job_data['posting_date'] = date if date else "Recently posted"
            except:
                job_data['posting_date'] = "Recently posted"
            
            # Extract Job Type infer from title and tags 
            title_lower = job_data['title'].lower()
            tags_text = ''
            
            # Get tags to help with job type inference
            tags_list = []
            try:
                tags_div = job_element.find_element(By.CSS_SELECTOR, "div.Job_job-card__tags__zfriA")
                tag_links = tags_div.find_elements(By.TAG_NAME, "a")
                tags_list = [tag.text.strip() for tag in tag_links if tag.text.strip()]
                tags_text = ' '.join(tags_list).lower()
            except:
                pass
            
            # ---Improved job type inference
            if 'intern' in title_lower or 'intern' in tags_text:
                job_data['job_type'] = 'Internship'
            elif 'part-time' in title_lower or 'part time' in title_lower or 'part-time' in tags_text:
                job_data['job_type'] = 'Part-time'
            elif 'contract' in title_lower or 'contractor' in tags_text:
                job_data['job_type'] = 'Contract'
            else:
                job_data['job_type'] = 'Full-time'
            
            # If no tags were extracted we add default ones
            if not tags_list:
                tags_list = ['Actuary', 'Insurance']
            
            job_data['tags'] = ','.join(tags_list[:8])  # Limit to 8 tags
            
            return job_data
            
        except Exception as e:
            print(f"  Error extracting job data: {str(e)}")
            return None
    
    def scrape_jobs(self):
        """Legacy method now handled by scrape_current_page()"""
        # method no longer needed but kept for compatibility
        # The scraping now happens in the scroll_and_load_more()
        print("\n" + "="*60)
        print("SCRAPING COMPLETE")
        print("="*60)
        print(f"Successfully scraped {len(self.jobs_data)} total jobs")
        
        # Show failed extractions if any
        if self.failed_extractions:
            print(f"Failed to extract {len(self.failed_extractions)} jobs")
            if len(self.failed_extractions) <= 5:
                for fail in self.failed_extractions:
                    print(f"  - Position {fail['page_position']}: {fail['error']}")
        
        # Print sample
        if self.jobs_data:
            print("\nSample of scraped jobs:")
            for i, job in enumerate(self.jobs_data[:5], 1):
                url_preview = job.get('url', 'No URL')[:50] + '...' if job.get('url') else 'No URL'
                print(f"  {i}. {job['title']} at {job['company']}")
                print(f"     Location: {job['location']} | URL: {url_preview}")
        
        return self.jobs_data
    
    def save_to_database(self, app):
        """Save scraped jobs to the database"""
        print("\n" + "="*10)
        print("SAVING TO DATABASE")
        
        with app.app_context():
            saved_count = 0
            duplicate_count = 0
            error_count = 0
            
            for job_data in self.jobs_data:
                try:
                    # Check for duplicates.. means same title and company
                    existing_job = Job.query.filter_by(
                        title=job_data['title'],
                        company=job_data['company']
                    ).first()
                    
                    if existing_job:
                        duplicate_count += 1
                        continue
                    
                    # Create the new job entry
                    new_job = Job(
                        title=job_data['title'],
                        company=job_data['company'],
                        location=job_data['location'],
                        posting_date=job_data['posting_date'],
                        job_type=job_data['job_type'],
                        tags=job_data['tags'],
                    )
                    
                    db.session.add(new_job)
                    saved_count += 1
                    
                    # Commit in batches of 50
                    if saved_count % 50 == 0:
                        db.session.commit()
                        print(f"  Saved {saved_count} jobs...")
                    
                except Exception as e:
                    error_count += 1
                    print(f"  Error saving job: {str(e)}")
                    db.session.rollback()
                    continue
            
            # Final commit
            try:
                db.session.commit()
                print(f"\n{'='*60}")
                print(f"DATABASE SAVE COMPLETE")
                print(f"{'='*60}")
                print(f"Successfully saved: {saved_count} jobs")
                print(f"Duplicates skipped: {duplicate_count} jobs")
                if error_count > 0:
                    print(f"Errors: {error_count} jobs")
                print(f"{'='*60}\n")
                
            except Exception as e:
                db.session.rollback()
                print(f"Error during final commit: {str(e)}")
    
    def run(self, target_pages=10):
        """Main execution method"""
        try:
            print("\n" + "="*10)
            print("ACTUARY LIST JOB SCRAPER")
            print("="*60)
            print(f"Target: {target_pages} pages (est: 30 jobs per page)")
            print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            
            # Setup
            self.setup_driver()
            
            # Load page
            if not self.load_page():
                return False
            
            # Load more pages by clicking Next and then scrape each page
            self.scroll_and_load_more(target_pages)
            
            # Call the scrape_jobs to show final summary
            self.scrape_jobs()
            
            if len(self.jobs_data) == 0:
                print("\nNo jobs were scraped.")
                return False
            
            # Save to database
            app = create_app()
            self.save_to_database(app)
            
            return True
            
        except Exception as e:
            print(f"\nFatal error during scraping: {str(e)}")
            import traceback
            traceback.print_exc()
            return False
            
        finally:
            if self.driver:
                self.driver.quit()
                print("WebDriver closed")
            print(f"\nFinished at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

def main():
    """THE Entry point for the scraper
    
    Note: This scraper targets the first 10 pages (est 300 jobs) from actuarylist.com
    for demo purposes. The site contains alot of jobs but we limit
    the scope as per project requirements.....
    """
    # Set headless=False to see the browser and to True to run in background
    scraper = ActuaryListScraper(headless=False)
    
    # Scrape 10 pages
    success = scraper.run(target_pages=10)
    
    if success:
        print("\nScraping completed successfully!")
        return 0
    else:
        print("\nScraping failed!")
        return 1

if __name__ == "__main__":
    exit(main())