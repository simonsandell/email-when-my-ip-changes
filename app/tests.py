import requests
from requests.exceptions import ConnectionError

class Test:
    Tests = {}
    def __init__(self, decoree):
        if decoree.__name__ not in Test.Tests:
            Test.Tests[decoree.__name__] = decoree

    def __call__(self, *args, **kwargs):
        pass

class TestResult:
    def __init__(self):
        self.testdesc = ""
        self.notify = False
        self.message = ""

@Test
def test_ip_changed(config):
    """Test if Public IP changed"""
    result = TestResult()
    result.testdesc = "TestIpChanged"
    try:
        r = requests.get("http://ifconfig.me")
    except ConnectionError:
        # TODO: logging
        result.message = "Failed to get current ip"
        return result
    current_ip = r.text
    cache_file = config['Tests']['ip_cache_file']
    with open(cache_file, 'r') as f:
        previous_ip = f.read().strip()
    with open(cache_file, 'w') as f:
        f.write(current_ip)
    if not previous_ip == current_ip:
        result.notify = True
        result.message = "The Public IP changed from {} to {}".format(previous_ip, current_ip)
    else:
        result.message = "The Public IP is unchanged"
    return result

@Test
def test_dns(config):
    """Test if domain resolves"""
    result = TestResult()
    result.testdesc = "TestDomain"

    cache_file = config['Tests']['dns_status_cache_file']
    ping_url = config['Tests']['dns_ping_url']

    with open(cache_file, 'r') as f:
        previous_result = f.read().strip()
    try:
        r = requests.get(ping_url)
        rjson = r.json()
        if not rjson['ping'] == 'pong':
            current_result = 'not resolving'
            result.message = "{} sends incorrect response, {}".format(ping_url, r.text)
        else:
            current_result = 'resolving'
            result.message = "{} is resolving correctly".format(ping_url)
    except ConnectionError:
        # TODO: logging
        current_result = 'not resolving'
        result.message = "{} is not resolving".format(ping_url)

    if current_result != previous_result:
        result.notify = True
    return result
