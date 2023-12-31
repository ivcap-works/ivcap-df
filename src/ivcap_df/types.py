#
# Copyright (c) 2023 Commonwealth Scientific and Industrial Research Organisation (CSIRO). All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file. See the AUTHORS file for names of contributors.
#

class NotAuthorizedException(BaseException):
    pass

# Should be made more specific, same as ivcap-client-sdk
URN = str
