# from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest
from django.http import HttpResponseServerError, HttpResponseRedirect
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
from .forms import AddDynameForm
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _
from django.conf import settings

class DNSQueryException(Exception):
    pass


def addRecordToDNS(dyname):
    update = dns.update.Update(dyname.zone)
    update.add(dyname.prefix, 60, 'a', dyname.ip)

    response = dns.query.tcp(update, dyname.primary_dns_ip)
    if (response.rcode() != dns.rcode.NOERROR):
        raise DNSQueryException("DNS Query Ex. code: " + str(response.rcode()))


def updateRecordInDNS(dyname):
    update = dns.update.Update(dyname.zone)
    update.replace(dyname.prefix, 60, 'a', dyname.ip)

    response = dns.query.tcp(update, dyname.primary_dns_ip)
    if (response.rcode() != dns.rcode.NOERROR):
        raise DNSQueryException("DNS Query Ex. code: " + response.rcode())


def deleteRecordFromDNS(dyname):
    update = dns.update.Update(dyname.zone)
    update.delete(dyname.prefix, 'a')

    response = dns.query.tcp(update, dyname.primary_dns_ip)
    if (response.rcode() != dns.rcode.NOERROR):
        raise DNSQueryException("DNS Query Ex. code: " + response.rcode())


# Create your views here.
@login_required
def addDyname(request):
    if request.method == 'POST':
        form = AddDynameForm(request.POST)
        if form.is_valid():
            ip = get_ip(request)
            if ip is None:
                ip = '0.0.0.0'
            dyname = form.save(commit=False)
            dyname.ip = ip
            dyname.token = get_random_string(length=30)
            dyname.user = request.user
            try:
                addRecordToDNS(dyname=dyname)
            except DNSQueryException:
                raise ValidationError(
                    _("DNS server is not valid/not responding/refusing query"),
                    code='invalid_dns'
                )
            form.save()

            return HttpResponseRedirect('/mydomains/')

    else:
        form = AddDynameForm(
            initial={'zone': settings.SETTINGS_DICT["DEFAULT_ZONE"]}
        )

    return render(request, 'ddns_query/add_domain.html', {'form': form})


@login_required
def modifyDyname(request, prefix):
    dyname = Dyname.objects.get(prefix=prefix)
    pdyname = Dyname(
        prefix=dyname.prefix,
        zone=dyname.zone,
        primary_dns_ip=dyname.primary_dns_ip,
        primary_dns_host=dyname.primary_dns_host,
        ip=dyname.ip,
        mod=dyname.mod,
        token=dyname.token,
        user=dyname.user
    )
    if request.user != dyname.user:
        return HttpResponseBadRequest("Error: Not a valid domain.")
    if request.method == 'POST':
        form = AddDynameForm(
            request.POST,
            instance=dyname
        )
        if form.is_valid():
            if (
                dyname.prefix != form.cleaned_data['prefix'] or
                dyname.zone != form.cleaned_data['zone'] or
                dyname.primary_dns_ip != form.cleaned_data['zone']
            ):
                try:
                    deleteRecordFromDNS(pdyname)
                except DNSQueryException:
                    pass
                dyname = form.save(commit=False)
                try:
                    addRecordToDNS(dyname)
                except DNSQueryException:
                    addRecordToDNS(pdyname)
                    raise ValidationError(
                        _("DNS server is not" +
                          " valid/not responding/refusing query"),
                        code='invalid_dns'
                    )
            form.save()
            return HttpResponseRedirect('/mydomains/')

    else:
        form = AddDynameForm(instance=dyname)

    return render(request, 'ddns_query/modify_domain.html', {'form': form})


@require_POST
@login_required
def deleteDyname(request):
    try:
        dyname = get_object_or_404(Dyname, prefix=request.POST['prefix'])
        token = request.POST['token']
    except (KeyError):
        return HttpResponseBadRequest("Error: Parameter(s) missing.")
    else:
        if (token != dyname.token):
            return HttpResponseBadRequest("Error: Bad token.")
        try:
            deleteRecordFromDNS(dyname)
            dyname.delete()
        except DNSQueryException:
            pass
        return HttpResponseRedirect('/mydomains/')


@require_POST
@login_required
def updateToken(request):
    try:
        dyname = get_object_or_404(Dyname, prefix=request.POST['prefix'])
        token = request.POST['token']
    except (KeyError):
        return HttpResponseBadRequest("Error: Parameter(s) missing.")
    else:
        if (token != dyname.token):
            return HttpResponseBadRequest("Error: Bad token.")

        dyname.token = get_random_string(length=30)
        dyname.save()
        return HttpResponseRedirect('/mydomains/')


@csrf_exempt
@require_POST
def updateDyname(request):
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
            dyname.prefix + "." + dyname.zone +
            " with your IP " +
            dyname.ip
        )
        httpresponse.status_code = 201
        return httpresponse