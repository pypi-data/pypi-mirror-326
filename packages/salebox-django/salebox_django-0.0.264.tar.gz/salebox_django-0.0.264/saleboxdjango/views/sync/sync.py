from datetime import datetime

from django import forms
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from saleboxdjango.models import LastUpdate, KeyValueStore
from saleboxdjango.lib.common import get_client_ip


class SaleboxSyncForm(forms.Form):
    key = forms.CharField()
    license = forms.CharField()


@csrf_exempt
def salebox_sync_view(request):
    # is this a POST that came from the server IP?
    # if request.method == "POST" and settings.SALEBOX["API"]["IP"] == get_client_ip(
    #     request
    # ):
    if request.method == "POST":
        # did it send a valid key / license combo?
        form = SaleboxSyncForm(request.POST)
        if form.is_valid():
            if settings.SALEBOX["API"]["KEY"] == str(
                form.cleaned_data["key"]
            ) and settings.SALEBOX["API"]["LICENSE"] == str(
                form.cleaned_data["license"]
            ):
                # ok, we're good. reset the LastUpdate value
                lu = (
                    LastUpdate.objects.filter(code="saleboxsync_pull_start")
                    .filter(value__gt=0)
                    .first()
                )
                if lu is not None:
                    lu.value = 0
                    lu.save()

                # update the keyvalue store
                kvs = KeyValueStore.objects.filter(key="sync_inventory").first()
                if kvs is not None:
                    kvs.value["recent"] = True
                    kvs.save()

                return JsonResponse({"status": "OK"})

    # fallback
    return JsonResponse({"status": "Fail"})
