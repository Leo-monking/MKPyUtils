# -*- coding: UTF-8 -*-
'''
    Created on 2018年11月21日

    使用itchat完成的一个简易的微信机器人，尝试使用图灵机器人进行尬聊

    @author: monking
'''

import os,re,sys,itchat,requests,time
from itchat.content import *


#当前强制使用utf-8编码模式
reload(sys)
sys.setdefaultencoding('utf-8')

msgInfomation = {}
friends = []
tulingChatList = []
#针对表情包的内容
face_bug = None

TULING_KEY = '04f44290d4cf462aae8ac563ea7aac16'
def GetResponseByTuLing(msg):
    apiUrl = 'http://www.tuling123.com/openapi/api'
    data = {
        'key'    : TULING_KEY,
        'info'   : msg,
        'userid' : 'wechat-robot',
    }
    try:
        r = requests.post(apiUrl, data=data).json()
        return r.get('text')
    except:
        return

'''
# 这里的TEXT表示如果有人发送文本消息()
# TEXT    文本    文本内容(文字消息)
# MAP    地图    位置文本(位置分享)
# CARD    名片    推荐人字典(推荐人的名片)
# SHARING    分享    分享名称(分享的音乐或者文章等)
# PICTURE 下载方法        图片/表情
# RECORDING    语音    下载方法
# ATTACHMENT    附件    下载方法
# VIDEO    小视频    下载方法
# FRIENDS    好友邀请    添加好友所需参数
# SYSTEM    系统消息    更新内容的用户或群聊的UserName组成的列表
# NOTE    通知    通知文本(消息撤回等)，那么就会调用下面的方法
# 其中isFriendChat表示好友之间，isGroupChat表示群聊，isMapChat表示公众号
'''
@itchat.msg_register([TEXT, PICTURE, FRIENDS, CARD, MAP, SHARING, RECORDING, ATTACHMENT, VIDEO],isFriendChat=True, isGroupChat=True, isMpChat=True)
def iChat_Handle_Rec_Msg(msg):
    global face_bug,msgInfomation
    
    #消息类型
    msgType = msg['Type']
    #接收消息的时间
    msgTimeRec = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    #在好友列表中查询发送信息的好友昵称
    msgFrom = itchat.search_friends(userName = msg['FromUserName'])['NickName']
    #消息发送时间
    msgTime = msg['CreateTime']
    #消息的id
    msgId = msg['MsgId']
    #消息的内容
    msgContent = None
    #分享的链接，比如分享的文章和音乐
    msgShareUrl = None
    
    # ActualNickName : 实际 NickName(昵称) 群消息里(msg)才有这个值
    if 'ActualNickName' in msg:
        #群消息的发送者,用户的唯一标识
        from_user = msg['ActualUserName']
        #发送者群内的昵称
        msgFrom = msg['ActualNickName']
        friends = itchat.get_friends(update=True)#获取所有好友
        for f in friends:
            if from_user == f['UserName']: #如果群消息是好友发的
                if f['RemarkName']: # 优先使用好友的备注名称，没有则使用昵称
                    msgFrom = f['RemarkName']
                else:
                    msgFrom = f['NickName']
                break
        groups = itchat.get_chatrooms(update=True)#获取所有的群
        for g in groups:
            if msg['FromUserName'] == g['UserName']:#根据群消息的FromUserName匹配是哪个群
                group_name = g['NickName']
                group_menbers = g['MemberCount']
                break
        group_name = group_name + "(" + str(group_menbers) +")"
    #否则的话是属于个人朋友的消息
    else:
        if itchat.search_friends(userName=msg['FromUserName'])['RemarkName']:#优先使用备注名称
            msgFrom = itchat.search_friends(userName=msg['FromUserName'])['RemarkName']
        else:
            msgFrom = itchat.search_friends(userName=msg['FromUserName'])['NickName'] #在好友列表中查询发送信息的好友昵称
        group_name = ""
    #如果发送的消息是文本或者好友推荐
    if msgType == TEXT or msgType == FRIENDS:
        msgContent = msg[TEXT]
        if msgContent == '初始化' or  msgContent.lower() == 'init':
            friendInfo_init()
        elif len(tulingChatList) >= 0:
            if msg['FromUserName'] in tulingChatList:
                print msgContent
                iChat_reply(msg)
        else:
            print msgContent 
    #如果发送的消息是附件、视频、图片、语音
    elif msgType == ATTACHMENT or msgType == VIDEO or msgType == PICTURE or msgType == RECORDING:
        #内容就是他们的文件名
        msgContent = msg['FileName']
        #下载文件
        msg[TEXT](str(msgContent))
        
        print (msgContent)
    #如果消息时推荐的名片
    elif msgType == CARD:
        '''
        #内容就是推荐人的昵称和性别
        msgContent = msg['RecommendInfo']['NickName'] + ' 的名片'
        if msg['RecommendInfo']['Sex'] == 1:
            msgContent += ' 性别为男!'
        else:
            msgContent += ' 性别为女!'
            
        print (msgContent)
        '''
        addFriendToTuLingList(msg['RecommendInfo']['NickName'])
        print tulingChatList
    #如果消息是分享的位置信息
    elif msgType == MAP:
        x,y,location = re.search("<location x=\"(.*?)\" y=\"(.*?)\".*label=\"(.*?)\".*",msg['OriContent']).group(1, 2, 3)
        if location is None:
            msgContent = r"纬度->" + x.__str__() + " 经度->" + y.__str__()     #内容为详细的地址
        else:
            msgContent = r"" + location
            
        print (msgContent)
    #如果消息为分享的音乐或者文章，详细的内容为文章的标题或者是分享的名字
    elif msgType == SHARING:
        msgContent = msg[TEXT]
        #记录分享的Url
        msgShareUrl = msg['Url']
        
        print (msgShareUrl)
        
    face_bug = msgContent
    
    ##将信息存在在字典中，每个msgId对应一条消息
    msgInfomation.update(
        {
            msgId:{
                "msgFrom":msgFrom, 
                "msgTime":msgTime, 
                "msgTimeRec":msgTimeRec,
                "msgType":msg["Type"],
                "msgContent":msgContent,
                "msgShareUrl":msgShareUrl
            }
        }
    )
        #自动删除130秒之前的消息，避免数据量太大后引起内存不足
    del_info = []
    for k in msgInfomation:
        m_time = msgInfomation[k]['msgTime'] #取得消息时间
        if int(time.time()) - m_time > 130:
            del_info.append(k)
    if del_info:
        for i in del_info:
            msgInfomation.pop(i)

