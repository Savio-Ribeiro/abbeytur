from copy import deepcopy
from django.conf import settings
from django.contrib import admin
from django.core.exceptions import ImproperlyConfigured
from django.urls import resolve, Resolver404

try:
    from django.utils.deprecation import MiddlewareMixin
except ImportError:
    MiddlewareMixin = object


class ModelAdminReorder(MiddlewareMixin):
    def init_config(self, request, app_list):
        self.request = request
        self.app_list = app_list

        self.config = getattr(settings, 'ADMIN_REORDER', None)
        if not self.config:
            raise ImproperlyConfigured('ADMIN_REORDER config is not defined.')

        if not isinstance(self.config, (tuple, list)):
            raise ImproperlyConfigured(
                'ADMIN_REORDER must be a list or tuple.')

        admin_index = admin.site.index(request)
        try:
            app_list = admin_index.context_data['app_list']
        except (AttributeError, KeyError):
            return

        self.models_list = []
        for app in app_list:
            for model in app['models']:
                model['model_name'] = self.get_model_name(
                    app['app_label'], model['object_name'])
                self.models_list.append(model)

    def get_app_list(self):
        ordered_app_list = []
        for app_config in self.config:
            app = self.make_app(app_config)
            if app:
                ordered_app_list.append(app)
        return ordered_app_list

    def make_app(self, app_config):
        if isinstance(app_config, str):
            return self.find_app(app_config)
        elif isinstance(app_config, dict):
            return self.process_app(app_config)
        else:
            raise TypeError('ADMIN_REORDER items must be str or dict.')

    def find_app(self, app_label):
        for app in self.app_list:
            if app['app_label'] == app_label:
                return app
        return None

    def get_model_name(self, app_name, model_name):
        return f'{app_name}.{model_name}'

    def process_app(self, app_config):
        app = self.find_app(app_config['app'])
        if app:
            app = deepcopy(app)
            if 'label' in app_config:
                app['name'] = app_config['label']
            if 'models' in app_config:
                app['models'] = self.process_models(app_config['models'])
            return app
        return None

    def process_models(self, models_config):
        models = []
        for item in models_config:
            if isinstance(item, str):
                model = self.find_model(item)
            elif isinstance(item, dict):
                model = self.process_model(item)
            else:
                continue
            if model:
                models.append(model)
        return models

    def find_model(self, model_name):
        for model in self.models_list:
            if model['model_name'] == model_name:
                return model
        return None

    def process_model(self, model_config):
        model = self.find_model(model_config.get('model'))
        if model and 'label' in model_config:
            model = deepcopy(model)
            model['name'] = model_config['label']
        return model

    def process_template_response(self, request, response):
        try:
            url = resolve(request.path_info)
        except Resolver404:
            return response

        if not (url.app_name == 'admin' or url.namespace == 'admin'):
            return response

        try:
            app_list = response.context_data['app_list']
        except (AttributeError, KeyError):
            return response

        self.init_config(request, app_list)
        ordered_app_list = self.get_app_list()
        response.context_data['app_list'] = ordered_app_list
        return response
