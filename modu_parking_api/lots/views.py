from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view
from rest_framework.response import Response

from lots.models import Lot
from lots.serializers import LotsSerializer, MapSerializer
from users.models import User


class LotsViewSet(viewsets.ModelViewSet):
    queryset = Lot.objects.all()
    serializer_class = LotsSerializer
    # def get_serializer(self, *args, **kwargs):
    #     if self.action == 'order_price':
    #         return LotsSerializer
    #     elif self.action == 'order_distance':
    #         return
    #     return super().get_serializer(*args, **kwargs)

    @action(detail=False)
    def order(self, request, *args, **kwargs):
        if request.data.pop('order') == 'price':
            self.queryset = Lot.objects.filter().order_by('basic_rate')
        elif request.data.pop('order') == 'distance':
            distance = 2000
            ref_location = Point(1.232433, 1.2323232)
            res = Lot.objects.filter(
                location__distance_lte=(
                    ref_location,
                    D(m=distance)
                )
            ).distance(
                ref_location
            ).order_by(
                'distance'
            )
            self.queryset = Lot.objects.filter().order_by('distance')

        return super().list(request, *args, **kwargs)

    @action(detail=False)
    def order_distance(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        pass

    @api_view('GET')
    def lots_detail(self, request, pk):
        try:
            lot = Lot.objects.get(pk=pk)
            serializer = LotsSerializer(lot)
            return Response(serializer.data)

        except Lot.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class MapViewSet(viewsets.ModelViewSet):
    queryset = Lot.objects.all()
    serializer_class = MapSerializer

    @action(detail=False)
    def maps(self, request, *args, **kwargs):
        return super().list(self, *args, **kwargs)
