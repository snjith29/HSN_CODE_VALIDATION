"""
HSN Validator Agent package.

This package provides a Google ADK-based agent for validating
Harmonized System Nomenclature (HSN) codes.
"""

from .agent import hsn_validator_agent

# Export the agent as the primary interface
agent = hsn_validator_agent
