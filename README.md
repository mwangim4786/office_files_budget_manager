# office_files_budget_manager
Office Files Budget Manager is a web application that facilitates cashless payments for bills incurred during processing of client instructions in an organisation. It is built by utilising the mobile money technology in Kenya.

The justification of the project apart from cashless transactions is that it allows reconciliation of spending on client file fees since transactions are done against the client’s file. This also allows the user to view either overspending or underspending on client’s file fees

Employees in an organisation prepare budgets that are approved by directors/admins and avail the funds to their portal. Transactions are therefore made from these budgets against the particular client file.

# Check out the DEMO VIDEO HERE.
https://drive.google.com/file/d/1NsmByHJDNZ3DXioOv_a-Xo04RsnV2-gg/view?usp=sharing

# Running the project
To successfully run the project, a tunnelling tool is required as the project is not deployed. I use ngrok for this purpose. It gives me the functionality of a secure http(https).
This is a requirement for the payment request API to work.
The following command is run on ngrok
- ngrok http 5000
here, 5000 is the port from where the project runs

This generates the secure url for the project.
The following url is generated and can run the project successfully
    - https://3916-2c0f-fe38-2014-b463-d55f-ccdd-c50a-6b18.ngrok-free.app/

To access the project, run the following python commands to add users for login purposes


from app import app, db, Bcrypt
from datetime import datetime
bcrypt = Bcrypt()
date_val =  '2024-11-01'
date_value = datetime.strptime(date_val, "%Y-%m-%d")
with app.app_context():
	from app.models.users import Users
	user1 = Users(name='John Doe', email='jon@gmail.com', phone='254722345678', role='Admin', password=bcrypt.generate_password_hash('123').decode('utf-8'), date=date_value)
	user2 = Users(name='New User', email='new@gmail.com', phone='254742345678', role='Staff', password=bcrypt.generate_password_hash('123').decode('utf-8'), date=date_value)
	user3 = Users(name='Pat Jenkins', email='pat@gmail.com', phone='254712345678', role='Admin', password=bcrypt.generate_password_hash('123').decode('utf-8'), date=date_value)
	db.session.add(user1)
	db.session.add(user2)
	db.session.add(user3)
	db.session.commit()

Use phone = 254722345678 and password = 123 to login