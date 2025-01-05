from yoomoney import Authorize, Quickpay, Client

token = "4100118911991584.23B4ED42CC68DD76247C39396EE4E7AC62C6F9DE6D77EA4550AB4FB87741C8FEF5E4EEBACF4F8914C4313E14B74F58861F5D0E04F9FB7836A3AF67EE4726CA3BF6231DFCA29A898EDE78C8F96D3D482C01AA4F98ACF1E131F47C312800673361017BA66EE463F7218698DB5DF032F406C99E10833C45DE7715446D242373C19F"

#
async def create_url_payment(user_id: int, price: float):
    """
    Функция для формирования ссылки на оплату подписки
    :param user_id: id пользователя телеграм
    :return: url
    """
    label = f'{user_id}:{price}'
    quickpay = Quickpay(receiver="4100118911991584", quickpay_form='shop', targets="Sponsor this project",
                        paymentType='AC', sum=price, label=label)
    return quickpay.redirected_url

# АВТОРИЗАЦИЯ ПРИЛОЖЕНИЯ
# client_id: str = "460C7E434B0503C10B13443519749415033949783C917F55E837EA3AEEAF9C6D"
# secret_key: str = "C5125AA2BC744D28CC8770F84CC1FB21B5CE80AE12015E127E39A199E527790CD4D418E91D3B78BDB877B71556071612010A7B8F4B2F47C6AC0A1C65465836CB"
# Authorize(client_id=client_id,
#           # client_id полученный при регистрации приложения (B7598786A657D9CB4F455468BE00C2BD1590A07453456784F85133098E0D9)
#           redirect_uri="https://t.me/spoolfit_bot",
#           # redirect_uri указанный при регистрации приложения (https://f.ggdt.ru/)
#           client_secret=secret_key,
#           scope=["account-info", "operation-history", "operation-details", "incoming-transfers", "payment-p2p",
#                  "payment-shop", ])