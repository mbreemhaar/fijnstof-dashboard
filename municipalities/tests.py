from django.db import IntegrityError
from django.db.models import ProtectedError
from django.test import TestCase

from municipalities.models import Province, Municipality


class ProvinceTestCase(TestCase):
    def test_create_province(self):
        province = Province.objects.create(code=123, name='Test Province')

        self.assertEquals(province.code, 123)
        self.assertEquals(province.name, 'Test Province')

    def test_province_code_unique(self):
        with self.assertRaises(expected_exception=IntegrityError):
            Province.objects.create(code=123, name='Test Province 1')
            Province.objects.create(code=123, name='Test Province 2')

    def test_delete_province(self):
        province = Province.objects.create(code=123, name='Test Province')
        province.delete()

        self.assertFalse(Province.objects.filter(code=123).exists())

    def test_delete_province_with_municipalities(self):
        province = Province.objects.create(code=123, name='Test Province')
        Municipality.objects.create(code=456, name='Test Municipality', province=province)

        with self.assertRaises(ProtectedError):
            province.delete()


class MunicipalityTestCase(TestCase):
    def setUp(self):
        self.province = Province.objects.create(code=1, name='Test Province 1')

    def test_create_municipality(self):
        municipality = Municipality.objects.create(code=123, name='Test Municipality', province=self.province)

        self.assertEquals(municipality.code, 123)
        self.assertEquals(municipality.name, 'Test Municipality')
        self.assertEquals(municipality.province, self.province)

    def test_municipality_code_unique(self):
        with self.assertRaises(expected_exception=IntegrityError):
            Municipality.objects.create(code=123, name='Test Municipality 1', province=self.province)
            Municipality.objects.create(code=123, name='Test Municipality 2', province=self.province)

    def test_delete_province(self):
        municipality = Municipality.objects.create(code=123, name='Test Municipality', province=self.province)
        municipality.delete()

        self.assertFalse(Municipality.objects.filter(code=123).exists())
