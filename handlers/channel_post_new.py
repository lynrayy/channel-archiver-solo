from pyrogram.types import Message
from pyrogram import Client, filters
from app import app, Post, MediaGroup
from datetime import datetime
import config


@app.on_message(filters.chat(config.source_channel_id))
async def on_new_post(client: Client, message: Message):
    if message.media_group_id is not None:
        mgid, is_mgid_new = MediaGroup.get_or_create(source_channel_id=message.chat.id, source_mg_id=message.media_group_id)
        if not is_mgid_new: return
    title = message.chat.title
    try:
        archive = await app.get_chat(config.archive_channel_id)
    except Exception as e:
        print(f"{datetime.now().strftime('%H:%M %d.%m.%Y')}   Нет доступа к каналу-архиву, новый пост из источника ({title}) не сохранён!", e)
        return
    archive_title = archive.title

    post, _ = Post.get_or_create(source_channel_id=message.chat.id, source_msg_id=message.id)
    post: Post
    if message.media_group_id is None:
        try:
            if config.store_as_archive:
                sent = await client.copy_message(config.archive_channel_id, message.chat.id, message.id)  # Вариант с копированием постов
            else:
                sent = await client.forward_messages(config.archive_channel_id, message.chat.id, message.id)  # Вариант с репостом
        except Exception as e:
            print(f"{datetime.now().strftime('%H:%M %d.%m.%Y')}   Невозможно сохранить пост в канал-архив ({archive_title}), новый пост из источника ({title}) не сохранён!", e)
            return
    else:
        try:
            if config.store_as_archive:
                sents = await client.copy_media_group(config.archive_channel_id, message.chat.id, message.id)  # Вариант с копированием
            else:
                messages = await client.get_media_group(message.chat.id, message.id)
                message_ids = [_message.id for _message in messages]
                sents = await client.forward_messages(config.archive_channel_id, message.chat.id, message_ids)
        except Exception as e:
            print(f"{datetime.now().strftime('%H:%M %d.%m.%Y')}   Невозможно сохранить пост в канал-архив ({archive_title}), новый пост из источника ({title}) не сохранён!", e)
            return


        sent: Message = sents[0]
        post.is_media_group = True


    # print("\n\nMESSAGE", message)
    # print("\n\nSENT", sent)
    post.archive_channel_id = sent.chat.id
    post.archive_msg_id = sent.id
    post.source_post_timestamp = datetime.utcnow().timestamp()
    post.save()
    print(f"{datetime.now().strftime('%H:%M %d.%m.%Y')}   В источнике ({title}) опубликован новый пост, сохранено.")

PostNewHandler = ...
