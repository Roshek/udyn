#!/bin/bash
echo "#!/bin/bash
echo \"import urllib2, urllib
url = 'https://ddns.aszabados.eu/update/'
data = urllib.urlencode({'prefix': '$2', 'token':'$3'})
req = urllib2.Request(url, data)
response = urllib2.urlopen(req)
d = response.read()
print d\" | python" > ~/ddns_cron.sh
chmod +x ~/ddns_cron.sh
echo "*/$1 * * * * ~/ddns.cron.sh" > job
crontab job
rm job