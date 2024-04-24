from pyrogram.types import Message, Chat
from pyrogram import Client, filters
from app import app, Post
from typing import List
from datetime import datetime, timedelta
import config


async def send_notif(client, chat_id, timestamp, title):
    time = datetime.fromtimestamp(timestamp) + timedelta(hours=3)
    try:
        await client.send_message(chat_id, f"<b>🗑️ В канале {title} \n"
                                           f"удалён пост от</b> {time.strftime(f'%d.%m.%Y %H:%M')} по МСК ⬇️")
    except Exception as e:
        print(f"{datetime.now().strftime('%H:%M %d.%m.%Y')}   Нет доступа к каналу для сохранения удалённых сообщений, пост не сохранён.", e)


@app.on_deleted_messages(filters.chat(config.source_channel_id))
async def on_del_post(client: Client, messages_list: List[Message]):
    src_channel: Chat = await client.get_chat(messages_list[0].chat.id)
    src_title = src_channel.title
    for message in messages_list:
        source_post: Post = Post.get_or_none(source_channel_id=message.chat.id, source_msg_id=message.id)
        if source_post is None: continue
        if source_post.is_media_group:
            messages = await client.get_media_group(source_post.archive_channel_id, source_post.archive_msg_id)
            message_ids = [_message.id for _message in messages]
            await send_notif(client, config.deleted_channel_id, source_post.source_post_timestamp, src_title)
            try:
                await client.forward_messages(config.deleted_channel_id, source_post.archive_channel_id, message_ids)
            except:
                ...
            else:
                print(f"{datetime.now().strftime('%H:%M %d.%m.%Y')}   В источнике ({src_title}) удалён пост ({messages_list[0].id}-{messages_list[-1].id}). Он опубликован в канале-удалёнке.")
        else:
            await send_notif(client, config.deleted_channel_id, source_post.source_post_timestamp, src_title)
            try:
                await client.forward_messages(config.deleted_channel_id, source_post.archive_channel_id, source_post.archive_msg_id)
            except:
                ...
            else:
                print(f"{datetime.now().strftime('%H:%M %d.%m.%Y')}   В источнике ({src_title}) удалён пост ({message.id}). Он опубликован в канале-удалёнке.")
PostDelHandler = ...
