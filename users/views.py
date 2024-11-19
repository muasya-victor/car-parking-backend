from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.views import APIView
import io
from xhtml2pdf import pisa
from django.http import HttpResponse
from django.template.loader import render_to_string
from io import BytesIO
import io
from xhtml2pdf import pisa
from django.http import HttpResponse
from django.template.loader import render_to_string
from io import BytesIO
from django.http import FileResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.exceptions import ValidationError
from . import serializers
from .models import CustomUser
from .serializers import CustomUserSerializer, MiniUserSerializer, CustomTokenObtainPairSerializer


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [AllowAny]  # Adjust permissions as needed


class CustomTokenObtainPairView(TokenObtainPairView):
    permission_classes = [AllowAny]
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            user = CustomUser.objects.get(email=request.data.get('email'))
            user_data = CustomUserSerializer(user).data
            response.data['user'] = user_data
        return response

# class CustomTokenObtainPairView(TokenObtainPairView):
#     permission_classes = [AllowAny]
#
#     def post(self, request, *args, **kwargs):
#         email = request.data.get('email')
#         password = request.data.get('password')
#
#         user = authenticate(request, email=email, password=password)
#
#         if not user:
#             raise ValidationError({'detail': 'Invalid email or password.'})
#
#         response = super().post(request, *args, **kwargs)
#
#         user_data = CustomUserSerializer(user).data  # Serialize user data
#         response.data['user'] = user_data
#
#         return response


class CurrentUserViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = MiniUserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Returning a queryset with the single current user
        return CustomUser.objects.filter(id=self.request.user.id)

    def list(self, request, *args, **kwargs):
        # Return the current user's data as a single result
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(serializer.data)


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Custom claims
        token['email'] = user.email
        token['user_role'] = user.user_role
        return token

    def validate(self, attrs):
        user_email = attrs.get('email')
        user_password = attrs.get('password')

        user = CustomUser.objects.filter(email=user_email).first()
        if user and user.check_password(user_password):
            return super().validate(attrs)
        else:
            raise serializers.ValidationError("Invalid credentials")


# class CustomTokenObtainPairView(TokenObtainPairView):
#     serializer_class = CustomTokenObtainPairSerializer
#

from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status, viewsets
from .models import CustomUser
from .serializers import CustomUserSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'user_id'

    def get_queryset(self):
        user = self.request.user

        if user.user_role == 'driver':
            return CustomUser.objects.filter(user_id=self.request.user.user_id)

        return CustomUser.objects.all()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_permissions(self):
        """
        Customize permissions for specific actions.
        """
        if self.action == 'create':
            return [AllowAny()]
        return super().get_permissions()

    def create(self, request, *args, **kwargs):
        """
        Handle user creation, allowing unrestricted access for this action.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)



class PDFView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user

        users = CustomUser.objects.all() if user.is_superuser else None

        serializer = CustomUserSerializer(
            users, many=True, context={'request': request})
        context = {'users': serializer.data}

        html_string = render_to_string('user_list.html', context)
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=user_list.pdf'

        result = BytesIO()
        pdf = pisa.pisaDocument(BytesIO(html_string.encode("UTF-8")), result)
        if not pdf.err:
            response.write(result.getvalue())
            return response
        return HttpResponse('We had some errors <pre>' + html_string +'</pre>')


