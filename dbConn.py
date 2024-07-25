import pymysql
import datetime

#连接数据库
conn = pymysql.connect(
    host='localhost',
    user='root',
    passwd='147369',
    database='DBsystem'
)
cursor = conn.cursor()

#用户登录
def checkLogin(id:str, pw:str)->dict:

    msg = {'status':False, 'msg':''}

    sql = f'''select username, psword
            from userInfo where username = "{id}"'''
    cursor.execute(sql)
    res = list(cursor)

    #用户不存在
    if len(res) == 0:
        msg['msg'] = "用户名不存在！再试试吧"
        return msg

    #密码错误
    elif not pw == res[0][-1]:
        msg['msg'] = "密码错误，再试一次吧！"
        return msg
    
    #成功登录返回信息
    else:
        msg['status'] = True
        msg['username'] = id
        return msg

#获取用户信息
def getUserInfo(uesrname):
    sql = f'''
    select username, email, phoneNumber, age, job, year_
    from userInfo
    where username = '{uesrname}'
    '''
    cursor.execute(sql)
    res = list(cursor)[0]

    user_info = {'username' : res[0],
                 'email' : res[1],
                 'phone' : res[2],
                 'age' : res[3],
                 'job' : res[4],
                 'year' : res[5]}

    return user_info

#注册用户
def registerNewUser(userInfo):
    msg = {'status':False, "msg":''}

    #检查电话号码是否全为数字
    def checkPhone(phone:str):
        for p in phone:
            if not p.isdigit():
                return False
        return True

    #非法用户名
    if len(userInfo['username']) > 20:
        msg['msg'] = '用户名长度不能超过20位'
        return msg
    #非法电子邮箱
    elif len(userInfo['email']) > 50:
        msg['msg'] = '非法邮箱'
        return msg
    #非法电话字符
    elif not checkPhone(userInfo['phone']):
        msg['msg'] = '非法号码字符'
        return msg
    #非法电话长度
    elif len(userInfo['phone']) != 11:
        msg['msg'] = '电话号码需为11位'
        return msg
    #非法年龄
    elif int(userInfo['age']) < 0 or int(userInfo['age']) > 150:
        msg['msg'] = '非法年龄'
        return msg
    #非法工作
    elif len(userInfo['job']) > 30:
        msg['msg'] = '工作名称不能超过30位'
        return msg
    #非法入学年份
    elif int(userInfo['year']) > datetime.date.today().year:
        msg['msg'] = '非法入学年份'
        return msg
    #密码不同
    elif not userInfo['password'] == userInfo['confirm_password']:
        msg['msg'] = '密码不一致'
        return msg
    #非法密码
    elif len(userInfo['password']) > 20:
        msg['msg'] = '密码长度不能超过20位'
        return msg
    
    sql = f'''
    insert into userInfo (username, email, phoneNumber, age, job, year_, psword)
    values ('{userInfo['username']}', '{userInfo['email']}', '{userInfo['phone']}', {int(userInfo['age'])}, 
            '{userInfo['job']}', {int(userInfo['year'])}, '{userInfo['password']}')
    '''
    
    try:
        cursor.execute(sql)
        conn.commit()
    except pymysql.err.IntegrityError as e:
        if e.args[0] == 1062:
            msg['msg'] = '用户已存在'
            return msg
        
    msg['status'] = True
    msg['msg'] = '注册成功'
    return msg
    
