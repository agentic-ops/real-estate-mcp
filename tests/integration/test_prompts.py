"""
Integration tests for MCP prompt templates (refactored modular structure)
"""

from unittest.mock import Mock

import pytest

from prompts import register_all_prompts
from prompts.agent_prompts import register_agent_prompts
from prompts.client_prompts import register_client_prompts
from prompts.market_prompts import register_market_prompts
from prompts.property_prompts import register_property_prompts


class TestPromptTemplates:
    """Test MCP prompt templates with new modular structure"""

    @pytest.fixture
    def mock_mcp(self):
        """Create a mock MCP server and register all prompts"""
        mcp = Mock()
        prompts = {}

        def mock_prompt():
            def decorator(func):
                prompts[func.__name__] = func
                return func

            return decorator

        mcp.prompt = mock_prompt
        register_all_prompts(mcp)
        return prompts

    @pytest.fixture
    def mock_mcp_property(self):
        """Create a mock MCP server with only property prompts"""
        mcp = Mock()
        prompts = {}

        def mock_prompt():
            def decorator(func):
                prompts[func.__name__] = func
                return func

            return decorator

        mcp.prompt = mock_prompt
        register_property_prompts(mcp)
        return prompts

    @pytest.fixture
    def mock_mcp_client(self):
        """Create a mock MCP server with only client prompts"""
        mcp = Mock()
        prompts = {}

        def mock_prompt():
            def decorator(func):
                prompts[func.__name__] = func
                return func

            return decorator

        mcp.prompt = mock_prompt
        register_client_prompts(mcp)
        return prompts

    @pytest.fixture
    def mock_mcp_market(self):
        """Create a mock MCP server with only market prompts"""
        mcp = Mock()
        prompts = {}

        def mock_prompt():
            def decorator(func):
                prompts[func.__name__] = func
                return func

            return decorator

        mcp.prompt = mock_prompt
        register_market_prompts(mcp)
        return prompts

    @pytest.fixture
    def mock_mcp_agent(self):
        """Create a mock MCP server with only agent prompts"""
        mcp = Mock()
        prompts = {}

        def mock_prompt():
            def decorator(func):
                prompts[func.__name__] = func
                return func

            return decorator

        mcp.prompt = mock_prompt
        register_agent_prompts(mcp)
        return prompts

    # Property Prompts Tests
    def test_property_analysis_prompt(self, mock_mcp_property):
        """Test property_analysis_prompt template"""
        result = mock_mcp_property["property_analysis_prompt"]("PROP001")

        assert "PROP001" in result
        assert "Property Details and Features" in result
        assert "Market Context" in result
        assert "Area Analysis" in result
        assert "Investment Potential" in result
        assert "Pricing Strategy" in result

    def test_property_analysis_prompt_default(self, mock_mcp_property):
        """Test property_analysis_prompt with default parameter"""
        result = mock_mcp_property["property_analysis_prompt"]()

        assert "PROP001" in result  # Default value
        assert "comprehensive report" in result

    def test_property_comparison_prompt(self, mock_mcp_property):
        """Test property_comparison_prompt template"""
        result = mock_mcp_property["property_comparison_prompt"]("PROP001,PROP002")

        assert "PROP001" in result
        assert "PROP002" in result
        assert "Side-by-Side Property Details" in result
        assert "Financial Comparison" in result
        assert "Location and Area Comparison" in result

    # Client Prompts Tests
    def test_client_matching_prompt(self, mock_mcp_client):
        """Test client_matching_prompt template"""
        result = mock_mcp_client["client_matching_prompt"]("CLI001")

        assert "CLI001" in result
        assert (
            "client's profile" in result.lower() or "Client Profile Analysis" in result
        )
        assert (
            "property recommendations" in result.lower()
            or "Property Recommendations" in result
        )
        assert "Budget" in result
        assert "preferences" in result.lower() or "Preference" in result

    def test_client_matching_prompt_default(self, mock_mcp_client):
        """Test client_matching_prompt with default parameter"""
        result = mock_mcp_client["client_matching_prompt"]()

        assert "CLI001" in result  # Default value
        assert "personalized" in result.lower()

    def test_client_consultation_prompt(self, mock_mcp_client):
        """Test client_consultation_prompt template"""
        result = mock_mcp_client["client_consultation_prompt"]("CLI001", "initial")

        assert "CLI001" in result
        assert "initial" in result
        assert "consultation" in result.lower() or "Consultation" in result
        assert "needs assessment" in result.lower() or "Needs Assessment" in result

    def test_client_feedback_analysis_prompt(self, mock_mcp_client):
        """Test client_feedback_analysis_prompt template"""
        result = mock_mcp_client["client_feedback_analysis_prompt"]("CLI001")

        assert "CLI001" in result
        assert "feedback" in result.lower() or "Feedback" in result
        assert "analysis" in result.lower() or "Analysis" in result

    # Market Prompts Tests
    def test_market_report_prompt(self, mock_mcp_market):
        """Test market_report_prompt template"""
        result = mock_mcp_market["market_report_prompt"]("Downtown Riverside")

        assert "Downtown Riverside" in result
        assert "Market Overview" in result
        assert "Price Analysis" in result
        assert "Active Listings" in result or "Inventory Analysis" in result
        assert "Recent Sales" in result or "Transaction Analysis" in result
        assert "Demographics" in result

    def test_market_report_prompt_default(self, mock_mcp_market):
        """Test market_report_prompt with default parameter"""
        result = mock_mcp_market["market_report_prompt"]()

        assert "Downtown Riverside" in result  # Default value
        assert (
            "comprehensive market report" in result.lower()
            or "Market Analysis Report" in result
        )

    def test_investment_analysis_prompt(self, mock_mcp_market):
        """Test investment_analysis_prompt template"""
        result = mock_mcp_market["investment_analysis_prompt"]("500000", "1000000")

        assert "500000" in result
        assert "1000000" in result
        assert (
            "investment opportunities" in result.lower()
            or "Investment Analysis" in result
        )
        assert "Rental Market" in result or "rental" in result.lower()
        assert "ROI" in result
        assert "Cash Flow" in result

    def test_investment_analysis_prompt_default(self, mock_mcp_market):
        """Test investment_analysis_prompt with default parameters"""
        result = mock_mcp_market["investment_analysis_prompt"]()

        assert "500000" in result  # Default min
        assert "1000000" in result  # Default max
        assert "investment opportunities" in result.lower() or "Investment" in result

    def test_comparative_market_analysis_prompt(self, mock_mcp_market):
        """Test comparative_market_analysis_prompt template"""
        result = mock_mcp_market["comparative_market_analysis_prompt"](
            "Downtown Riverside,Woodcrest"
        )

        assert "Downtown Riverside" in result
        assert "Woodcrest" in result
        assert "comparative" in result.lower() or "Comparative" in result
        assert "comparison" in result.lower() or "Comparison" in result

    # Agent Prompts Tests
    def test_agent_performance_prompt(self, mock_mcp_agent):
        """Test agent_performance_prompt template"""
        result = mock_mcp_agent["agent_performance_prompt"]("AGT001")

        assert "AGT001" in result
        assert "Agent Profile" in result
        assert "performance" in result.lower() or "Performance" in result
        assert "Sales Performance" in result or "sales" in result.lower()
        assert "Client" in result

    def test_agent_performance_prompt_default(self, mock_mcp_agent):
        """Test agent_performance_prompt with default parameter"""
        result = mock_mcp_agent["agent_performance_prompt"]()

        assert "AGT001" in result  # Default value
        assert "performance analysis" in result.lower() or "Performance" in result

    def test_agent_marketing_strategy_prompt(self, mock_mcp_agent):
        """Test agent_marketing_strategy_prompt template"""
        result = mock_mcp_agent["agent_marketing_strategy_prompt"](
            "AGT001", "lead_generation"
        )

        assert "AGT001" in result
        assert "lead_generation" in result.lower() or "Lead Generation" in result
        assert "marketing" in result.lower() or "Marketing" in result
        assert "strategy" in result.lower() or "Strategy" in result

    def test_agent_training_development_prompt(self, mock_mcp_agent):
        """Test agent_training_development_prompt template"""
        result = mock_mcp_agent["agent_training_development_prompt"](
            "AGT001", "negotiation"
        )

        assert "AGT001" in result
        assert "negotiation" in result.lower() or "Negotiation" in result
        assert "training" in result.lower() or "Training" in result
        assert "development" in result.lower() or "Development" in result

    # Integration Tests
    def test_all_prompts_registered(self, mock_mcp):
        """Test that all prompts are registered with the central function"""
        expected_prompts = [
            "property_analysis_prompt",
            "property_comparison_prompt",
            "client_matching_prompt",
            "client_consultation_prompt",
            "client_feedback_analysis_prompt",
            "market_report_prompt",
            "investment_analysis_prompt",
            "comparative_market_analysis_prompt",
            "agent_performance_prompt",
            "agent_marketing_strategy_prompt",
            "agent_training_development_prompt",
        ]

        for prompt_name in expected_prompts:
            assert prompt_name in mock_mcp, f"Prompt {prompt_name} not registered"

    def test_all_prompts_return_strings(self, mock_mcp):
        """Test that all prompts return strings"""
        prompts_to_test = [
            ("property_analysis_prompt", []),
            ("property_comparison_prompt", []),
            ("client_matching_prompt", []),
            ("client_consultation_prompt", []),
            ("client_feedback_analysis_prompt", []),
            ("market_report_prompt", []),
            ("investment_analysis_prompt", []),
            ("comparative_market_analysis_prompt", []),
            ("agent_performance_prompt", []),
            ("agent_marketing_strategy_prompt", []),
            ("agent_training_development_prompt", []),
        ]

        for prompt_name, args in prompts_to_test:
            result = mock_mcp[prompt_name](*args)
            assert isinstance(
                result, str
            ), f"Prompt {prompt_name} did not return a string"
            assert len(result) > 0, f"Prompt {prompt_name} returned empty string"

    def test_prompts_contain_instructions(self, mock_mcp):
        """Test that all prompts contain proper analysis instructions"""
        prompts_to_test = [
            "property_analysis_prompt",
            "property_comparison_prompt",
            "client_matching_prompt",
            "client_consultation_prompt",
            "client_feedback_analysis_prompt",
            "market_report_prompt",
            "investment_analysis_prompt",
            "comparative_market_analysis_prompt",
            "agent_performance_prompt",
            "agent_marketing_strategy_prompt",
            "agent_training_development_prompt",
        ]

        for prompt_name in prompts_to_test:
            result = mock_mcp[prompt_name]()
            assert (
                "analyze" in result.lower()
                or "analysis" in result.lower()
                or "create" in result.lower()
                or "generate" in result.lower()
            )
            assert (
                len(result.split("\n")) > 5
            ), f"Prompt {prompt_name} should have multi-line instructions"

    def test_prompts_with_custom_parameters(self, mock_mcp):
        """Test prompts with various custom parameters"""
        # Test property analysis with different property ID
        result = mock_mcp["property_analysis_prompt"]("CUSTOM_PROP")
        assert "CUSTOM_PROP" in result

        # Test property comparison with multiple properties
        result = mock_mcp["property_comparison_prompt"]("PROP1,PROP2,PROP3")
        assert "PROP1" in result
        assert "PROP2" in result
        assert "PROP3" in result

        # Test client matching with different client ID
        result = mock_mcp["client_matching_prompt"]("CUSTOM_CLIENT")
        assert "CUSTOM_CLIENT" in result

        # Test market report with different area
        result = mock_mcp["market_report_prompt"]("Custom Area")
        assert "Custom Area" in result

        # Test agent performance with different agent ID
        result = mock_mcp["agent_performance_prompt"]("CUSTOM_AGENT")
        assert "CUSTOM_AGENT" in result

        # Test investment analysis with different budget
        result = mock_mcp["investment_analysis_prompt"]("750000", "1500000")
        assert "750000" in result
        assert "1500000" in result