##监听是否有消息被撤回
@itchat.msg_register(NOTE, isFriendChat=True, isGroupChat=True, isMpChat=True)
def infoBack(msg):
    global msgInfomation
    #这里如果这里的msg['Content']中包含消息撤回和id，就执行下面的语句
    if '撤回了一条消息' in msg['Content']:
        #在返回的content查找撤回的消息的id
        oldMsgId = re.search("\<msgid\>(.*?)\<\/msgid\>", msg['Content']).group(1)
        
        #获取到消息原文,类型：字典
        oldMsg = msgInfomation.get(oldMsgId)
        
        if oldMsg == None:
            return
        #如果发送的时表情包
        if len(oldMsgId) < 11:
            itchat.send_file(face_bug,toUserName = 'filehelper')
        #发送撤回的提示给文件助手
        else:
            msgBody = "告诉你一个秘密~" + "\n" \
                       + oldMsg.get('msgFrom') + " 撤回了 " + oldMsg.get("msgType") + " 消息" + "\n" \
                       + oldMsg.get('msgTimeRec') + "\n" \
                       + "撤回了什么 ⇣" + "\n" \
                       + r"" + oldMsg.get("msgContent")
            #如果是分享的文件被撤回了，那么就将分享的url加在msg_body中发送给文件助手
            if oldMsg['msgType'] == "Sharing":
                msgBody += "\n就是这个链接➣ " + oldMsg.get('msgShareUrl')
            
            # 将撤回消息发送到文件助手
            itchat.send_msg(msgBody, toUserName='filehelper')
            # 有文件的话也要将文件发送回去
            if oldMsg["msgType"] == "Picture" \
                    or oldMsg["msgType"] == "Recording" \
                    or oldMsg["msgType"] == "Video" \
                    or oldMsg["msgType"] == "Attachment":
                msgFile = '@fil@%s' % (oldMsg['msgContent'])
                itchat.send(msg=msgFile, toUserName='filehelper')
                os.remove(oldMsg['msgContent'])
            # 删除字典旧消息
            msgInfomation.pop(oldMsgId)
#图灵机器人自动回复功能
def iChat_reply(msg):
    replyMsg = GetResponseByTuLing(msg['Text'])
    print replyMsg
    #itchat.send_msg(replyMsg,msg['FromUserName'])
    
#聊天机器人初始化
def iChat_init():
    #itchat.auto_login(hotReload = True,enableCmdQR=-1)
    itchat.auto_login(hotReload = True,enableCmdQR=-2)
    itchat.run()

#获取所有好友信息
def friendInfo_init():
    global friends
    friendInfo = {}
    for myFriend in itchat.get_friends(update=True):
        friendInfo.update(
            {
                "UserName":myFriend["UserName"],
                "RemarkName":myFriend["RemarkName"],
                "NickName":myFriend["NickName"],
                "RemarkPYQuanPin":myFriend["RemarkPYQuanPin"],
                "Sex":myFriend["Sex"]
            }
        )
        friends.append(friendInfo)

def addFriendToTuLingList(NickName):
    global tulingChatList
    for fri in friends:
        if NickName == fri['NickName']:
            tulingChatList.append(fri['UserName'])


if __name__ == '__main__':
    iChat_init()
    