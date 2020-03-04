from django.shortcuts import render
# 类视图
from django.http import HttpResponse,FileResponse,JsonResponse
from django.views import View
# Create your views here.
import json
import re
from myfirstapp.models import User
from django.core.paginator import Paginator
from django.conf import settings
import os
import requests
from mixinde.responseutil import UtilMixin,APPID,SECRET_KEY
from myfirstapp.models import Article
# class Myonly(View):
#     def get(self):
#         return HttpResponse('这是我的第一个应用')

def article(request):

    # 获取page参数
    page=request.GET.get('page')
    if page:
        page=int(page)
    else:
        page=1
    all_article = Article.objects.all()

    pag = Paginator(all_article, 1)
    page_article_list=pag.page(pag.num_pages)
    page_num=pag.num_pages
    if page_article_list.has_next():
        next_page=page+1
    else:
        next_page=page
    if page_article_list.has_previous():
        previous=page-1
    else:
        previous=page
    return  render(request,'index.html',
                   {
                       'article_list':page_article_list,
                       'pag_num':range(1,page_num+1),
                       'curr_page':page,
                       'next_page':next_page,
                       'previous':previous
                   }
                   )
def get_detail_page(request,article_id):
    all_article=Article.objects.all()
    curr_article=None
    previous_index=0
    next_index=0
    previous_article=None
    next_article=None
    for index,article in enumerate(all_article):
        if index==0:
            previous_index=0
            next_index=index+1
        elif index==len(all_article)-1:
            previous_index=index-1
            next_index=index
        else:
            previous_index=index-1
            next_index=index+1
        if article.article_id==article_id:
            curr_article=article
            previous_article=all_article[previous_index]
            next_article=all_article[next_index]
            break
    section_list=curr_article.content.split('\n')
    return render(request, 'detail.html',
                  {
                      'curr_article': curr_article,
                      'section_list':section_list,
                      'previous_article':previous_article,
                      'next_article':next_article
                  }
                  )
def image(request):
    with open(r'D:\wxaaa\pages\images\grid.png','rb') as e:
        return HttpResponse(content=e.read(),content_type='image/png')
        # return FileResponse(e,content_type='image/png') 下面这个要用open的方法

def apps(request):
    return JsonResponse([{'name':'测QQ号吉凶'},{'name':'支付宝'},{'name':'笑话'}],safe=False)

class ImageView(View,UtilMixin):

    def get(self, request):
        filepath = os.path.join(settings.STATIC_ROOT_SELF, 'abc.jpg')
        f = open(filepath, 'rb')
        # with open(filepath, 'rb') as f:
        # return HttpResponse(content=f.read(),content_type='image/png')
        return FileResponse(f, content_type='image/jpg')
        # return render(request,'upfile.html')

    def post(self, request):
        files1 = request.FILES
        # class 'django.utils.datastructures.MultiValueDict'
        # print(type(files))
        picdir = settings.UPLOAD_PIC_DIR

        for key,value in files1.items():
            filename = os.path.join(picdir,key[-8:])
            UtilMixin.savepic(filename,value.read())

        # return HttpResponse(filename)
        return JsonResponse(UtilMixin.wrapdic({'filename':key[-8:]}))

    def delete(self,request):
        picdir = settings.UPLOAD_PIC_DIR
        picname=request.GET.get('name')
        # 图片的全路径
        pic_full_path=os.path.join(picdir,picname)
        print(pic_full_path)
        # 如果这个路径不存在这张图片
        if not os.path.exists(pic_full_path):
            return HttpResponse('图片不存在')
        else:
            os.remove(pic_full_path)
            return HttpResponse('删除成功')


class Cookietest(View):
    # 发送cookie值给小程序
    def get(self,request):
        # print(dir(request))
        request.session['mykey']='我的值'
        return JsonResponse({'key':"value"})

class Cookietest1(View):
    # 接收小程序发来的cookie值
    def get(self,request):
        # print(dir(request))
        print(request.session['mykey'])
        print(request.session.items())
        return JsonResponse({'key2':"value2"})


class Authorize(View):
    def get(self,request):
        return self.post(request)
    def post(self,request):
        # 获取小程序端发来的code b'{"code":"001DMoLu1qdg3i0hv1Mu1wQwLu1DMoLr"}'
        # print(request.body)
        bodystr=request.body.decode('utf-8')
        bodydict=json.loads(bodystr)
        print(bodydict)
        code=bodydict.get('code')
        nickname=bodydict.get('nickname')
        # print(code,nickname)
        # 发起请求
        url='https://api.weixin.qq.com/sns/jscode2session?appid={}&secret={}&js_code={}&grant_type=authorization_code'.format(APPID,SECRET_KEY,code)
        res=requests.get(url)
        print(res.text)
        res_dict=json.loads(res.text)
        openid=res_dict.get('openid')
        if not openid:
            return HttpResponse('认证错误')
        # 给这个用户赋予了一些状态
        request.session['openid']=openid
        request.session['is_authorized']=True
        # 将用户保存到本地数据库
        if not User.objects.filter(openid=openid):
            new_user=User(openid=openid,nickname=nickname)
            new_user.save()
        return  HttpResponse('ok了')

# '.........................................................'
def c2s(appid, code):
    return code2session(appid, code)


def code2session(appid, code):
    API = 'https://api.weixin.qq.com/sns/jscode2session'
    params = 'appid=%s&secret=%s&js_code=%s&grant_type=authorization_code' % \
             (APPID,SECRET_KEY, code)
    url = API + '?' + params
    response = requests.get(url=url, )
    data = json.loads(response.text)
    print(data)
    return data


