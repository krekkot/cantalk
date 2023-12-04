import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText



addr_from = "ihormorozov91@gmail.com"
addr_to = "sales@transaviagroup.com"
password = "cjau zdom jlts uhif"
img_data = open("pho.png", 'rb').read()
msg = MIMEMultipart()
msg['From'] = addr_from
msg['To'] = addr_to
msg['Subject'] = "Тема"
text1 = ("Дякуємо Вам за замовлення!\nНайближчим часом Вам надішлють деталі що додступу до курсу\n\n")
msg.attach(MIMEText(text1, 'plain'))
# attach photo
try:
    image = MIMEImage(img_data)
    image.add_header('Content-Disposition', 'attachment', filename="image.jpg")
    msg.attach(image)
except Exception as e:
    print(e)

smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
smtpObj.starttls()
smtpObj.login(addr_from, password)
smtpObj.send_message(msg)
smtpObj.quit()
print("Mailed")
