"""
Script to generate sample HSN data for testing the HSN Validator Agent.
"""

import pandas as pd
import random
import os

# Sample HSN code data - organized by hierarchical sections
# Format: 2-digit, 4-digit, 6-digit, and 8-digit codes with descriptions
hsn_data = [
    # Section 1: Electronic goods (Chapter 85)
    {"HSNCode": "85", "Description": "Electrical machinery and equipment"},
    {"HSNCode": "8517", "Description": "Telephone sets and other apparatus for voice/data transmission"},
    {"HSNCode": "851712", "Description": "Telephones for cellular networks or other wireless networks"},
    {"HSNCode": "85171290", "Description": "Mobile Phones"},
    
    # Section 2: Pharmaceutical products (Chapter 30)
    {"HSNCode": "30", "Description": "Pharmaceutical products"},
    {"HSNCode": "3004", "Description": "Medicaments in measured doses or for retail sale"},
    {"HSNCode": "300490", "Description": "Other medicaments, for therapeutic uses"},
    {"HSNCode": "30049099", "Description": "Other medicaments for therapeutic or prophylactic uses"},
    
    # Section 3: Machinery (Chapter 84)
    {"HSNCode": "84", "Description": "Nuclear reactors, boilers, machinery"},
    {"HSNCode": "8471", "Description": "Automatic data processing machines and units"},
    {"HSNCode": "847130", "Description": "Portable digital automatic data processing machines"},
    {"HSNCode": "84713010", "Description": "Laptop computers"},
    
    # Section 4: Textiles (Chapter 61)
    {"HSNCode": "61", "Description": "Articles of apparel and clothing accessories, knitted or crocheted"},
    {"HSNCode": "6109", "Description": "T-shirts, singlets and other vests, knitted or crocheted"},
    {"HSNCode": "610910", "Description": "T-shirts, singlets of cotton, knitted or crocheted"},
    {"HSNCode": "61091000", "Description": "T-shirts, singlets of cotton, knitted or crocheted"},
    
    # Section 5: Vehicles (Chapter 87)
    {"HSNCode": "87", "Description": "Vehicles other than railway or tramway"},
    {"HSNCode": "8703", "Description": "Motor cars and other motor vehicles for transport of persons"},
    {"HSNCode": "870321", "Description": "Vehicles with spark-ignition engine of cylinder capacity ≤ 1,000 cc"},
    {"HSNCode": "87032100", "Description": "Small cars with engine capacity not exceeding 1,000 cc"},
    
    # Add more sections as needed...
]

def create_sample_data(output_file="HSN_Master_Data.xlsx"):
    """
    Creates a sample HSN master data file with the specified data.
    
    Args:
        output_file: Path to the output Excel file
    """
    # Convert to DataFrame
    df = pd.DataFrame(hsn_data)
    
    # Ensure directory exists
    output_dir = os.path.dirname(output_file)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Save to Excel
    df.to_excel(output_file, index=False)
    print(f"Sample HSN data created: {output_file}")
    print(f"Created {len(df)} HSN code entries across different hierarchical levels")

if __name__ == "__main__":
    create_sample_data()
    
    # Optionally create a larger dataset with random variations
    # Uncomment the following code to generate a larger dataset
    """
    large_data = []
    
    # Add all original data
    large_data.extend(hsn_data)
    
    # Generate random variations for testing
    chapters = [str(i).zfill(2) for i in range(10, 99)]
    
    for chapter in chapters[:20]:  # Limit to 20 chapters for sample
        # Add chapter (2-digit)
        large_data.append({
            "HSNCode": chapter,
            "Description": f"Sample chapter {chapter}"
        })
        
        # Add some 4-digit codes
        for _ in range(random.randint(2, 5)):
            heading = chapter + str(random.randint(10, 99))
            large_data.append({
                "HSNCode": heading,
                "Description": f"Sample heading {heading}"
            })
            
            # Add some 6-digit codes
            for _ in range(random.randint(1, 3)):
                subheading = heading + str(random.randint(10, 99))
                large_data.append({
                    "HSNCode": subheading,
                    "Description": f"Sample subheading {subheading}"
                })
                
                # Add some 8-digit codes
                for _ in range(random.randint(1, 2)):
                    tariff_code = subheading + str(random.randint(10, 99))
                    large_data.append({
                        "HSNCode": tariff_code,
                        "Description": f"Sample tariff item {tariff_code}"
                    })
    
    # Save large dataset
    large_df = pd.DataFrame(large_data)
    large_df.to_excel("HSN_Master_Data_Large.xlsx", index=False)
    print(f"Created large HSN dataset with {len(large_df)} entries")
    """
