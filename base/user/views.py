from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView, ListCreateAPIView, RetrieveAPIView, \
    ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import CustomUser, Transaction, Category
from .serializers import CustomUserSerializers, TransactionSerializers, CategorySerializers, CustomUserSerializers1, \
    ViewCustomUserSerializer,  CreateCategorySerializers
from rest_framework import filters
from .permissions import IsOwner


class RegisterUserView(CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializers
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = CustomUserSerializers(data=request.data)
        data = {}
        if serializer.is_valid():
            serializer.save()
            data['response'] = True
            return Response(data, status=status.HTTP_200_OK)
        else:
            data = serializer.errors
            return Response(data)


class ListCreateTransaction(ListCreateAPIView):
    serializer_class = TransactionSerializers
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['summary', 'date_creation', 'time']
    ordering_fields = ['summary', 'date_creation', 'time']

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        data = {}
        if serializer.is_valid():
            serializer.save()
            return Response(data, status=status.HTTP_200_OK)
        else:
            data = serializer.errors
            return Response(data)


class DetailTransaction(RetrieveUpdateDestroyAPIView):
    serializer_class = TransactionSerializers
    permission_classes = [IsAuthenticated, ]

    lookup_field = 'id'

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)


class ListCreateCategory(ListCreateAPIView):
    serializer_class = CreateCategorySerializers
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        return Category.objects.filter(customuser__id=self.request.user.id)

    def post(self, request, *args, **kwargs):
        serializer = CategorySerializers(data=request.data, context={'request': request})
        data = {}
        if serializer.is_valid():
            serializer.save()
            return Response(data, status=status.HTTP_200_OK)
        else:
            data = serializer.errors
            return Response(data)


class DetailCategory(RetrieveUpdateDestroyAPIView):
    serializer_class = CategorySerializers
    permission_classes = [IsAuthenticated, ]

    lookup_field = 'id'

    def get_queryset(self):
        return Category.objects.filter(customuser__id=self.request.user.id)


class DetailUser(RetrieveAPIView):
    serializer_class = CustomUserSerializers1
    permission_classes = [IsOwner, ]
    lookup_field = 'id'
    queryset = CustomUser.objects.all()


class ListCustomUser(ListAPIView):
    serializer_class = ViewCustomUserSerializer
    permission_classes = [IsAuthenticated, ]
    queryset = CustomUser.objects.all()
