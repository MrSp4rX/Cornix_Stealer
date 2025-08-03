from __future__ import print_function
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException

def send_otp(email, otp):
    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key['api-key'] = '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'
    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))
    subject = "Cornix OTP Verification"
    html_content = f"""<div style="font-family: Helvetica,Arial,sans-serif;min-width:1000px;overflow:auto;line-height:2">
      <div style="margin:50px auto;width:70%;padding:20px 0">
        <div style="border-bottom:1px solid #eee">
          <a href="" style="font-size:1.4em;color: #00466a;text-decoration:none;font-weight:600">Cornix OTP Verification</a>
        </div>
        <p style="font-size:1.1em">Hi,</p>
        <p>Thank you for choosing Cornix Auto Trading Bot. Use the following OTP to complete your Sign Up procedures. OTP is valid for 5 minutes</p>
        <h2 style="background: #00466a;margin: 0 auto;width: max-content;padding: 0 10px;color: #fff;border-radius: 4px;">{otp}</h2>
        <p style="font-size:0.9em;">Regards,<br />Cornix Team</p>
        <hr style="border:none;border-top:1px solid #eee" />
        <div style="float:right;padding:8px 0;color:#aaa;font-size:0.8em;line-height:1;font-weight:300">
          <p>Cornix Inc</p>
        </div>
      </div>
    </div>"""
    sender = {"name":"Cornix Verification","email":"no-reply@cornix.buzz"}
    to = [{"email":email,"name":"Cornix User"}]
    reply_to = {"email":"no-reply@cornix.buzz","name":"Cornix"}
    params = {"parameter":"My param value","subject":"Cornix OTP Verification Code"}
    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(to=to, reply_to=reply_to, html_content=html_content, sender=sender, subject=subject)

    try:
        api_response = api_instance.send_transac_email(send_smtp_email)
        return True
    except ApiException as e:
        return False
