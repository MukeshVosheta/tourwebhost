from email.message import EmailMessage
import ssl
import smtplib

e_pass="rmlercdaahzndkpi"
e_send="sunkon.com@gmail.com"

#________________________Booking mail____________________________
def booking_mail(reciver_mail,bill,pack_start,pack_end,members,package,price):
    
    e_reci=reciver_mail

    sub="Tour Booking"
    body=f''' From Tour For You 

        Your tour package {package} successfully booked
        tour date : {pack_start} to {pack_end}
        with {members} member,
        per person price : {price} Rs
        Total bill: {bill} Rs
    '''

    es=EmailMessage()

    es['FROM']=e_send
    es['TO']=e_reci
    es['SUBJECT']=sub

    es.set_content(body)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465,context=context) as smtp:
        smtp.login(e_send,e_pass)
        smtp.sendmail(e_send,e_reci,es.as_string())

    return True


#________________________cancel tour mail____________________________
def Cancel_mail(reciver_mail,bill,pack_start,pack_end,members,package,price):
    e_reci=reciver_mail

    sub="Tour Cancel Booking"
    body=f''' From Tour For You 

        Your tour package {package} Cancelled
        tour date : {pack_start} to {pack_end}
        with {members} member,
        per person price : {price} Rs
        Total bill: {bill} Rs


    '''

    es=EmailMessage()

    es['FROM']=e_send
    es['TO']=e_reci
    es['SUBJECT']=sub

    es.set_content(body)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465,context=context) as smtp:
        smtp.login(e_send,e_pass)
        smtp.sendmail(e_send,e_reci,es.as_string())

    return True