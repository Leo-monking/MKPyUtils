# -*- coding: UTF-8 -*-
'''
    Created on 2018年11月16日

    使用itchat完成的一个简易的微信机器人，尝试使用图灵机器人进行尬聊

    @author: monking
'''
import sys,itchat,requests,random,Utils
from sqlite3 import *
from itchat.content import *

reload(sys)
sys.setdefaultencoding('utf-8')
wxConn = None
wxCursor = None

KEY = '04f44290d4cf462aae8ac563ea7aac16'

'''
itchat msg TEXT=== >>>
{
u'AppInfo': {u'Type': 0, u'AppID': u''}, 
u'ImgWidth': 0, 
u'FromUserName': u'@0d1b3fba04eed93761ba67adb15e51bc', 
u'PlayLength': 0, 
u'OriContent': u'', 
u'ImgStatus': 1, 
u'RecommendInfo': {u'UserName': u'', u'Province': u'', u'City': u'', u'Scene': 0, u'QQNum': 0, u'Content': u'', u'Alias': u'', u'OpCode': 0, u'Signature': u'', u'Ticket': u'', u'Sex': 0, u'NickName': u'', u'AttrStatus': 0, u'VerifyFlag': 0}, 
u'Content': u'\u54c8\u54c8\u54c8\uff5e\u6211\u4e5f\u662f\u8d85\u4eba', 
u'MsgType': 1, 
u'ImgHeight': 0, 
u'StatusNotifyUserName': u'', 
u'StatusNotifyCode': 0, 
'Type': 'Text', 
u'NewMsgId': 6474052915172854903, 
u'Status': 3, 
u'VoiceLength': 0, 
u'MediaId': u'', 
u'MsgId': u'6474052915172854903', 
u'ToUserName': u'@0d1b3fba04eed93761ba67adb15e51bc', 
u'ForwardFlag': 0, 
u'FileName': u'', 
u'Url': u'', 
u'HasProductId': 0, 
u'FileSize': u'', 
u'AppMsgType': 0, 
'Text': u'\u54c8\u54c8\u54c8\uff5e\u6211\u4e5f\u662f\u8d85\u4eba',
u'Ticket': u'', 
u'CreateTime': 1542701112, 
u'EncryFileName': u'', 
u'SubMsgType': 0
}
'''

'''
itchat search_friends ===>>>
dict: {
u'UserName': u'@09d730a423bd0baac9417da37580dd6ec7f16bd931ac8750f2a247159c42ad3b', 
u'City': u'\u6210\u90fd', 
u'DisplayName': u'', 
u'UniFriend': 0, 
u'MemberList': [], 
u'PYQuanPin': u'qianyu', 
u'RemarkPYInitial': u'ZS', 
u'Uin': 0, 
u'AppAccountFlag': 0, 
u'VerifyFlag': 0, 
u'Province': u'\u56db\u5ddd', 
u'KeyWord': u'', 
u'RemarkName': u'\u6731\u59dd', 
u'PYInitial': u'QY', 
u'ChatRoomId': 0, 
u'IsOwner': 0, 
u'HideInputBarFlag': 0, 
u'EncryChatRoomId': u'', 
u'AttrStatus': 231525, 
u'SnsFlag': 17, 
u'MemberCount': 0, 
u'OwnerUin': 0, 
u'Alias': u'', 
u'Signature': u'\u6b64\u8eab\u4e0d\u5411\u4eca\u751f\u6e21\uff1b\u66f4\u5f85\u4f55\u751f\u6e21\u6b64\u8eab\u3002', 
u'ContactFlag': 1, 
u'NickName': u'\u9077\u7fbd', 
u'RemarkPYQuanPin': u'zhushu', 
u'HeadImgUrl': u'/cgi-bin/mmwebwx-bin/webwxgeticon?seq=673759769&username=@09d730a423bd0baac9417da37580dd6ec7f16bd931ac8750f2a247159c42ad3b&skey=@crypt_796dd2bb_27a4a00b047bb019e7c19f1a1b180ac9', 
u'Sex': 2, 
u'StarFriend': 0, 
u'Statues': 0
}
'''

