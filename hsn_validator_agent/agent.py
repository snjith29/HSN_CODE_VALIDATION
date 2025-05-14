"""
HSN Code Validator Agent

This module implements an intelligent agent for validating Harmonized System Nomenclature (HSN) codes
using Google's Agent Development Kit (ADK).
"""

import os
import re
import pandas as pd
from typing import List, Dict, Union, Optional
from google.adk.agents import Agent
from google.adk.tools.tool_context import ToolContext

# Default model to use if not specified
DEFAULT_MODEL = "gemini-2.0-flash"

# Global variable to store loaded HSN data
hsn_data = None


def load_hsn_data(file_path: str, tool_context: ToolContext = None) -> dict:
    """Loads HSN codes from the master Excel file.
    
    Args:
        file_path: Path to the Excel file containing HSN codes and descriptions.
        tool_context: Tool context for state management (optional).
        
    Returns:
        dict: Status of the operation and loaded data information.
    """
    global hsn_data
    
    try:
        # Check if file exists
        if not os.path.exists(file_path):
            return {
                "status": "error",
                "error_message": f"HSN master data file not found at {file_path}"
            }
        
        # Load Excel file
        df = pd.read_excel(file_path)
        
        # Check if required columns exist
        required_columns = ['HSNCode', 'Description']
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            return {
                "status": "error",
                "error_message": f"Missing required columns in HSN master data: {', '.join(missing_columns)}"
            }
            
        # Convert HSN codes to string format (for handling numeric codes stored as numbers)
        df['HSNCode'] = df['HSNCode'].astype(str)
        
        # Create a lookup dictionary for faster access
        code_dict = dict(zip(df['HSNCode'], df['Description']))
        
        # Store in global variable
        hsn_data = {
            "data": code_dict,
            "count": len(code_dict),
            "file_path": file_path,
            "load_time": pd.Timestamp.now().isoformat()
        }
        
        # Store in state if tool_context is provided
        if tool_context:
            tool_context.state["hsn_data"] = hsn_data
        
        return {
            "status": "success",
            "message": f"Successfully loaded {len(code_dict)} HSN codes from {file_path}",
            "code_count": len(code_dict)
        }
        
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Failed to load HSN master data: {str(e)}"
        }


def validate_hsn_format(code: str) -> dict:
    """Validates if an HSN code has the correct format.
    
    Args:
        code: The HSN code to validate.
        
    Returns:
        dict: Validation results with explanation.
    """
    # Check if code is empty
    if not code:
        return {
            "status": "error",
            "format_valid": False,
            "error_message": "HSN code is empty"
        }
    
    # Check if code contains only digits
    if not code.isdigit():
        return {
            "status": "error",
            "format_valid": False,
            "error_message": "HSN code must contain only digits"
        }
    
    # Check code length (typically 2, 4, 6, or 8 digits)
    valid_lengths = [2, 4, 6, 8]
    if len(code) not in valid_lengths:
        return {
            "status": "error",
            "format_valid": False,
            "error_message": f"HSN code length must be one of {valid_lengths}, found {len(code)}"
        }
    
    return {
        "status": "success",
        "format_valid": True,
        "message": "HSN code format is valid"
    }


def validate_hsn_existence(code: str, tool_context: ToolContext = None) -> dict:
    """Checks if an HSN code exists in the master database.
    
    Args:
        code: The HSN code to check.
        tool_context: Tool context for state management (optional).
        
    Returns:
        dict: Validation results with explanation.
    """
    global hsn_data
    
    # Get HSN data from state if available, otherwise use global variable
    data = None
    if tool_context and "hsn_data" in tool_context.state:
        data = tool_context.state["hsn_data"]["data"]
    elif hsn_data:
        data = hsn_data["data"]
    else:
        return {
            "status": "error",
            "exists_in_database": False,
            "error_message": "HSN database not loaded. Please load HSN data first."
        }
    
    # Check if code exists in database
    if code in data:
        return {
            "status": "success",
            "exists_in_database": True,
            "description": data[code],
            "message": f"HSN code exists: {data[code]}"
        }
    
    return {
        "status": "error",
        "exists_in_database": False,
        "error_message": "HSN code not found in database"
    }


def validate_hsn_hierarchy(code: str, tool_context: ToolContext = None) -> dict:
    """Validates the hierarchy of an HSN code by checking its parent levels.
    
    For an 8-digit code, checks if its 2, 4, and 6-digit parent codes exist.
    For a 6-digit code, checks if its 2 and 4-digit parent codes exist.
    For a 4-digit code, checks if its 2-digit parent code exists.
    
    Args:
        code: The HSN code to validate.
        tool_context: Tool context for state management (optional).
        
    Returns:
        dict: Validation results with explanation.
    """
    # Check if code has valid length and format first
    format_result = validate_hsn_format(code)
    if not format_result["format_valid"]:
        return {
            "status": "error",
            "hierarchy_valid": False,
            "error_message": "Invalid HSN code format. Cannot validate hierarchy."
        }
    
    # For 2-digit codes, there's no hierarchy to check
    if len(code) == 2:
        return {
            "status": "success",
            "hierarchy_valid": True,
            "message": "2-digit code. No parent hierarchy to validate."
        }
    
    # Define parent levels to check based on code length
    parent_levels = []
    if len(code) >= 4:
        parent_levels.append(2)
    if len(code) >= 6:
        parent_levels.append(4)
    if len(code) >= 8:
        parent_levels.append(6)
    
    # Check each parent level
    missing_parents = []
    for level in parent_levels:
        parent_code = code[:level]
        parent_result = validate_hsn_existence(parent_code, tool_context)
        
        if not parent_result.get("exists_in_database", False):
            missing_parents.append(parent_code)
    
    # Return results
    if missing_parents:
        return {
            "status": "error",
            "hierarchy_valid": False,
            "missing_parents": missing_parents,
            "error_message": f"Missing parent codes in hierarchy: {', '.join(missing_parents)}"
        }
    
    return {
        "status": "success",
        "hierarchy_valid": True,
        "message": "HSN code hierarchy is valid"
    }