def __authorize_by_code(request):
    '''
    使用wx.login的到的临时code到微信提供的code2session接口授权

    post_data = {
        'encryptedData': 'xxxx',
        'appId': 'xxx',
        'sessionKey': 'xxx',
        'iv': 'xxx'
    }
    '''
    response = {}
    post_data = request.body.decode('utf-8')
    post_data = json.loads(post_data)
    app_id = post_data.get('appId').strip()
    nickname = post_data.get('nickname').strip()
    code = post_data.get('code').strip()
    print(code)
    print(app_id)
    if not (app_id and code):
        response['result_code'] = 2500
        response['message'] = 'authorized failed. need entire authorization data.'
        return JsonResponse(response, safe=False)
    try:
        data = c2s(app_id, code)
    except Exception as e:
        print(e)
        response['result_code'] = 2500
        response['message'] = 'authorized failed.'
        return JsonResponse(response, safe=False)
    openid = data.get('openid')
    if not openid:
        response['result_code'] = 2500
        response['message'] = 'authorization error.'
        return JsonResponse(response, safe=False)
    request.session['openid'] = openid
    request.session['is_authorized'] = True

    print(openid)
    # User.objects.get(openid=openid) # 不要用get，用get查询如果结果数量 !=1 就会抛异常
    # 如果用户不存在，则新建用户
    if not User.objects.filter(openid=openid):
        new_user = User(openid=openid, nickname=nickname)
        new_user.save()

    # message = 'user authorize successfully.'
    # response = wrap_json_response(data={}, code=ReturnCode.SUCCESS, message=message)
    return JsonResponse(response, safe=False)


def authorize(request):
    return __authorize_by_code(request)


# 判断是否已经授权
def already_authorized(request):
    is_authorized = False
    if request.session.get('is_authorized'):
        is_authorized = True
    return is_authorized


def get_user(request):
    if not already_authorized(request):
        raise Exception('not authorized request')
    openid = request.session.get('openid')
    user = User.objects.get(openid=openid)
    return user



#https://api.weixin.qq.com/sns/jscode2session?appid=APPID&secret=SECRET&js_code=JSCODE&grant_type=authorization_code
# 小程序登录接口
class UserView(View):
    # 关注的城市、股票和星座
    def get(self, request):
        if not already_authorized(request):
            return JsonResponse(data={'key':'没认证'}, safe=False)
        openid = request.session.get('openid')
        print(openid,'...............................mmmmmmmmmmmmmmmm')
        user = User.objects.get(openid=openid)
        data = {}
        data['focus'] = {}
        a=str(user.focus_cities)
        b=str(user.focus_stocks)
        c=str(user.focus_constellations)
        data['focus']['city'] = json.loads(re.sub('\'','\"',a))
        data['focus']['stock'] = json.loads(re.sub('\'','\"',b))
        data['focus']['constellation'] = json.loads(re.sub('\'','\"',c))
        return JsonResponse(data=data, safe=False)
        pass

    def post(self, request):
        if not already_authorized(request):
            return JsonResponse(data={'key':'没认证'}, safe=False)
        openid = request.session.get('openid')
        user = User.objects.get(openid=openid)
        received_body = request.body.decode('utf-8')
        received_body = json.loads(received_body)
        print(received_body)
        cities = received_body.get('city')
        stocks = received_body.get('stock')
        constellations = received_body.get('constellation')
        # 追加的形式,而不是覆盖形式
        user.focus_cities =cities
        user.focus_stocks = stocks
        user.focus_constellations =constellations
        user.save()
        return JsonResponse(data={'msg':'成功'}, safe=False)
        pass

class Loginout(View):
    def get(self,request):
        request.session.clear()
        return JsonResponse(data={'key':'logout'},safe=False)

class Status(View):
    # 判断是否登录
    def get(self,request):
        print('call get status')
        if already_authorized(request):
            data={"is_authorized":1}
        else:
            data = {"is_authorized": 0}
        print(data)
        return JsonResponse(data,safe=False)


def weather(cityname):
    '''
    :param cityname: 城市名字
    :return: 返回实况天气
    '''
    key = 'ec66a80ef89ff89c4b0ffcbb6a64f5cc'
    api = 'http://apis.juhe.cn/simpleWeather/query'
    params = 'city=%s&key=%s' % ('柳州', key)
    url = api + '?' + params
    print(url)
    response = requests.get(url=url)
    data = json.loads(response.text)
    print(data)
    result = data.get('result')
    realtime = result.get('realtime')
    response = {}
    response['temperature'] = realtime.get('temperature')
    response['wid'] = realtime.get('wid')
    response['power'] = realtime.get('power')
    # response = {}
    # response['temperature'] = 'temperature'
    # response['win'] = 'win'
    # response['humidity'] = 'humidity'
    return response


class Weather(View):
    def get(self, request):
        if not already_authorized(request):
            response = {'key':2500}
        else:
            data = []
            openid = request.session.get('openid')
            user = User.objects.filter(openid=openid)[0]
            # '''''''''''''''''''''''''''''''''''''''''''''''''re.sub('\'','\"',a)
            city=str(user.focus_cities)
            cities = json.loads(re.sub('\'','\"',city))
            for city in cities:
                result = weather(city.get('city'))
                result['city_info'] = city
                data.append(result)
            response = data
        return JsonResponse(data=response, safe=False)
        pass

    def post(self, request):
        data = []
        received_body = request.body.decode('utf-8')
        received_body = json.loads(received_body)
        print(received_body)
        cities = received_body.get('cities')
        for city in cities:
            result = weather(city.get('city'))
            result['city_info'] = city
            data.append(result)
        response_data = {'key':'post..'}
        return JsonResponse(data=response_data, safe=False)