#修改用户信息
def modifyUserInfo(username:str, userInfo):
    msg = {'status':False, "msg":''}

    #检查电话号码是否全为数字
    def checkPhone(phone:str):
        for p in phone:
            if not p.isdigit():
                return False
        return True

    #非法用户名
    if len(userInfo['username']) > 20:
        msg['msg'] = '用户名长度不能超过20位'
        return msg
    #非法电子邮箱
    elif len(userInfo['email']) > 50:
        msg['msg'] = '非法邮箱'
        return msg
    #非法电话字符
    elif not checkPhone(userInfo['phone']):
        msg['msg'] = '非法号码字符'
        return msg
    #非法电话长度
    elif len(userInfo['phone']) != 11:
        msg['msg'] = '电话号码需为11位'
        return msg
    #非法年龄
    elif int(userInfo['age']) < 0 or int(userInfo['age']) > 150:
        msg['msg'] = '非法年龄'
        return msg
    #非法工作
    elif len(userInfo['job']) > 30:
        msg['msg'] = '工作名称不能超过30位'
        return msg
    #非法入学年份
    elif int(userInfo['year']) > datetime.date.today().year:
        msg['msg'] = '非法入学年份'
        return msg
    
    sql = ''
    if username == userInfo['username']:
        sql = f'''
        update userInfo
        set email = '{userInfo['email']}',
            phoneNumber = '{userInfo['phone']}',
            age = {int(userInfo['age'])},
            job = '{userInfo['job']}',
            year_ = {int(userInfo['year'])}
        where username = '{username}'
        '''
    else:
        sql = f'''
        update userInfo
        set username = '{userInfo['username']}',
            email = '{userInfo['email']}',
            phoneNumber = '{userInfo['phone']}',
            age = {int(userInfo['age'])},
            job = '{userInfo['job']}',
            year_ = {int(userInfo['year'])}
        where username = '{username}'
        '''
        
    try:
        cursor.execute(sql)
        conn.commit()
    except pymysql.err.IntegrityError as e:
        if e.args[0] == 1062:
            msg['msg'] = '用户已存在'
            return msg
        
    msg['status'] = True
    msg['msg'] = '修改成功'
    return msg
    
#修改密码
def modifyPassword(username, data):
    # 获取用户密码
    def getUserPassword(username):
        sql = f'''
        select psword
        from userInfo
        where username = '{username}'
        '''
        cursor.execute(sql)
        return list(cursor)[0][0]

    msg = {'status':False, "msg":''}

    psword=data['last_password'] 
    new_p=data['new_password']
    confirm_p=data['confirm_password']    

    if not new_p == confirm_p:
        msg['msg'] = "新密码不一致"
        return msg

    if not getUserPassword(username) == psword:
        msg['msg'] = "原密码输入错误"
        return msg
    #非法密码
    elif len(psword) > 20:
        msg['msg'] = '密码长度不能超过20位'
        return msg

    sql = f'''
    update userInfo
    set psword='{new_p}'
    where username='{username}'
    '''
    cursor.execute(sql)
    conn.commit()
    msg['status'] = True
    msg['msg'] = '修改成功'
    return msg

# 查看用户班级信息
def checkUserCLassInfo(username):
    msg = {'have_class' : False}

    # 查找班级
    sql = f'''
    select c_id
    from userInfo
    where username = '{username}'
    '''
    cursor.execute(sql)
    c_id = list(cursor)[0][0]
    if c_id == None:
        return msg
    
    # 查找班级信息
    sql = f'''
    select c_name
    from class_info
    where c_id = {c_id}
    '''
    cursor.execute(sql)
    c_name = list(cursor)[0][0]

    # 查找班级成员
    sql = f'''
    select username, phoneNumber, email, year_, age, job, is_admin
    from userInfo
    where c_id = {c_id}
    '''
    cursor.execute(sql)
    class_info = list(cursor)
    
    #查找班级管理员
    admins = [user[0] for user in class_info if user[-1] == 1]
    admins = ','.join(admins)

    msg['have_class'] = True
    msg['num_students'] = len(class_info)
    msg['class_id'] = c_id
    msg['class_name'] = c_name
    msg['admin'] = admins

    stus = [{'name':stu[0], 
             'contact':stu[1],
             'email' : stu[2],
             'year' : stu[3],
             'age' : stu[4],
             'job' : stu[5]} for stu in class_info]
    msg['students'] = stus
    return msg

