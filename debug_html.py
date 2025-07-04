#!/usr/bin/env python3
"""
Debug script to examine the HTML structure
"""

import requests
from bs4 import BeautifulSoup

def debug_wcl_page():
    """Debug the WCL page structure"""
    url = "https://www.warcraftlogs.com/zone/statistics/42?class=Any"
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Look for any tables
        tables = soup.find_all('table')
        print(f"Found {len(tables)} tables on the page")
        
        for i, table in enumerate(tables):
            print(f"\nTable {i+1}:")
            print(f"  Classes: {table.get('class', [])}")
            print(f"  ID: {table.get('id', 'None')}")
            
            # Look for rows
            rows = table.find_all('tr')
            print(f"  Rows: {len(rows)}")
            
            if rows and len(rows) > 0:
                # Check first row for headers
                first_row = rows[0]
                cells = first_row.find_all(['th', 'td'])
                print(f"  First row cells: {len(cells)}")
                if cells:
                    for j, cell in enumerate(cells[:10]):  # Only show first 10
                        print(f"    Cell {j+1}: {cell.get_text(strip=True)[:50]}")
        
        # Look for specific class patterns
        elements_with_summary = soup.find_all(class_=lambda x: x and isinstance(x, list) and any('summary' in cls.lower() for cls in x))
        print(f"\nFound {len(elements_with_summary)} elements with 'summary' in class")
        
        for elem in elements_with_summary:
            print(f"  Tag: {elem.name}, Classes: {elem.get('class', [])}")
        
        # Save a snippet of HTML for manual inspection
        with open('page_snippet.html', 'w', encoding='utf-8') as f:
            f.write(str(soup)[:10000])  # First 10k characters
        print("\nSaved first 10k characters to page_snippet.html")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    debug_wcl_page()
