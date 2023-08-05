#!/usr/bin/env python
# Copyright (C) The Arvados Authors. All rights reserved.
#
# SPDX-License-Identifier: AGPL-3.0

from __future__ import absolute_import, print_function

import errno
import logging
import time
import threading
import unittest

import mock
import pykka

from . import testutil

import arvnodeman.baseactor

class BogusActor(arvnodeman.baseactor.BaseNodeManagerActor):
    def __init__(self, e):
        super(BogusActor, self).__init__()
        self.exp = e

    def doStuff(self):
        raise self.exp

    def ping(self):
        # Called by WatchdogActorTest, this delay is longer than the test timeout
        # of 1 second, which should cause the watchdog ping to fail.
        time.sleep(4)
        return True

class ActorUnhandledExceptionTest(testutil.ActorTestMixin, unittest.TestCase):
    def test_fatal_error(self):
        for e in (MemoryError(), threading.ThreadError(), OSError(errno.ENOMEM, "")):
            with mock.patch('os.kill') as kill_mock:
                act = BogusActor.start(e).tell_proxy()
                act.doStuff()
                act.actor_ref.stop(block=True)
                self.assertTrue(kill_mock.called)

    @mock.patch('os.kill')
    def test_nonfatal_error(self, kill_mock):
        act = BogusActor.start(OSError(errno.ENOENT, "")).tell_proxy()
        act.doStuff()
        act.actor_ref.stop(block=True)
        self.assertFalse(kill_mock.called)

class WatchdogActorTest(testutil.ActorTestMixin, unittest.TestCase):
    @mock.patch('os.kill')
    def test_time_timout(self, kill_mock):
        act = BogusActor.start(OSError(errno.ENOENT, ""))
        watch = arvnodeman.baseactor.WatchdogActor.start(1, act)
        watch.stop(block=True)
        act.stop(block=True)
        self.assertTrue(kill_mock.called)