'''
itchat card ===>>>
{
u'AppInfo': {u'Type': 0, u'AppID': u''}, 
u'ImgWidth': 0, 
u'FromUserName': u'@a269a504d6b949161fc1ce170e92e050c6c3bebe24d0b928f2c675804b7ef821', 
u'PlayLength': 0, 
u'OriContent': u'', 
u'ImgStatus': 1, 
u'RecommendInfo': 
{u'UserName': 
    u'@864902f148b482020c7f9e29d447dabec7b502665161e66871191a815629acbb', 
    u'Province': u'\u56db\u5ddd', 
    u'City': u'\u6210\u90fd', 
    u'Scene': 17, 
    u'QQNum': 0, 
    u'Content': u'', 
    u'Alias': u'', 
    u'OpCode': 0, 
    u'Signature': u'', 
    u'Ticket': u'', 
    u'Sex': 2, 
    u'NickName': u'\u9077\u7fbd', 
    u'AttrStatus': 231525, 
    u'VerifyFlag': 0
}, 
u'Content': u'<?xml version="1.0"?>\n<msg bigheadimgurl="http://wx.qlogo.cn/mmhead/ver_1/45nktyG68ibIPIdRNKkAmGTibWicQqqluYwBWjeUPiaCno5rjyl3iaTpAv3vTFHDg5zbq5twIUuXbfafoXw15nczTrc4RC4hrQjMeicaI0Y3oAV18/0" smallheadimgurl="http://wx.qlogo.cn/mmhead/ver_1/45nktyG68ibIPIdRNKkAmGTibWicQqqluYwBWjeUPiaCno5rjyl3iaTpAv3vTFHDg5zbq5twIUuXbfafoXw15nczTrc4RC4hrQjMeicaI0Y3oAV18/132" username="wxid_m9mplhhfqz0j22" nickname="\u9077\u7fbd"  shortpy="QY" alias="" imagestatus="3" scene="17" province="\u56db\u5ddd" city="\u6210\u90fd" sign="" sex="2" certflag="0" certinfo="" brandIconUrl="" brandHomeUrl="" brandSubscriptConfigUrl="" brandFlags="0" regionCode="CN_Sichuan_Chengdu" />\n', 
u'MsgType': 42, 
u'ImgHeight': 0, 
u'StatusNotifyUserName': u'', 
u'StatusNotifyCode': 0, 
'Type': 'Card', 
u'NewMsgId': 4963383244124980002, 
u'Status': 3, 
u'VoiceLength': 0, 
u'MediaId': u'', 
u'MsgId': u'4963383244124980002',
 u'ToUserName': u'@a269a504d6b949161fc1ce170e92e050c6c3bebe24d0b928f2c675804b7ef821', 
 u'ForwardFlag': 0, 
 u'FileName': u'', 
 u'Url': u'', 
 u'HasProductId': 0, 
 u'FileSize': u'', 
 u'AppMsgType': 0, 
 'Text': 
 {u'UserName': u'@864902f148b482020c7f9e29d447dabec7b502665161e66871191a815629acbb', 
 u'Province': u'\u56db\u5ddd', 
 u'City': u'\u6210\u90fd', 
 u'Scene': 17, 
 u'QQNum': 0, 
 u'Content': u'', 
 u'Alias': u'', 
 u'OpCode': 0, 
 u'Signature': u'', 
 u'Ticket': u'', 
 u'Sex': 2, 
 u'NickName': u'\u9077\u7fbd', 
 u'AttrStatus': 231525, 
 u'VerifyFlag': 0}, 
 u'Ticket': u'', 
 u'CreateTime': 1543548792, 
 u'EncryFileName': u'', 
 u'SubMsgType': 0
 }
'''

#机器人列表
createRobotsSql = '''
CREATE TABLE IF NOT EXISTS Robots(
ID INT PRIMARY KEY NOT NULL,
botName CHAR(40) not null,
botSex CHAR(10) not null,
botMemo CHAR(100));
'''

#允许机器人回复的好友列表
createAutoReplyFriendsSql = '''
CREATE TABLE IF NOT EXISTS Friends(
userName CHAR(60) not null,
userNickName CHAR(40),
userRemarkName CHAR(40)
autoReply CHAR(10) not null,
userSignature CHAR(40)
'''

def get_response(msg):
    apiUrl = 'http://www.tuling123.com/openapi/api'
    data = {
        'key'    : KEY,
        'info'   : msg,
        'userid' : 'wechat-robot',
    }
    try:
        r = requests.post(apiUrl, data=data).json()
        return r.get('text')
    except:
        return

    
