#!/usr/bin/env python3
"""
Test script to verify the WCL scraping functionality
"""

import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import re

def scrape_wcl_damage_data():
    """Scrape damage statistics from Warcraft Logs"""
    url = "https://www.warcraftlogs.com/zone/statistics/42?class=Any"
    
    try:
        # Make request with proper headers to avoid blocking
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        print(f"Fetching data from: {url}")
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        # Parse HTML
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find the summary table
        table = soup.find('table', class_='summary-table')
        if not table:
            raise ValueError("Could not find summary table on the page")
        
        print("Found summary table")
        
        # Extract data from table
        data = []
        tbody = table.find('tbody')
        if tbody:
            rows = tbody.find_all('tr')
        else:
            # If no tbody, get all rows and skip the first one (header)
            all_rows = table.find_all('tr')
            rows = all_rows[1:] if len(all_rows) > 1 else []
        
        print(f"Found {len(rows)} rows to process")
        
        for i, row in enumerate(rows):
            cells = row.find_all('td')
            if len(cells) >= 5:  # Ensure we have all required columns
                # Extract text content only, removing images and extra whitespace
                class_name = cells[0].get_text(strip=True)
                spec_name = cells[1].get_text(strip=True)
                score = cells[2].get_text(strip=True)
                # Skip max column (cells[3])
                parses = cells[4].get_text(strip=True)
                
                # Clean numeric values
                score_clean = re.sub(r'[^\d.]', '', score)
                parses_clean = re.sub(r'[^\d,]', '', parses).replace(',', '')
                
                entry = {
                    'class': class_name,
                    'spec': spec_name,
                    'score': float(score_clean) if score_clean else 0.0,
                    'parses': int(parses_clean) if parses_clean else 0,
                    'scraped_at': datetime.utcnow().isoformat()
                }
                
                data.append(entry)
                
                # Print first few entries for verification
                if i < 5:
                    print(f"Row {i+1}: {entry}")
        
        return data
        
    except Exception as e:
        print(f"Error scraping WCL data: {str(e)}")
        raise

if __name__ == "__main__":
    try:
        data = scrape_wcl_damage_data()
        print(f"\nSuccessfully scraped {len(data)} records")
        
        # Save to file for inspection
        with open('wcl_test_data.json', 'w') as f:
            json.dump(data, f, indent=2)
        
        print("Data saved to wcl_test_data.json")
        
    except Exception as e:
        print(f"Test failed: {e}")
