def test_get_activities_returns_all_activities_with_expected_structure(client):
    # Arrange
    expected_activity_count = 9
    required_keys = {"description", "schedule", "max_participants", "participants"}

    # Act
    response = client.get("/activities")
    payload = response.json()

    # Assert
    assert response.status_code == 200
    assert isinstance(payload, dict)
    assert len(payload) == expected_activity_count

    for activity_name, details in payload.items():
        assert isinstance(activity_name, str)
        assert required_keys.issubset(details.keys())
        assert isinstance(details["participants"], list)
