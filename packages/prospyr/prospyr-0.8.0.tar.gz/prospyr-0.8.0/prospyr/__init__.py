# -*- coding: utf-8 -*-
# flake8: noqa

from __future__ import absolute_import, print_function, unicode_literals

# alias some useful things here.
from prospyr.connection import connect
from prospyr.resources import (Account, Activity, ActivityType, Company,
                               CustomerSource, Identifier, Lead, LossReason,
                               Opportunity, Person, Pipeline, PipelineStage,
                               Task, User, Webhook)
from prospyr.version import VERSION
