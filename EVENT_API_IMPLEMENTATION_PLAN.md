# RamsHere Backend: Event API Implementation Plan

## Context
The frontend `RamsHere` application is moving away from hardcoded mock events to a persistent database model. We need to implement the backend API necessary to support CRUD (Create, Read, Update, Delete) operations for university events.

This backend serves an Admin dashboard (where school administrators can create and manage events) and a Student view (where students can view live and upcoming events).

## Target Architecture
- **Framework**: Django + Django REST Framework (DRF)
- **Target App**: The existing `api` app within the `RamsHereBackend` project.
- **Database**: PostgreSQL (via Render for production) / SQLite (local dev). The project is already configured to use `dj-database-url`.

---

## Required Implementation Steps

### 1. Database Model defined in `api/models.py`
Create an `Event` model that exactly mirrors the requirements of the frontend TypeScript interface. 

The frontend expects this exact payload structure:
```json
{
  "id": "1", // Frontend expects string or number, DRF's auto PK is fine
  "title": "Spring Festival 2026",
  "description": "Celebrate the arrival of spring...",
  "date": "2026-04-02", // YYYY-MM-DD
  "time": "12:00 PM - 5:00 PM", // String
  "location": "Campus Main Quad",
  "type": "live", // choices: "live" or "upcoming"
  "category": "Cultural",
  "attendees": 450, // optional integer
  "photo": "https://example.com/image.jpg", // optional URL/String
  "majorTags": ["All Majors", "Computer Science"] // Optional array of strings
}
```

**Implementation Details for `models.py`:**
- **`title`**: `CharField` (max_length=200)
- **`description`**: `TextField`
- **`date`**: `DateField`
- **`time`**: `CharField` (max_length=100) - Note: keep as a string to match "12:00 PM - 5:00 PM" format from the frontend.
- **`location`**: `CharField` (max_length=200)
- **`type`**: `CharField` with choices (`live`, `upcoming`), max_length=20
- **`category`**: `CharField` (max_length=100)
- **`attendees`**: `IntegerField` (null=True, blank=True, default=0)
- **`photo`**: `URLField` or `CharField` (null=True, blank=True)
- **`majorTags`**: `JSONField` (null=True, blank=True, default=list) - *CRITICAL: The frontend expects this to be an array of strings natively.*

**Important**: Implement a `__str__` method returning the `title`.

### 2. Serializer defined in `api/serializers.py`
Create an `EventSerializer` mapping to the new model.
- Because the frontend uses camelCase (`majorTags`) and Python uses snake_case, you have two options. The easiest is to define the field explicitly in the model as `majorTags`, OR handle the mapping in the serializer.
- **Recommendation**: Map `major_tags` to `majorTags` in the serializer if you use snake_case in the model.
```python
from rest_framework import serializers

class EventSerializer(serializers.ModelSerializer):
    # Map frontend majorTags to backend major_tags (if snake case used in model)
    majorTags = serializers.JSONField(source='major_tags', required=False)

    class Meta:
        model = Event
        fields = ['id', 'title', 'description', 'date', 'time', 'location', 'type', 'category', 'attendees', 'photo', 'majorTags']
```

### 3. Views defined in `api/views.py`
Use DRF generic API views to handle the REST endpoints.
- Create `EventListCreateView` inheriting from `generics.ListCreateAPIView`.
- Create `EventDetailView` inheriting from `generics.RetrieveUpdateDestroyAPIView` (for future editing/deleting capabilities).

Ensure `queryset = Event.objects.all().order_by('-date')` and `serializer_class = EventSerializer`.

### 4. Routing defined in `api/urls.py`
Hook the new views into the existing URLs.
- Add `path('events/', EventListCreateView.as_view(), name='event-list-create')`
- Add `path('events/<int:pk>/', EventDetailView.as_view(), name='event-detail')`

### 5. Admin Integration defined in `api/admin.py` (Optional but highly recommended)
Register the `Event` model in the Django Admin portal so database administrators can manually edit records if necessary.
- `admin.site.register(Event)`

---

## Deliverables for the Backend Agent
1. Modify `api/models.py`.
2. Create/modify `api/serializers.py`.
3. Modify `api/views.py`.
4. Modify `api/urls.py`.
5. Run the migration generation: `python manage.py makemigrations`.
6. Run the local migration: `python manage.py migrate`.

**Post-Implementation Testing:**
Start the development server and verify that hitting `GET http://localhost:8000/api/events/` returns an empty JSON list `[]` with a 200 OK status. Ensure CORS allows requests from localhost:5173 or localhost:3000 (which should already be configured in `settings.py` via `CORS_ALLOW_ALL_ORIGINS = True`).
