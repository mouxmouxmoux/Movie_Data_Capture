from peewee import *
from datetime import datetime

db = SqliteDatabase('./JavInfoDb.db')

class UnknownField(object):
    def __init__(self, *_, **__): pass

class BaseModel(Model):
    class Meta:
        database = db

class JavInfo(BaseModel):
    actor = TextField(column_name='ACTOR', null=True)
    actor_photo = TextField(column_name='ACTOR_PHOTO', null=True)
    adddate = TextField(column_name='ADDDATE', null=True)
    cover = TextField(column_name='COVER', null=True)
    cover_small = TextField(column_name='COVER_SMALL', null=True)
    director = TextField(column_name='DIRECTOR', null=True)
    extrafanart = TextField(column_name='EXTRAFANART', null=True)
    id = AutoField(column_name='ID', null=True)
    imagecut = IntegerField(column_name='IMAGECUT', null=True)
    label = TextField(column_name='LABEL', null=True)
    number = TextField(column_name='NUMBER')
    outline = TextField(column_name='OUTLINE', null=True)
    release = TextField(column_name='RELEASE', null=True)
    runtime = TextField(column_name='RUNTIME', null=True)
    series = TextField(column_name='SERIES', null=True)
    source = TextField(column_name='SOURCE', null=True)
    status = IntegerField(column_name='STATUS', null=True)
    studio = TextField(column_name='STUDIO', null=True)
    tag = TextField(column_name='TAG', null=True)
    title = TextField(column_name='TITLE', null=True)
    trailer = TextField(column_name='TRAILER', null=True)
    uncensored = TextField(column_name='UNCENSORED', null=True)
    userrating = FloatField(column_name='USERRATING', null=True)
    uservotes = TextField(column_name='USERVOTES', null=True)
    website = TextField(column_name='WEBSITE', null=True)
    year = TextField(column_name='YEAR', null=True)

    class Meta:
        table_name = 'JavInfo'

    def addto_localDB(self, json_data):
        # 增加写入数据库操作，用于后续整理减少爬取过程 by mouxwu
        number = json_data['number']
        try:
            db.connect()
            # db.create_tables([JavInfo])
            try:
                if JavInfo.get(number=number, status=1):
                    return  # 成功则说明存在此条数据，无需再写入
            except:
                pass

            # 出错说明不存在此条数据，需写入
            javinfo = JavInfo()
            javinfo.actor = ','.join(json_data['actor_list'])
            actor_photos = []
            try:
                for actor_name in json_data['actor_photo']:
                    try:
                        actor_photos.append(actor_name + ',' + json_data['actor_photo'].get(str(actor_name)))
                    except:
                        pass
            except:
                pass
            javinfo.actor_photo = ';'.join(actor_photos)
            javinfo.cover = json_data['cover']
            javinfo.cover_small = json_data['cover']
            javinfo.director = json_data['director']
            javinfo.extrafanart = ','.join(json_data['extrafanart'])
            javinfo.imagecut = json_data['imagecut']
            javinfo.label = json_data['label']
            javinfo.number = json_data['number']
            javinfo.outline = json_data['outline']
            javinfo.release = json_data['release']
            javinfo.runtime = json_data['runtime']
            javinfo.series = json_data['series']
            javinfo.source = json_data['source']
            javinfo.studio = json_data['studio']
            javinfo.tag = ','.join(json_data['tag'])
            javinfo.title = json_data['title']
            javinfo.trailer = json_data['trailer']
            javinfo.uncensored = int(json_data['uncensored'])
            try:
                javinfo.userrating = float(json_data['userrating'])
            except:
                javinfo.userrating = 0.0
            try:
                javinfo.uservotes = int(json_data['uservotes'])
            except:
                javinfo.uservotes = 0
            javinfo.website = json_data['website']
            javinfo.year = json_data['year']
            javinfo.adddate = datetime.now().strftime("%Y-%m-%d %H:%M")
            javinfo.status = 1
            javinfo.save()
            db.close()
        except:
            db.close()

    def search(self, number):
        try:
            db.connect()
            javinfo = JavInfo.get(number=number)
            if javinfo.status == 1:
                # 存在，直接读取
                try:
                    actor_photo = javinfo.actor_photo
                    actor_photo_dict = {}
                    try:
                        actor_pairs = actor_photo.split(';')
                        for actor_pair in actor_pairs:
                            actor_name, actor_photo_url =  actor_pair.split(',',1)
                            actor_photo_dict[actor_name] =  actor_photo_url
                    except:
                        pass
                    dic = {
                        'number': javinfo.number,
                        'title': javinfo.title,
                        'studio': javinfo.studio,
                        'release': javinfo.release,
                        'year': javinfo.year,
                        'outline': javinfo.outline,
                        'runtime': javinfo.runtime,
                        'director': javinfo.director,
                        'actor': javinfo.actor.split(','),    #List
                        'actor_photo': actor_photo_dict,   #dict
                        'cover': javinfo.cover,
                        'cover_small': javinfo.cover_small,
                        'extrafanart': javinfo.extrafanart.split(','),  #list
                        'trailer': javinfo.trailer,
                        'tag': javinfo.tag.split(','),   #List
                        'label': javinfo.label,
                        'series': javinfo.series,
                        'userrating': float(javinfo.userrating),    #float
                        'uservotes': int(javinfo.uservotes),    #int
                        'uncensored': bool(javinfo.uncensored),   #bool
                        'website': javinfo.website,
                        'source': f'{javinfo.source}[local]',
                        'imagecut': int(javinfo.imagecut)
                    }
                    db.close()
                    return dic
                except Exception as e:
                    db.close()
                    return 404
            else:
                db.close()
                return 404
        except:
            db.close()
            return 404


class SqliteSequence(BaseModel):
    name = BareField(null=True)
    seq = BareField(null=True)

    class Meta:
        table_name = 'sqlite_sequence'
        primary_key = False