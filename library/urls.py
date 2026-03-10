from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import CategoryViewSet, BookViewSet, CategoryDeleteView

router = SimpleRouter()
router.register('categories', CategoryViewSet, basename='category')
router.register('books', BookViewSet, basename='book')

urlpatterns = [
    path('', include(router.urls)),
    path('categories/<int:pk>/delete/', CategoryDeleteView.as_view()),
]