# 查看用户是否是管理员
def checkIsAdmin(username):
    sql = f'''
    select is_admin
    from userInfo
    where username = '{username}'
    '''
    cursor.execute(sql)
    res = list(cursor)[0][0]

    if res == 1:
        return True
    else:
        return False

# 查看班级邀请
def checkClassInvitation(username):
    #获取班级名称
    def getClassNameById(id):
        sql = f'''
        select c_name
        from class_info
        where c_id = {id}
        '''
        cursor.execute(sql)
        return list(cursor)[0][0]
    # 获取当前用户的班级
    def getClassNameByUsername(username):
        sql = f'''
        select c_id
        from userInfo
        where username = '{username}'
        '''
        cursor.execute(sql)
        res = list(cursor)[0][0]
        if res == None:
            return ""
        else:
            return getClassNameById(res)
    
    getClassNameByUsername(username)

    sql = f'''
    select inviter, c_id, invite_time, invite_id
    from invite_info
    where invitee = '{username}'
    order by invite_time desc
    '''

    class_name = []

    cursor.execute(sql)
    res = list(cursor)

    invite_info = [{'index':index, 
                    'inviter':info[0], 
                    'class_id':info[1], 
                    'class_name':getClassNameById(info[1]), 
                    'invite_time':info[2],
                    'invite_id': info[3]} 
                    for index, info in enumerate(res)]
    class_name = getClassNameByUsername(username)
    return invite_info, class_name

# 响应班级邀请
def responseClassInvitation(username, invite_id, response):
    # 拒绝邀请
    if response == "refuse":
        sql = f'''
        delete from invite_info
        where invite_id = {invite_id}
        '''
        cursor.execute(sql)
        conn.commit()
    # 接受邀请
    else:
        # 获取班级id
        sql = f'''
        select c_id
        from invite_info
        where invite_id = {invite_id}
        '''
        cursor.execute(sql)
        c_id = list(cursor)[0][0]
        # 删除来自同一班级的邀请
        sql = f'''
        delete from invite_info
        where c_id = {c_id}
        '''
        cursor.execute(sql)
        conn.commit()
        # 加入班级
        sql = f'''
        update userInfo
        set c_id = {c_id}
        where username = '{username}'
        '''
        cursor.execute(sql)
        conn.commit()
    # 更新班级邀请
    return checkClassInvitation(username)

# 退出班级
def quitClass(username):
    sql = f'''
    update userInfo
    set c_id = null, is_admin = false
    where username = '{username}'
    '''
    print(sql)
    cursor.execute(sql)
    # conn.commit()

# 获取用户的班级
def getUserClass(username):
    sql = f'''
    select c_id
    from userInfo
    where username = '{username}'
    '''
    cursor.execute(sql)
    res = list(cursor)[0][0]
    if res == None:
        return ""
    else:
        sql = f'''
        select c_name
        from class_info
        where c_id = {res}
        '''
        cursor.execute(sql)
        return list(cursor)[0][0]

# 搜索班级
def searchClass(username, data, method):
    msg = {'success':False}
    sql = None
    if method == "class_name":
        sql = f'''
        select c_id, c_name
        from class_info
        where c_name = '{data}'
        '''
    else:
        sql = f'''
        select c_id, c_name
        from class_info
        where c_id = {data}
        '''
    cursor.execute(sql)
    res = list(cursor)
    if len(res) == 0:
        return msg
    
    class_info = [{'c_id':info[0],
                   'c_name':info[1]} for info in res]
    msg['success'] = True
    msg['user_class'] = getUserClass(username)
    msg['class_info'] = class_info
    return msg

# 获取时间(字符串格式)
def getTimeString():
    time_ = datetime.datetime.now()
    time_ = str(time_)
    time_ = time_.split(".")
    time_ = str(time_[0])

    return time_

