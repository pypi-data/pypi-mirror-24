#
# General:
#      This file is pary of .NET Bridge
#
# Copyright:
#      2010 Jonathan Shore
#      2017 Jonathan Shore and Contributors
#
# License:
#      Licensed under the Apache License, Version 2.0 (the "License");
#      you may not use this file except in compliance with the License.
#      You may obtain a copy of the License at:
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#      Unless required by applicable law or agreed to in writing, software
#      distributed under the License is distributed on an "AS IS" BASIS,
#      WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#      See the License for the specific language governing permissions and
#      limitations under the License.
#


from pydotnet.clr.CLRMessage import CLRMessage
from pydotnet.core.io import *


class CLRTemplateReply (CLRMessage):
    """
    Class for representing information about a type
    """

    def __init__(self, info = {}):

        super().__init__ (CLRMessage.TypeTemplateReply, info)


    def serialize (self, sock: BinarySocketWriter):
        """
        Serialize message
        """
        super().serialize(sock)
        properties = self.value["properties"]
        methods = self.value["methods"]
        classmethods = self.value["classmethods"]

        sock.writeStringArray(properties)
        sock.writeStringArray(methods)
        sock.writeStringArray(classmethods)


    def deserialize (self, sock: BinarySocketReader):
        """
        Deserialize message (called after magic & type read)
        """
        super().deserialize(sock)
        properties = sock.readStringArray()
        methods = sock.readStringArray()
        classmethods = sock.readStringArray()
        self.value = {"properties": properties, "methods": methods, "classmethods": classmethods}

