import falcon
import uuid

from .utils import (
        find,
        getData,
        writeData,
        )


class MockAPI:
    def on_get(self, req, res, id = None):

        data = []

        try: 
            data = getData()
            if id is not None and id != '':
                print (id)
                data = find(data, 'id', id)
        except ex as Exception:
            print(ex)
            data = []
        finally:
            res.media = data
    
    def on_post(self, req, res):

        try:
            db = getData()
            data = req.media
            data['id'] = str(uuid.uuid4())
            db.append(data)
            writeData(db)
            res.media = data
        except ex as Exception:
            print(ex)
            res.media = { 'error': 'Faild to save data'}
            res.status = falcon.HTTP_400


api = falcon.API()
api.add_route('/v1/user', MockAPI());
api.add_route('/v1/user/{id}', MockAPI());
