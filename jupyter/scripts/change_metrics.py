from pymongo import MongoClient

# Connect To Database
client = MongoClient(
    "mongodb+srv://dbuser:B0st0n2021%2a%2a@development-kzgkz.mongodb.net/admin?authSource=admin&replicaSet=Development-shard-0&readPreference=primary&appname=MongoDB%20Compass&ssl=true")

# GET DATABASE
db = client['regatta-staging']
# GET COLLECTIONS
records_collection = db['lessonrecords']

data = records_collection.find()

print('what happend')
for record in data:
    old_records = record['records']
    print(record['_id'])
    for old_record in old_records:
        if old_record.get("dis") is not None:
            dis = old_record['dis']
            del old_record['dis']
            old_record['distance'] = dis
        if old_record.get("cal") is not None:
            cal = old_record['cal']
            del old_record['cal']
            old_record['calories'] = cal
        if old_record.get("kj") is not None:
            kj = old_record['kj']
            del old_record['kj']
            old_record['kilojoules'] = kj

        dis = old_record['distance'] if 'distance' in old_record else 0
        pace = 0
        if isinstance(dis, int) and dis > 0:
          pace = (old_record['et'] / dis) * 500
        old_record['averagePace'] = pace
    records_collection.update_one({'_id': record['_id']}, {
                                  '$set': {'records': old_records}})
