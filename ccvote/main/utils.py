from django.template import Context
from django.template import RequestContext
from django.template import loader
from django.template import TemplateDoesNotExist
from django.http import HttpResponse

simple_response = '''<html>
<head><title>{response_string}</title></head>
<body><h1>{response_string}</h1><p>{details}</p></body>
</html>'''

class ActionView:
    '''
    This is a base class convenience request handler.  The idea is that,
    regardless of the method of data transfer, the programmer will only
    have to define an action_<name>() method to process that data.  The
    class will take care of normalizing data sent via a GET query 
    string, a POST uri-encoded body, or even "cruft" free URL params.

    ::

        class MyPage(ActionView):

            def prompt_form(self, form):
                self.data['form'] = form.as_p()
                return self.render_html('my-template.html')

            def action_clear(self, args):
                return self.default()

            def action_submit(self, args):
                form = MyForm(args)
                if not form.is_valid():
                    self.data['error_message'] = 'Form errors'
                    return self.prompt_form(form)

                # TODO: do login stuff
                return HttpResponseRedirect('/')

            def default(self, args):
                form = MyForm()
                return self.prompt_form(form)
                

    The only stipulation is that you implement an action_<name>(args)
    method where args is a django QueryDict object and a variable
    "action_<name>" exists in the QueryDict.  Which is easy because
    there is usually a type="submit" input that will be named 
    "action_<name>".

    In addition to automatic action dispatch there will be a set of 
    convenience functions and member variables.  self.data will serve
    as a cache of transaction results to render into the table
    automatically.
    '''

    def __init__(self):
        # Request/response objects as built by django
        self.request = None
        # response headers
        self.response_headers = {}
        # template data
        self.data = {}
        # list of defined actions for the request handler
        self._actions = []
        # set up the action via introspection
        self._init_actions()

    def _init_actions(self):
        prefix = 'action_'
        prefix_len = len(prefix)
        for attr in dir(self):
            if callable(getattr(self, attr)) and (attr[:prefix_len] == prefix):
                self._actions.append(attr)

    def _dispatch(self, args):
        for action in self._actions:
            if action in args:
                method = getattr(self, action)
                return method(args)
        return self.action(args)

    def not_implemented(self):
        data = dict(response_string='501 Not implemented', details='')
        try:
            template = loader.get_template('main/error_page.html')
            c = Context(data)
            body = template.render(c)
        except TemplateDoesNotExist:
            body = str.format(simple_response, **data)
        return HttpResponse(content=body,
                            content_type='text/html; charset=utf-8',
                            status=501)

    def not_found(self, details=''):
        '''This can also be overridden if a more detailed 404 is required'''
        if not details:
            details = self.request.path
        data = dict(response_string='404 Not found', details=details)
        try:
            template = loader.get_template('main/not_found.html')
            c = Context(data)
            body = template.render(c)
        except TemplateDoesNotExist:
            body = str.format(simple_response, **data)
        return HttpResponse(content=body,
                            content_type='text/html; charset=utf-8',
                            status=404)

    def render_html(self, template):
        template = loader.get_template(template)
        c = RequestContext(self.request, self.data)
        return HttpResponse(content=template.render(c),
                            content_type='text/html; charset=utf-8',
                            status=200)

    @classmethod
    def as_view(cls):
        def aux(request, *args, **kwargs):
            handler = cls()
            return handler(request, *args, **kwargs)
        return aux

    def default(self):
        '''Method place-holder.  Override.'''
        return self.not_implemented()

    def action(self):
        '''Method place-holder.  Override.'''
        return self.not_implemented()
    
    def __call__(self, request, *args, **kwargs):
        self.url_args = args
        self.request = request
        #
        # Normalize request data into an "args" parameter.
        # "args" will be a QueryDict in _all_ cases.
        # URL arguments always override other data (for now)
        #
        if request.method == 'GET':
            if request.GET is not None:
                args = request.GET.copy()
                args.update(kwargs) # we'll see how this works
                return self._dispatch(args)
            elif kwargs:
                args = QueryDict()
                # Fake out url regex args as form args
                # that will then allow binding and 
                # futher validation
                args.update(kwargs)
                return self._dispatch(args)
            else:
                return self.default()
        elif request.method == 'POST':
            if request.POST is not None:
                args = request.POST.copy()
                args.update(kwargs) # we'll see how this works
                return self._dispatch(args)
        else:
            return self.not_implemented()


# vim: set sts=4 sw=4 expandtab:
