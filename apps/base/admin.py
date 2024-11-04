from djangoql.admin import DjangoQLSearchMixin, apply_search


class CustomDjangoQLSearchMixin(DjangoQLSearchMixin):
    def get_search_results(self, request, queryset, search_term):
        qs = apply_search(queryset, search_term, self.djangoql_schema)
        return qs, False
