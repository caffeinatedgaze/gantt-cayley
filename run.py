from gantt_cayley import app
from db import driver


# print(driver.get_quads(label='PROJECT', relation='group', value='TopCats'))
# print(driver.get_object_by_id(object_type='GROUP', object_id='1').project)

# for i in range(1, 5):
#     print(driver.get_object_by_id(object_type='USER', object_id=i).in_group)


user = driver.get_user_by_id(4)
print(user.in_group)

# if __name__ == "__main__":
#     app.run(debug=True, host='0.0.0.0')
