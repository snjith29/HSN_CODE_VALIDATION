"""
Demo script to test the HSN Code Validator Agent.

This script demonstrates how to use the HSN Validator Agent
in both interactive and programmatic modes.
"""

import os
import json
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

# Import the agent - changed the import to reference the local module
from agent import hsn_validator_agent

# Ensure sample data exists
from create_sample_data import create_sample_data

# Constants
APP_NAME = "hsn_validator_demo"
USER_ID = "demo_user"
SESSION_ID = "demo_session"

def setup_environment():
    """
    Sets up the environment for testing the HSN Validator Agent.
    
    Returns:
        tuple: (session_service, runner) prepared for running the agent
    """
    # Create sample data if it doesn't exist
    if not os.path.exists("HSN_Master_Data.xlsx"):
        create_sample_data()
        print("Created sample HSN master data file for testing")
    
    # Create session and runner
    session_service = InMemorySessionService()
    session = session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID
    )
    
    # Create the runner
    runner = Runner(
        agent=hsn_validator_agent,
        app_name=APP_NAME,
        session_service=session_service
    )
    
    return session_service, runner

def run_validation(runner, query):
    """
    Runs the HSN validation with the given query.
    
    Args:
        runner: The ADK runner
        query: The validation query (string or dict)
    """
    # Convert query to Content object if it's a dict or string
    if isinstance(query, dict):
        content = types.Content(
            role='user',
            parts=[types.Part(text=json.dumps(query))]
        )
    else:
        content = types.Content(
            role='user',
            parts=[types.Part(text=query)]
        )
    
    # Run the agent
    events = runner.run(
        user_id=USER_ID,
        session_id=SESSION_ID,
        new_message=content
    )
    
    # Print agent responses
    for event in events:
        if event.is_final_response():
            final_response = event.content.parts[0].text
            print("\nAgent Response:")
            print(f"{final_response}")
            return final_response

def demo_single_validation(runner):
    """Demonstrates validation of a single HSN code."""
    print("\n=== Single HSN Code Validation ===")
    
    # Test a valid HSN code
    valid_query = {"code": "85171290"}
    print(f"\nValidating: {valid_query}")
    run_validation(runner, valid_query)
    
    # Test an invalid HSN code (incorrect format)
    invalid_format_query = {"code": "123456789"}
    print(f"\nValidating: {invalid_format_query}")
    run_validation(runner, invalid_format_query)
    
    # Test a code with valid format but not in database
    non_existent_query = {"code": "12345678"}
    print(f"\nValidating: {non_existent_query}")
    run_validation(runner, non_existent_query)

def demo_batch_validation(runner):
    """Demonstrates validation of multiple HSN codes in batch."""
    print("\n=== Batch HSN Code Validation ===")
    
    # Test a batch of mixed valid and invalid codes
    batch_query = {
        "codes": [
            "85171290",  # Valid
            "123456789",  # Invalid format (too long)
            "12345678",   # Invalid (not in database)
            "3004"        # Valid
        ]
    }
    
    print(f"\nValidating batch: {batch_query}")
    run_validation(runner, batch_query)

def demo_text_query(runner):
    """Demonstrates using natural language to validate HSN codes."""
    print("\n=== Natural Language Query ===")
    
    # Test natural language query
    nl_query = "Please validate the HSN code 85171290 for mobile phones"
    print(f"\nQuery: {nl_query}")
    run_validation(runner, nl_query)
    
    # Test multiple codes in natural language
    multi_nl_query = "I need to check these HSN codes: 3004, 84713010, and 123456789"
    print(f"\nQuery: {multi_nl_query}")
    run_validation(runner, multi_nl_query)

def interactive_mode(runner):
    """
    Enters an interactive mode where the user can enter queries.
    """
    print("\n=== Interactive Mode ===")
    print("Enter HSN codes or queries. Type 'exit' to quit.")
    
    while True:
        user_input = input("\nYour query: ")
        
        if user_input.lower() in ('exit', 'quit', 'q'):
            break
            
        run_validation(runner, user_input)

def main():
    """Main entry point for the demo."""
    print("HSN Code Validator Agent Demo")
    print("==============================")
    
    # Setup
    _, runner = setup_environment()
    
    # Run demonstrations
    demo_single_validation(runner)
    demo_batch_validation(runner)
    demo_text_query(runner)
    
    # Interactive mode
    interactive_mode(runner)
    
    print("\nDemo completed. Thank you for using the HSN Validator Agent!")

if __name__ == "__main__":
    main()
