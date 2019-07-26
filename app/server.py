import falcon
import uuid
from falcon_cors import CORS
from math import ceil

from .utils import (
        find,
        findIndex,
        getData,
        writeData,
        )


class MockAPI:
    def on_get(self, req, res, id = None):
        data = []
        page = 0
        row = 0
        total = 0

        try: 
            data = getData()
            total = len(data)
            
            if id is not None and id != '':
                print (id)
                data = find(data, 'id', id)

            row = int(req.params.get('row', len(data)))
            page = int(req.params.get('page', 1)) - 1
            totalPages = ceil(len(data) / row)
            data = data[(row * page):(row * page) + row]
        except Exception as ex:
            print(ex)
            data = []
        finally:
            res.media = {
                    'data': data,
                    'page': page + 1,
                    'row': row,
                    'total_row': total
                    }
    
    def on_post(self, req, res, *arg, **kws):
        try:
            db = getData()
            data = req.media
            data['id'] = str(uuid.uuid4())
            db.append(data)
            writeData(db)
            res.media = { 'data': data }
        except Exception as ex:
            print(ex)
            res.media = { 'error': 'Faild to save data'}
            res.status = falcon.HTTP_400

    def on_put(self, req, res, id = None):
        try:
            db = getData()
            data = req.media
            del data['id']
            index = findIndex(db, 'id', id)
            
            if index < 0:
                raise Exception()

            for key in data.keys():
                db[index][key] = data.get(key, None)

            writeData(db)
            res.media = { 'data': db[index] }
        except Exception as ex:
            print(ex)
            res.media = { 'error': 'Faild to save data'}
            res.status = falcon.HTTP_400

    def on_delete(self, req, res, id = None):
        try:
            db = getData()
            index = findIndex(id)
            
            if index < 0:
                raise Exception()

            db.remove(index)
            res.media = { 'data': id }
        except Exception as ex:
            print(ex)
            res.media = { 'error': 'Faild to save data'}
            res.status = falcon.HTTP_400


API_PREFIX = '/api/v1'
cors = CORS(allow_all_origins=True)
api = falcon.API(middleware=[cors.middleware])
api.add_route(API_PREFIX + '/user', MockAPI());
api.add_route(API_PREFIX + '/user/{id}', MockAPI());

