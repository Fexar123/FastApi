from fastapi import HTTPException
class EmailAlreadyRegistred(HTTPException):
    def __init__ (self, detail:str = "Email already registret"):
        super().__init__(status_code=404, detail=detail)
    