# 申请加入班级
def applyForClass(username, c_id):
    sql = f'''
    insert into application_info (applicant, c_id, apply_time)
    values
        ('{username}', {c_id}, '{getTimeString()}')
    '''
    try:
        cursor.execute(sql)
        conn.commit()
    except:
        print("请勿频繁操作")

# 删除班级成员
def removeClassMember(remove_user, execute_user):
    quitClass(remove_user)
    return checkUserCLassInfo(execute_user)

# 获取班级申请信息
def checkClassApplication(c_id):
    msg = {'is_empty': True}
    # 获取用户邮箱
    def getEmailByUsername(username):
        sql = f'''
        select email
        from userInfo
        where username = '{username}'
        '''
        cursor.execute(sql)
        return list(cursor)[0][0]
    
    sql = f'''
    select apply_id, applicant, apply_time
    from application_info
    where c_id = {c_id}
    order by apply_time desc
    '''
    cursor.execute(sql)
    res = list(cursor)

    if len(res) == 0:
        return msg

    apply_info = [{'apply_id': info[0],
                   'applicant': info[1],
                   'apply_time': info[2],
                   'email': getEmailByUsername(info[1])} for info in res]
    msg['is_empty'] = False
    msg['apply_info'] = apply_info
    return msg

# 处理申请信息
def dealWithClassApplication(apply_id, action):
    # 获取申请者 和申请班级
    sql = f'''
    select applicant, c_id
    from application_info
    where apply_id = {apply_id}
    '''
    cursor.execute(sql)
    applicant, c_id = list(cursor)[0]

    # 拒绝申请
    if action == "reject":
        sql = f'''
        delete from application_info
        where apply_id = {apply_id}
        '''
        cursor.execute(sql)
        conn.commit()
    # 同意申请
    else:
        # 更新用户班级
        sql = f'''
        update userInfo
        set c_id = {c_id}
        where username = '{applicant}'
        '''
        cursor.execute(sql)
        conn.commit()

        # 删除重复申请
        sql = f'''
        delete from application_info
        where applicant = '{applicant}' and c_id = {c_id}
        '''
        cursor.execute(sql)
        conn.commit()
    
    # 获取更新后的班级申请信息
    return checkClassApplication(c_id)

# 获取用户的班级id
def getClassIdByUsername(username):
    sql = f'''
    select c_id
    from userInfo
    where username = '{username}'
    '''
    cursor.execute(sql)
    return list(cursor)[0][0]

# 获取留言的点赞者
def getMessageHailer(msg_id):
    # 获取点赞者
    sql = f'''
    select hail_id, username, hail_time
    from hail_info
    where msg_id = {msg_id}
    order by hail_time desc
    '''
    cursor.execute(sql)
    res = list(cursor)
    if len(res) == 0:
        return ""
    
    hailer = [info[1] for info in res]
    return ",".join(hailer)

# 获取留言的评论
def getMessageComment(msg_id):
    # 获取评论
    sql = f'''
    select comment_id, username, content, comment_time
    from comment_info
    where msg_id = {msg_id}
    order by comment_time desc
    '''
    cursor.execute(sql)
    res = list(cursor)
    comments = [{'comment_id' : info[0],
                 'username' : info[1],
                 'content' : info[2],
                 'comment_time' : info[3]} for info in res]
    return comments

