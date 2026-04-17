from django.urls import path
from .views import (
    CanvasCoursesView, 
    CanvasCourseFilesView, 
    CanvasCourseFoldersView, 
    CanvasFolderFilesView,
    WeeklyMaterialsFilesView,
    EventListCreateView,
    EventDetailView
)

urlpatterns = [
    path('canvas/courses/', CanvasCoursesView.as_view(), name='canvas-courses'),
    path('canvas/courses/<int:course_id>/files/', CanvasCourseFilesView.as_view(), name='canvas-course-files'),
    path('canvas/courses/<int:course_id>/folders/', CanvasCourseFoldersView.as_view(), name='canvas-course-folders'),
    path('canvas/folders/<int:folder_id>/files/', CanvasFolderFilesView.as_view(), name='canvas-folder-files'),
    path('canvas/weekly-materials/', WeeklyMaterialsFilesView.as_view(), name='canvas-weekly-materials'),
    path('events/', EventListCreateView.as_view(), name='event-list-create'),
    path('events/<int:pk>/', EventDetailView.as_view(), name='event-detail'),
]
