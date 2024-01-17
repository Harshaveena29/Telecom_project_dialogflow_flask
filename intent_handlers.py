from db import db
import generic_helper as gh
from models import MobileNumbers

inprogress_transaction = {}

def handle_intent(req):
    output_contexts = req['queryResult']['outputContexts']
    parameters = output_contexts[0]["parameters"] if "parameters" in output_contexts[0] else None
    session_id = gh.extract_session_id(output_contexts[0]["name"])
    intent = str(req['queryResult']['intent']['displayName']).strip()

    intent_handler_dict = {
        'PlanChange.MobileNumber context:ongoing-planchange': planchange_mobile_extraction,
        'PlanChange.MobileNumber context:ongoing-planchange - yes': planchange_yes,
        'PlanChange.MobileNumber context:ongoing-planchange - no': planchange_no,
        'plan.add - context:ongoing-planchange': planname_add,
        'Plan.Details': plandetails,
        'PlanDetails.MobileNumber context:ongoing-plandetails-extraction' : plandetails_extraction,
        'Complete_transaction': complete_transaction 
    }

    return intent_handler_dict[intent](parameters, session_id)

def planchange_no(parameters, session_id):
    return {'fulfillmentText': 'Sure Thanks for reaching out, Cancelled your Plan update transaction!Anything else?'}

def planchange_yes(parameters, session_id):
    print(inprogress_transaction)
    plan_id = inprogress_transaction[session_id]["plan"]
    mobile_number = inprogress_transaction[session_id]["selected_mobile"]
    MobileNumbers.query.filter_by(MobileNumber=mobile_number).update({"PlanID": plan_id})
    db.session.commit()
    return {'fulfillmentText': f'Successfully updated your plan {plan_id} for mobile number {mobile_number}. The corresponding changes will be reflected in your upcoming bill.Anything else?'}

def complete_transaction(parameters,session_id):
    del inprogress_transaction[session_id]
    return {'fulfillmentText': f'Okay,Have a good day!'}


def planname_add(parameters, session_id):
    cust_id = gh.generate_customer_id()

    if parameters["Plan_entity"]:
        inprogress_transaction[session_id] = {"plan": parameters["Plan_entity"], "cust_id": cust_id, "active_mobiles": [],"active_plans":[]}
        return(active_mobile_number_extraction(inprogress_transaction,session_id))
    else:
        return {'fulfillmentText': f"I'm having trouble finding your Plan Change Transaction. Sorry! Can you place a new plan change request, please?"}

def plandetails(parameters,session_id):   
    if session_id not in inprogress_transaction:
        inprogress_transaction[session_id] = {}
        cust_id = gh.generate_customer_id()
        inprogress_transaction[session_id]["cust_id"] = cust_id
    inprogress_transaction[session_id]["active_mobiles"]=[]
    inprogress_transaction[session_id]["active_plans"]=[]
    return(active_mobile_number_extraction(inprogress_transaction,session_id))
        
def plandetails_extraction(parameters,session_id):
    user_selected_mobile = parameters["phone-number"]
    active_mobiles = inprogress_transaction[session_id]["active_mobiles"]
    if user_selected_mobile not in active_mobiles:
            active_mobiles = str(active_mobiles)
            fulfillment_text = f"Please select a Mobile Number only from the displayed active list ----> {active_mobiles}"
            return {'fulfillment_text': fulfillment_text}
    else:
            
            data = gh.generate_plan_details_data(user_selected_mobile) 
            del inprogress_transaction[session_id]
            return(gh.generate_html(data,"yourplan.html"))

def active_mobile_number_extraction(inprogress_transaction,session_id):
    cust_id = inprogress_transaction[session_id]['cust_id']
    active_mobile_numbers = MobileNumbers.query.filter_by(CustomerID=cust_id,
                                                           IsActive=True).all()
    output_string = []
    for mobile in active_mobile_numbers:
        inprogress_transaction[session_id]["active_mobiles"].append(mobile.MobileNumber)
        inprogress_transaction[session_id]["active_plans"].append(mobile.PlanID)
        output_string.append(f"MobileNumber: {mobile.MobileNumber}, Active_Plan: {mobile.PlanID}")

    return {'fulfillmentText': f"Please select a Mobile Number from the list of active numbers associated with your account #{cust_id}---->{output_string}"}

def planchange_mobile_extraction(parameters, session_id):
    print(inprogress_transaction)
    user_selected_mobile = parameters["phone-number"]
    active_mobiles = inprogress_transaction[session_id]["active_mobiles"]
    plan = inprogress_transaction[session_id]["plan"]

    if session_id not in inprogress_transaction:
        fulfillment_text = "I'm having trouble finding your Plan Change Transaction. Sorry! Can you place a new plan change request, please?"
    else:
        if user_selected_mobile not in active_mobiles:
            active_mobiles = str(active_mobiles)
            fulfillment_text = f"Please select a Mobile Number only from the displayed active list ----> {active_mobiles}"
        else:
            inprogress_transaction[session_id]["selected_mobile"] = user_selected_mobile
            fulfillment_text = f"Thanks for providing Plan and Mobile Details, Do you wish to proceed with this plan update Plan: {plan} on {user_selected_mobile} ?"

    return {'fulfillment_text': fulfillment_text}
