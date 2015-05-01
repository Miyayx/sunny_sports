# -*- coding:utf-8 -*-
from django.shortcuts import render

"""
Copy from https://github.com/fengli/alipay_python
"""

from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.template import RequestContext
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
  b_no = generate_order_num(params['order_num'])
  print params['body']
  bill = Bill.objects.create(no=b_no, user=request.user, bill_type=b_type, total_fee=params['total_fee'], body=params['comment'].encode('unicode_escape'))
  ratio = 1 - settings.ALIPAY_RATIO
  our_ratio = 0.05
  org_ratio = 1-our_ratio

  alipayTool=alipay.Alipay(  
            pid=settings.ALIPAY_PARTNER,  
            key=settings.ALIPAY_KEY,  
            seller_email=settings.ALIPAY_SELLER_EMAIL
            )
  params['out_trade_no'] = b_no
  params['paymethod'] = 'directPay'
  if 'bank' in params:
      params['defaultbank'] = params['bank']
  #params['need_ctu_check'] = 'Y'
  params['enable_paymethod'] = 'directPay^bankPay'
  params['royalty_type'] = "10"
  params['royalty_parameters'] = '%s^%0.2f^%s'%(params['org_email'], params['total_fee']*org_ratio, params['comment'])
  print params['royalty_parameters']
  url = alipayTool.create_direct_pay_by_user_url(**params)
  print url
  return url, bill

#('bankname','bank_no_alipay','bank_imageclass')
BANKS = [
        #(u'中国工商银行','ICBC','ICBC'), #工商银行的混合渠道总是超时
        (u'中国建设银行','CCB','CCB'),
        (u'中国农业银行','ABC','ABC'),
        (u'中国邮政储蓄银行','POSTGC','PSBC'),
        #(u'交通银行','COMM-DEBIT','COMM'), #出错啦！
        (u'招商银行','CMB','CMB'),
        (u'中国银行','BOCB2C','BOC'),
        ##(u'中国光大银行','CEB-DEBIT','CEB'),
        (u'中信银行','CITIC-DEBIT','CITIC'), #中信关闭了信用卡网银支付
        (u'浦发银行','SPDB','SPDB'),
        (u'中国民生银行','CMBC','CMBC'),
        (u'广发银行','GDB','GDB'),
        ]

        
@login_required
def pay_method(request, params):
    return render_to_response('pay_method.html',{"bill":params, "banks":BANKS}, RequestContext(request))

