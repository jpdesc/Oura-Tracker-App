# import app
# # from datetime import date

# # # for event in app.events:
# # #     print(event)

# # if log_query:
# #     print('success')
# # app.db.session.commit()
# # print("committed")


# log_query = app.Log.query.order_by(app.Log.id).all()
# for entry in log_query:
#     entry.focus = entry.focus // 2
#     entry.mood = entry.mood // 2
#     entry.energy = entry.energy // 2
#     app.db.session.add(entry)
#     # print(type(entry))
# #     print(entry.mood)
# # print(log_query)
# # print(type(log_query))
# app.db.session.commit()
