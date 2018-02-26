import os
import json
import requests


def w3c_validator(document, output='json'):
    '''
    Programmatic checking of modern HTML documents using the API provided by
    the W3C HTML Checker.

    Parameters
    ----------
    * out: str {gnu, json, xhtml, xml, text}
    '''
    w3c_validator = 'https://validator.w3.org/nu/?out={}'.format(output)
    headers = {'Content-Type': 'text/html; charset=utf-8'}
    response = requests.post(w3c_validator, data=document, headers=headers)
    response.raise_for_status()

    if output == 'json':
        results = json.loads(response.content)['messages']
        if results:
            return results
        else:
            return True
    else:
        return response.content
