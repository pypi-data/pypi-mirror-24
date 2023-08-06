# -*- coding: utf-8 -*-
"""
Tests for geojson/validation
"""

import unittest

import geojson


class TestValidationGeometry(unittest.TestCase):

    def test_invalid_geometry_with_validate(self):
        self.assertRaises(
            ValueError, geojson.Point, (10, 20, 30, 40), validate=True)

    def test_invalid_geometry_without_validate(self):
        try:
            geojson.Point((10, 20, 30))
            geojson.Point((10, 20, 30), validate=False)
        except ValueError:
            self.fail("Point raised ValueError unexpectedly")

    def test_valid_geometry(self):
        try:
            geojson.Point((10, 20), validate=True)
            geojson.Point((10, 20), validate=False)
        except ValueError:
            self.fail("Point raised ValueError unexpectedly")

    def test_valid_geometry_with_elevation(self):
        try:
            geojson.Point((10, 20, 30), validate=True)
            geojson.Point((10, 20, 30), validate=False)
        except ValueError:
            self.fail("Point raised ValueError unexpectedly")


class TestValidationGeoJSONObject(unittest.TestCase):

    def test_valid_jsonobject(self):
        point = geojson.Point((-10.52, 2.33))
        self.assertEqual(point.is_valid, True)


class TestValidationPoint(unittest.TestCase):

    def test_invalid_point(self):
        point = geojson.Point((10, 20, 30, 40))
        self.assertEqual(point.is_valid, False)

    def test_valid_point(self):
        point = geojson.Point((-3.68, 40.41))
        self.assertEqual(point.is_valid, True)

    def test_valid_point_with_elevation(self):
        point = geojson.Point((-3.68, 40.41, 3.45))
        self.assertEqual(point.is_valid, True)


class TestValidationMultipoint(unittest.TestCase):

    def test_invalid_multipoint(self):
        mpoint = geojson.MultiPoint(
            [(3.5887,), (3.5887, 10.44558),
             (2.5555, 3.887, 4.56), (2.44, 3.44, 2.555, 4.56)])
        self.assertEqual(mpoint.is_valid, False)

    def test_valid_multipoint(self):
        mpoint = geojson.MultiPoint([(10, 20), (30, 40)])
        self.assertEqual(mpoint.is_valid, True)

    def test_valid_multipoint_with_elevation(self):
        mpoint = geojson.MultiPoint([(10, 20, 30), (30, 40, 50)])
        self.assertEqual(mpoint.is_valid, True)


class TestValidationLineString(unittest.TestCase):

    def test_invalid_linestring(self):
        ls = geojson.LineString([(8.919, 44.4074)])
        self.assertEqual(ls.is_valid, False)

    def test_valid_linestring(self):
        ls = geojson.LineString([(10, 5), (4, 3)])
        self.assertEqual(ls.is_valid, True)


class TestValidationMultiLineString(unittest.TestCase):

    def test_invalid_multilinestring(self):
        mls = geojson.MultiLineString([[(10, 5), (20, 1)], []])
        self.assertEqual(mls.is_valid, False)

    def test_valid_multilinestring(self):
        ls1 = [(3.75, 9.25), (-130.95, 1.52)]
        ls2 = [(23.15, -34.25), (-1.35, -4.65), (3.45, 77.95)]
        mls = geojson.MultiLineString([ls1, ls2])
        self.assertEqual(mls.is_valid, True)


class TestValidationPolygon(unittest.TestCase):

    def test_invalid_polygon(self):
        poly1 = geojson.Polygon(
            [[(2.38, 57.322), (23.194, -20.28), (-120.43, 19.15)]])
        self.assertEqual(poly1.is_valid, False)
        poly2 = geojson.Polygon(
            [[(2.38, 57.322), (23.194, -20.28),
                (-120.43, 19.15), (2.38, 57.323)]])
        self.assertEqual(poly2.is_valid, False)

    def test_valid_polygon(self):
        poly = geojson.Polygon(
            [[(2.38, 57.322), (23.194, -20.28),
                (-120.43, 19.15), (2.38, 57.322)]])
        self.assertEqual(poly.is_valid, True)


class TestValidationMultiPolygon(unittest.TestCase):

    def test_invalid_multipolygon(self):
        poly1 = [(2.38, 57.322), (23.194, -20.28),
                 (-120.43, 19.15), (25.44, -17.91)]
        poly2 = [(2.38, 57.322), (23.194, -20.28),
                 (-120.43, 19.15), (2.38, 57.322)]
        multipoly = geojson.MultiPolygon([poly1, poly2])
        self.assertEqual(multipoly.is_valid, False)

    def test_valid_multipolygon(self):
        poly1 = [[(2.38, 57.322), (23.194, -20.28),
                  (-120.43, 19.15), (2.38, 57.322)]]
        poly2 = [[(-5.34, 3.71), (28.74, 31.44),
                  (28.55, 19.10), (-5.34, 3.71)]]
        poly3 = [[(3.14, 23.17), (51.34, 27.14),
                  (22, -18.11), (3.14, 23.17)]]
        multipoly = geojson.MultiPolygon([poly1, poly2, poly3])
        self.assertEqual(multipoly.is_valid, True)
