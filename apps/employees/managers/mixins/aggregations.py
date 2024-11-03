from django.db.models import Count


class AggregationsMixin:
      
    def get_counts_grouped_by(self, group_by: str = 'gender'):
      return self.get_queryset().values(group_by).annotate(
          counts=Count('pk')
      )
