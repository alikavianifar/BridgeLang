"""
Custom error handlers for the BridgeLang application.

Provides user-friendly error pages for HTTP 400, 403, 404, and 500 errors
instead of Django's default error responses.
"""

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def error_400(request: HttpRequest, exception: Exception = None) -> HttpResponse:
    """Handle 400 Bad Request errors with a custom template."""
    context = {"exception": exception}
    response = render(request, "errors/400.html", context=context)
    response.status_code = 400
    return response


def error_403(request: HttpRequest, exception: Exception = None) -> HttpResponse:
    """Handle 403 Permission Denied errors with a custom template."""
    context = {"exception": exception}
    response = render(request, "errors/403.html", context=context)
    response.status_code = 403
    return response


def error_404(request: HttpRequest, exception: Exception = None) -> HttpResponse:
    """Handle 404 Page Not Found errors with a custom template."""
    context = {"exception": exception}
    response = render(request, "errors/404.html", context=context)
    response.status_code = 404
    return response


def error_500(request: HttpRequest) -> HttpResponse:
    """Handle 500 Internal Server errors with a custom template."""
    response = render(request, "errors/500.html")
    response.status_code = 500
    return response