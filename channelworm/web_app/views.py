from django.http import JsonResponse
from django.views.generic import ListView


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


class BaseAjaxAction(AjaxResponseMixin):
    parentId_url_kwarg = None
    json_success_response = {'status': 'success', 'result': 'Entity data has been saved.'}
    json_error_response = {'status': 'error', 'message': 'Entity has not been saved.', 'validation': None}

    def get_ajax(self, request, *args, **kwargs):
        response = self.get(request, *args, **kwargs)
        if self.parentId_url_kwarg:
            response.context_data[self.parentId_url_kwarg] = kwargs[self.parentId_url_kwarg]

        return response

    def create_success_ajax_response(self):
        self.json_success_response['pk'] = self.object.pk
        return self.json_success_response

    def post_ajax(self, request, *args, **kwargs):
        form = self.get_form()

        if form.is_valid():
            self.form_valid(form)
            response_data = self.create_success_ajax_response()
            return JsonResponse(response_data)
        else:
            self.json_error_response['validation'] = form.errors
            return JsonResponse(self.json_error_response, status=400)


class AjaxMixinCreateView(BaseAjaxAction):
    parentId_url_kwarg = None
    json_success_response = {'status': 'success', 'result': 'Entity has been saved.'}

    def get_ajax(self, request, *args, **kwargs):
        self.template_name_suffix = '_create_form_ajax'
        return super(AjaxMixinCreateView, self).get_ajax(self, request, *args, **kwargs)


class AjaxMixinUpdateView(BaseAjaxAction):
    parentId_url_kwarg = None
    json_success_response = {'status': 'success', 'result': 'Entity has been saved.'}

    def get_ajax(self, request, *args, **kwargs):
        self.template_name_suffix = '_update_form_ajax'
        return super(AjaxMixinUpdateView, self).get_ajax(self, request, *args, **kwargs)

    def post_ajax(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(AjaxMixinUpdateView, self).post_ajax(request, *args, **kwargs)


class AjaxMixinDeleteView(BaseAjaxAction):
    json_success_response = {'status': 'success', 'result': 'Entity has been deleted.'}

    def get_ajax(self, request, *args, **kwargs):
        self.template_name_suffix = '_confirm_delete_ajax'
        return super(AjaxMixinDeleteView, self).get_ajax(self, request, *args, **kwargs)

    def delete_ajax(self, request, *args, **kwargs):
        print("delete_ajax")
        self.object = self.get_object()
        self.object.delete()

        return JsonResponse(self.create_success_ajax_response())

    def post_ajax(self, request, *args, **kwargs):
        print("post_ajax")
        return self.delete_ajax(self, request, *args, **kwargs)

    def create_success_ajax_response(self):
        return self.json_success_response