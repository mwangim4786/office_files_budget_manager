#!/usr/bin/python3

from flask import render_template, request, url_for, flash, redirect, abort, session, Blueprint
from app import db, bcrypt
from app.views.payment.forms import PayForm
from app.models.budget import Budget
from app.models.files import Files
from datetime import datetime
from flask_login import login_user, current_user, logout_user, login_required

payments = Blueprint('payments', __name__)


filezNo = ''
budgetzId = 0
descriptionZ = ''
uzer_id = 0


@payments.route('/payment_request', methods=['POST', 'GET'])
@login_required
def payment_request():
    # files = Files.query.all()
    form = PayForm()
    budgets_list = [("wrong-Budgetz", "Select Budget")]
    budgets = Budget.query.filter_by(user_id=current_user.id, status=1).all()
    for budget in budgets:
        bdgtPurpose = budget.bdgt_name
        bdgtId = budget.id
        bdgtAmnt = str(budget.amount)
        bdgtFig = bdgtPurpose+ ' - ' +bdgtAmnt
        budgets_list.append((bdgtId, bdgtFig))
    form.budget_no.choices = budgets_list
    
    files = Files.query.all()
    files_list = [("wrong-Filez", "Select File")]
    for file in files:
        fileNo = file.file_no
        fileName = file.file_name
        full_desc = fileNo+ ' - ' +fileName
        files_list.append((fileNo, full_desc))
    form.file_no.choices = files_list

    if form.validate_on_submit():
        # Payment variables
        amount = form.amount.data
        narration = str(form.narration.data)
        partyB = form.paybill.data
        file = str(form.file_no.data)
        budgetId = form.budget_no.data
        print(budgetId)

        # -----------------------------------------------------------------------------
        budget = Budget.query.get_or_404(budgetId)
        transactions = Transaction.query.filter_by(budget=budgetId).all()
        trans_amnt_list = []
        if transactions:
            for trans in transactions:
                trans_amount = trans.amount
                trans_amnt_list.append(trans_amount)
        utilised_funds = sum(trans_amnt_list)
        available_funds = budget.amount - utilised_funds

        if amount > available_funds:
            flash('Insufficient funds for this transaction!  Avalilable funds - '+str(available_funds)+'', 'warning')
            return redirect(url_for('transactionz.transactions'))
        # -----------------------------------------------------------------------------

        token = generate_access_token()
        initiator_pass = "Safaricom999!*!"
        public_key = "-----BEGIN CERTIFICATE-----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-----END CERTIFICATE-----"
        # security_credential = base64.b64encode((initiator_pass + public_key).encode('utf-8')).decode()
        securityCredential = "ZdWTIszTXMkF07d8tPQKxwLYSqBhWODLzu66+m5uXBgdg8mGmUQRVjjdo16KqRKKpwl5SLzjTzyLBKncYHew2iuSZzBeBzG4k7U7g8SO+ThizuM7UvFSHTj0AchQqBRppcFcYFnIo8t+QmfNfnqbsYGnT/nd0biR7Cn1G8w1UE7kTYBsY5TkB4WzmleByvyzGMpiz9UQHGIv9q3yrKmdH3+Akw80u8ibMriN1iyQFORILZvpA7pfsjr0VIC9sV0hFh632fuskT4biklhn4CbOCmpAkfCe90mf2GEUCsQBjLJ1WR1ewFuLPiJvxPEsywv5Kr9q8vRmlEMoQXDcaqhEw=="

        url = 'https://sandbox.safaricom.co.ke/mpesa/b2b/v1/paymentrequest'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer %s' % token
        }
        payload = {
            "Initiator": "testapi",
            "SecurityCredential": securityCredential,
            "CommandID": "BusinessPayBill",
            "SenderIdentifierType": "4",
            "RecieverIdentifierType": 4,
            "Amount": amount,
            "PartyA": 600997,
            "PartyB": partyB,
            "AccountReference": "353353",
            "Requester": "254700000000",
            "Remarks": "OK",
            "QueueTimeOutURL": "https://budgetfiles.onrender.com/callback",
            "ResultURL": "https://budgetfiles.onrender.com/callback"
        }

        try:
            response = requests.request("POST", url, headers = headers, json = payload).json()
            if response['ResponseCode'] == '0':
                global filezNo, budgetzId, descriptionZ, uzer_id
                filezNo = file
                budgetzId = budgetId
                descriptionZ = narration
                uzer_id = current_user.id
                print(filezNo)
                # return response
                data = dict()
                data['amount'] = amount
                data['paybill']   = partyB
                data['file_no']   = file
                return render_template('pay.html', resp_details=response, resp_data=data)
            else:
                flash('Transaction Failed!.', 'danger')
                return redirect(url_for('transactionz.transactions'))
        except Exception as e:
            print('Error:', str(e))

    

    return render_template('payment_request.html', title='Request New Payment',
                           form=form, legend='New Payment')


