def product_directory_path(instance, filename):
    # файл будет загружен в MEDIA_ROOT/<products>/<category>
    return 'products/{0}/{1}'.format(instance.product.category, filename)