# 获取班级留言
def checkClassMessages(username):
    msg = {'is_empty' : True, 'have_class' : False}
    # 获取用户邮箱
    def getEmailByUsername(username):
        sql = f'''
        select email
        from userInfo
        where username = '{username}'
        '''
        cursor.execute(sql)
        return list(cursor)[0][0]
    # 判断是否被用户点赞过
    def isMsgHailed(username, msg_id):
        sql = f'''
        select hail_id
        from hail_info
        where username='{username}' and msg_id = {msg_id}
        '''
        cursor.execute(sql)
        if len(list(cursor)) == 0:
            return False
        else:
            return True

    c_id = getClassIdByUsername(username)
    if c_id == None:
        return msg
    msg['have_class'] = True
    
    sql = f'''
    select username, content, pub_time, msg_id
    from messages
    where c_id = {c_id}
    order by pub_time desc
    '''
    cursor.execute(sql)
    res = list(cursor)
    if len(res) == 0:
        return msg
    
    msg_info = [{'username' : info[0],
                 'content' : info[1],
                 'date' : info[2],
                 'msg_id' : info[3],
                 'is_hailed' : isMsgHailed(username, info[3]),
                 'email' : getEmailByUsername(info[0],),
                 'hailer' : getMessageHailer(info[3]),
                 'comment' : getMessageComment(info[3])} for info in res]
    msg['is_empty'] = False
    msg['msg_info'] = msg_info
    
    return msg
    
# 获取用户留言
def checkUserMessages(username):
    c_id = getClassIdByUsername(username)

    msg = {'is_empty' : True}
    sql = f'''
    select content, pub_time, msg_id
    from messages
    where c_id = {c_id} and username = '{username}'
    order by pub_time desc
    '''

    cursor.execute(sql)
    res = list(cursor)
    if len(res) == 0:
        return msg

    user_msg = [{'content' : info[0],
                 'date' : info[1],
                 'msg_id' : info[2],
                 'hailer' : getMessageHailer(info[2]),
                 'comment' : getMessageComment(info[2])} for info in res]
    msg['is_empty'] = False
    msg['user_msg'] = user_msg
    return msg

# 删除留言
def deleteMessages(msg_id):
    sql = f'''
    delete from messages
    where msg_id = {msg_id}
    '''
    cursor.execute(sql)
    conn.commit()

# 发布新的留言
def pubMessage(username, content):

    c_id = getClassIdByUsername(username)

    content = content.replace("'", "''")
    sql = f'''
    insert into messages (username, c_id, content, pub_time)
    values
        ('{username}', {c_id}, '{content}', '{getTimeString()}')
    '''
    cursor.execute(sql)
    conn.commit()

# 搜索用户
def searchUser(data, option):
    # 获取班级名称
    def getClassNameById(c_id):

        if c_id == None:
            return ""

        sql = f'''
        select c_name
        from class_info
        where c_id = {c_id}
        '''
        cursor.execute(sql)
        return list(cursor)[0][0]

    msg = {'is_empty' : True}

    sql = None
    if option == 'name':
        sql = f'''
        select username, c_id, phoneNumber
        from userInfo
        where username='{data}'
        '''
    elif option == 'class':
        sql = f'''
        select username, c_id, phoneNumber
        from userInfo
        where c_id in (
            select c_id
            from class_info
            where c_name = '{data}'
        )
        '''
    else:
        sql = f'''
        select username, c_id, phoneNumber
        from userInfo
        where phoneNumber='{data}'
        '''

    cursor.execute(sql)
    res = list(cursor)

    if len(res) == 0:
        return msg
    
    user_info = [{'username' : info[0],
                 'class_name' : getClassNameById(info[1]),
                 'phone' : info[2]} for info in res]

    msg['is_empty'] = False
    msg['user_info'] = user_info
    return msg    

# 留言点赞状态更新
def updateHailStatus(username, msg_id, mode):
    if mode == 'todo':
        sql = f'''
        insert into hail_info (username, msg_id, hail_time)
        values
            ('{username}', {msg_id}, '{getTimeString()}')
        '''
    else:
        sql = f'''
        delete from hail_info
        where username = '{username}' and msg_id = {msg_id}
        '''
    try:
        cursor.execute(sql)
        conn.commit()
    except:
        return

# 提交评论
def sendComment(username, msg_id, content:str):
    content = content.replace("'", "''")
    sql = f'''
    insert into comment_info (username, msg_id, content, comment_time)
    values
        ('{username}', {msg_id}, '{content}', '{getTimeString()}')
    '''
    cursor.execute(sql)
    conn.commit()

