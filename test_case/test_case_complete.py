import http_request_decorator as timse
import urllib.request
import requests

if __name__ == '__main__':

    # TODO: use more https://jsonplaceholder.typicode.com/ examples to test
    test_url = 'https://jsonplaceholder.typicode.com/posts/1'
    test_name = 'timse'

    @timse.x(third_party='a', purpose=[Purpose.CHECK_IDENTITY], data_disclosed=[DataDisclosed.ATTITUDE], storage_period=[5, 'minutes'])
    a = requests.get(test_url)
    print(a)

    #timse.x(
    #   third_party='Elias GmbH',
    #   purpose=[Purpose.CHECK_IDENTITY]
    #   data_disclosed=[DataDisclosed.AGE]
    #   storage_period=[300, 'seconds']
    # )
    b = requests.get(test_url)
    print(b)

    response = timse.x(requests.get(test_url))('requests_direct_zweck')
