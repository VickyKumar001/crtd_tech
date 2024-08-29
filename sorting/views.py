
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from operator import itemgetter

class ExternalAPIDataView(APIView):
    def post(self, request):
        try:
            response = requests.get('http://13.127.246.196:8000/api/registers')
            response.raise_for_status()
            data = response.json()
        except requests.RequestException as e:
            return Response({"error": f"Failed to fetch data from external API: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        
        filters = request.data.get('filters', {})
        sort_by = request.data.get('sort_by', 'time_end') 


        college_name_filter = filters.get('college_name', '')
        if college_name_filter:
            data = [item for item in data if college_name_filter.lower() in item.get('college_name', '').lower()]

        
        
        if sort_by:
            reverse = sort_by.startswith('-')
            key = sort_by.lstrip('-')
            try:
                data = sorted(data, key=itemgetter(key), reverse=reverse)
            except KeyError:
                return Response({"error": f"Invalid sorting key: {key}"}, status=status.HTTP_400_BAD_REQUEST)

        return Response(data)
