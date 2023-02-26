def product_directory_path(instance, filename):
    # файл будет загружен в MEDIA_ROOT/<products>/<category>/<product_name>/
    return 'products/{0}/{1}/{2}'.format(instance.category, instance, filename)
