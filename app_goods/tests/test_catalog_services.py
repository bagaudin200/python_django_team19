from django.test import TestCase, RequestFactory, SimpleTestCase

from app_goods.services.catalog_services import Builder, CatalogQueryStringBuilder


class TestBuilder(SimpleTestCase):
    URLS = {
        '/catalog': {},
        '/catalog/?category=bytovaya-tehnika': {'category': 'bytovaya-tehnika'},

        # sort URLs
        '/catalog/?&category=bytovaya-tehnika&order_by=price&order=asc': {'category': 'bytovaya-tehnika',
                                                                          'order_by': 'price', 'order': 'asc'},
        '/catalog/?&category=bytovaya-tehnika&order_by=price&order=desc': {'category': 'bytovaya-tehnika',
                                                                           'order_by': 'price', 'order': 'desc'},
        '/catalog/?&category=bytovaya-tehnika&order_by=reviews&order=asc': {'category': 'bytovaya-tehnika',
                                                                            'order_by': 'reviews', 'order': 'asc'},
        '/catalog/?&category=bytovaya-tehnika&order_by=reviews&order=desc': {'category': 'bytovaya-tehnika',
                                                                             'order_by': 'reviews', 'order': 'desc'},
        '/catalog/?&category=bytovaya-tehnika&order_by=novelty&order=asc': {'category': 'bytovaya-tehnika',
                                                                            'order_by': 'novelty', 'order': 'asc'},
        '/catalog/?&category=bytovaya-tehnika&order_by=novelty&order=desc': {'category': 'bytovaya-tehnika',
                                                                             'order_by': 'novelty', 'order': 'desc'},
        '/catalog/?&category=bytovaya-tehnika&order_by=popular&order=asc': {'category': 'bytovaya-tehnika',
                                                                            'order_by': 'popular', 'order': 'asc'},
        '/catalog/?&category=bytovaya-tehnika&order_by=popular&order=desc': {'category': 'bytovaya-tehnika',
                                                                             'order_by': 'popular', 'order': 'desc'},

        # tag URLs
        '/catalog/?tag=asus': {'tag': 'asus'},

        # filter URLs
        '/catalog/?category=None&order=None&order_by=None&price=642.84%3B1142.84&title=&in_stock=0&free_delivery=0': {
            'category': 'None', 'order': 'None', 'order_by': 'None', 'price': '642.84%3B1142.84', 'title': '',
            'in_stock': '0', 'free_delivery': '0'
        },
        '/catalog/?category=None&order=None&order_by=None&price=642.84%3B847&title=LG&in_stock=0&in_stock=1'
        '&free_delivery=0&free_delivery=1': {
            'category': 'None', 'order': 'None', 'order_by': 'None', 'price': '642.84%3B847', 'title': 'LG',
            'in_stock': '1', 'free_delivery': '1'
        },

        # pagination URLs
        '/catalog/?&page=2': {},
        '/catalog/?category=None&order=None&order_by=None&price=642.84%3B847&title=LG&in_stock=0&in_stock=1'
        '&free_delivery=0&free_delivery=1&page=2': {
            'category': 'None', 'order': 'None', 'order_by': 'None', 'price': '642.84%3B847', 'title': 'LG',
            'in_stock': '1', 'free_delivery': '1'
        },

        # incorrect URLs
        '/catalog/?ggg=34098ih&sdflfgh=5': {},
        '/catalog/?ggg=34098ih&sdflfgh=5&sdf;lgkjdf;lkg=;lkj09j?gdfg=444': {},
        '/catalog/?ggg=dfgdfg&fff=sdf=gdfg=': {},
    }

    def setUp(self) -> None:
        self.factory = RequestFactory()

    def test_query_string_to_dict(self):
        for url, dict_ in self.URLS.items():
            builder = Builder(self.factory.get(url))
            self.assertEqual(builder.query_string_to_dict(), dict_)


class TestCatalogQueryStringBuilder(SimpleTestCase):
    PARAMS = [
        {'params': dict(order_by='popular', order='asc'), 'string': '?&order_by=popular&order=asc'},
        {'params': dict(order_by='popular', order='desc'), 'string': '?&order_by=popular&order=desc'},
        {'params': dict(order_by='price', order='asc'), 'string': '?&order_by=price&order=asc'},
        {'params': dict(order_by='price', order='desc'), 'string': '?&order_by=price&order=desc'},
        {'params': dict(order_by='reviews', order='asc'), 'string': '?&order_by=reviews&order=asc'},
        {'params': dict(order_by='reviews', order='desc'), 'string': '?&order_by=reviews&order=desc'},
        {'params': dict(order_by='novelty', order='asc'), 'string': '?&order_by=novelty&order=asc'},
        {'params': dict(order_by='novelty', order='desc'), 'string': '?&order_by=novelty&order=desc'},
    ]

    def setUp(self) -> None:
        self.factory = RequestFactory()

    def test_build(self):
        url = self.factory.get('/catalog/')
        for params in self.PARAMS:
            qsb = CatalogQueryStringBuilder(url, **params['params']).build()
            self.assertEqual(qsb, params['string'])


class TestCatalogQuerySetBuilder(TestCase):
    pass
