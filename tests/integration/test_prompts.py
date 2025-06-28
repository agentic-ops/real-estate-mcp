"""
Integration tests for MCP prompt templates
"""

import pytest
from unittest.mock import Mock

from prompts.prompt_templates import register_prompts


class TestPromptTemplates:
    """Test MCP prompt templates"""
    
    @pytest.fixture
    def mock_mcp(self):
        """Create a mock MCP server and register prompts"""
        mcp = Mock()
        prompts = {}
        
        def mock_prompt():
            def decorator(func):
                prompts[func.__name__] = func
                return func
            return decorator
        
        mcp.prompt = mock_prompt
        register_prompts(mcp)
        return prompts
    
    def test_property_analysis_prompt(self, mock_mcp):
        """Test property_analysis_prompt template"""
        result = mock_mcp['property_analysis_prompt']("PROP001")
        
        assert "PROP001" in result
        assert "Property Details and Features" in result
        assert "Market Context" in result
        assert "Area Analysis" in result
        assert "Investment Potential" in result
        assert "Pricing Strategy" in result
    
    def test_property_analysis_prompt_default(self, mock_mcp):
        """Test property_analysis_prompt with default parameter"""
        result = mock_mcp['property_analysis_prompt']()
        
        assert "PROP001" in result  # Default value
        assert "comprehensive report" in result
    
    def test_client_matching_prompt(self, mock_mcp):
        """Test client_matching_prompt template"""
        result = mock_mcp['client_matching_prompt']("CLI001")
        
        assert "CLI001" in result
        assert "client's profile" in result
        assert "property recommendations" in result
        assert "Budget alignment" in result
        assert "Location preferences" in result
    
    def test_client_matching_prompt_default(self, mock_mcp):
        """Test client_matching_prompt with default parameter"""
        result = mock_mcp['client_matching_prompt']()
        
        assert "CLI001" in result  # Default value
        assert "personalized property recommendations" in result
    
    def test_market_report_prompt(self, mock_mcp):
        """Test market_report_prompt template"""
        result = mock_mcp['market_report_prompt']("Downtown Riverside")
        
        assert "Downtown Riverside" in result
        assert "Market Overview" in result
        assert "Price Analysis" in result
        assert "Active Listings" in result
        assert "Recent Sales" in result
        assert "Demographics" in result
    
    def test_market_report_prompt_default(self, mock_mcp):
        """Test market_report_prompt with default parameter"""
        result = mock_mcp['market_report_prompt']()
        
        assert "Downtown Riverside" in result  # Default value
        assert "comprehensive market report" in result
    
    def test_agent_performance_prompt(self, mock_mcp):
        """Test agent_performance_prompt template"""
        result = mock_mcp['agent_performance_prompt']("AGT001")
        
        assert "AGT001" in result
        assert "Agent Profile" in result
        assert "Current Listings" in result
        assert "Sales Performance" in result
        assert "Client Base" in result
        assert "performance improvement" in result
    
    def test_agent_performance_prompt_default(self, mock_mcp):
        """Test agent_performance_prompt with default parameter"""
        result = mock_mcp['agent_performance_prompt']()
        
        assert "AGT001" in result  # Default value
        assert "performance analysis" in result
    
    def test_investment_analysis_prompt(self, mock_mcp):
        """Test investment_analysis_prompt template"""
        result = mock_mcp['investment_analysis_prompt']("500000", "1000000")
        
        assert "500000" in result
        assert "1000000" in result
        assert "investment opportunities" in result
        assert "Rental Market Analysis" in result
        assert "ROI Analysis" in result
        assert "Cash Flow Projections" in result
    
    def test_investment_analysis_prompt_default(self, mock_mcp):
        """Test investment_analysis_prompt with default parameters"""
        result = mock_mcp['investment_analysis_prompt']()
        
        assert "500000" in result  # Default min
        assert "1000000" in result  # Default max
        assert "investment opportunities" in result
    
    def test_all_prompts_return_strings(self, mock_mcp):
        """Test that all prompts return strings"""
        prompts_to_test = [
            ('property_analysis_prompt', []),
            ('client_matching_prompt', []),
            ('market_report_prompt', []),
            ('agent_performance_prompt', []),
            ('investment_analysis_prompt', [])
        ]
        
        for prompt_name, args in prompts_to_test:
            result = mock_mcp[prompt_name](*args)
            assert isinstance(result, str)
            assert len(result) > 0
    
    def test_prompts_contain_instructions(self, mock_mcp):
        """Test that all prompts contain proper analysis instructions"""
        prompts_to_test = [
            'property_analysis_prompt',
            'client_matching_prompt', 
            'market_report_prompt',
            'agent_performance_prompt',
            'investment_analysis_prompt'
        ]
        
        for prompt_name in prompts_to_test:
            result = mock_mcp[prompt_name]()
            assert "analyze" in result.lower() or "analysis" in result.lower()
            assert len(result.split('\n')) > 5  # Multi-line instructions
    
    def test_prompts_with_custom_parameters(self, mock_mcp):
        """Test prompts with various custom parameters"""
        # Test property analysis with different property ID
        result = mock_mcp['property_analysis_prompt']("CUSTOM_PROP")
        assert "CUSTOM_PROP" in result
        
        # Test client matching with different client ID
        result = mock_mcp['client_matching_prompt']("CUSTOM_CLIENT")
        assert "CUSTOM_CLIENT" in result
        
        # Test market report with different area
        result = mock_mcp['market_report_prompt']("Custom Area")
        assert "Custom Area" in result
        
        # Test agent performance with different agent ID
        result = mock_mcp['agent_performance_prompt']("CUSTOM_AGENT")
        assert "CUSTOM_AGENT" in result
        
        # Test investment analysis with different budget
        result = mock_mcp['investment_analysis_prompt']("750000", "1500000")
        assert "750000" in result
        assert "1500000" in result 