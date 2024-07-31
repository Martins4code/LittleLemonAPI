from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from .serializers import MenuItemSerializer
from.models import MenuItem
 from django.core.paginator import Paginator, EmptyPage
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import permission_classes, throttle_classes
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from django.contrib.auth.models import User, Group


# Create your views here.

@api_view(['GET','POST'])
def menu_items(request):
    if request.method == 'GET':
        items = MenuItem.objects.select_related('category').all()
        category_name = request.query_params.get('category')
        to_price = request.query_params.get('to_price')
        search = request.query_params.get('search')
        # perpage = request.query_params.get('perpage', default=2)
        # page = request.query_params.get('page', default=1)
        if category_name:
            items = items.filter(category_title=category_name)
        if to_price:
            items = items.filter(price=to_price)
        if search:
            items = items.filter(title_contains=search)
            
        # Paginator = Paginator(items, per_page=perpage)
        # try:
        #     items = Paginator.page(number=page)
        # except EmptyPage:
        #     items = []
        serialized_item= MenuItemSerializer(items, many=True)
        return Response(serialized_item.data)
    if request.method == 'POST':
        serialized_item = MenuItemSerializer(data=request.data)
        serialized_item.is_valid(raise_exception=True)
        serialized_item.save()
        return Response(serialized_item, status.HTTP_201_CREATED)


@api_view()
def SingleMenuItem(request, pk):
    item = get_object_or_404(MenuItem, pk)
    serialized_item = MenuItemSerializer(item)
    return Response(serialized_item.data)

@api_view()
@throttle_classes([AnonRateThrottle])
def throttle_check(request):
    return Response({"message": "success"})

@api_view()
@permission_classes(IsAuthenticated)
@throttle_classes([UserRateThrottle])
def throttle_check_auth(request):
    return Response({"message": "success authenticated user"})

@api_view()
@permission_classes(IsAuthenticated)
def me(request):
    return Response(request.user.email)

@api_view(["POST"])
@permission_classes([IsAdminUser])
def managers(request):
    username = request.data['username']
    if username:
        user = get_object_or_404(User, username=username)
        managers = Group.objects.get(name="Manager")
        if request.method == 'POST':
             managers.user_set.add(user)
        elif request.method == "DELETE":
            managers.user_set.remove(user)
        return Response({"message":"ok"})
    
    return Response({"message":"error"}, status.HTTP_400_BAD_REQUEST)

