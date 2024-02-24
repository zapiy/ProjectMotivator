# from database.base import ThroughModelHelper
# from database.models.telegram import *

# query = (
#     ThroughModelHelper.from_through(BotChat2UserModel)
#         .included(BotChatModel(id=1))
#         .where(BotUserModel.id == 3)
#         .exists()
# )

# for u in BotUserModel.select():
#     u: BotUserModel
#     u.delete_instance()

# "/\B@\w+/g"

# 4bbce8ed-637b-45f1-bf20-53a96731de2e

# from database.models.bot import WebAdminModel
# from peewee import IntegrityError

# try:
#     WebAdminModel(
#         user_identity_token = "123123"
#     ).save()
# except IntegrityError:
#     print("Exists")




# model:BotUserModel = BotUserModel.get_by_id(1)
# model.current_balance = 90
# model.save()

# from datetime import datetime
# import locale
# locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')
# print(datetime.now().strftime('%d %B'))

