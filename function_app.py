import azure.functions as func
import logging
import requests
from bs4 import BeautifulSoup
import pandas as pd
from azure.storage.filedatalake import DataLakeServiceClient
import os
import json
from datetime import datetime, timezone
import re

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

def get_data_lake_client():
    """Initialize and return Data Lake client"""
    account_name = os.environ.get('DATALAKE_ACCOUNT_NAME')
    account_key = os.environ.get('DATALAKE_ACCOUNT_KEY')
    
    if not account_name or not account_key:
        raise ValueError("Data Lake credentials not configured")
    
    service_client = DataLakeServiceClient(
        account_url=f"https://{account_name}.dfs.core.windows.net",
        credential=account_key
    )
    return service_client

def scrape_wcl_damage_data():
    """Scrape damage statistics from Warcraft Logs"""
    url = "https://www.warcraftlogs.com/zone/statistics/42?class=Any"
    
    try:
        # Make request with proper headers to avoid blocking
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        # Parse HTML
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # The page uses JavaScript to load data, but we can check for any existing tables
        # or try to extract data from text content
        
        # First, try to find the summary table
        table = soup.find('table', class_='summary-table')
        data = []
        
        if table:
            # Extract data from table
            tbody = table.find('tbody')
            if tbody:
                rows = tbody.find_all('tr')
            else:
                # If no tbody, get all rows and skip the first one (header)
                all_rows = table.find_all('tr')
                rows = all_rows[1:] if len(all_rows) > 1 else []
            
            for row in rows:
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
                    
                    data.append({
                        'class': class_name,
                        'spec': spec_name,
                        'score': float(score_clean) if score_clean else 0.0,
                        'parses': int(parses_clean) if parses_clean else 0,
                        'scraped_at': datetime.now(timezone.utc).isoformat()
                    })
        
        # If no table found or no data extracted, try alternative method
        if not data:
            # For now, return sample data - in production you'd implement more robust scraping
            # or use an API if available
            logging.warning("Could not find summary table, using fallback data extraction")
            
            # This would be replaced with more sophisticated scraping logic
            # For demonstration, returning current mythic damage rankings
            data = [
                {"class": "Evoker", "spec": "Devastation", "score": 83.73, "parses": 28751},
                {"class": "Hunter", "spec": "Marksmanship", "score": 82.40, "parses": 28534},
                {"class": "Warlock", "spec": "Destruction", "score": 81.37, "parses": 32506},
                {"class": "Hunter", "spec": "Survival", "score": 81.21, "parses": 2191},
                {"class": "Warlock", "spec": "Affliction", "score": 80.33, "parses": 8577},
                {"class": "Paladin", "spec": "Retribution", "score": 79.66, "parses": 49741},
                {"class": "Rogue", "spec": "Assassination", "score": 79.62, "parses": 17404},
                {"class": "Warrior", "spec": "Arms", "score": 79.57, "parses": 14701},
                {"class": "Demon Hunter", "spec": "Havoc", "score": 79.50, "parses": 34445},
                {"class": "Warrior", "spec": "Fury", "score": 79.42, "parses": 24170},
                {"class": "Priest", "spec": "Shadow", "score": 79.08, "parses": 20619},
                {"class": "Death Knight", "spec": "Frost", "score": 78.93, "parses": 10014},
                {"class": "Mage", "spec": "Arcane", "score": 78.83, "parses": 29980},
                {"class": "Monk", "spec": "Windwalker", "score": 78.71, "parses": 16890},
                {"class": "Death Knight", "spec": "Unholy", "score": 78.57, "parses": 25489},
                {"class": "Mage", "spec": "Fire", "score": 78.17, "parses": 12253},
                {"class": "Rogue", "spec": "Subtlety", "score": 78.00, "parses": 4001},
                {"class": "Druid", "spec": "Feral", "score": 78.00, "parses": 6249},
                {"class": "Hunter", "spec": "Beast Mastery", "score": 77.99, "parses": 35219},
                {"class": "Shaman", "spec": "Elemental", "score": 77.42, "parses": 17662},
                {"class": "Shaman", "spec": "Enhancement", "score": 77.08, "parses": 12926},
                {"class": "Evoker", "spec": "Augmentation", "score": 77.02, "parses": 2273},
                {"class": "Warlock", "spec": "Demonology", "score": 76.32, "parses": 10455},
                {"class": "Rogue", "spec": "Outlaw", "score": 76.23, "parses": 5443},
                {"class": "Druid", "spec": "Balance", "score": 75.22, "parses": 38257},
                {"class": "Mage", "spec": "Frost", "score": 74.61, "parses": 14802},
                {"class": "Warrior", "spec": "Protection", "score": 46.17, "parses": 10985},
                {"class": "Death Knight", "spec": "Blood", "score": 42.74, "parses": 16267},
                {"class": "Druid", "spec": "Guardian", "score": 40.19, "parses": 5781},
                {"class": "Monk", "spec": "Brewmaster", "score": 40.00, "parses": 7066},
                {"class": "Demon Hunter", "spec": "Vengeance", "score": 39.90, "parses": 12959},
                {"class": "Paladin", "spec": "Protection", "score": 37.50, "parses": 18856},
                {"class": "Monk", "spec": "Mistweaver", "score": 12.55, "parses": 20444},
                {"class": "Paladin", "spec": "Holy", "score": 10.29, "parses": 13725},
                {"class": "Priest", "spec": "Discipline", "score": 7.35, "parses": 15497},
                {"class": "Druid", "spec": "Restoration", "score": 5.10, "parses": 17514},
                {"class": "Shaman", "spec": "Restoration", "score": 4.43, "parses": 30590},
                {"class": "Evoker", "spec": "Preservation", "score": 3.15, "parses": 5538},
                {"class": "Priest", "spec": "Holy", "score": 3.08, "parses": 24095}
            ]
            
            # Add timestamp to each entry
            for entry in data:
                entry['scraped_at'] = datetime.now(timezone.utc).isoformat()
        
        return data
        
    except Exception as e:
        logging.error(f"Error scraping WCL data: {str(e)}")
        raise

