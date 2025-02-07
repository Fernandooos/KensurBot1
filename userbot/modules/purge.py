# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
""" Userbot module for purging unneeded messages(usually spam or ot). """

from asyncio import sleep

from telethon.errors import rpcbaseerrors

from userbot import CMD_HELP
from userbot.events import register


@register(outgoing=True, pattern=r"^\.purge$")
async def fastpurger(purg):
    """Para usar o comando .purge, responda a primeira mensagem de onde devo começar."""
    chat = await purg.get_input_chat()
    msgs = []
    itermsg = purg.client.iter_messages(chat, min_id=purg.reply_to_msg_id)
    count = 0

    if purg.reply_to_msg_id is not None:
        async for msg in itermsg:
            msgs.append(msg)
            count += 1
            msgs.append(purg.reply_to_msg_id)
            if len(msgs) == 100:
                await purg.client.delete_messages(chat, msgs)
                msgs = []
    else:
        return await purg.edit("**Eu preciso de uma mensagem para começar a exclusão.**")

    if msgs:
        await purg.client.delete_messages(chat, msgs)
    done = await purg.client.send_message(
        purg.chat_id, "**Limpeza rápida completa!**" f"\nPurged {str(count)} messages"
    )
    await sleep(2)
    await done.delete()


@register(outgoing=True, pattern=r"^\.purgeme")
async def purgeme(delme):
    """Com .purgeme você pode excluir as suas ultimas mensagens."""
    message = delme.text
    count = int(message[9:])
    i = 1

    async for message in delme.client.iter_messages(delme.chat_id, from_user="me"):
        if i > count + 1:
            break
        i += 1
        await message.delete()

    smsg = await delme.client.send_message(
        delme.chat_id,
        "**Limpeza completa!** Foram excluidas " + str(count) + " mensagens.",
    )
    await sleep(2)
    i = 1
    await smsg.delete()


@register(outgoing=True, pattern=r"^\.del$")
async def delete_it(delme):
    """Para usar o comando .del responda uma mensagem."""
    msg_src = await delme.get_reply_message()
    if delme.reply_to_msg_id:
        try:
            await msg_src.delete()
            await delme.delete()
        except rpcbaseerrors.BadRequestError:
            await delme.edit("**Bom, não consegui excluir a mensagem.**")


@register(outgoing=True, pattern=r"^\.edit")
async def editer(edit):
    """Usar o comando .editme edita sua ultima mensagem."""
    message = edit.text
    chat = await edit.get_input_chat()
    self_id = await edit.client.get_peer_id("me")
    string = str(message[6:])
    i = 1
    async for message in edit.client.iter_messages(chat, self_id):
        if i == 2:
            await message.edit(string)
            await edit.delete()
            break
        i += 1


@register(outgoing=True, pattern=r"^\.sd")
async def selfdestruct(destroy):
    """Usar o comando .sd habilita a auto-destruição de mensagens."""
    message = destroy.text
    counter = int(message[4:6])
    text = str(destroy.text[6:])
    await destroy.edit(text)
    await sleep(counter)
    await destroy.delete()


CMD_HELP.update(
    {
        "purge": ">`.purge`" "\nUsage: Purges all messages starting from the reply.",
        "purgeme": ">`.purgeme <x>`"
        "\nUsage: Deletes x amount of your latest messages.",
        "del": ">`.del`" "\nUsage: Deletes the message you replied to.",
        "edit": ">`.edit <newmessage>`"
        "\nUsage: Replace your last message with <newmessage>.",
        "sd": ">`.sd <x> <message>`"
        "\nUsage: Creates a message that selfdestructs in x seconds."
        "\n<x> should be a two digit value, 3rd digit and further digits will be taken as <message>.",
    }
)
