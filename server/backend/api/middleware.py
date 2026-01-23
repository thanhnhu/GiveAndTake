class UpgradeInsecureMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        # Add Header CSP for docs only
        if request.path.startswith('/docs/'):
            response["Content-Security-Policy"] = "upgrade-insecure-requests"
        return response
