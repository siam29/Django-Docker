import pytest
from django.contrib.auth.models import User
from your_app.models import Location, Accommodation

@pytest.mark.django_db
def test_location_creation():
    location = Location.objects.create(
        id="001",
        title="New York",
        country_code="US",
        location_type="city",
    )
    assert location.title == "New York"
    assert location.country_code == "US"
    assert location.location_type == "city"

@pytest.mark.django_db
def test_accommodation_creation():
    user = User.objects.create_user(username="testuser", password="password")
    location = Location.objects.create(
        id="001",
        title="New York",
        country_code="US",
        location_type="city"
    )
    accommodation = Accommodation.objects.create(
        id="A001",
        title="Luxury Villa",
        country_code="US",
        bedroom_count=3,
        usd_rate=200.00,
        location=location,
        user=user
    )
    assert accommodation.title == "Luxury Villa"
    assert accommodation.bedroom_count == 3
    assert accommodation.usd_rate == 200.00
    assert accommodation.location.title == "New York"
    assert accommodation.user.username == "testuser"
