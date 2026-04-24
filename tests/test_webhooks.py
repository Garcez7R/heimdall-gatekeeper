"""Tests for webhook integration, triggers, and MITRE display (PHASE 2-3)."""
from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from backend.api.main import app
from backend.storage.webhook_storage import (
    create_webhook,
    delete_webhook,
    get_active_webhooks,
    get_webhook,
    list_webhooks,
)


client = TestClient(app)


@pytest.fixture
def db_setup():
    """Setup test database (assumes fresh DB for each test)."""
    # Clear webhooks by deleting all (would need DB cleanup in real tests)
    yield
    # Cleanup can go here if needed


def test_create_webhook_in_storage():
    """Test creating webhooks in persistent storage."""
    webhook = create_webhook(
        webhook_id="wh_test001",
        name="Test Webhook",
        url="https://example.com/webhook",
        platform="generic",
        severity_filter="medium",
    )
    
    assert webhook is not None
    assert webhook["name"] == "Test Webhook"
    assert webhook["platform"] == "generic"


def test_get_webhook_from_storage():
    """Test retrieving a webhook from storage."""
    create_webhook(
        webhook_id="wh_test002",
        name="Retrieve Test",
        url="https://example.com/test",
        platform="discord",
    )
    
    webhook = get_webhook("wh_test002")
    assert webhook is not None
    assert webhook["name"] == "Retrieve Test"


def test_list_webhooks_from_storage():
    """Test listing webhooks from storage."""
    # Create a few webhooks
    for i in range(3):
        create_webhook(
            webhook_id=f"wh_list_{i:03d}",
            name=f"List Test {i}",
            url=f"https://example.com/{i}",
            platform="generic",
        )
    
    webhooks = list_webhooks()
    assert len(webhooks) >= 3


def test_get_active_webhooks_filtering():
    """Test that get_active_webhooks filters by severity."""
    create_webhook(
        webhook_id="wh_sev_high",
        name="High Severity Only",
        url="https://example.com/high",
        platform="generic",
        severity_filter="high",
        active=True,
    )
    create_webhook(
        webhook_id="wh_sev_low",
        name="Low Severity",
        url="https://example.com/low",
        platform="generic",
        severity_filter="low",
        active=True,
    )
    
    # Get webhooks for high severity alert
    high_webhooks =get_active_webhooks(severity="high")
    assert len(high_webhooks) >= 1
    
    # Get webhooks for low severity alert
    low_webhooks = get_active_webhooks(severity="low")
    assert len(low_webhooks) >= 1


def test_delete_webhook():
    """Test deleting a webhook from storage."""
    create_webhook(
        webhook_id="wh_delete_test",
        name="To Delete",
        url="https://example.com/delete",
        platform="generic",
    )
    
    success = delete_webhook("wh_delete_test")
    assert success is True
    
    deleted = get_webhook("wh_delete_test")
    assert deleted is None


def test_list_webhooks_endpoint():
    """Test the /api/webhooks list endpoint."""
    response = client.get("/api/webhooks")
    assert response.status_code == 200
    data = response.json()
    assert "webhooks" in data
    assert "total" in data


def test_create_webhook_via_api():
    """Test creating webhook via REST API."""
    webhook_data = {
        "name": "API Test Webhook",
        "url": "https://example.com/webhook",
        "platform": "discord",
        "active": True,
        "severity_filter": "medium",
    }
    response = client.post("/api/admin/webhooks", json=webhook_data)
    assert response.status_code == 200
    data = response.json()
    assert data["created"] is True
    assert "id" in data


def test_create_webhook_validates_platform():
    """Test that webhook creation validates platform."""
    webhook_data = {
        "name": "Invalid Platform",
        "url": "https://example.com/test",
        "platform": "invalid_platform",
        "active": True,
        "severity_filter": "low",
    }
    response = client.post("/api/admin/webhooks", json=webhook_data)
    assert response.status_code == 422


def test_mitre_in_alerts_table():
    """Test that MITRE tactics display in alerts."""
    response = client.get("/")
    assert response.status_code == 200
    html = response.text
    assert "MITRE ATT&CK" in html
    assert "alerts-table" in html


def test_advanced_detection_debug_endpoint():
    """Test that advanced detection debug endpoints exist."""
    response = client.post(
        "/api/debug/test-behavior",
        json={
            "name": "Brute Force Detection",
            "description": "Detect brute force attempts",
            "stages": ["auth_failure", "auth_failure", "auth_failure", "auth_success"],
            "time_window_minutes": 5,
            "group_by": "user",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert "rule_name" in data
    assert "detections" in data


def test_ecs_normalization_debug_endpoint():
    """Test that ECS normalization debug endpoint works."""
    raw_event = {
        "source": "test-system",
        "event_type": "authentication",
        "title": "Auth attempt",
        "severity": "medium",
        "ip_address": "192.168.1.100",
    }
    response = client.post("/api/debug/normalize-ecs", json=raw_event)
    assert response.status_code == 200
    data = response.json()
    assert "input" in data
    assert "output" in data
    assert data["status"] == "success"


def test_login_endpoint_valid_credentials():
    """Test /api/auth/login with valid credentials."""
    response = client.post(
        "/api/auth/login",
        json={"username": "admin", "password": "admin123"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "Bearer"
    assert data["expires_in"] > 0


def test_login_endpoint_invalid_credentials():
    """Test /api/auth/login with invalid credentials."""
    response = client.post(
        "/api/auth/login",
        json={"username": "admin", "password": "wrong_password"},
    )
    assert response.status_code == 401
    data = response.json()
    assert "detail" in data


def test_login_with_analyst_credentials():
    """Test /api/auth/login with analyst credentials."""
    response = client.post(
        "/api/auth/login",
        json={"username": "analyst", "password": "analyst123"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "Bearer"

