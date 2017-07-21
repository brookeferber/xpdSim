import bluesky.examples as be


class Robot(be.Mover):
    # Not a "Device" - not from Ophyd
    # Include class variables (and the mpas) that appear in reference code?
    def __init__(self, name, fields, initial_set, theta, diff=None, **kwargs):
        # theta : motor
        # diff : motor, optional (not used in reference code)
        self.theta = theta
        self._current_sample_gemorety = None
        super().__init__(name, fields, initial_set, **kwargs)

    # What functions should be included?