def validate_hsn_code(code: str, tool_context: ToolContext = None) -> dict:
    """Performs comprehensive validation of an HSN code.
    
    Args:
        code: The HSN code to validate.
        tool_context: Tool context for state management (optional).
        
    Returns:
        dict: Comprehensive validation results.
    """
    # Normalize code (remove spaces, convert to string)
    code = str(code).strip()
    
    # Validate format
    format_result = validate_hsn_format(code)
    format_valid = format_result.get("format_valid", False)
    
    # If format is invalid, return early
    if not format_valid:
        return {
            "code": code,
            "valid": False,
            "format_valid": False,
            "exists_in_database": False,
            "hierarchy_valid": False,
            "error": format_result.get("error_message", "Invalid format")
        }
    
    # Validate existence in database
    existence_result = validate_hsn_existence(code, tool_context)
    exists_in_database = existence_result.get("exists_in_database", False)
    
    # Validate hierarchy
    hierarchy_result = validate_hsn_hierarchy(code, tool_context)
    hierarchy_valid = hierarchy_result.get("hierarchy_valid", False)
    
    # Combine results
    return {
        "code": code,
        "valid": format_valid and exists_in_database and hierarchy_valid,
        "format_valid": format_valid,
        "exists_in_database": exists_in_database,
        "hierarchy_valid": hierarchy_valid,
        "description": existence_result.get("description", "") if exists_in_database else "",
        "error": (
            hierarchy_result.get("error_message") if not hierarchy_valid else 
            existence_result.get("error_message") if not exists_in_database else 
            None
        )
    }


def validate_hsn_codes(codes: List[str], tool_context: ToolContext = None) -> dict:
    """Validates multiple HSN codes in batch.
    
    Args:
        codes: List of HSN codes to validate.
        tool_context: Tool context for state management (optional).
        
    Returns:
        dict: Validation results for all codes with summary.
    """
    if not codes:
        return {
            "status": "error",
            "error_message": "No HSN codes provided for validation"
        }
    
    results = []
    valid_count = 0
    
    for code in codes:
        result = validate_hsn_code(code, tool_context)
        results.append(result)
        
        if result.get("valid", False):
            valid_count += 1
    
    return {
        "status": "success",
        "results": results,
        "summary": {
            "total": len(codes),
            "valid": valid_count,
            "invalid": len(codes) - valid_count
        }
    }


def process_hsn_validation_request(request: Dict, tool_context: ToolContext = None) -> dict:
    """Processes an HSN validation request, handling both single and batch validation.
    
    Args:
        request: The validation request, containing either a single code or a list of codes.
        tool_context: Tool context for state management (optional).
        
    Returns:
        dict: Validation results.
    """
    # Check if HSN data is loaded
    global hsn_data
    data_source = None
    
    if tool_context and "hsn_data" in tool_context.state:
        data_source = tool_context.state["hsn_data"]
    elif hsn_data:
        data_source = hsn_data
    
    if not data_source:
        # Try to load the default HSN data file
        load_result = load_hsn_data("HSN_Master_Data.xlsx", tool_context)
        if load_result["status"] == "error":
            return {
                "status": "error",
                "error_message": "HSN database not loaded and default file not found"
            }
    
    # Process single code validation
    if "code" in request:
        code = request["code"]
        result = validate_hsn_code(code, tool_context)
        return {
            "status": "success",
            "results": [result],
            "summary": {
                "total": 1,
                "valid": 1 if result.get("valid", False) else 0,
                "invalid": 0 if result.get("valid", False) else 1
            }
        }
    
    # Process batch validation
    elif "codes" in request:
        codes = request["codes"]
        return validate_hsn_codes(codes, tool_context)
    
    else:
        return {
            "status": "error",
            "error_message": "Invalid request format. Please provide either 'code' or 'codes' field."
        }


# Define the HSN Validator Agent
hsn_validator_agent = Agent(
    name="hsn_validator_agent",
    model=DEFAULT_MODEL,
    description="An agent that validates Harmonized System Nomenclature (HSN) codes against a master database",
    instruction="""
    You are an HSN Code Validator Agent that helps users validate Harmonized System Nomenclature codes.
    
    You can:
    1. Validate if an HSN code has the correct format (numeric and correct length)
    2. Check if an HSN code exists in the master database
    3. Verify the hierarchical validity of an HSN code
    4. Process both single HSN codes and batches of codes
    
    When a user provides an HSN code or multiple codes:
    - Use the process_hsn_validation_request tool to validate the code(s)
    - Present the validation results in a clear, structured manner
    - For invalid codes, explain what makes them invalid
    - For valid codes, include their description from the master database
    
    If the HSN database needs to be loaded or refreshed, use the load_hsn_data tool.
    
    Always provide a summary for batch validations, showing the total count of valid and invalid codes.
    """,
    tools=[
        load_hsn_data,
        validate_hsn_format,
        validate_hsn_existence,
        validate_hsn_hierarchy,
        validate_hsn_code,
        validate_hsn_codes,
        process_hsn_validation_request
    ]
)


# For module-level execution
if __name__ == "__main__":
    print("HSN Validator Agent initialized")
    # Load HSN data from default location
    result = load_hsn_data("HSN_Master_Data.xlsx")
    print(result["message"] if result["status"] == "success" else result["error_message"])
