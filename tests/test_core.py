"""Independent metric examples, numerical stability and leakage checks."""
import unittest
import io
from zipfile import ZipFile
import numpy as np
from appletree.data import split_records, load_record, inventory
from appletree.metrics import confusion, scores
from appletree.model import GaussianPixels, features


class CoreTests(unittest.TestCase):
    def test_pairing_uses_timestamp_not_just_identity(self):
        archive = io.BytesIO()
        with ZipFile(archive, "w") as source:
            for kind in ("RGB", "D", "GT"):
                source.writestr(f"dataset/R01N01_Summer_{kind}-12-00-00.png", b"placeholder")
            source.writestr("dataset/R01N02_Summer_GT-12-00-01.png", b"placeholder")
            source.writestr("dataset/R01N02_Summer_RGB-12-00-02.png", b"placeholder")
        archive.seek(0)
        records, issues = inventory(archive)
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0]["tree"], "R01N01")
        self.assertEqual(issues[0]["missing"], ["D", "RGB"])

    def test_known_confusion(self):
        counts = confusion([1, 1, 0, 0], [1, 0, 1, 0])
        np.testing.assert_array_equal(counts, [1, 1, 1, 1])
        self.assertAlmostEqual(scores(counts)["iou"], 1/3)
        self.assertEqual(scores(counts)["dice"], .5)

    def test_empty_masks(self):
        self.assertEqual(scores(confusion([0], [0]))["iou"], 1)
        self.assertEqual(scores(confusion([1], [0]))["recall"], 0)

    def test_invalid_masks(self):
        with self.assertRaises(ValueError):
            confusion([255], [1])

    def test_identity_split(self):
        records = [{"tree": str(i)} for i in range(20) for _ in range(2)]
        splits = split_records(records)
        sets = [set(r["tree"] for r in rows) for rows in splits.values()]
        self.assertEqual(sum(map(len, splits.values())), len(records))
        self.assertFalse(sets[0] & sets[1] or sets[0] & sets[2] or sets[1] & sets[2])
        self.assertEqual(splits, split_records(records))

    def test_geometry_gate(self):
        with self.assertRaises(ValueError):
            load_record(None, None)

    def test_classifier_separation_and_stability(self):
        model = GaussianPixels().fit(np.array([[0.], [0.], [1.], [1.]]), np.array([0,0,1,1]))
        p = model.predict_proba(np.array([[0.], [1.], [10000.]]))
        self.assertLess(p[0], .01)
        self.assertGreater(p[1], .99)
        self.assertTrue(np.isfinite(p).all())

    def test_class_absence(self):
        with self.assertRaises(ValueError):
            GaussianPixels().fit(np.zeros((2, 1)), np.zeros(2))

    def test_depth_feature_ablation(self):
        rgb = np.zeros((2,3,3), dtype=np.uint8)
        self.assertEqual(features(rgb).shape, (6,3))
        self.assertEqual(features(rgb, rgb).shape, (6,6))


if __name__ == "__main__":
    unittest.main()
