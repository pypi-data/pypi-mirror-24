""" can.py

Defines the low-level implementation of CAN.

"""


class FrameType:
    """ Enumerates the types of CAN frames """
    DataFrame = 1
    RemoteFrame = 2
    ErrorFrame = 3
    OverloadFrame = 4


class Frame(object):
    """ Represents a CAN Frame

    Attributes:
        arb_id (int): Arbitration identifier of the Frame
        data (list of int): CAN data bytes
        frame_type (int): type of CAN frame
    """

    def __init__(self, arb_id, data=None, frame_type=FrameType.DataFrame,
                 interface=None, timestamp=None, extended=False):
        """ Initializer of Frame
        Args:
            arb_id (int): identifier of CAN frame
            data (list, optional): data of CAN frame, defaults to empty list
            frame_type (int, optional): type of frame, defaults to
                                        FrameType.DataFrame
            interface (string, optional): name of the interface the frame is on
                                          defaults to None
            ts (float, optional): time frame was received at
                                  defaults to None
        """

        self.frame_type = frame_type
        self.interface = interface
        self.timestamp = timestamp
        self.is_extended_id = extended
        self.arb_id = arb_id
        if data:
            self.data = data
        else:
            self.data = []

    @property
    def arb_id(self):
        return self._arb_id

    @arb_id.setter
    def arb_id(self, value):
        # ensure value is an integer
        assert isinstance(value, int), 'arbitration id must be an integer'
        # ensure id is in range
        if not self.is_extended_id and value >= 0 and value <= 0x7FF:
            self._arb_id = value
        elif self.is_extended_id and value >= 0 and value <= 0x1FFFFFFF:
            self._arb_id = value
        else:
            # otherwise, id is not valid
            raise ValueError('Arbitration ID out of range')

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        # data should be a list
        assert isinstance(value, list), 'CAN data must be a list'
        # data can only be 8 bytes maximum
        assert not len(value) > 8, 'CAN data cannot contain more than 8 bytes'
        # each byte must be a valid byte, int between 0x0 and 0xFF
        for byte in value:
            assert isinstance(byte, int), 'CAN data must consist of bytes'
            assert byte >= 0 and byte <= 0xFF, 'CAN data must consist of bytes'
        # data is valid
        self._data = value

    @property
    def frame_type(self):
        return self._frame_type

    @frame_type.setter
    def frame_type(self, value):
        assert value == FrameType.DataFrame or value == FrameType.RemoteFrame \
            or value == FrameType.ErrorFrame or \
            value == FrameType.OverloadFrame, 'invalid frame type'
        self._frame_type = value

    @property
    def dlc(self):
        return len(self.data)

    def __str__(self):
        return ('ID=0x%03X, DLC=%d, Data=[%s]' %
                (self.arb_id, self.dlc, ', '.join(('%02X' % b)
                                                  for b in self.data)))

    def __eq__(self, other):
        return (self.arb_id == other.arb_id and
                self.data == other.data and
                self.frame_type == other.frame_type and
                self.is_extended_id == other.is_extended_id)
