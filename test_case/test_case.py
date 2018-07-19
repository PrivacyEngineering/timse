import http_request_decorator as timse
import urllib.request
import requests

if __name__ == '__main__':

    # TODO: use more https://jsonplaceholder.typicode.com/ examples to test
    test_url = 'https://jsonplaceholder.typicode.com/posts/1'
    test_name = 'timse'

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

    requests.post('elias.grünewald.xyz', 'Dies ist eine Übung!')

    response = timse.x(requests.get(test_url))('requests_direct_zweck')
