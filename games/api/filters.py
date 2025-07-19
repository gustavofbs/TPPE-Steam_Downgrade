import django_filters
from django.db.models import Q
from decimal import Decimal
from games.models import Game


class GameFilter(django_filters.FilterSet):
    """
    Filtro customizado para jogos com suporte a filtros de preço,
    desenvolvedores, gêneros e outros parâmetros.
    """
    
    # Filtros de preço
    min_price = django_filters.NumberFilter(
        method='filter_min_price',
        help_text="Preço mínimo"
    )
    max_price = django_filters.NumberFilter(
        method='filter_max_price',
        help_text="Preço máximo"
    )
    
    # Filtro para jogos em promoção
    on_sale = django_filters.BooleanFilter(
        field_name='discount_percent',
        method='filter_on_sale',
        help_text="Apenas jogos em promoção"
    )
    
    # Filtros por múltiplos valores (separados por vírgula)
    genres = django_filters.CharFilter(
        method='filter_genres',
        help_text="IDs dos gêneros separados por vírgula (ex: 1,2,3)"
    )
    
    developers = django_filters.CharFilter(
        method='filter_developers', 
        help_text="IDs dos desenvolvedores separados por vírgula (ex: 1,2,3)"
    )
    
    publishers = django_filters.CharFilter(
        method='filter_publishers',
        help_text="IDs das publicadoras separados por vírgula (ex: 1,2,3)"
    )
    
    # Filtros existentes
    is_featured = django_filters.BooleanFilter()
    is_active = django_filters.BooleanFilter()
    
    class Meta:
        model = Game
        fields = {
            'title': ['icontains'],
            'release_date': ['gte', 'lte'],
            'base_price': ['gte', 'lte'],
            'discount_percent': ['gte', 'lte'],
        }
    
    def filter_min_price(self, queryset, name, value):
        """Filtrar por preço mínimo usando preço final (com desconto se aplicável)"""
        if value is not None:
            # Usar uma abordagem mais simples: filtrar jogos individualmente
            filtered_ids = []
            for game in queryset:
                final_price = game.discount_price  # Usa a propriedade que calcula o preço final
                if final_price >= value:
                    filtered_ids.append(game.id)
            return queryset.filter(id__in=filtered_ids)
        return queryset
    
    def filter_max_price(self, queryset, name, value):
        """Filtrar por preço máximo usando preço final (com desconto se aplicável)"""
        if value is not None:
            # Usar uma abordagem mais simples: filtrar jogos individualmente
            filtered_ids = []
            for game in queryset:
                final_price = game.discount_price  # Usa a propriedade que calcula o preço final
                if final_price <= value:
                    filtered_ids.append(game.id)
            return queryset.filter(id__in=filtered_ids)
        return queryset
    
    def filter_on_sale(self, queryset, name, value):
        """Filtrar apenas jogos em promoção (discount_percent > 0)"""
        if value:
            return queryset.filter(discount_percent__gt=0)
        return queryset
    
    def filter_genres(self, queryset, name, value):
        """Filtrar por múltiplos gêneros"""
        if value:
            try:
                genre_ids = [int(id.strip()) for id in value.split(',') if id.strip()]
                if genre_ids:
                    return queryset.filter(genres__id__in=genre_ids).distinct()
            except ValueError:
                pass
        return queryset
    
    def filter_developers(self, queryset, name, value):
        """Filtrar por múltiplos desenvolvedores"""
        if value:
            try:
                dev_ids = [int(id.strip()) for id in value.split(',') if id.strip()]
                if dev_ids:
                    return queryset.filter(developer__id__in=dev_ids).distinct()
            except ValueError:
                pass
        return queryset
    
    def filter_publishers(self, queryset, name, value):
        """Filtrar por múltiplas publicadoras"""
        if value:
            try:
                pub_ids = [int(id.strip()) for id in value.split(',') if id.strip()]
                if pub_ids:
                    return queryset.filter(publisher__id__in=pub_ids).distinct()
            except ValueError:
                pass
        return queryset