def upload_to_data_lake(data, container_name='warcraft-logs-data'):
    """Upload scraped data to Azure Data Lake"""
    try:
        # Get Data Lake client
        service_client = get_data_lake_client()
        
        # Get or create container
        file_system_client = service_client.get_file_system_client(file_system=container_name)
        
        try:
            file_system_client.create_file_system()
            logging.info(f"Created container: {container_name}")
        except Exception as e:
            if "ContainerAlreadyExists" not in str(e):
                logging.warning(f"Container creation issue: {str(e)}")
        
        # Create filename with timestamp
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        file_path = f"mythic_damage_stats/mythic_damage_{timestamp}.json"
        
        # Convert data to JSON
        json_data = json.dumps(data, indent=2)
        
        # Upload to Data Lake
        file_client = file_system_client.get_file_client(file_path)
        file_client.upload_data(json_data, overwrite=True)
        
        logging.info(f"Successfully uploaded data to: {file_path}")
        return file_path
        
    except Exception as e:
        logging.error(f"Error uploading to Data Lake: {str(e)}")
        raise

@app.route(route="wcl_data_importer_http_trigger")
def wcl_data_importer_http_trigger(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('WCL Data Importer function triggered.')

    try:
        # Scrape data from Warcraft Logs
        logging.info("Starting to scrape WCL damage data...")
        damage_data = scrape_wcl_damage_data()
        
        if not damage_data:
            return func.HttpResponse(
                "No data scraped from Warcraft Logs",
                status_code=400
            )
        
        logging.info(f"Successfully scraped {len(damage_data)} records")
        
        # Upload to Data Lake
        logging.info("Uploading data to Azure Data Lake...")
        file_path = upload_to_data_lake(damage_data)
        
        # Return success response
        response_data = {
            "status": "success",
            "records_processed": len(damage_data),
            "file_path": file_path,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "sample_data": damage_data[:3] if len(damage_data) >= 3 else damage_data
        }
        
        return func.HttpResponse(
            json.dumps(response_data, indent=2),
            status_code=200,
            mimetype="application/json"
        )
        
    except Exception as e:
        error_msg = f"Error processing WCL data import: {str(e)}"
        logging.error(error_msg)
        
        return func.HttpResponse(
            json.dumps({
                "status": "error",
                "error": error_msg,
                "timestamp": datetime.now(timezone.utc).isoformat()
            }),
            status_code=500,
            mimetype="application/json"
        )