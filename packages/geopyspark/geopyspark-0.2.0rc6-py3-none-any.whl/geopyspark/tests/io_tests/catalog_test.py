import unittest
import os
import pytest

from shapely.geometry import box

from geopyspark.geotrellis import Extent, SpatialKey, GlobalLayout
from geopyspark.geotrellis.catalog import read, read_value, query, read_layer_metadata, AttributeStore
from geopyspark.geotrellis.constants import LayerType
from geopyspark.geotrellis.geotiff import get
from geopyspark.tests.base_test_class import BaseTestClass
from geopyspark.tests.python_test_utils import geotiff_test_path


class CatalogTest(BaseTestClass):
    rdd = get(LayerType.SPATIAL, geotiff_test_path("srtm_52_11.tif"))

    metadata = rdd.collect_metadata()
    reprojected = rdd.tile_to_layout(layout=GlobalLayout(zoom=11), target_crs="EPSG:3857")
    result = reprojected.pyramid()

    dir_path = geotiff_test_path("catalog/")
    uri = "file://{}".format(dir_path)
    layer_name = "catalog-test"

    @pytest.fixture(autouse=True)
    def tearDown(self):
        yield
        BaseTestClass.pysc._gateway.close()

    def test_read(self):
        for x in range(11, 0, -1):
            actual_layer = query(self.uri, self.layer_name, x)
            expected_layer = self.result.levels[x]

            self.assertDictEqual(actual_layer.layer_metadata.to_dict(),
                                 expected_layer.layer_metadata.to_dict())

    def test_read_value(self):
        tiled = read_value(self.uri,
                           self.layer_name,
                           11,
                           1450,
                           966)

        self.assertEqual(tiled.cells.shape, (1, 256, 256))

    def test_bad_read_value(self):
        tiled = read_value(self.uri,
                           self.layer_name,
                           11,
                           1450,
                           2000)

        self.assertEqual(tiled, None)

    @pytest.mark.skipif('TRAVIS' in os.environ,
                         reason="test_query_1 causes issues on Travis")
    def test_query1(self):
        intersection = box(8348915.46680623, 543988.943201519, 8348915.4669, 543988.943201520)
        queried = query(self.uri, self.layer_name, 11, intersection)

        self.assertEqual(queried.to_numpy_rdd().first()[0], SpatialKey(1450, 996))

    def test_query2(self):
        intersection = Extent(8348915.46680623, 543988.943201519, 8348915.4669, 543988.943201520)
        queried = query(self.uri, self.layer_name,
                        11, intersection,
                        query_proj=3857)

        self.assertEqual(queried.to_numpy_rdd().first()[0], SpatialKey(1450, 996))

    def test_query3(self):
        intersection = box(8348915.46680623, 543988.943201519, 8348915.4669, 543988.943201520).wkb
        queried = query(self.uri, self.layer_name,
                        11, intersection)

        self.assertEqual(queried.to_numpy_rdd().first()[0], SpatialKey(1450, 996))

    def test_query4(self):
        intersection = 42
        with pytest.raises(TypeError):
            queried = query(self.uri, self.layer_name,
                            11, query_geom=intersection, num_partitions=2)
            result = queried.to_numpy_rdd().first()[0]

    def test_query_partitions(self):
        intersection = box(8348915.46680623, 543988.943201519, 8348915.4669, 543988.943201520)
        queried = query(self.uri, self.layer_name,
                        11, intersection, num_partitions=2)

        self.assertEqual(queried.to_numpy_rdd().first()[0], SpatialKey(1450, 996))

    def test_query_crs(self):
        intersection = box(8348915.46680623, 543988.943201519, 8348915.4669, 543988.943201520)
        queried = query(self.uri, self.layer_name, 11, intersection,
                        query_proj=3857)

        self.assertEqual(queried.to_numpy_rdd().first()[0], SpatialKey(1450, 996))

    def test_read_metadata_exception(self):
        uri = "abcxyz://123"
        with pytest.raises(ValueError):
            layer = read_layer_metadata(uri, self.layer_name, 5)

    def test_read_metadata1(self):
        layer = query(self.uri, self.layer_name, 5)
        actual_metadata = layer.layer_metadata

        expected_metadata = read_layer_metadata(self.uri, self.layer_name, 5)
    def test_read_metadata2(self):
        layer = query(self.uri, self.layer_name, 5)
        actual_metadata = layer.layer_metadata

        expected_metadata = read_layer_metadata(self.uri, self.layer_name, 5)

        self.assertEqual(actual_metadata.to_dict(), expected_metadata.to_dict())

    def test_layer_ids(self):
        ids = AttributeStore(self.uri).layers()
        self.assertTrue(len(ids) == 11)

    def test_attributestore(self):
        store = AttributeStore(self.uri)
        layer_name = "boop-epsg-bop"
        value = {"first": 113, "second": "44two"}
        store.layer(layer_name, 34).write("val", value)
        self.assertEqual(value,
                         store.layer(layer_name, 34).read("val"))

        self.assertEqual(value,
                         store.layer(layer_name, 34)["val"])
        store.layer(layer_name, 34).delete("val")
        with pytest.raises(KeyError):
            store.layer(layer_name, 34)["val"]

if __name__ == "__main__":
    unittest.main()
