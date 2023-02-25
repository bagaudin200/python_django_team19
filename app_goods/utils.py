import os


def product_directory_path(instance, filename):
    # файл будет загружен в MEDIA_ROOT/<products>/<category>
    file_name, file_extension = os.path.splitext(filename)
    return 'products/{0}/{1}'.format(instance.category, f"{instance}{file_extension}")
