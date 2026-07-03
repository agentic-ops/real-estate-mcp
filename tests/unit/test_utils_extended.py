"""Unit tests for the utils additions: stats, singleton, and audit."""

import logging

from utils import (
    RealEstateDataManager,
    audit,
    data_manager,
    get_data_manager,
)


class TestStats:
    def test_stats_shape(self):
        stats = data_manager.stats()
        assert set(stats) == {
            "properties",
            "agents",
            "clients",
            "recent_sales",
            "areas",
        }
        assert all(isinstance(v, int) for v in stats.values())

    def test_stats_reflect_seed_data(self):
        stats = data_manager.stats()
        # Seed data ships with 50 enriched listings and 5 areas.
        assert stats["properties"] >= 1
        assert stats["areas"] >= 1


class TestSingleton:
    def test_get_data_manager_is_singleton(self):
        assert get_data_manager() is get_data_manager()

    def test_singleton_matches_module_global(self):
        assert get_data_manager() is data_manager

    def test_returns_data_manager_instance(self):
        assert isinstance(get_data_manager(), RealEstateDataManager)


class TestAudit:
    def test_audit_emits_log(self, caplog):
        with caplog.at_level(logging.INFO, logger="real_estate_mcp.utils"):
            audit("unit_test_event", key="value", number=42)
        assert any("unit_test_event" in message for message in caplog.messages)

    def test_audit_no_details(self, caplog):
        with caplog.at_level(logging.INFO, logger="real_estate_mcp.utils"):
            audit("bare_event")
        assert any("bare_event" in message for message in caplog.messages)
