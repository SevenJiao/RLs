#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import importlib

from typing import \
    Optional

from rls.common.config import Config
from rls.memories.replay_buffer import ReplayBuffer
from rls.utils.logging_utils import get_logger
logger = get_logger(__name__)


BufferDict = {
    'ER': 'ExperienceReplay',
    'PER': 'PrioritizedExperienceReplay',
    'NstepER': 'NStepExperienceReplay',
    'NstepPER': 'NStepPrioritizedExperienceReplay',
    'EpisodeER': 'EpisodeExperienceReplay'
}


def get_buffer(apex_buffer_args: Config) -> Optional[ReplayBuffer]:
    '''
    parsing arguments of replay buffer
    params:
        apex_buffer_args: configurations of replay buffer
    return:
        Correct experience replay mechanism.
        For On-Policy algorithms, they don't have to specify a replay buffer out of model class, so return None
    '''

    if apex_buffer_args.get('buffer_size', 0) <= 0:
        logger.info('This algorithm does not need sepecify a data buffer oustside the model.')
        return None

    _buffer_type = apex_buffer_args.get('type', 'None')
    logger.info(_buffer_type)

    if _buffer_type in BufferDict.keys():
        Buffer = getattr(importlib.import_module(f'rls.memories.replay_buffer'),
                         BufferDict[_buffer_type])
        return Buffer(batch_size=apex_buffer_args['batch_size'],
                      capacity=apex_buffer_args['buffer_size'],
                      **apex_buffer_args[_buffer_type].to_dict)
    else:
        return None
