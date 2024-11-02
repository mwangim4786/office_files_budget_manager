# office_files_budget_manager
Office Files Budget Manager is a web application that facilitates cashless payments for bills incurred during processing of client instructions in an organisation. It is built by utilising the mobile money technology in Kenya.

The justification of the project apart from cashless transactions is that it allows reconciliation of spending on client file fees since transactions are done against the client’s file. This also allows the user to view either overspending or underspending on client’s file fees

Employees in an organisation prepare budgets that are approved by directors/admins and avail the funds to their portal. Transactions are therefore made from these budgets against the particular client file.

# Check out the DEMO VIDEO HERE.
https://drive.google.com/file/d/1istzqJaX-__1G1ab1UYQQHYzJHtWMIFi/view?usp=sharing

# Running the project
To successfully run the project, a tunnelling tool is required as the project is not deployed. I use engrok for this purpose. It gives me the functionality of a secure http(https).
This is a requirement for the payment request API to work.
The following command is run on ngrok
- ngrok http 5000
here, 5000 is the port from where the project runs