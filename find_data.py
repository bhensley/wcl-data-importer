#!/usr/bin/env python3
"""
Look for JSON data embedded in the page
"""

import requests
from bs4 import BeautifulSoup
import re
import json

def find_embedded_data():
    """Look for embedded JSON data in the page"""
    url = "https://www.warcraftlogs.com/zone/statistics/42?class=Any"
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        content = response.text
        
        # Look for script tags with JSON data
        soup = BeautifulSoup(content, 'html.parser')
        scripts = soup.find_all('script')
        
        print(f"Found {len(scripts)} script tags")
        
        for i, script in enumerate(scripts):
            script_content = script.string if script.string else ""
            
            # Look for patterns that might contain data
            if any(keyword in script_content.lower() for keyword in ['damage', 'class', 'spec', 'score', 'parses']):
                print(f"\nScript {i+1} contains relevant keywords:")
                print(script_content[:500] + "..." if len(script_content) > 500 else script_content)
        
        # Look for specific patterns in the full content
        json_patterns = [
            r'window\.__INITIAL_STATE__\s*=\s*({.*?});',
            r'window\..*?=\s*({.*?"damage".*?});',
            r'var\s+.*?=\s*({.*?"spec".*?});',
        ]
        
        for pattern in json_patterns:
            matches = re.findall(pattern, content, re.DOTALL)
            if matches:
                print(f"\nFound JSON pattern: {pattern}")
                for j, match in enumerate(matches[:3]):  # Only show first 3
                    print(f"Match {j+1}: {match[:200]}...")
        
        # Save full page content for manual inspection
        with open('full_page.html', 'w', encoding='utf-8') as f:
            f.write(content)
        print("\nSaved full page to full_page.html")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    find_embedded_data()