'''
    判断当前库的某表格中某字段是否存在该数据，如果存在返回True，不存在则返回False
'''
def IsExist(tableName,keyName,keyValue):
    sqlStr = ("select * from %s where ") % (tableName)
    keyCount = len(keyName)
    for i in (0,keyCount-1):
        if i == 0:
            sqlStr = sqlStr + (" %s like '%s'") % (keyName[i],keyValue[i])
        else:
            sqlStr = sqlStr + (" and %s like '%s'") % (keyName[i],keyValue[i])
    ret = wxConn.GetBySql(sqlStr)
    if (ret.rowcount >= 1):
        return True
    else:
        return False
    
'''
@param cmdMsgList: 
    cmdMsgList[0]    userRemarkName
    cmdMsgList[1]    Yes/No,系统默认是不使用机器人自动回复
    
    逻辑：
    1、如果用户在自动回复列表中存在，则更新相关信息；
    2、如果用户不在自动回复列表中，则新增该用户到自动回复列表中。
'''
def autoReplyFriends(cmdMsgList):
    users=itchat.search_friends(cmdMsgList[0])
    if len(users) > 0:
        keyName = keyValue = []
        keyName.append("userName")
        keyValue.append(users[0]['UserName'])
        if (IsExist("Friends", keyName,keyValue )):
            sqlStr = ("update Friends set userNickName = '%s' ,userRemarkName = '%s' ,autoReply = '%s' ,userSignature = '%s' \
                      where userName like '%s'") %\
            (users[0]['userNickName'],users[0]['userRemarkName'],cmdMsgList[1],users[0]['Signature)'],users[0]['UserName'])
        else:
            sqlStr = ("INSERT INTO Friends (userName,userNickName,userRemarkName,autoReply,userSignature) \
            values ('%s','%s','%s','%s','%s')") % \
            (users[0]['UserName'],users[0]['userNickName'],users[0]['userRemarkName'],cmdMsgList[1],users[0]['Signature)'])
               
        print sqlStr
        wxConn.ExecBySql(sqlStr)
        

'''
    逻辑：
    1、获取TEXT消息；
    2、判断消息是否有本地命令，如果有本地命令，则执行命令；
    3、如果不是本地命令，则根据FromUserName判断是否使用图灵机器人自动回复    
'''
@itchat.msg_register(TEXT,NOTE)
def wxBot_Msg(msg):
    
    msg_type = msg['Type']
    if msg_type == TEXT:
        contact = itchat.get_contact()
        
        print "通讯录：\n"
        print contact
        print msg['FromUserName']
        
        print "\n\n\n获取微信朋友：get_friends:\n"
        print itchat.get_friends()
        
        print itchat.search_friends("朱姝")
        cmdMsgList = msg[TEXT].split(' ')
        if cmdMsgList[0] == 'autoreply' or cmdMsgList[0] == 'ar':
            autoReplyFriends(cmdMsgList)
        else:
            wxBot_reply(msg)
    elif msg_type == 'NOTE':
        print '通知消息'
    else:
        print '消息异常'
        
def wxBot_reply(msg):
    keyName = []
    keyValue = []
    keyName.append('userName')
    keyValue.append(msg['FromUserName'])
    keyName.append('autoReply')
    keyValue.append('yes')
    if (IsExist("Friends", keyName,keyValue )):
        #robots=['——By Houjun','——By 侯军','——By 侯明亮','--By MONKING']
        #replyMsg = get_response(msg['Text'])+random.choice(robots)
        replyMsg = get_response(msg['Text'])
        print replyMsg
        #itchat.send_msg(replyMsg,msg['FromUserName'])
#机器人初始化
def wxBot_init(dbName):
    wxConn = Utils.Sqlite3DB(dbName)
    '''
    conn.execute(createAutoReplyFriendsSql)
    conn.execute(createRobotsSql)
    conn.commit()
    '''
    
#添加机器人信息
def wxRobot_add(robot):
    cursor = wxConn.execute('''
        select count(*) from Robots;
    ''')
    for ret in cursor:
        insertSql = ("INSERT INTO Robots (ID,botName,botSex,botMemo) values (%d,'')") % (ret[0]+1)
        print insertSql
        #wxConn.execute(insertSql)
        #wxConn.commit()

        
    
if __name__ == '__main__':
    #itchat.auto_login(hotReload = True,enableCmdQR = 2)
    dbName = 'WXBot.db'
    wxBot_init(dbName)
    #wxRobot_add(wxConn,[])
    itchat.auto_login(hotReload = True)
    itchat.run()
       
    