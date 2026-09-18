import math
import random
import unittest

from humanbotty_sense_head.policies import idle_saccade, look_at_face, look_at_sound


class PolicyTests(unittest.TestCase):
    def test_face_centers(self):
        pan, tilt = look_at_face((0.4, 0.4, 0.2, 0.2), 0.0, 0.0, gain=1.0)
        self.assertAlmostEqual(pan, 0.0)
        self.assertAlmostEqual(tilt, 0.0)

    def test_face_right_pans_left(self):
        pan, _tilt = look_at_face((0.7, 0.4, 0.2, 0.2), 0.0, 0.0, gain=1.0)
        self.assertLess(pan, 0.0)

    def test_missing_box(self):
        self.assertEqual(look_at_face(None, 0.1, -0.2), (0.1, -0.2))

    def test_face_non_finite_holds(self):
        self.assertEqual(
            look_at_face((float("nan"), 0.4, 0.2, 0.2), 0.1, -0.2),
            (0.1, -0.2),
        )

    def test_face_non_positive_size_holds(self):
        self.assertEqual(look_at_face((0.4, 0.4, 0.0, 0.2), 0.1, -0.2), (0.1, -0.2))
        self.assertEqual(look_at_face((0.4, 0.4, 0.2, -0.1), 0.1, -0.2), (0.1, -0.2))

    def test_face_out_of_frame_holds(self):
        # Wholly right of / below / left of / above the normalized image.
        self.assertEqual(look_at_face((1.2, 0.4, 0.2, 0.2), 0.1, -0.2), (0.1, -0.2))
        self.assertEqual(look_at_face((0.4, 1.1, 0.2, 0.2), 0.1, -0.2), (0.1, -0.2))
        self.assertEqual(look_at_face((-0.5, 0.4, 0.2, 0.2), 0.1, -0.2), (0.1, -0.2))
        self.assertEqual(look_at_face((0.4, -0.4, 0.2, 0.2), 0.1, -0.2), (0.1, -0.2))

    def test_face_center_outside_unit_square_holds(self):
        # Intersects the frame but geometric center is outside [0,1].
        self.assertEqual(look_at_face((-0.05, 0.4, 0.08, 0.2), 0.1, -0.2), (0.1, -0.2))
        self.assertEqual(look_at_face((0.9, 0.4, 0.3, 0.2), 0.1, -0.2), (0.1, -0.2))
        self.assertEqual(look_at_face((0.4, -0.05, 0.2, 0.08), 0.1, -0.2), (0.1, -0.2))

    def test_sound(self):
        pan, tilt = look_at_sound(0.4, 0.0, 0.1, gain=0.5)
        self.assertAlmostEqual(pan, 0.2)
        self.assertAlmostEqual(tilt, 0.1)

    def test_saccade_bounded(self):
        rng = random.Random(0)
        pan, tilt = idle_saccade(0.0, 0.0, rng=rng, max_step=0.04)
        self.assertLessEqual(abs(pan), 0.04)
        self.assertLessEqual(abs(tilt), 0.02)


class LookMemoryTests(unittest.TestCase):
    def test_import_look_arbiter_symbols(self):
        from humanbotty_sense_head.policies import (
            LookMemory,
            remember_face,
            remember_pose,
            remember_sound,
            tick_look,
        )
        mem = LookMemory()
        remember_pose(mem, 0.1, -0.2)
        remember_face(mem, (0.4, 0.4, 0.2, 0.2), 1.0)
        remember_sound(mem, 0.3, 1.0)
        pan, tilt = tick_look(mem, 1.05, rng=random.Random(0))
        self.assertTrue(math.isfinite(pan) and math.isfinite(tilt))

    def test_stale_face_falls_to_idle(self):
        from humanbotty_sense_head.policies import LookMemory, remember_face, tick_look
        mem = LookMemory(pan=0.0, tilt=0.0)
        remember_face(mem, (0.8, 0.4, 0.2, 0.2), 0.0)
        pan, _tilt = tick_look(mem, 5.0, rng=random.Random(1), face_ttl=0.35)
        self.assertLessEqual(abs(pan), 0.05)

    def test_bad_face_payload_ignored(self):
        from humanbotty_sense_head.policies import LookMemory, remember_face
        mem = LookMemory()
        remember_face(mem, (0.1, 0.2), 1.0)  # too short
        self.assertIsNone(mem.face_box)
        remember_face(mem, (float("nan"), 0.4, 0.2, 0.2), 1.0)
        self.assertIsNone(mem.face_box)


if __name__ == "__main__":
    unittest.main()