@payments.route("/callback", methods=["POST"])
def handle_callback():

    fileNo = session.get("fileId", None)
    print(fileNo)

    json_repsonse = request.get_json()
    result = json_repsonse["Result"]

    # --------------- Write to file ------------------------------------------------------------
    msg = json_repsonse

    with open("callbackfile.json", "a") as f:
        json.dump(msg, f)
    # ---------------------------------------------------------------------------
    
    status = result['ResultCode']
    if status == 0:
        mpesa_ref = result["TransactionID"]
        merchant_req_id = result['ConversationID']
        date_values = str(result['ResultParameters']['ResultParameter'][3]['Value'])

        date_val = date_values[0:4]+"-"+date_values[4:6]+"-"+date_values[6:8]+" "+date_values[8:10]+":"+date_values[10:12]+":"+date_values[12:14]
        trans_date = datetime.strptime(date_val, "%Y-%m-%d %H:%M:%S")

        amount = result['ResultParameters']['ResultParameter'][5]['Value']
        transaction_id = str(uuid.uuid4())
        user_id = uzer_id
        budget = budgetzId
        file = filezNo
        narration = descriptionZ

        trans = Transaction(transaction_id=transaction_id, mpesa_ref=mpesa_ref, merchant_req_id=merchant_req_id, trans_date=trans_date, status=status, amount=amount, user_id=user_id, budget=budget, file=file, narration=narration)
        db.session.add(trans)
        db.session.commit()
        
        return mpesa_ref
    else:
        msg = result['ResultDesc']

        with open("callbackfile.json", "a") as f:
            json.dump(msg, f)
        flash(msg, 'success')
        return redirect("/transactions")



# Confirm Payment
@payments.route("/pay/<string:merchant_req_id>/confirm_payment", methods=['POST'])
def confirm_payment(merchant_req_id):
    wait = 1
    count = 0

    while count < 5:
        time.sleep(wait)
        # payment = Transaction.query.get_or_404(merchant_req_id)
        payment = Transaction.query.filter_by(merchant_req_id=merchant_req_id).first()
        if payment:
            count = 5
            budget = session.get("budgetId", None)
            fileNo = session.get("fileId", None)
            description = session.get("descr", None)
            payment.user_id = current_user.id
            payment.budget = budget
            payment.file = fileNo
            payment.narration = description
            
            db.session.commit()
            if payment.status == '0':
                flash('Your payment with Mpesa ref:  '+payment.mpesa_ref+ '  was Successful', 'success')
                return redirect(url_for('transactionz.transactions'))
            else:
                flash('Your payment with REQUEST ID:  '+merchant_req_id+ '  was NOT Successful.', 'danger')
                return redirect(url_for('transactionz.transactions'))
        else:
            count+=1

    else:
        flash('Your payment with REQUEST ID:  '+merchant_req_id+ '  was NOT Successful.', 'danger')
        return redirect(url_for('transactionz.transactions'))



def generate_access_token():
    consumer_key = "XZSPT4CIhfvAhRPdfq6EIkP1zcfHOFGigSb3fjueD4AKFKQO"
    consumer_secret = "jr04RpkXcvJsJwUHA3MMdgxS7lxwNyMiHujPOTpdOaGGGCLOIhyszxIDnDFL23bZ"

    url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"

    try:

        encoded_credentials = base64.b64encode(f"{consumer_key}:{consumer_secret}".encode()).decode()


        headers = {
            "Authorization": f"Basic {encoded_credentials}",
            "Content-Type": "application/json"
        }

        # Send the request and parse the response
        response = requests.request("GET", url, headers=headers).json()

        # Check for errors and return the access token
        if "access_token" in response:
            return response["access_token"]
        else:
            raise Exception("Failed to get access token: " + response["error_description"])
    except Exception as e:
        raise Exception("Failed to get access token: " + str(e))
