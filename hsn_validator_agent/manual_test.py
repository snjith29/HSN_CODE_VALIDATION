"""
Manual test script for HSN code validation functions.

This script tests the core HSN validation functions without requiring the ADK infrastructure.
"""

import os
import json
from agent import (
    load_hsn_data,
    validate_hsn_format,
    validate_hsn_existence,
    validate_hsn_hierarchy,
    validate_hsn_code,
    validate_hsn_codes,
    process_hsn_validation_request
)
from create_sample_data import create_sample_data

def print_json(data):
    """Print data as formatted JSON"""
    print(json.dumps(data, indent=2))

def main():
    print("HSN Code Validator - Manual Test")
    print("================================")
    
    # Create sample data if it doesn't exist
    if not os.path.exists("HSN_Master_Data.xlsx"):
        print("Creating sample HSN data...")
        create_sample_data()
    
    # Load HSN data
    print("\nLoading HSN data:")
    result = load_hsn_data("HSN_Master_Data.xlsx")
    print_json(result)
    
    # Test format validation
    print("\nTesting format validation:")
    codes_to_validate_format = ["85171290", "123", "abcdef", "12345678901", ""]
    for code in codes_to_validate_format:
        print(f"\nValidating format for '{code}':")
        result = validate_hsn_format(code)
        print_json(result)
    
    # Test existence validation
    print("\nTesting existence validation:")
    codes_to_validate_existence = ["85171290", "3004", "12345678"]
    for code in codes_to_validate_existence:
        print(f"\nChecking if '{code}' exists in database:")
        result = validate_hsn_existence(code)
        print_json(result)
    
    # Test hierarchy validation
    print("\nTesting hierarchy validation:")
    codes_to_validate_hierarchy = ["85171290", "30049099", "12345678"]
    for code in codes_to_validate_hierarchy:
        print(f"\nValidating hierarchy for '{code}':")
        result = validate_hsn_hierarchy(code)
        print_json(result)
    
    # Test comprehensive validation
    print("\nTesting comprehensive validation:")
    codes_to_validate = ["85171290", "123456789", "abcdef", "12345678"]
    for code in codes_to_validate:
        print(f"\nComprehensive validation for '{code}':")
        result = validate_hsn_code(code)
        print_json(result)
    
    # Test batch validation
    print("\nTesting batch validation:")
    batch = ["85171290", "3004", "123456789", "12345678"]
    print(f"Validating batch: {batch}")
    result = validate_hsn_codes(batch)
    print_json(result)
    
    # Test request processing
    print("\nTesting request processing:")
    
    # Single code request
    single_request = {"code": "85171290"}
    print(f"\nProcessing single code request: {single_request}")
    result = process_hsn_validation_request(single_request)
    print_json(result)
    
    # Batch request
    batch_request = {"codes": ["85171290", "3004", "123456789", "12345678"]}
    print(f"\nProcessing batch request: {batch_request}")
    result = process_hsn_validation_request(batch_request)
    print_json(result)
    
    print("\nManual test completed.")

if __name__ == "__main__":
    main()
