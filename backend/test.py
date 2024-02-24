# url = config("INTERNET_URL", default=123)
# url = config("INTERNET_URL", default='http://127.0.0.1:8000')
# 7aa4a5d9-116e-4c7c-a235-643c5af7f1ae



# print(int("kkk"))

# import os
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.settings')
# from django import setup
# setup()

# from django.conf import settings


# from dashboard.models import BotUserBalanceModel


# user = BotUserBalanceModel.objects.get(id=1)
# user.safe_balance = 99999999999
# user.save(force_update=True)


# from database.base import DB
# from database.models.bot import *
# from database.models.telegram import *

# DB.create_tables([ BotProductsModel, BotBuyHistoryModel ])

# (
#     ThroughModelHelper.from_through(WebAdmin2TG_ChatModel)
#         .remove(WebAdminModel(id=2), BotChatModel(id=1))
# )

# BotChatProductsModel.create()



# BotProductsModel.create(
#     creator=2,
#     type=BotProductsModel.Type.REAL,
#     name="Какая-то залупа",
#     description="Какая-то залупа",
#     count=10,
# )

# for x in BotChat2UserModel.select():
#     x: BotChat2UserModel
#     x.delete_instance()

"""


user_id = 2
query = (
    ThroughModelHelper.from_through(WebAdmin2TG_ChatModel)
        .included(WebAdminModel(id=user_id))
        .join(BotChat2UserModel)
        .group_by(BotChat2UserModel._meta.primary_key)
        .join(BotUserModel)
        .group_by(BotUserModel.get_pk())
        .join(BotChatBuyHistoryModel)
        .group_by(BotChatBuyHistoryModel.get_pk())
        # .switch(BotUserModel)
        # .objects()
)

for model in query:
    model: BotUserModel
    print("@USER", model.id)


"""



# """


# paginator = Paginator(
#     BotUserModel,
#     lambda fields: (
#         ThroughModelHelper.from_through(WebAdmin2TG_ChatModel)
#             .included(WebAdminModel.get_by_id(2), fields=fields)
#             .join(BotChat2UserModel)
#             .group_by(BotChat2UserModel._meta.primary_key)
#             .join(BotUserModel)
#             .group_by(BotUserModel.get_pk())
#             .switch(BotUserModel)
#             .objects()
#     )
    
# )

# print(query)
# print(list(query))

# print(paginator.count)
# id = 2

# paginator = Paginator(
#     BotTransferHistoryModel,
#     lambda fields: (
#         BotTransferHistoryModel.select(*fields)
#             .where(
#                 (BotTransferHistoryModel.u_from == id)
#                 | (BotTransferHistoryModel.u_to == id)
#             )
#             .order_by(BotTransferHistoryModel.get_pk().desc())
#     )
# )


# for model in paginator.goto_page(2):
#     model: BotTransferHistoryModel
#     print("@USER", model.id)


# for model in paginator.get_page(2):
#     model: BotUserModel
#     print("@USER", model.id, model.login)

# """
    

"""
import rsa

pub_key, priv_key = rsa.newkeys(256)

print("Private RSA key (2048). (aka master_key_priv for for file mfkey.priv)")
s_privkey = priv_key.save_pkcs1()
print(s_privkey)
print('')

print("Public RSA key (2048). (aka master_key_pub for file mfkey.pub)")
s_pubkey = pub_key.save_pkcs1()
print(s_pubkey)
print('')
"""
"""
import jwt

SECRET_KEY = '@tu0z&kw18zn04f7hx#_1p2x645c&)5bkpcjozz7fz)7z2_u)q'

token = jwt.encode({
    'id': "123",
}, SECRET_KEY, algorithm='HS256')


print(token)


print(jwt.decode(token, SECRET_KEY, algorithms=['HS256']))
"""

