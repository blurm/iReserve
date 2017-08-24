# -*- coding: utf-8 -*-


class IReserveError(BaseException):
    def __init__(self, message):

        if isinstance(message, unicode):
            super(IReserveError, self).__init__(message.encode('utf-8'))
            self.message = message

        elif isinstance(message, str):
            super(IReserveError, self).__init__(message)
            self.message = message.decode('utf-8')

        # This shouldn't happen...
        else:
            raise TypeError

    def __unicode__(self):

        return self.message
    pass


class IReserveLoginError(IReserveError):
    pass


class IReserveLoginFastError(IReserveError):
    pass


class IReserveSMSError(IReserveError):
    pass


class IReserveReserveError(IReserveError):
    pass


class IReserveAvailError(IReserveError):
    pass


class ISMSTimeoutError(IReserveError):
    '''Raised when message recieving time out'''
    pass

