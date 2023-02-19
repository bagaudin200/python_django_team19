import os

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage, InvalidPage


def product_directory_path(instance, filename):
    # файл будет загружен в MEDIA_ROOT/<products>/<category>
    file_name, file_extension = os.path.splitext(filename)
    return 'products/{0}/{1}'.format(instance.category, f"{instance}{file_extension}")


class CatalogPaginator(Paginator):
    def validate_number(self, number):
        try:
            return super().validate_number(number)
        except InvalidPage:
            if int(number) > 1:
                return self.num_pages
            return 1
