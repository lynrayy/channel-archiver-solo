import auth
from peewee import Model, BigIntegerField, BooleanField, SqliteDatabase, FloatField
from pyrogram import Client


app = Client("ChannelArchiver",
             auth.api_id,
             auth.api_hash,
             app_version='Archiver 0.0.5',
             device_model='Xiaomi MI 9',
             system_version='Android 11 R', phone_number=auth.phone_number)

_db = SqliteDatabase('posts.db')


class Post(Model):
    source_channel_id = BigIntegerField()
    source_msg_id = BigIntegerField()
    source_post_timestamp = FloatField(null=True)
    archive_channel_id = BigIntegerField(null=True)
    archive_msg_id = BigIntegerField(null=True)

    is_media_group = BooleanField(default=False)
    restored_to_deleted_msgs_channel = BooleanField(default=False)

    class Meta:
        database = _db


class MediaGroup(Model):
    source_channel_id = BigIntegerField()
    source_mg_id = BigIntegerField()

    class Meta:
        database = _db


_db.connect()
_db.create_tables([Post, MediaGroup])
