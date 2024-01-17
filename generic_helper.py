import re
import random
from db import db
from models import MobileNumbers, MobilePlans,MobileUsage
from flask import render_template
import os

output_file_path = r'C:/Users/veena/Downloads/plandetails/'

def extract_session_id(session_str: str):
    match = re.search(r"/sessions/(.*?)/contexts/", session_str)
    if match:
        extracted_string = match.group(0)
        return extracted_string

    return ""

def generate_customer_id():
    id = random.randint(1,5)
    return(id)

def generate_plan_details_data(mobile_number):
    selected_mobile_number_id = MobileNumbers.query.filter_by(MobileNumber=mobile_number).first().MobileNumberID
    
    result = db.session.query(
        MobilePlans.PlanID,
        MobilePlans.PlanName,
        MobilePlans.MonthlyAllowanceData,
        MobilePlans.MonthlyAllowanceTalkTime,
        MobilePlans.MonthlyAllowanceTextMessages,
        MobileUsage.DataUsage,
        MobileUsage.CallsUsage,
        MobileUsage.TextUsage,
        MobileUsage.InternationalRoaming
                            ).join(MobileNumbers, MobilePlans.PlanID == MobileNumbers.PlanID).outerjoin(MobileUsage, MobileNumbers.MobileNumberID == MobileUsage.MobileNumberID) \
        .filter(MobileNumbers.MobileNumberID == selected_mobile_number_id).first()

    
    plan_id,plan_name,monthly_allowance_data, monthly_allowance_talk_time, monthly_allowance_text_messages, data_usage, calls_usage,text_usage, international_roaming = result

   
    data = {
        'plan_id': plan_id,
        'plan_name': plan_name,
        'mobile_number': mobile_number,
        'MonthlyAllowanceData':monthly_allowance_data,
        'MonthlyAllowanceTalkTime':monthly_allowance_talk_time,
        'MonthlyAllowanceTextMessages':monthly_allowance_text_messages,
        'data_usage':data_usage,
        'calls_usage':calls_usage,
        'text_usage':text_usage,
        'international_roaming':international_roaming
                            }
    return(data)

def generate_html(data,html_page):

    html_content = render_template('plandetails.html', data=data)
    
    with open(os.path.join(output_file_path,html_page), 'w', encoding='utf-8') as file:
        file.write(html_content)

    
    return {'fulfillmentText': f'You can view the details in here ---> {html_page}.'}
   


