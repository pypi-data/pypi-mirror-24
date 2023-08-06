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


class CLRGetIndexedProperty (CLRMessage):
    """
    Class for calling index on object
    """

    def __init__(self, objectId: int = 0, property: str = "", idx: int = 0):
        super().__init__ (CLRMessage.TypeGetIndexedProperty, (objectId, property, idx))
        self.objectId = objectId
        self.property = property
        self.index = idx


    def serialize (self, sock: BinarySocketWriter):
        """
        Serialize message
        """
        super().serialize(sock)
        sock.writeInt32(self.objectId)
        sock.writeString(self.property)
        sock.writeInt32(self.index)


    def deserialize (self, sock: BinarySocketReader):
        """
        Deserialize message (called after magic & type read)
        """
        super().deserialize(sock)
        self.objectId = sock.readInt32()
        self.property = sock.readString()
        self.index = sock.readInt32()


