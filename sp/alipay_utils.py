# -*- coding:utf-8 -*-
import alipay

def generate_order_num(_id):
    """
    Generate order number
    Format:year(4)month(2)day(2)hour(2)minute(2)coachtrainid
    """
    now = datetime.datetime.now()
    return "{0:0>4d}{1:0>2d}{2:0>2d}{3:0>2d}{4:0>2d}{5}".format(now.year, now.month, now.day, now.hour, now.minute, _id)

def alipay_payment(_id, params):
    alipayTool=alipay.alipay(  
            partner="支付宝身份ID",  
            key="支付宝生成的key",  
            sellermail="商家支付宝帐号（邮箱）",  
            notifyurl="异步回调的URL",  
            returnurl="跳转回的URL",  
            showurl="显示网站商品的URL"  
            )
    #支付信息，订单号必须唯一。  
    #以下包含的内容替换为实际的内容。  
    params['out_trade_no'] = generate_order_num(_id)
    payhtml=alipayTool.createPayForm(params)  
    #将payhtml写到页面，这是个包含有提交按钮的表单 
    # f 为包含POST过来的数据python字典，即名-值对。  
    # verify 是否回调支付宝确认数据是否真实有效  
    # rlt为处理的结果，为success或fail  

    rlt=alipayTool.notifiyCall(f,verify=True)  

    #依据支付宝的要求，此URL返回的值为success或fail  
    #因此，当rlt为success时（即支付成功），做相应的处理  
    #然后，直接将rlt写到输出流。  
    return rlt

    #if rlt=='success':  
    #    paySuccess(f['out_trade_no'])  

    #return rlt 
    #注意，与异步回处理相同，在跳转回调的处理上，仍是调用notifiyCall函数  
    #并且参数与返回完全一样。  

    #rlt=alipayTool.notifiyCall(f,verify=True)  

    ##只是验证后的处理不同，这里需要给用户显示一个页面。  
    #if rlt=='success':  
    #    paySuccess(f['out_trade_no'])  
    ##显示支付成功的页面  
    #else:  
    ##显示未能成功支付的页面  
    #    pass

