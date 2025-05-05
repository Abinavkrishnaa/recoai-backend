from rest_framework.generics import CreateAPIView,UpdateAPIView
from rest_framework import viewsets,permissions,status
from .models import  User,UserInteraction,Content
from .serializers import UserInteractionSerializer,UserSerializer,ContentSerializer,RegisterSerializer
from  rest_framework.response import Response
from rest_framework.views import APIView
from ml.services import RecommenderService
from .permissions import IsAdminOrReadOnly
# Create your views here.
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import update_session_auth_hash
from .serializers import UserUpdateSerializer, PasswordChangeSerializer

class UserProfileView(UpdateAPIView):
    serializer_class = UserUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

class PasswordChangeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PasswordChangeSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = request.user
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            update_session_auth_hash(request, user)
            return Response({"message": "Password updated successfully"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
recommender_service = RecommenderService()
class RegisterView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

class ContentViewSet(viewsets.ModelViewSet):
    queryset = Content.objects.all()
    serializer_class = ContentSerializer
    permission_classes = [permissions.IsAuthenticated]

class UserInteractionViewSet(viewsets.ModelViewSet):
    queryset = UserInteraction.objects.all()
    serializer_class = UserInteractionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class RecommendationView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            user = request.user
            content_ids = recommender_service.get_recommendations(user.id)
            print("Recommended Content IDs:", content_ids)  # Debug
            contents = Content.objects.filter(id__in=content_ids)
            print("Matched Content:", contents.count())  # Debug
            # Maintain recommendation order
            ordered_contents = []
            for cid in content_ids:
                for content in contents:
                    if content.id == cid:
                        ordered_contents.append(content)
                        break

            serializer = ContentSerializer(ordered_contents, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)