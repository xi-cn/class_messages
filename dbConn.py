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

    sql = f'''select username, email, phoneNumber, age, job, year_, c_id, is_admin, psword
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
        msg['msg'] = '登录成功！'
        msg['info'] = list(res[0])
        return msg

#获取用户信息
def getUserInfo(uesrname):
    sql = f'''
    select username, email, phoneNumber, age, job, year_, psword
    from userInfo
    where username = '{uesrname}'
    '''
    res = cursor.execute(sql)
    return list(res[0])

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
def modifyPassword(changeInfo, last_p):
    msg = {'status':False, "msg":''}

    user_name = changeInfo['user']
    psword=changeInfo['last_password'] 
    new_p=changeInfo['new_password']
    confirm_p=changeInfo['confirm_password']    

    if not new_p == confirm_p:
        msg['msg'] = "新密码不一致"
        return msg
    if not last_p == psword:
        msg['msg'] = "原密码输入错误"
        return msg
    #非法密码
    elif len(psword) > 20:
        msg['msg'] = '密码长度不能超过20位'
        return msg

    sql = f'''
    update userInfo
    set psword='{new_p}'
    where username='{user_name}'
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
    select username, phoneNumber, is_admin
    from userInfo
    where c_id = {c_id}
    '''
    cursor.execute(sql)
    class_info = list(cursor)
    
    #查找班级管理员
    admins = [user[0] for user in class_info if user[2] == 1]
    admins = ','.join(admins)

    msg['have_class'] = True
    msg['num_students'] = len(class_info)
    msg['class_id'] = c_id
    msg['class_name'] = c_name
    msg['admin'] = admins

    stus = [{'name':stu[0], 'contact':stu[1]} for stu in class_info]
    msg['students'] = stus
    return msg

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

    return invite_info

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
        print(sql)
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
    cursor.execute(sql)
    conn.commit()

# 搜索班级
def searchClass(data, method):
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

# 获取班级留言
def checkClassMessages(c_id):
    # 获取用户邮箱
    def getEmailByUsername(username):
        sql = f'''
        select email
        from userInfo
        where username = '{username}'
        '''
        cursor.execute(sql)
        return list(cursor)[0][0]

    msg = {'is_empty' : True}
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
                 'email' : getEmailByUsername(info[0])} for info in res]
    msg['is_empty'] = False
    msg['msg_info'] = msg_info
    
    return msg_info
    
# 获取用户留言
def checkUserMessages(username, c_id):
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
                 'msg_id' : info[2]} for info in res]
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
def pubMessage(username, c_id, content):
    content = content.replace("'", "''")
    sql = f'''
    insert into messages (username, c_id, content, pub_time)
    values
        ('{username}', {c_id}, '{content}', '{getTimeString()}')
    '''
    print(sql)
    cursor.execute(sql)
    conn.commit()

if __name__ == "__main__":
    data = checkUserMessages('ww', 1)
    print(data)