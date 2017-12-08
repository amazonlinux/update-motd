# Copyright (c) 2011 Amazon.com, Inc. or its affiliates.  All Rights Reserved.
#
# Licensed under the Amazon Software License (the "License").  You may not use
# this file except in compliance with the License. A copy of the License is
# located at http://aws.amazon.com/asl or in the "license" file accompanying
# this file.  This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES
# OR CONDITIONS OF ANY KIND, either express or implied. See the License for
# the specific language governing permissions and limitations under the License.

__version__     = '1.0'
__author__      = 'Amazon Web Services, Inc.'
__license__     = 'Amazon Software License (http://aws.amazon.com/asl/)'

import os, subprocess
from yum.plugins import TYPE_CORE

requires_api_version = '2.3'
plugin_type = (TYPE_CORE)

def posttrans_hook(conduit):
    try:
        if not os.path.exists('/var/lib/update-motd/disabled'):
            subprocess.Popen(['/sbin/start', '--quiet', 'update-motd'], stdout=open('/dev/null', 'w'), stderr=subprocess.STDOUT)
    except:
        return
