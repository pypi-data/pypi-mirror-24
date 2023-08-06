sanic-mongo
===========

sanic的mongodb异步工具,灵感来源自[官方例子](https://github.com/channelcat/sanic/blob/master/examples/sanic_motor.py).是[motor](https://motor.readthedocs.io/en/stable/tutorial-asyncio.html)的封装,目的只是为了简化操作.

特点 Features
-------------

-   [motor](https://motor.readthedocs.io/en/stable/tutorial-asyncio.html)
    支持的操作都支持
-   支持3.5版本以上的

依赖 Requirements
-----------------

1.  motor&gt;=1.1
2.  pymongo&gt;=3.4.0
3.  sanic&gt;=0.4.1

安装 Installation
-----------------

    pip install sanic-mongo

文档 Document
-------------

[sanic-mongo](https://sanic-extensions.github.io/sanic-mongo/)

例子 Example
------------

``` {.python}
from sanic import Sanic
from sanic.response import json
from sanic_mongo import Mongo

app = Sanic(__name__)
mongo_uri = "mongodb://{host}:{port}/{database}".format(
    database='test',
    port=27017,
    host='localhost'
)

mongo = Mongo(mongo_uri)
db = mongo(app)
@app.get('/objects')
async def get(request):
    docs = await db().test_col.find().to_list(length=100)
    for doc in docs:
        doc['id'] = str(doc['_id'])
        del doc['_id']
    return json(docs)


@app.post('/objects')
async def new(request):
    doc = request.json
    object_id = await db("test_col").save(doc)
    return json({'object_id': str(object_id)})


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8000)
```
