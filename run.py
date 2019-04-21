from gantt_cayley import app
from db import driver

# driver.filter_by('USER', 'ff')
print(driver.get_user_by_id(4))

# if __name__ == "__main__":
#     app.run(debug=True, host='0.0.0.0')
