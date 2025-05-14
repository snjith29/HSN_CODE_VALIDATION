# HSN Code Validator Agent

This intelligent agent validates Harmonized System Nomenclature (HSN) codes against a master database. Built using Google's Agent Development Kit (ADK), it provides a robust solution for HSN code verification in taxation and international trade applications.

## Features

- **Format Validation**: Verifies if the HSN code follows the correct format (numeric, proper length)
- **Existence Validation**: Checks if the HSN code exists in the master database
- **Hierarchical Validation**: For 8-digit codes, checks presence of parent levels (2, 4, and 6-digit prefixes)
- **Batch Processing**: Ability to validate multiple HSN codes in a single request
- **Detailed Responses**: Provides comprehensive validation results with status and descriptions

## Setup Instructions

1. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Ensure your HSN master data file (HSN_Master_Data.xlsx) is in the correct format with columns:
   - HSNCode: The HSN code (as string or number)
   - Description: Description of the item/category

3. Run the agent:
   ```
   python -m google.adk run hsn_validator_agent
   ```

## Usage Examples

Single code validation:
```json
{
  "code": "85171290"
}
```

Multiple code validation:
```json
{
  "codes": ["85171290", "3004", "0123456789"]
}
```

## Response Format

```json
{
  "results": [
    {
      "code": "85171290",
      "valid": true,
      "format_valid": true,
      "exists_in_database": true,
      "hierarchy_valid": true,
      "description": "Mobile Phones"
    }
  ],
  "summary": {
    "total": 1,
    "valid": 1,
    "invalid": 0
  }
}
```

## Architecture

This agent is built using Google's Agent Development Kit (ADK) and follows the agentic approach to AI development. It leverages a multi-component architecture with function tools, state management, and LLM-based decision making.
