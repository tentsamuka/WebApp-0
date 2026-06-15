class UserAlreadyExists(Exception):
     pass

class UserNotFounded(Exception):
    pass

class WrongPasswordError(Exception):
     pass 

class AccessTokenExpired(Exception):
     pass

class AccessTokenMismatch(Exception):
     pass

class InvalidCredentials(Exception):
     pass