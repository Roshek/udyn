from django.test import TestCase, Client
from ddns_query.models import Dyname, User
from django.http import HttpRequest


# Create your tests here.
class UpdateDynameViewTests(TestCase):
    def setUp(self):
        self.url ='/update/'
        self.user = User.objects.create(username="testuser")
        self.dyname = Dyname.objects.create(prefix="prefix", token="token", user=self.user)
        self.bad_dyname = Dyname.objects.create(prefix="prefix2", token="token2", user=self.user, zone="example.com")
        self.foreign_dyname = Dyname.objects.create(prefix="prefix3", token="token3", user=self.user, zone="roshek.eu")


    def test_invalid_prefix_returns_http400(self):
        response = self.client.post(self.url,data={"prefix":"wrongprefix", "token": "dontcare"}, follow=True, secure=True)
        self.assertEquals(response.status_code, 400)
        self.assertEquals(response.content, b'Error: Bad prefix.\n')

    def test_invalid_token_returns_http400(self):
        response = self.client.post(self.url,data={"prefix":"prefix", "token": "wrongtoken"}, follow=True, secure=True)
        self.assertEquals(response.status_code, 400)
        self.assertEquals(response.content, b'Error: Bad token.\n')
    
    def test_valid_data_returns_http200(self):
        response = self.client.post(self.url,data={"prefix":"prefix", "token": "token"}, follow=True, secure=True)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.content, b'Updated hostname prefix.ddns.aszabados.eu with your IP 127.0.0.1\n')

    def test_wrong_http_method_returns_http405(self):
        response = self.client.get(self.url, follow=True, secure=True)
        self.assertEquals(response.status_code,405)
    
    def test_no_post_data_returns_http400(self):
        response = self.client.post(self.url, follow=True, secure=True)
        self.assertEquals(response.status_code, 400)
        self.assertEquals(response.content, b'Error: Parameter(s) missing.\n')

    def test_no_prefix_in_post_data_returns_http400(self):
        response = self.client.post(self.url, data={"token": "dontcare"}, follow=True, secure=True)
        self.assertEquals(response.status_code, 400)
        self.assertEquals(response.content, b'Error: Parameter(s) missing.\n')

    def test_no_token_in_post_data_returns_http400(self):
        response = self.client.post(self.url, data={"prefix": "prefix"}, follow=True, secure=True)
        self.assertEquals(response.status_code, 400)
        self.assertEquals(response.content, b'Error: Parameter(s) missing.\n')

    def test_no_retrieveable_ip_in_request_returns_http500(self):
        request = HttpRequest()
        request.method = 'POST'
        from ddns_query.views import updateDyname
        response = updateDyname(request)
        self.assertEquals(response.status_code, 500)
        self.assertEquals(response.content, b"Error: Couldn't get your IP.\n")

    def test_dns_response_has_error_returns_http500(self):
        response = self.client.post(self.url, data={"prefix": "prefix2", "token":"token2"}, follow=True, secure=True)
        self.assertEquals(response.status_code, 500)
        self.assertEquals(response.content, b'Error: DNS Update failed.\n')

    def test_custom_dyname_with_valid_data_returns_http200(self):
        response = self.client.post(self.url,data={"prefix": "prefix3", "token": "token3"}, follow=True, secure=True)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.content, b'Updated hostname prefix3.roshek.eu with your IP 127.0.0.1\n')
