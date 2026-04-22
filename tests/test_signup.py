def test_signup_adds_participant_when_activity_exists_and_has_space(client):
    # Arrange
    activity_name = "Chess Club"
    email = "new.student@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})
    activities_response = client.get("/activities")
    participants = activities_response.json()[activity_name]["participants"]

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity_name}"
    assert email in participants


def test_signup_returns_400_when_student_is_already_signed_up(client):
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_signup_returns_404_when_activity_does_not_exist(client):
    # Arrange
    activity_name = "Unknown Club"
    email = "student@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_returns_400_when_activity_is_full(client):
    # Arrange
    activity_name = "Tennis Club"

    for index in range(8):
        email = f"fill{index}@mergington.edu"
        client.post(f"/activities/{activity_name}/signup", params={"email": email})

    extra_email = "overflow@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": extra_email})

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Activity is full"
