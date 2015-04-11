from django.shortcuts import render

"""
Copy from https://github.com/fengli/alipay_python
"""

from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
import datetime
import logging
import urllib
import alipay 

from models import  *
from payment.alipay_python.config import *

logger1 =logging.getLogger(__name__)
logger1.setLevel(logging.INFO)
#logger1.addHandler (logging.FileHandler(LOGGING_PAYMENT))

def upgrade_bill(bill):
  """
  Upgrade bill BILL valide for VALIDE_DAYS from today. And update
  """
  start_date = datetime.datetime.now()
  expire_date=start_date+datetime.timedelta(days=1)
  bill.start_date=start_date
  bill.expire_date=expire_date
  bill.save()

@login_required
def pay(request, b_type, params, b_no=None ):
  """
  Request for upgrade account to acc_type. Redirect to alipay
  payment web page due to ACC_TYPE.
  """
  bill = None
  try: bill = Bill.objects.get(no=b_no,user=request.user) 
  except: 
      b_no = generate_order_num(params.pop('order_num'))
      bill = Bill.objects.create(no=b_no, user=request.user, bill_type=b_type)

  alipayTool=alipay.Alipay(  
            pid=settings.ALIPAY_PARTNER,  
            key=settings.ALIPAY_KEY,  
            seller_email=settings.ALIPAY_SELLER_EMAIL
            )
  params['out_trade_no'] = b_no
  url = alipayTool.create_direct_pay_by_user_url(**params)
  return url

