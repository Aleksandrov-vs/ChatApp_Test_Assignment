from pydantic import BaseModel


class AuthResponse(BaseModel):
    cabinetUserId: int
    accessToken: str
    accessTokenEndTime: int
    refreshToken: str
    refreshTokenEndTime: int


class CheckPhoneResponse(BaseModel):
    exist: bool
    chatId: str | None


class SendMsgData(BaseModel):
    id: str
    chatId: str


class SendMsgResponse(BaseModel):
    success: bool
    data: SendMsgData


class PairOfTokens(BaseModel):
    access_token: str
    refresh_token: str
