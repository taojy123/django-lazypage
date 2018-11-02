# django-lazypage
django 页面异步加载解决方案

[![PyPI Downloads](https://pypistats.com/badge/django-lazypage.png)](https://pypistats.com/package/django-lazypage)


此项目旨在于解决由于后端处理时间较长导致载入页面上无响应地等待过久的问题。
参考示例 https://tools.athenagu.com/test_slow_page/?s=8


###简易使用方法:
```
# requirements.txt
django
...
django-lazypage  # <--- 添加依赖
```

```
# settings.py
INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'myapp',
    'lazypage',  # <--- 引入 app
)
```

```
# views.py
# -*- coding: utf-8 -*-

import time
from django.http import HttpResponse
from django.shortcuts import render_to_response
from lazypage.decorators import lazypage_decorator  # <--- 引入装饰器

def index(request):
    return render_to_response('index.html', locals())

@lazypage_decorator  # <--- 在原来的 view 上添加 lazypage_decorator 装饰器即可
def test_slow_page(request):
    s = int(request.GET.get('s', 18))
    print(s)
    time.sleep(s)
    page = """
    <html>
    <body>
        此页面将在请求后 %s 秒, 才会呈现!
    </body>
    </html>
    """ % s
    return HttpResponse(page)



```

```
# urls.py
from django.conf.urls import url, include
from views import *
import lazypage.urls  # <--- 引入 lazypage 路由

urlpatterns = [
    url(r'^$', index),
    url(r'^test_slow_page/$', test_slow_page),
    url(r'^lazypage/', lazypage.urls.get_urls()),  # <--- 添加 lazypage 的路由
]

```

```
# 最后需要跑一次 migrate 创建 LazyStore 表
$ python manage.py migrate
```

完成以上步骤后，访问 `/test_slow_page/` 就可以看到效果了


###进阶配置:
可在 `settings.py` 中添加 lazypage 配置项，调整参数符合自己的需求
```
LAZYPAGE = {
    'EXPIRED_SECONDS': 3600,  # 页面最长等待超时，默认 3600 秒，超过还没加载出来的页面，将报错。所以这里建议设置一个足够大的值
    'POLLING_SECONDS': 5,     # 等待加载页面的刷新间隔(秒)，间隔越短越能第一时间看到加载完成后的页面

    'ASYNC_BY_CELERY': False,  # 是否使用 celery 来做生成页面内容的异步任务，默认为否，即使用另开一个线程的方式来实现异步生成页面
    'CELERY_APP': None,  # ASYNC_BY_CELERY 为 True 时生效，这里需要是一个 Celery 实例，或是一个引入实例的路径(如:"myproj.celery.app")
    # 关于 celery 以及在 django 中应用的相关内容可以查看官方文档:
    # http://docs.celeryproject.org/
    # http://docs.celeryproject.org/en/latest/django/first-steps-with-django.html

    'STORE_BY_REDIS': False,   # 是否使用 redis 来存储异步加载出来的页面内容，默认为否，即使用数据库存储
    'REDIS_HOST': '127.0.0.1', # STORE_BY_REDIS 为 True 是生效，redis 的 host 地址
    'REDIS_PORT': '6379',	   # 同上，redis 的端口号
    'REDIS_PASSWORD': '',      # 同上，redis 的连接密码
    'REDIS_DB': '2',           # 同上，redis 使用的库序号
    # 当使用 redis 储存页面内容时，就不必执行 migrate 创建 LazyStore 了
}
```



