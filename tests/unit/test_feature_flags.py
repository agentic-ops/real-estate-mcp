"""Unit tests for the category-level feature flags."""

import pytest

import feature_flags


class TestFeatureFlags:
    def test_all_enabled_by_default(self, monkeypatch):
        # Ensure no category env vars are set.
        for env_name in feature_flags.TOOL_CATEGORIES.values():
            monkeypatch.delenv(env_name, raising=False)
        states = feature_flags.enabled_categories()
        assert all(states.values())
        assert feature_flags.disabled_categories() == []

    def test_disable_single_category(self, monkeypatch):
        monkeypatch.setenv("REALESTATE_MCP_ENABLE_MORTGAGE", "false")
        assert feature_flags.is_category_enabled("mortgage") is False
        assert feature_flags.is_category_enabled("valuation") is True
        assert "mortgage" in feature_flags.disabled_categories()

    @pytest.mark.parametrize(
        "value,expected",
        [
            ("false", False),
            ("0", False),
            ("no", False),
            ("off", False),
            ("true", True),
            ("1", True),
            ("yes", True),
            ("on", True),
        ],
    )
    def test_bool_parsing(self, monkeypatch, value, expected):
        monkeypatch.setenv("REALESTATE_MCP_ENABLE_INTEGRATIONS", value)
        assert feature_flags.is_category_enabled("integrations") is expected

    def test_unknown_category_raises(self):
        with pytest.raises(KeyError):
            feature_flags.is_category_enabled("does_not_exist")

    def test_categories_cover_expected_groups(self):
        expected = {
            "property",
            "agent",
            "market",
            "client",
            "area",
            "mortgage",
            "valuation",
            "document",
            "analysis_queue",
            "integrations",
            "system",
        }
        assert set(feature_flags.TOOL_CATEGORIES) == expected
