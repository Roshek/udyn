# from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest
from django.http import HttpResponseServerError
from .models import Dyname
from ipware.ip import get_ip
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404, render
import dns.query
import dns.update
import dns.rcode
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.contrib.auth.decorators import login_required

# Create your views here.


def index(request):
    return HttpResponse("ddns stuff")


def get_address(request, host_name):
    try:
        dyname = Dyname.objects.get(prefix=host_name)
    except Dyname.DoesNotExist:
        return HttpResponse('The hostname ' + host_name +
                            '.ddns.aszabados.eu has not been registered.')
    else:
        return render(request, 'ddns_query/get.html', {"dyname": dyname})

@csrf_exempt
@require_POST
def update(request):
    ip = get_ip(request)
    if ip is None:
        return HttpResponseServerError("Error: Couldn't get your IP.")
    try:
        dyname = get_object_or_404(Dyname, prefix=request.POST['prefix'])
        token = request.POST['token']
    except (KeyError):
        return HttpResponseBadRequest("Error: Parameter(s) missing.")
    else:
        if (token != dyname.token):
            return HttpResponseBadRequest("Error: Bad token.")

        update = dns.update.Update(dyname.zone)
        update.replace(dyname.prefix, 60, 'a', ip)

        response = dns.query.tcp(update, dyname.primary_dns_ip)
        if (response.rcode() != dns.rcode.NOERROR):
            return HttpResponseServerError("Error: DNS Update failed.")
        dyname.ip = ip
        dyname.mod = timezone.now()
        dyname.save()
        httpresponse = HttpResponse(
            "Updated hostname " +
            dyname.prefix + dyname.zone +
            " with your IP " +
            dyname.ip
        )
        httpresponse.status_code = 201
        return httpresponse
