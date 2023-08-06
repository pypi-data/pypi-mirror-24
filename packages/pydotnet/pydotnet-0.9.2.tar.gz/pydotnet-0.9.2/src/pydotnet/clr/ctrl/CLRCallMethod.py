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

from pydotnet.core.io import *
from pydotnet.clr.CLRMessage import CLRMessage
from pydotnet.clr.CLRTypeFactory import CLRTypeFactory


class CLRCallMethod (CLRMessage):
    """
    Class for calling methods
    """

    def __init__(self, objectId: int = 0, methodname: str="", argv=[]):
        from pydotnet.clr.CLRMessage import CLRMessage
        super().__init__ (CLRMessage.TypeCallMethod, (objectId, methodname, argv))
        self.objectId = objectId
        self.methodname = methodname
        self.argv = argv


    def serialize (self, sock: BinarySocketWriter):
        """
        Serialize message
        """
        super().serialize(sock)
        sock.writeInt32(self.objectId)
        sock.writeString(self.methodname)
        sock.writeInt16(len(self.argv))
        for arg in self.argv:
            msg = CLRTypeFactory.createByValue(arg)
            msg.serialize(sock)


    def deserialize (self, sock: BinarySocketReader):
        """
        Deserialize message (called after magic & type read)
        """
        super().deserialize(sock)
        self.objectId = sock.readInt32()
        self.methodname = sock.readString()
        argc = sock.readInt16()
        self.argv = [CLRMessage.read(sock).value for i in range(0,argc)]


