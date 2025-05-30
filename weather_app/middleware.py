# coding=utf-8

class HeadersMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        # response['Retry-After'] = 30

        return response
