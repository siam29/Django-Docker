import pytest
from django.urls import reverse
from django.contrib.messages import get_messages
from django.test import Client
from django.db import IntegrityError



from django.contrib.auth.models import User
from django.core.exceptions import ValidationError  # Import ValidationError
from django.contrib.gis.geos import Point  # Import Point for geospatial data
from properties.models import Location, Accommodation

# Test for Location creation with valid center field
@pytest.mark.django_db
def test_location_creation():
    # Create a valid Point for the 'center' field (Longitude, Latitude for New York)
    center_point = Point(-74.0060, 40.7128)  # New York coordinates

    location = Location.objects.create(
        id="001",
        title="New York",
        country_code="US",
        location_type="city",
        center=center_point  # Providing the valid center
    )

    # Test assertions
    assert location.title == "New York"
    assert location.country_code == "US"
    assert location.location_type == "city"
    assert location.center == center_point  # Check that center is correctly set

# Test for Accommodation creation with valid location and center
@pytest.mark.django_db
def test_accommodation_creation_with_center():
    user = User.objects.create_user(username="testuser", password="password")

    # Create a valid Location with a valid center
    location = Location.objects.create(
        id="001",
        title="New York",
        country_code="US",
        location_type="city",
        center=Point(-74.0060, 40.7128)  # Providing the valid center
    )

    # Create the accommodation with valid center
    accommodation = Accommodation.objects.create(
        id="A002",
        title="Beach House",
        country_code="US",
        bedroom_count=2,
        usd_rate=150.00,
        user=user,
        location=location,
        center=Point(-74.0060, 40.7128)  # Add a valid center here too
    )

    # Test assertions
    assert accommodation.title == "Beach House"
    assert accommodation.location.title == "New York"
    assert accommodation.center.x == -74.0060  # Validate the longitude
    assert accommodation.center.y == 40.7128  # Validate the latitude

# Test for Accommodation with review score range issue (set review_score to an invalid value)
@pytest.mark.django_db
def test_accommodation_review_score_range():
    user = User.objects.create_user(username="testuser", password="password")
    
    # Create a valid Location
    location = Location.objects.create(
        id="001",
        title="New York",
        country_code="US",
        location_type="city",
        center=Point(-74.0060, 40.7128)  # New York coordinates
    )
    
    # Create accommodation with invalid review score (should raise error)
    accommodation = Accommodation(
        id="A003",
        title="Mountain Retreat",
        country_code="US",
        bedroom_count=1,
        usd_rate=120.00,
        location=location,
        user=user,
        review_score=6.0,  # Invalid review score above max of 5.0
        center=Point(-74.0060, 40.7128)  # Valid center
    )
    
    # Trigger validation
    with pytest.raises(ValidationError):
        accommodation.full_clean()  # This explicitly triggers the validation

# Test for Location creation with missing center (should raise an error)
@pytest.mark.django_db
def test_location_missing_center():
    # Try to create a Location without a 'center' (Point), this should raise an error
    with pytest.raises(IntegrityError):  # Expecting database-level integrity error due to missing 'center'
        Location.objects.create(
            id="006",
            title="Test Location",
            country_code="US",
            location_type="city"
        )

# Test for the 'home' view
@pytest.mark.django_db
def test_home_view():
    # Create a test client
    client = Client()

    # Send a GET request to the home page
    response = client.get(reverse('home'))  # Assuming 'home' is the URL name

    # Assert that the response contains the expected text
    assert response.status_code == 200
    assert response.content.decode() == "Hello"


# Test for the 'signup' view

# Test for the 'signup' view
@pytest.mark.django_db
class TestSignupView:
    
    # Test GET request for the signup page (empty form)
    def test_signup_get(self):
        client = Client()

        # Send a GET request to the signup page
        response = client.get(reverse('signup'))  # Assuming 'signup' is the URL name

        # Assert that the response is successful and contains the signup form
        assert response.status_code == 200
        assert 'form' in response.context  # The form should be in the context

    # Test POST request with valid form data
    
    # Test POST request with invalid form data
    def test_signup_post_invalid(self):
        client = Client()

        # Prepare invalid data for the signup form (passwords don't match)
        invalid_data = {
            'username': 'testuser',
            'password1': 'password123',
            'password2': 'wrongpassword',
            'email': 'testuser@example.com',
        }

        # Send a POST request with invalid data
        response = client.post(reverse('signup'), data=invalid_data)

        # Assert that the response contains validation errors
        assert response.status_code == 200  # Page should reload with form errors
        assert 'form' in response.context  # The form should be in the context
        assert len(response.context['form'].errors) > 0  # There should be form errors



    def signup(request):
        if request.method == 'POST':
            form = CustomUserRegistrationForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Your account has been created! You are now a Property Owner.')
                return redirect('home')  # Redirect to the home page
            else:
                # Handle form errors (optional debugging)
                print(form.errors)  # You can remove this line after debugging
        else:
            form = CustomUserRegistrationForm()

        return render(request, 'signup.html', {'form': form})


@pytest.mark.django_db
def test_accommodation_image_creation():
    # Create a user
    user = User.objects.create_user(username="testuser", password="password")

    # Create a location
    location = Location.objects.create(
        id="001",
        title="Miami",
        country_code="US",
        location_type="city",
        center="POINT(25.7617 -80.1918)"
    )

    # Create an accommodation
    accommodation = Accommodation.objects.create(
        id="A005",
        title="Luxury Condo",
        country_code="US",
        bedroom_count=3,
        usd_rate=250.00,
        location=location,
        user=user,
        center="POINT(25.7617 -80.1918)",
        review_score=4.5,  # Valid review score
    )

    # Mock an image file upload
    image_file = SimpleUploadedFile("sample_image.jpg", b"file_content", content_type="image/jpeg")

    # Create an accommodation image
    image = AccommodationImage.objects.create(
        accommodation=accommodation,
        image=image_file
    )

    # Assertions:
    assert image.accommodation == accommodation
    # Check if the image path is generated correctly
    expected_path = f"accommodations/{accommodation.id}/images/sample_image-{uuid4().hex[:8]}.jpg"
    assert image.image.name.startswith(f"accommodations/{accommodation.id}/images/sample_image-")
    
    # Check if the image file was correctly uploaded (the filename will include the UUID)
    assert image.image.name.endswith(".jpg")

@pytest.mark.django_db
def test_signup_post_valid(client):
    valid_data = {
        'username': 'testuser',
        'password1': 'password123',
        'password2': 'password123',
        'email': 'testuser@example.com',
    }
    response = client.post(reverse('signup'), data=valid_data)
    
    # Assert that the user is redirected to the home page (status code 302)
    
    # Check if user is created
