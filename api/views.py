import os
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

def get_canvas_credentials():
    canvas_domain = os.getenv('CANVAS_DOMAIN')
    access_token = os.getenv('CANVAS_ACCESS_TOKEN')
    return canvas_domain, access_token

class CanvasCoursesView(APIView):
    def get(self, request):
        canvas_domain, access_token = get_canvas_credentials()
        
        if not canvas_domain or not access_token:
            return Response(
                {"error": "Canvas credentials not configured. Please set CANVAS_DOMAIN and CANVAS_ACCESS_TOKEN in .env."}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        
        # GET /api/v1/courses - fetch active courses
        url = f"{canvas_domain}/api/v1/courses?per_page=50&enrollment_state=active"
        
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            courses = response.json()
            return Response(courses, status=status.HTTP_200_OK)
        except requests.exceptions.RequestException as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class CanvasCourseFilesView(APIView):
    def get(self, request, course_id):
        canvas_domain, access_token = get_canvas_credentials()
        if not canvas_domain or not access_token:
            return Response({"error": "Canvas credentials not configured."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
        headers = {"Authorization": f"Bearer {access_token}"}
        url = f"{canvas_domain}/api/v1/courses/{course_id}/files?per_page=100"
        
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return Response(response.json(), status=status.HTTP_200_OK)
        except requests.exceptions.RequestException as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class CanvasCourseFoldersView(APIView):
    def get(self, request, course_id):
        canvas_domain, access_token = get_canvas_credentials()
        if not canvas_domain or not access_token:
            return Response({"error": "Canvas credentials not configured."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
        headers = {"Authorization": f"Bearer {access_token}"}
        url = f"{canvas_domain}/api/v1/courses/{course_id}/folders?per_page=100"
        
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return Response(response.json(), status=status.HTTP_200_OK)
        except requests.exceptions.RequestException as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class CanvasFolderFilesView(APIView):
    def get(self, request, folder_id):
        canvas_domain, access_token = get_canvas_credentials()
        if not canvas_domain or not access_token:
            return Response({"error": "Canvas credentials not configured."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
        headers = {"Authorization": f"Bearer {access_token}"}
        url = f"{canvas_domain}/api/v1/folders/{folder_id}/files?per_page=100"
        
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return Response(response.json(), status=status.HTTP_200_OK)
        except requests.exceptions.RequestException as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class WeeklyMaterialsFilesView(APIView):
    def get(self, request):
        canvas_domain, access_token = get_canvas_credentials()
        if not canvas_domain or not access_token:
            return Response({"error": "Canvas credentials not configured."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
        headers = {"Authorization": f"Bearer {access_token}"}
        
        try:
            # 1. Get all active courses
            courses_url = f"{canvas_domain}/api/v1/courses?per_page=50&enrollment_state=active"
            courses_resp = requests.get(courses_url, headers=headers)
            courses_resp.raise_for_status()
            courses = courses_resp.json()
            
            all_files = []
            
            # 2. Iterate through each course
            for course in courses:
                course_id = course.get('id')
                # Some objects might be empty or restricted
                if not course_id:
                    continue
                    
                # 3. Get folders for the course
                folders_url = f"{canvas_domain}/api/v1/courses/{course_id}/folders?per_page=100"
                folders_resp = requests.get(folders_url, headers=headers)
                
                # Gracefully ignore if we don't have access to this course's folders
                if not folders_resp.ok:
                    continue
                    
                folders = folders_resp.json()
                
                # 4. Find folder(s) named "Weekly Materials" (case-insensitive)
                for folder in folders:
                    if folder.get('name', '').lower() == 'weekly materials':
                        folder_id = folder.get('id')
                        
                        # 5. Get files for this specific folder
                        files_url = f"{canvas_domain}/api/v1/folders/{folder_id}/files?per_page=100"
                        files_resp = requests.get(files_url, headers=headers)
                        
                        if files_resp.ok:
                            files = files_resp.json()
                            # Annotate each file with the course name to give frontend context
                            for file in files:
                                file['course_name'] = course.get('name')
                                file['course_id'] = course_id
                                all_files.append(file)
            
            return Response(all_files, status=status.HTTP_200_OK)
            
        except requests.exceptions.RequestException as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

from rest_framework import generics
from .models import Event
from .serializers import EventSerializer

class EventListCreateView(generics.ListCreateAPIView):
    queryset = Event.objects.all().order_by('-date')
    serializer_class = EventSerializer

class EventDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
