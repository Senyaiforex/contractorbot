from yoomoney import Authorize, Quickpay, Client

token = "4100118944044936.C2B7E48BB2B6058C7835CE3A63C1B0519BB508B6232CC20DC8840B15F01DE0DCED9AA014B125E214F6DEF87B5EF8920B60D56EDA7736964F963017BE815E75B399B3F2BA5733EB1E5DACA2640DB2E0887CAF77ECF5ABF4031D2506E6196FDE30046E5791755A0493B03B5933CB96C3F18843115BBE44CF9155EC73A40145B5DA"

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

# client_id: str = "3F7F48D75FCE9BC4BA2323A0F2B286925E8BE68C3C889D71317B2EBAE1E33271"
# secret_key: str = "1D1B227E7B19197144E9D113B906E0B7B6C660335C1C8D88E730F433641CE28C6F2EF0919CBAAFE85E1EDF14E3882B968F5AB8D420DA5E93CA90595DD5245943"
# Authorize(client_id=client_id,
#           # client_id полученный при регистрации приложения (B7598786A657D9CB4F455468BE00C2BD1590A07453456784F85133098E0D9)
#           redirect_uri="https://t.me/BHleads_bot",
#           # redirect_uri указанный при регистрации приложения (https://f.ggdt.ru/)
#           client_secret=secret_key,
#           scope=["account-info", "operation-history", "operation-details", "incoming-transfers", "payment-p2p",
#                  "payment-shop", ])