from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from basket.basket import Basket
from .models import *
from store.models import Product
from django.contrib import messages
import random
from .forms import OrderForm
from store.models import Product
# imports for invoice

from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter

# # invoice
# def orders_pdf(request):
#     # bytestream buffer
#     buf = io. BytesIO()
#     # canva
#     c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
#     # textobject
#     textob = c.beginText()
#     textob.setTextOrigin(inch, inch)
#     textob.setFont("Helvetica",14)

#     orderitems = Order.objects.filter(user=request.user)
    
#     # blan list
#     lines = [
#         "Ecobag Suppliers ke",
#         "Invoice",
#         "---------------------------------------------------",

#     ]
    

#     for orderitem in orderitems:
#         lines.append("First Name: " + orderitem.fname)
#         lines.append("Last Name: " + orderitem.lname)
#         lines.append("Phone: " + str(orderitem.phone))
#         lines.append("Email: " + orderitem.email)
#         lines.append("Tracking no: " + orderitem.tracking_no)
#         lines.append("Amount Paid: " + orderitem.amount_paid)
#         lines.append("Status: " + orderitem.orderstatus)
#         lines.append("======================")

#     # blan list
#     lines = [
#         "Thank you for being part of us",
#         "---------------------------------------------------",

#     ]

#     # loop
#     for line in lines:
#         textob.textLine(line)

    
#     # finish
#     c.drawText(textob)
#     c.showPage()
#     c.save()
#     buf.seek(0)

#     return FileResponse(buf, as_attachment=True, filename='invoice.pdf')




#