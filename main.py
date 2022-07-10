import os
import discord
import time
from dotenv import load_dotenv

import log_writter
# import update
import server_action

client = discord.Client()
localtime = time.localtime()
base_dir = os.path.abspath(os.path.dirname(__file__))


@client.event
async def on_ready():
    music = discord.Activity(type=discord.ActivityType.playing, name="Still developing...")
    await client.change_presence(status=discord.Status.dnd, activity=music)
    log_writter.write_log("-------------------------------------------------------------\n", True)
    log_writter.write_log("\n登入成功！\n目前登入身份：" +
                          str(client.user) + "\n以下為使用紀錄(只要開頭訊息有\"a!\"，則這則訊息和系統回應皆會被記錄)：\n\n")

testing = False


@client.event
async def on_message(message):
    global testing
    final_msg_list = []
    msg_in = str(message.content)
    default_color = 0x1E14B0
    error_color = 0xF1411C
    if message.author == client.user:  # 排除自己的訊息，避免陷入無限循環
        return
    elif msg_in == "as!test":
        if testing:
            testing = False
            embed = discord.Embed(title="測試模式", description="測試模式已**關閉**。", color=default_color)
            final_msg_list.append(embed)
        else:
            testing = True
            embed = discord.Embed(title="測試模式", description="測試模式已**開啟**。", color=default_color)
            final_msg_list.append(embed)
        use_log = str(message.channel) + "/" + str(message.author) + ":\n" + msg_in + "\n\n"
        log_writter.write_log(use_log)
    elif testing:
        return
    elif msg_in.startswith("as!"):
        use_log = str(message.channel) + "/" + str(message.author) + ":\n" + msg_in + "\n\n"
        log_writter.write_log(use_log)
        parameter = msg_in[3:]
        if parameter == "start":
            load_dotenv(dotenv_path=os.path.join(base_dir, "SECRET.env"))
            username = os.getenv("USERNAME")
            password = os.getenv("PASSWORD")
            result = server_action.start_server(username, password)
            if not result:
                embed = discord.Embed(title="start", description="無法啟動伺服器！請參閱以下錯誤訊息。", color=error_color)
                if result.startswith("Login failed:"):
                    error_msg = result[result.find(":"):]
                    embed.add_field(name="登入錯誤", value=error_msg, inline=False)
                elif result.startswith("Status:"):
                    error_msg = "伺服器目前狀態({0})，不允許啟動！".format(result[result.find(":"):])
                    embed.add_field(name="啟動錯誤", value=error_msg, inline=False)
                elif result.startswith("Start failed:"):
                    error_msg = result[result.find(":"):]
                    embed.add_field(name="啟動錯誤", value=error_msg, inline=False)
                else:
                    embed.add_field(name="錯誤", value="(無錯誤訊息)", inline=False)
                final_msg_list.append(embed)
            else:
                embed = discord.Embed(title="start", description="伺服器已啟動！請稍微等待伺服器前置工作完成。", color=default_color)
                final_msg_list.append(embed)
        for i in range(len(final_msg_list)):
            current_msg = final_msg_list[i]
            if isinstance(current_msg, discord.File):
                await message.channel.send(file=final_msg_list[i])
            elif isinstance(current_msg, discord.Embed):
                await message.channel.send(embed=final_msg_list[i])
            elif isinstance(current_msg, str):
                await message.channel.send(final_msg_list[i])
            new_log = str(message.channel) + "/" + str(client.user) + ":\n" + str(final_msg_list[i]) + "\n\n"
            log_writter.write_log(new_log)
        final_msg_list.clear()


# 取得TOKEN
load_dotenv(dotenv_path=os.path.join(base_dir, "SECRET.env"))
TOKEN = str(os.getenv("TOKEN"))
client.run(TOKEN)
