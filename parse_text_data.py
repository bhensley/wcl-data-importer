#!/usr/bin/env python3
"""
Parse the WCL data from the webpage content we retrieved earlier
"""

from datetime import datetime
import re
import json

# This is the data from the webpage I fetched earlier
webpage_content = """
Class Spec Score Max Parses![Image](https://assets.rpglogs.com/img/warcraft/icons/actors.jpg?v=27)

Evoker![Image](https://assets.rpglogs.com/img/warcraft/icons/actors.jpg?v=27)

Devastation83.73113.2828,751![Image](https://assets.rpglogs.com/img/warcraft/icons/actors.jpg?v=27)

Hunter![Image](https://assets.rpglogs.com/img/warcraft/icons/actors.jpg?v=27)

Marksmanship82.40115.8828,534![Image](https://assets.rpglogs.com/img/warcraft/icons/actors.jpg?v=27)

Warlock![Image](https://assets.rpglogs.com/img/warcraft/icons/actors.jpg?v=27)

Destruction81.37108.2232,506![Image](https://assets.rpglogs.com/img/warcraft/icons/actors.jpg?v=27)

Hunter![Image](https://assets.rpglogs.com/img/warcraft/icons/actors.jpg?v=27)

Survival81.2196.602,191![Image](https://assets.rpglogs.com/img/warcraft/icons/actors.jpg?v=27)

Warlock![Image](https://assets.rpglogs.com/img/warcraft/icons/actors.jpg?v=27)

Affliction80.33103.548,577![Image](https://assets.rpglogs.com/img/warcraft/icons/actors.jpg?v=27)

Paladin![Image](https://assets.rpglogs.com/img/warcraft/icons/actors.jpg?v=27)

Retribution79.66104.9049,741![Image](https://assets.rpglogs.com/img/warcraft/icons/actors.jpg?v=27)

Rogue![Image](https://assets.rpglogs.com/img/warcraft/icons/actors.jpg?v=27)

Assassination79.6299.2717,404![Image](https://assets.rpglogs.com/img/warcraft/icons/actors.jpg?v=27)

Warrior![Image](https://assets.rpglogs.com/img/warcraft/icons/actors.jpg?v=27)

Arms79.57100.6414,701![Image](https://assets.rpglogs.com/img/warcraft/icons/actors.jpg?v=27)

Demon Hunter![Image](https://assets.rpglogs.com/img/warcraft/icons/actors.jpg?v=27)

Havoc79.50105.8234,445![Image](https://assets.rpglogs.com/img/warcraft/icons/actors.jpg?v=27)

Warrior![Image](https://assets.rpglogs.com/img/warcraft/icons/actors.jpg?v=27)

Fury79.4297.5924,170![Image](https://assets.rpglogs.com/img/warcraft/icons/actors.jpg?v=27)

Priest![Image](https://assets.rpglogs.com/img/warcraft/icons/actors.jpg?v=27)

Shadow79.08105.0220,619![Image](https://assets.rpglogs.com/img/warcraft/icons/actors.jpg?v=27)

Death Knight![Image](https://assets.rpglogs.com/img/warcraft/icons/actors.jpg?v=27)

Frost78.93103.8910,014![Image](https://assets.rpglogs.com/img/warcraft/icons/actors.jpg?v=27)

Mage![Image](https://assets.rpglogs.com/img/warcraft/icons/actors.jpg?v=27)

Arcane78.83105.1329,980![Image](https://assets.rpglogs.com/img/warcraft/icons/actors.jpg?v=27)

Monk![Image](https://assets.rpglogs.com/img/warcraft/icons/actors.jpg?v=27)

Windwalker78.71100.1616,890![Image](https://assets.rpglogs.com/img/warcraft/icons/actors.jpg?v=27)

Death Knight![Image](https://assets.rpglogs.com/img/warcraft/icons/actors.jpg?v=27)

Unholy78.57101.0525,489![Image](https://assets.rpglogs.com/img/warcraft/icons/actors.jpg?v=27)

Mage![Image](https://assets.rpglogs.com/img/warcraft/icons/actors.jpg?v=27)

Fire78.1798.1112,253![Image](https://assets.rpglogs.com/img/warcraft/icons/actors.jpg?v=27)

Rogue![Image](https://assets.rpglogs.com/img/warcraft/icons/actors.jpg?v=27)

Subtlety78.0096.434,001![Image](https://assets.rpglogs.com/img/warcraft/icons/actors.jpg?v=27)

Druid![Image](https://assets.rpglogs.com/img/warcraft/icons/actors.jpg?v=27)

Feral78.0098.556,249![Image](https://assets.rpglogs.com/img/warcraft/icons/actors.jpg?v=27)

Hunter![Image](https://assets.rpglogs.com/img/warcraft/icons/actors.jpg?v=27)

Beast Mastery77.99104.9835,219![Image](https://assets.rpglogs.com/img/warcraft/icons/actors.jpg?v=27)

Shaman![Image](https://assets.rpglogs.com/img/warcraft/icons/actors.jpg?v=27)

Elemental77.42105.6417,662![Image](https://assets.rpglogs.com/img/warcraft/icons/actors.jpg?v=27)

Shaman![Image](https://assets.rpglogs.com/img/warcraft/icons/actors.jpg?v=27)

Enhancement77.0899.4312,926![Image](https://assets.rpglogs.com/img/warcraft/icons/actors.jpg?v=27)

Evoker![Image](https://assets.rpglogs.com/img/warcraft/icons/actors.jpg?v=27)

Augmentation77.0298.882,273![Image](https://assets.rpglogs.com/img/warcraft/icons/actors.jpg?v=27)

Warlock![Image](https://assets.rpglogs.com/img/warcraft/icons/actors.jpg?v=27)

Demonology76.32100.0510,455![Image](https://assets.rpglogs.com/img/warcraft/icons/actors.jpg?v=27)

Rogue![Image](https://assets.rpglogs.com/img/warcraft/icons/actors.jpg?v=27)

Outlaw76.2399.945,443![Image](https://assets.rpglogs.com/img/warcraft/icons/actors.jpg?v=27)

Druid![Image](https://assets.rpglogs.com/img/warcraft/icons/actors.jpg?v=27)

Balance75.2299.4838,257![Image](https://assets.rpglogs.com/img/warcraft/icons/actors.jpg?v=27)

Mage![Image](https://assets.rpglogs.com/img/warcraft/icons/actors.jpg?v=27)

Frost74.6197.8914,802![Image](https://assets.rpglogs.com/img/warcraft/icons/actors.jpg?v=27)

Warrior![Image](https://assets.rpglogs.com/img/warcraft/icons/actors.jpg?v=27)

Protection46.1770.7510,985![Image](https://assets.rpglogs.com/img/warcraft/icons/actors.jpg?v=27)

Death Knight![Image](https://assets.rpglogs.com/img/warcraft/icons/actors.jpg?v=27)

Blood42.7462.9816,267![Image](https://assets.rpglogs.com/img/warcraft/icons/actors.jpg?v=27)

Druid![Image](https://assets.rpglogs.com/img/warcraft/icons/actors.jpg?v=27)

Guardian40.1961.035,781![Image](https://assets.rpglogs.com/img/warcraft/icons/actors.jpg?v=27)

Monk![Image](https://assets.rpglogs.com/img/warcraft/icons/actors.jpg?v=27)

Brewmaster40.0056.587,066![Image](https://assets.rpglogs.com/img/warcraft/icons/actors.jpg?v=27)

Demon Hunter![Image](https://assets.rpglogs.com/img/warcraft/icons/actors.jpg?v=27)

Vengeance39.9059.7512,959![Image](https://assets.rpglogs.com/img/warcraft/icons/actors.jpg?v=27)

Paladin![Image](https://assets.rpglogs.com/img/warcraft/icons/actors.jpg?v=27)

Protection37.5057.0818,856![Image](https://assets.rpglogs.com/img/warcraft/icons/actors.jpg?v=27)

Monk![Image](https://assets.rpglogs.com/img/warcraft/icons/actors.jpg?v=27)

Mistweaver12.5540.7320,444![Image](https://assets.rpglogs.com/img/warcraft/icons/actors.jpg?v=27)

Paladin![Image](https://assets.rpglogs.com/img/warcraft/icons/actors.jpg?v=27)

Holy10.2925.4313,725![Image](https://assets.rpglogs.com/img/warcraft/icons/actors.jpg?v=27)

Priest![Image](https://assets.rpglogs.com/img/warcraft/icons/actors.jpg?v=27)

Discipline7.3514.6615,497![Image](https://assets.rpglogs.com/img/warcraft/icons/actors.jpg?v=27)

Druid![Image](https://assets.rpglogs.com/img/warcraft/icons/actors.jpg?v=27)

Restoration5.1020.7817,514![Image](https://assets.rpglogs.com/img/warcraft/icons/actors.jpg?v=27)

Shaman![Image](https://assets.rpglogs.com/img/warcraft/icons/actors.jpg?v=27)

Restoration4.4324.9330,590![Image](https://assets.rpglogs.com/img/warcraft/icons/actors.jpg?v=27)

Evoker![Image](https://assets.rpglogs.com/img/warcraft/icons/actors.jpg?v=27)

Preservation3.1523.265,538![Image](https://assets.rpglogs.com/img/warcraft/icons/actors.jpg?v=27)

Priest![Image](https://assets.rpglogs.com/img/warcraft/icons/actors.jpg?v=27)

Holy3.0825.0524,095
"""

