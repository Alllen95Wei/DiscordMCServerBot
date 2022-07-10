import python_aternos as pa


def start_server(username, password):
    login_data = {
        "username": username,
        "password": password
    }
    print("登入資料：")
    print("使用者名稱：" + login_data["username"])
    print("密碼：" + login_data["password"])
    print("")
    print("嘗試登入...")
    try:
        aternos = pa.Client.from_credentials(login_data["username"], login_data["password"])
    except Exception as e:
        print("登入失敗！")
        print("錯誤訊息：{0}".format(e))
        return "Login failed:" + str(e)
    server_list = aternos.list_servers()
    serv = server_list[0]
    print("伺服器資訊：")
    print("名稱：" + serv.subdomain)
    print("版本：" + serv.version)
    print("軟體：" + serv.software)
    if serv.status_num == 0:
        server_status = "停止"
    elif serv.status_num == 1:
        server_status = "運作中"
    elif serv.status_num == 2:
        server_status = "啟動中"
    elif serv.status_num == 3:
        server_status = "關閉"
    elif serv.status_num == 6:
        server_status = "未知"
    elif serv.status_num == 7:
        server_status = "錯誤"
    elif serv.status_num == 10:
        server_status = "確認"
    else:
        server_status = "未知(無法取得資料)"
    print("狀態：" + server_status + "(" + str(serv.status_num) + ")")
    if serv.status_num != 0:
        print("錯誤：伺服器必須停止或關閉才能啟動！")
        return "Status:" + str(serv.status)
    print("嘗試啟動伺服器...")
    try:
        serv.start()
        print("啟動成功！")
        return True
    except Exception as e:
        print("啟動失敗！")
        print("錯誤訊息：{0}".format(e))
        return "Start failed:" + str(e)


def get_server_status(username, password):
    login_data = {
        "username": username,
        "password": password
    }
    print("登入資料：")
    print("使用者名稱：" + login_data["username"])
    print("密碼：" + login_data["password"])
    print("")
    print("嘗試登入...")
    try:
        aternos = pa.Client.from_credentials(login_data["username"], login_data["password"])
    except Exception as e:
        print("登入失敗！")
        print("錯誤訊息：{0}".format(e))
        return "Login failed:" + str(e)
    server_list = aternos.list_servers()
    serv = server_list[0]
    if serv.status_num == 0:
        server_status = "停止"
    elif serv.status_num == 1:
        server_status = "運作中"
    elif serv.status_num == 2:
        server_status = "啟動中"
    elif serv.status_num == 3:
        server_status = "關閉"
    elif serv.status_num == 6:
        server_status = "未知"
    elif serv.status_num == 7:
        server_status = "錯誤"
    elif serv.status_num == 10:
        server_status = "確認"
    else:
        server_status = "未知(無法取得資料)"
    print("狀態：" + server_status + "(" + str(serv.status_num) + ")")
    return "Status:" + str(server_status)