# 邀请好友加入班级
def inviteBuddy(inviter, invitee):
    # 查找邀请者的班级
    sql = f'''
    select c_id
    from userInfo
    where username = '{inviter}'
    '''
    cursor.execute(sql)
    c_id = list(cursor)[0][0]

    # 插入邀请信息
    sql = f'''
    insert into invite_info (inviter, c_id, invitee, invite_time)
    values
        ('{inviter}',{c_id}, '{invitee}', '{getTimeString()}')
    '''
    cursor.execute(sql)
    conn.commit()

# 获取班级人数
def getClassMemberNum(c_id):
    sql = f'''
    select count(c_id)
    from userInfo
    where c_id = {c_id}
    '''
    cursor.execute(sql)
    return list(cursor)[0][0]

# 管理员获取所有班级信息
def getAllClassInfo():
    sql = f'''
    select c_id, c_name
    from class_info
    '''
    cursor.execute(sql)
    res = list(cursor)
 
    result = [{'class_id' : info[0],
               'class_name' : info[1],
               'member_num' : getClassMemberNum(info[0])} for info in res]
    return result

# 获取班级中所有用户的信息
def getAllClassUserInfo(c_id):
    sql = f'''
    select username, email, phoneNumber, age, year_, job, is_admin
    from userInfo
    where c_id = {c_id}
    '''
    cursor.execute(sql)
    user_info = [{'username' : info[0],
               'email' : info[1],
               'phone' : info[2],
               'age' : info[3],
               'year' : info[4],
               'job' : info[5],
               'is_admin' : info[6]} for info in list(cursor)]
    result = {'user_info' : user_info}
    return result

# 管理员更新用户身份
def updateUserIdentity(username, response):
    if response == '0':
        new_id = 1
    else:
        new_id = 0
    sql = f'''
    update userInfo
    set is_admin = {new_id}
    where username = '{username}'
    '''
    cursor.execute(sql)
    conn.commit()

# 管理员移除班级成员
def removeClassMemberByAdmin(username):
    sql = f'''
    update userInfo
    set is_admin = 0, c_id = null
    where username = '{username}'
    '''
    cursor.execute(sql)
    conn.commit()

# 获取所有用户的信息
def getAllUserInfo():
    def getClassName(c_id):
        if c_id == None:
            return ""
        sql = f'''
        select c_name
        from class_info
        where c_id = {c_id}
        '''
        cursor.execute(sql)
        return list(cursor)[0][0]

    sql = f'''
    select username, email, phoneNumber, age, job, year_, c_id
    from userInfo
    '''
    cursor.execute(sql)

    result = [{'username' : info[0],
               'email' : info[1],
               'phone' : info[2],
               'age' : info[3],
               'job' : info[4],
               'year' : info[5],
               'class_id' : info[6],
               'class_name' : getClassName(info[6])} for info in list(cursor)]
    return result

# 重置用户密码
def resetUserPassword(username):
    sql = f'''
    update userInfo
    set psword = '88888888'
    where username = '{username}'
    '''
    cursor.execute(sql)
    conn.commit()

# 更新用户班级
def updateUserClass(username, class_id):
    sql = f'''
    update userInfo
    set c_id = {class_id}, is_admin = 0
    where username = '{username}'
    '''
    cursor.execute(sql)
    conn.commit()

# 注销用户
def distoryUser(username):
    sql = f'''
    delete from userInfo
    where username = '{username}'
    '''
    cursor.execute(sql)
    conn.commit()

# 创建班级
def create_class(class_name):
    sql = f'''
    insert into class_info (c_name)
    values
        ('{class_name}')
    '''
    cursor.execute(sql)
    conn.commit()

    sql = '''
    select max(c_id)
    from class_info
    '''
    cursor.execute(sql)
    return list(cursor)[0][0]

if __name__ == "__main__":
    data = checkClassInvitation('a')
    print(data)