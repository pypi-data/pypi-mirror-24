#!/usr/bin/env python
# -*- coding: utf-8 -*-

###############################################################################
#  Copyright Kitware Inc.
#
#  Licensed under the Apache License, Version 2.0 ( the "License" );
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
###############################################################################

from girder import events
from girder.constants import AssetstoreType

from . metadata_extractor import ServerMetadataExtractor


def handler(event):
    if event.info['assetstore']['type'] == AssetstoreType.FILESYSTEM:
        metadataExtractor = ServerMetadataExtractor(event.info['assetstore'],
                                                    event.info['file'])
        metadataExtractor.extractMetadata()


def load(info):
    events.bind('data.process', 'metadata_extractor_handler', handler)