def parse_wcl_text_data():
    """Parse the damage data from the text content"""
    data = []
    
    # Remove the image references
    cleaned_content = re.sub(r'!\[Image\]\([^)]+\)', '', webpage_content)
    
    # Split by classes, each class starts with the class name followed by specs
    # Pattern: Class followed by Spec followed by numbers
    pattern = r'([A-Za-z\s]+?)([A-Za-z\s]+?)(\d+\.\d+)(\d+\.\d+)([\d,]+)'
    
    lines = cleaned_content.strip().split('\n\n')
    
    current_class = None
    for line in lines:
        line = line.strip()
        if not line or 'Class Spec Score Max Parses' in line:
            continue
            
        # Try to extract class/spec/numbers from each line
        # Split the line to see if we can identify the components
        parts = line.split()
        
        if len(parts) >= 4:
            # Try to identify if this is a new class or a spec
            potential_class = parts[0]
            potential_spec = parts[1] if len(parts) > 1 else ""
            
            # Look for numbers in the line
            numbers = re.findall(r'[\d,]+\.?\d*', line)
            
            if len(numbers) >= 3:  # We need at least score, max, and parses
                try:
                    score = float(numbers[0].replace(',', ''))
                    # Skip max (numbers[1])
                    parses = int(numbers[2].replace(',', ''))
                    
                    # If we have a valid class name pattern
                    if potential_class and potential_spec:
                        current_class = potential_class
                        
                        entry = {
                            'class': current_class,
                            'spec': potential_spec,
                            'score': score,
                            'parses': parses,
                            'scraped_at': datetime.utcnow().isoformat()
                        }
                        
                        data.append(entry)
                        print(f"Parsed: {entry}")
                        
                except (ValueError, IndexError) as e:
                    print(f"Could not parse line: {line} - {e}")
    
    return data

if __name__ == "__main__":
    try:
        data = parse_wcl_text_data()
        print(f"\nSuccessfully parsed {len(data)} records")
        
        # Save to file for inspection
        with open('parsed_wcl_data.json', 'w') as f:
            json.dump(data, f, indent=2)
        
        print("Data saved to parsed_wcl_data.json")
        
    except Exception as e:
        print(f"Parsing failed: {e}")
