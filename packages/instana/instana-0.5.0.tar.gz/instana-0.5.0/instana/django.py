from __future__ import print_function
import opentracing as ot
from instana import tracer, options
import opentracing.ext.tags as ext


DJ_INSTANA_MIDDLEWARE = 'instana.django.InstanaMiddleware'


class InstanaMiddleware(object):
    """ Django Middleware to provide request tracing for Instana """
    def __init__(self, get_response):
        self.get_response = get_response
        opts = options.Options(service="Django")
        ot.global_tracer = tracer.InstanaTracer(opts)
        self

    def __call__(self, request):
        env = request.environ
        if 'HTTP_X_INSTANA_T' in env and 'HTTP_X_INSTANA_S' in env:
            ctx = ot.global_tracer.extract(ot.Format.HTTP_HEADERS, env)
            span = ot.global_tracer.start_span("django", child_of=ctx)
        else:
            span = ot.global_tracer.start_span("django")

        span.set_tag(ext.HTTP_URL, env['PATH_INFO'])
        span.set_tag("http.params", env['QUERY_STRING'])
        span.set_tag(ext.HTTP_METHOD, request.method)
        span.set_tag("http.host", env['HTTP_HOST'])

        response = self.get_response(request)

        span.set_tag(ext.HTTP_STATUS_CODE, response.status_code)
        ot.global_tracer.inject(span.context, ot.Format.HTTP_HEADERS, response)
        span.finish()
        return response


def hook(module):
    """ Hook method to install the Instana middleware into Django """
    if DJ_INSTANA_MIDDLEWARE in module.settings.MIDDLEWARE:
        return

    if type(module.settings.MIDDLEWARE) is tuple:
        module.settings.MIDDLEWARE = (
                DJ_INSTANA_MIDDLEWARE,) + module.settings.MIDDLEWARE
    elif type(module.settings.MIDDLEWARE) is list:
        module.settings.MIDDLEWARE = [
                DJ_INSTANA_MIDDLEWARE] + module.settings.MIDDLEWARE
    else:
        print("Instana: Couldn't add InstanaMiddleware to Django")
