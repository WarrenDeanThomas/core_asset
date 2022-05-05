from rest_framework.response import Response
from rest_framework.decorators import api_view
from core.models import Core
from .serializers import ItemSerializer


@api_view(['GET'])
def apiGetCoreData(request):
    items = Core.objects.all()
    serializer = ItemSerializer(items, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def apiGetCore(request, pk):
    items = Core.objects.get(id=pk)
    serializer = ItemSerializer(items, many=False)
    return Response(serializer.data)


@api_view(['POST'])
def apiAddCore(request):
    serializer = ItemSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


@api_view(['GET', 'POST'])
def apiUpdateCore(request, pk):
    item = Core.objects.get(id=pk)
    serializer = ItemSerializer(instance=item, data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


@api_view(['DELETE'])
def apiDeleteCore(request, pk):
    item = Core.objects.get(id=pk)
    item.delete()

    return Response('Item successfully deleted')