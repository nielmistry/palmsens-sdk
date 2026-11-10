from __future__ import annotations

import pytest
from PalmSens.Devices import (
    EmStat4HRCapabilities,
    EmStatPicoCapabilities,
    NexusCapabilities,
    PalmSens4Capabilities,
)

import pypalmsens as ps
from pypalmsens._instruments.shared import bipot_ranging_error

RANGING = {'min': '10nA', 'max': '100uA', 'start': '1uA'}


def method(current_range, enable_bipot_current=True):
    return ps.ChronoAmperometry(
        enable_bipot_current=enable_bipot_current,
        bipot={'mode': 'constant', 'potential': 1.0, 'current_range': current_range},
    )._to_psmethod()


@pytest.mark.parametrize(
    'capabilities', [PalmSens4Capabilities, EmStat4HRCapabilities, EmStatPicoCapabilities]
)
def test_ranging_refused(capabilities):
    message = bipot_ranging_error(method(RANGING), capabilities())

    assert message
    assert 'autoranging' in message


def test_ranging_allowed_on_nexus():
    assert bipot_ranging_error(method(RANGING), NexusCapabilities()) is None


@pytest.mark.parametrize('capabilities', [PalmSens4Capabilities, NexusCapabilities])
def test_fixed_range_allowed(capabilities):
    assert bipot_ranging_error(method('1uA'), capabilities()) is None


def test_default_allowed():
    psmethod = ps.ChronoAmperometry(enable_bipot_current=True)._to_psmethod()

    assert bipot_ranging_error(psmethod, PalmSens4Capabilities()) is None


def test_ignored_without_bipot_current():
    psmethod = method(RANGING, enable_bipot_current=False)

    assert bipot_ranging_error(psmethod, PalmSens4Capabilities()) is None
