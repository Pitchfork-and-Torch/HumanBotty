import unittest

from humanbotty_sense_head.safety import (
    Limits,
    SupervisorState,
    clear_estop,
    command_allowed,
    gated_command,
    latch_estop,
)


class SafetyTests(unittest.TestCase):
    def test_estop_blocks(self):
        st = SupervisorState(last_ok_monotonic=10.0)
        latch_estop(st, True)
        self.assertFalse(command_allowed(st, 10.05, Limits(), True))

    def test_watchdog_blocks(self):
        st = SupervisorState(last_ok_monotonic=0.0)
        self.assertFalse(command_allowed(st, 1.0, Limits(watchdog_sec=0.4), True))

    def test_clamps_and_rate(self):
        st = SupervisorState(last_ok_monotonic=1.0, last_pan=0.0, last_tilt=0.0)
        pan, tilt, ok = gated_command(9.0, 9.0, st, 1.05, 0.05, Limits(vel_max=0.8), True)
        self.assertTrue(ok)
        self.assertLess(abs(pan), 0.05)
        self.assertLess(abs(tilt), 0.05)

    def test_zero_dt_holds(self):
        st = SupervisorState(last_ok_monotonic=1.0, last_pan=0.2, last_tilt=-0.1)
        pan, tilt, ok = gated_command(0.4, 0.0, st, 1.0, 0.0, Limits(), True)
        self.assertTrue(ok)
        self.assertAlmostEqual(pan, 0.2)
        self.assertAlmostEqual(tilt, -0.1)

    def test_estop_clear_requires_allow(self):
        st = SupervisorState(last_ok_monotonic=10.0)
        latch_estop(st, True)
        clear_estop(st, False)
        self.assertTrue(st.estop_latched)
        clear_estop(st, True)
        self.assertFalse(st.estop_latched)
        self.assertTrue(command_allowed(st, 10.05, Limits(), True))



    def test_watchdog_soft_rearms_on_live_tick(self):
        st = SupervisorState(last_ok_monotonic=0.0, last_pan=0.1, last_tilt=-0.05)
        # Stale watchdog would block command_allowed forever without soft-rearm.
        self.assertFalse(command_allowed(st, 1.0, Limits(watchdog_sec=0.4), True))
        pan, tilt, ok = gated_command(0.2, 0.0, st, 1.0, 0.02, Limits(watchdog_sec=0.4), True)
        self.assertTrue(ok)
        self.assertAlmostEqual(st.last_ok_monotonic, 1.0)

    def test_after_estop_clear_watchdog_does_not_stick(self):
        st = SupervisorState(last_ok_monotonic=10.0, last_pan=0.0, last_tilt=0.0)
        latch_estop(st, True)
        clear_estop(st, True)
        # E-stop held > watchdog_sec; clear alone must not leave motion frozen.
        pan, tilt, ok = gated_command(0.0, 0.0, st, 11.0, 0.02, Limits(watchdog_sec=0.4), True)
        self.assertTrue(ok)
        self.assertFalse(st.estop_latched)

if __name__ == "__main__":
    unittest.main()
