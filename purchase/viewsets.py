from datetime import datetime, timedelta

from django.db.models import Max, Sum
from django.db.models.functions import TruncMonth

# from rest_framework import serializers
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import PurchaseStatusModel


class PurchaseModelViewSet(viewsets.ViewSet):

    permission_classes = [AllowAny]
    authentication_classes = []

    @action(url_path='purchase-data', methods=['get'], detail=False)
    def purchase_bar_data(self, request):

        try:
            start_date = self.request.query_params.get('start_date', None)
            start_date = datetime.strptime(start_date, '%d/%m/%Y')
        except Exception as e:
            start_date = datetime.today() - timedelta(days=365)

        try:
            end_date = self.request.query_params.get('end_date', None)
            end_date = datetime.strptime(end_date, '%d/%m/%Y')
        except Exception as e:
            end_date = datetime.today()

        print(start_date, end_date)

        all_latest_statuses = PurchaseStatusModel.objects.values('purchase').\
            annotate(max=Max('created_at')).values('max')

        purchase_statuses = PurchaseStatusModel.objects.\
            filter(created_at__in=all_latest_statuses)

        delivered_status_purchase_ids = purchase_statuses.\
            filter(status='delivered').values_list('purchase_id', flat=True)

        delivered_purchase_with_dipatched_status_ids = \
            PurchaseStatusModel\
            .objects\
            .filter(purchase_id__in=delivered_status_purchase_ids,
                    status='dispatched')\
            .values_list('purchase_id', flat=True)

        delivered_purchase_without_dispacted_status_ids = list(
            set(delivered_status_purchase_ids) -
            set(delivered_purchase_with_dipatched_status_ids))

        dispatched_and_delivered_status_purchases = PurchaseStatusModel\
            .objects\
            .filter(status='dispatched',
                    purchase_id__in=delivered_purchase_with_dipatched_status_ids
                    )\
            .filter(created_at__gte=start_date,
                    created_at__lte=end_date)

        only_delivered_purchases = PurchaseStatusModel\
            .objects\
            .filter(status='delivered',
                    purchase_id__in=delivered_purchase_without_dispacted_status_ids
                    )\
            .filter(created_at__gte=start_date,
                    created_at__lte=end_date)

        rest_status_purchases = purchase_statuses.\
            exclude(status='delivered').\
            filter(created_at__gte=start_date, created_at__lte=end_date)

        rest_status_purchases = rest_status_purchases |\
            dispatched_and_delivered_status_purchases |\
            only_delivered_purchases

        month_aggregated_queryset = rest_status_purchases.\
            annotate(month=TruncMonth('created_at')).\
            values('month').\
            annotate(sum=Sum('purchase__quantity')).\
            values('month', 'sum').order_by('month')

        month = []
        quantity = []

        for data in month_aggregated_queryset:
            month.append(data.get('month').strftime("%B, %Y"))
            quantity.append(data.get('sum'))

        return Response({
            'month': month,
            'quantity': quantity
        })
