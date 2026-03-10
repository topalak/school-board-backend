from rest_framework.response import Response
from rest_framework import viewsets, mixins, status
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from .models import Category, Book
from .serializers import CategorySerializer, BookSerializer


class CategoryViewSet(viewsets.GenericViewSet,
                      mixins.ListModelMixin,
                      mixins.CreateModelMixin):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class BookViewSet(viewsets.GenericViewSet,
                  mixins.ListModelMixin,
                  mixins.CreateModelMixin):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['tier_level', 'category']


    # def get_queryset(self):
    #     queryset = Book.objects.all()
    #     tier = self.request.query_params.get('tier')
    #     if tier:
    #         queryset = queryset.filter(tier_level=tier)
    #     return queryset


    def perform_create(self, serializer):
        user = self.request.user if self.request.user.is_authenticated else None
        serializer.save(uploaded_by=user)
        #this is for post part

class CategoryDeleteView(APIView):
    def delete(self, request, *args, **kwargs): #pk comes with kwargs
        category = Category.objects.get(pk=kwargs['pk'])
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)