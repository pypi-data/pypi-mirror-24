#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Nexmo API
# Copyright (c) 2008-2017 Hive Solutions Lda.
#
# This file is part of Hive Nexmo API.
#
# Hive Nexmo API is free software: you can redistribute it and/or modify
# it under the terms of the Apache License as published by the Apache
# Foundation, either version 2.0 of the License, or (at your option) any
# later version.
#
# Hive Nexmo API is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# Apache License for more details.
#
# You should have received a copy of the Apache License along with
# Hive Nexmo API. If not, see <http://www.apache.org/licenses/>.

__author__ = "João Magalhães <joamag@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008-2017 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """

import appier

from . import sms
from . import account

BASE_URL = "https://rest.nexmo.com/"
""" The default base url to be used when no other
base url value is provided to the constructor """

class API(
    appier.API,
    sms.SmsAPI,
    account.AccountAPI
):

    def __init__(self, *args, **kwargs):
        appier.API.__init__(self, *args, **kwargs)
        self.api_key = appier.conf("NEXMO_API_KEY", None)
        self.api_secret = appier.conf("NEXMO_API_SECRET", None)
        self.base_url = kwargs.get("base_url", BASE_URL)
        self.api_key = kwargs.get("api_key", self.api_key)
        self.api_secret = kwargs.get("api_secret", self.api_secret)

    def build(
        self,
        method,
        url,
        data = None,
        data_j = None,
        data_m = None,
        headers = None,
        params = None,
        mime = None,
        kwargs = None
    ):
        appier.API.build(self, method, url, headers, kwargs)
        kwargs["api_key"] = self.api_key
        kwargs["api_secret"] = self.api_secret
