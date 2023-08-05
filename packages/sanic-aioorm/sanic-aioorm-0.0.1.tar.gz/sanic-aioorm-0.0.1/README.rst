
sanic-aioorm
===============================

version: 0.0.1

author: hsz

email: hsz1273327@gmail.com

Feature
----------------------
* simple to use, just like using flask

Example
-------------------------------

model.py

.. code:: python

from sanic_aioorm import AioOrm, AioModel
from peewee import Proxy, CharField
db = Proxy()


@AioOrm.regist
class User(AioModel):
    username = CharField()

    class Meta:
        database = db



app.py

.. code:: python

from sanic import Sanic
from sanic.response import json
from sanic_aioorm import AioOrm
from ex_model import User, db
app = Sanic()
AioOrm.SetConfig(app, defaultdb="mysql://root:hsz881224@localhost:3306/test")
orm = AioOrm(app)
orm.init_proxys(defaultdb=db)
orm.create_tables(User=[{'username': "hsz"}, {'username': "jojo"}])


@app.get("/")
async def testget(request):
    try:
        users = await User.select()
    except Exception as e:
        return json({"error": str(e)})
    else:
        return json({"hello": [await u.to_dict() for u in users]})


@app.post("/")
async def testpost(request):
    try:
        users = await User.create(request.json)
    except Exception as e:
        return json({"error": str(e)})
    else:
        return json({"hello": [u.to_dict() for u in users]})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=4500)

Install
--------------------------------

- ``python -m pip install sanic-aioorm``


Documentation
--------------------------------

`Documentation on Readthedocs <https://github.com/Sanic-Extensions/sanic-aioorm>`_.



TODO
-----------------------------------
* auth Decorator



Limitations
-----------
* only support mysql and pgsql
