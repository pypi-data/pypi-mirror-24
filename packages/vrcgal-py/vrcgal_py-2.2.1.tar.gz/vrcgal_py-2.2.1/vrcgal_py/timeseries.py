# -*- coding: utf-8 -*-
# Copyright (c) Virtual Reality and Clinical Gait Analysis Laboratory

import numpy as np

from scipy import interpolate as interp


def interpolate(time, data, desired_frequency, kind='cubic'):
    interpolated = interp.interp1d(time, data, kind=kind)
    new_time = np.linspace(time[0], time[-1], time[-1] * desired_frequency)
    return [new_time, interpolated(new_time)]


def time_from_timestamp(time_stamp, timeconversion=1 / 1000):
    time = np.zeros(len(time_stamp))
    for t in range(0, len(time_stamp) - 1):
        dT = (time_stamp[t + 1] - time_stamp[t]) * timeconversion
        time[t + 1] = (t + 1 + dT) / 100
    return time
