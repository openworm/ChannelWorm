from django.views.generic import ListView, CreateView


class AjaxResponseMixin(object):
    """
    Mixin allows you to define alternative methods for ajax requests. Similar
    to the normal get, post, and put methods, you can use get_ajax, post_ajax,
    and put_ajax.
    """

    def dispatch(self, request, *args, **kwargs):
        request_method = request.method.lower()

        if request.is_ajax() and request_method in self.http_method_names:
            handler = getattr(self, u"{0}_ajax".format(request_method),
                              self.http_method_not_allowed)
            self.request = request
            self.args = args
            self.kwargs = kwargs
            return handler(request, *args, **kwargs)

        return super(AjaxResponseMixin, self).dispatch(
            request, *args, **kwargs)

    def get_ajax(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)

    def post_ajax(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def put_ajax(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)

    def delete_ajax(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)


class AjaxMixinListView(AjaxResponseMixin, ListView):
    def get_ajax(self, request, *args, **kwargs):
        self.template_name_suffix = '_list_ajax'
        return self.get(request, *args, **kwargs)


class AjaxMixinCreateView(AjaxResponseMixin, CreateView):
    parentId_url_kwarg = 'parentId'

    def get_ajax(self, request, *args, **kwargs):
        self.template_name_suffix = '_create_form_ajax'
        response = self.get(request, *args, **kwargs)
        response.context_data[self.parentId_url_kwarg] = kwargs[self.parentId_url_kwarg]
        return response
