class ResponseCode:
    SUCCESS = 200
    FAIL = -1
    NO_RESOURCE_FOUND = 40001  # 未找到资源
    INVALID_PARAMETER = 40002  # 参数无效
    ACCOUNT_OR_PASSWORD_ERROR = 40003  # 账户或密码错误
    VERIFICATION_CODE_ERROR = 40004  # 验证码错误
    PLEASE_SIGN_IN = 40005  # 请登录
    INVALID_OR_EXPIRED = 40006  # 验证码过期
    MOBILE_PHONE_ERROR = 40007  # 手机号错误
    FREQUENT_OPERATION = 40008  # 操作过于频繁，请稍后再试


class ResponseMessage:
    SUCCESS = '成功'
    FAIL = '失败'
    NO_RESOURCE_FOUND = '未找到资源'
    INVALID_PARAMETER = '参数无效'
    ACCOUNT_OR_PASSWORD_ERROR = '账户或密码错误'
    VERIFICATION_CODE_ERROR = '验证码错误'
    PLEASE_SIGN_IN = '请登录'
    INVALID_OR_EXPIRED = '验证码过期'
    MOBILE_PHONE_ERROR = '手机号错误'
    FREQUENT_OPERATION = '操作过于频繁，请稍后再试'
