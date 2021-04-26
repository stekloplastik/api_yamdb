import random

from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import filters, status, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import CustomUser
from .permissions import IsAdmin, IsOwnerProfileOrReadOnly
from .serializers import (ConfirmationSerializer, SendCodeSerializer,
                          UserSerializer)


class CreateUserViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdmin]
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    filter_backends = [filters.SearchFilter]
    search_fields = ['user__username', ]


@api_view(['POST'])
def send_confirmation_code(request):
    serializer = SendCodeSerializer(data=request.data)
    email = request.data.get('email', False)
    if serializer.is_valid():
        confirmation_code = ''.join(map(str, random.sample(range(10), 6)))
        user = CustomUser.objects.filter(email=email).exists()
        if not user:
            CustomUser.objects.create_user(email=email)
        CustomUser.objects.filter(email=email).update(
            confirmation_code=make_password(
                confirmation_code, salt=None, hasher='default'
            )
        )
        mail_subject = 'Код подтверждения'
        message = f'{confirmation_code}'
        send_mail(mail_subject, message, 'Yamdb.ru <admin@yamdb.ru>', [email])
        return Response(
            f'Код отправлен на адрес {email}', status=status.HTTP_200_OK
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def get_jwt_token(request):
    serializer = ConfirmationSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.data.get('email')
        confirmation_code = serializer.data.get('confirmation_code')
        user = get_object_or_404(CustomUser, email=email)
        if check_password(confirmation_code, user.confirmation_code):
            token = default_token_generator.make_token(user)
            return Response({'token': f'{token}'}, status=status.HTTP_200_OK)
        return Response({'confirmation_code': 'Неверный код подтверждения'},
                        status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserEdit(APIView):
    permission_classes = [IsOwnerProfileOrReadOnly]

    def get(self, request):
        if request.user.is_authenticated:
            user = get_object_or_404(CustomUser, id=request.user.id)
            serializer = UserSerializer(user)
            return Response(serializer.data)
        return Response(
            'Необходима авторизация', status=status.HTTP_401_UNAUTHORIZED
        )

    def patch(self, request):
        if request.user.is_authenticated:
            user = get_object_or_404(CustomUser, id=request.user.id)
            serializer = UserSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
        return Response(
            'Необходима авторизация', status=status.HTTP_401_UNAUTHORIZED
        )
