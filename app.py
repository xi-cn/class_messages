from flask import Flask, request, render_template,redirect, url_for,session, jsonify
import dbConn


app = Flask(__name__)

#启用客户端会话  安全 方便数据传递
app.secret_key = 'communication'

# 根目录  打开登录页面
@app.route('/')
def index():
    return render_template('main_page.html')


# 主页跳转 用户登录
@app.route('/user_login')
def to_user_login():
    return render_template('user_login.html')


# 主页跳转 管理员登录
@app.route('/admin_login')
def to_admin_login():
    return render_template('admin_login.html')

#主页跳转   用户注册
@app.route('/register')
def to_register():
    return render_template('register.html')

# 用户登录
@app.route('/user_login',methods=['POST','GET'])
def user_login():

    if request.method == 'POST':
        username=request.form['username']
        password=request.form['password']
    else:
        username=request.args['username']
        password=request.args['password']

    res = dbConn.checkLogin(username, password)
    if res['status'] == False:
        return render_template('user_login.html',message=res['msg'])
    else:
        session['username'] = username
        user_info = dbConn.getUserInfo(username)
        session['user_info'] = user_info
        return render_template('user_success.html', user_info=user_info)

# 管理员登录
@app.route('/admin_login')
def admin_login():
    if request.method=='POST':
        id=request.form['username']
        pw=request.form['password']
        # 这两个是从前端传来的 用户名和 数据  
        # 这里后端代码略  此处是登录功能
        # 此处应该能判断 是否成功登录 成功跳转至成功页面 否则重新回到登陆页面并告诉错误理由
        info=[] 
        return render_template('admin_login.html',message="管理员不存在！再试试吧")
        return render_template('admin_login.html',"密码错误，再试一次吧！")
        return render_template('admin_success.html',info=info) 

            #  注册函数  注册完跳转用户登录页面

# 用户注册
@app.route('/register',methods=['POST','GET'])
def register():
    if request.method=='POST':
        register_info=request.form
        res = dbConn.registerNewUser(register_info)
        if res['status'] == True:
            return render_template('user_login.html',message=res['msg'])
        else:
            return render_template('user_login.html',message=res['msg'])
    
# 返回个人主页
@app.route('/return_userinfo', methods=['POST','GET'])
def return_userinfo():
    if session.get('username') == None:
        return render_template('main_page.html')

    return render_template('user_success.html', user_info=session['user_info'])

# 前往修改信息页面
@app.route('/to_change_info', methods=['POST','GET'])
def to_change_info():
    if session.get('username') == None:
        return render_template('main_page.html')

    return render_template('change_info.html', user_info=session['user_info'])

# 修改用户信息
@app.route('/change_info',methods=['POST','GET'])
def change_info():
    # 未登录则返回主页面
    if session.get('username') == None:
        return render_template('main_page.html')
    username = session.get('username')

    if request.method=='POST':
        data = request.form
    else:
        data = request.args

    res = dbConn.modifyUserInfo(username, data)
    if res['status'] == False:
        return render_template('change_info.html',message=res['msg'],user_info=session['user_info'])
    else:
        #更新session
        user_info = dbConn.getUserInfo(username)
        session['user_info'] = user_info
        return render_template('change_info.html',message=res['msg'],user_info=user_info)

# 前往修改密码页面 
@app.route('/to_change_password',methods=['POST','GET'])
def to_change_password():
    # 未登录则返回主页面
    if session.get('username') == None:
        return render_template('main_page.html')
    username = session.get('username')

    return render_template('change_password.html',username=username)

# 修改密码
@app.route('/change_password',methods=['POST','GET'])
def change_password():
    # 未登录则返回主页面
    if session.get('username') == None:
        return render_template('main_page.html')
    username = session.get('username')

    if request.method=='POST':
        data = request.form
    else:
        data = request.args

    msg = dbConn.modifyPassword(username, data)
        
    if msg['status'] == False:
        return render_template('change_password.html', message=msg['msg'])
    else:
        return render_template('user_login.html',message="密码已修改，请重新登录")

# 前往班级信息页面
@app.route('/to_class_info',methods=['POST','GET'])
def to_class_info():
    # 未登录则返回主页面
    if session.get('username') == None:
        return render_template('main_page.html')
    username = session.get('username')

    # 找到该用户的班级信息
    class_data = dbConn.checkUserCLassInfo(username)
    # 判断用户是否是管理员
    is_admin = dbConn.checkIsAdmin(username)

    return render_template('class_info.html',class_data=class_data,username=username,is_admin=is_admin)

# 切换到班级邀请界面
@app.route('/to_invitation',methods=['POST','GET'])
def to_invitation():
    # 未登录则返回主页面
    if session.get('username') == None:
        return render_template('main_page.html')
    username = session.get('username')

    invite_info, class_name = dbConn.checkClassInvitation(username)
    return render_template("class_invitation.html", invite_info=invite_info, class_name=class_name)

#响应邀请
@app.route("/response_invitation", methods=['POST','GET'])
def response_invitation():
    # 未登录则返回主页面
    if session.get('username') == None:
        return render_template('main_page.html')
    username = session.get('username')

    if request.method == 'POST':
        response = request.form.get("response")
        invite_id = request.form.get("invite_id")
    else:
        response = request.args.get("response")
        invite_id = request.args.get("invite_id")

    invite_info, class_name = dbConn.responseClassInvitation(username, invite_id, response)
    return render_template("class_invitation.html", invite_info=invite_info, class_name=class_name)

# 切换到搜索班级界面
@app.route('/to_search_class', methods=['POST','GET'])
def to_search_class():
    # 未登录则返回主页面
    if session.get('username') == None:
        return render_template('main_page.html')

    return render_template("search_class.html")
    
# 搜索班级
@app.route('/search_class', methods=['POST','GET'])
def search_class():
    # 未登录则返回主页面
    if session.get('username') == None:
        return render_template('main_page.html')
    username = session.get('username')

    if request.method == 'POST':
        data = request.form.get("query")
        method = request.form.get("category")
    else:
        data = request.args.get("query")
        method = request.args.get("category")

    res = dbConn.searchClass(username, data, method)
    return render_template("search_class.html", result=res)

# 申请加入班级
@app.route('/apply_class', methods=['POST','GET'])
def apply_class():
    # 未登录则返回主页面
    if session.get('username') == None:
        return render_template('main_page.html')
    username = session.get('username')

    if request.method == 'POST':
        c_id = request.form.get("c_id")
    else:
        c_id = request.args.get("c_id")

    dbConn.applyForClass(username, c_id)
    return render_template("search_class.html")

#退出班级
@app.route('/out_class', methods=['POST','GET'])
def out_class():
    # 未登录则返回主页面
    if session.get('username') == None:
        return render_template('main_page.html')
    username = session.get('username')

    # 退出班级
    dbConn.quitClass(username)
    return render_template('user_success.html',user_info=session['user_info'])

# 前往管理班级页面
@app.route('/to_admin_class', methods=['POST','GET'])
def to_admin_class():
    # 未登录则返回主页面
    if session.get('username') == None:
        return render_template('main_page.html')
    username = session.get('username')

    class_data = dbConn.checkUserCLassInfo(username)
    return render_template('admin_class.html',class_data=class_data)

# 前往处理申请页面
@app.route('/to_handle_apply', methods=['POST','GET'])
def to_handle_apply():
    # 未登录则返回主页面
    if session.get('username') == None:
        return render_template('main_page.html')
    
    username = session.get('username')
    if request.method == 'POST':
        class_id=request.form.get('class_id')
    else:
        class_id=request.args.get('class_id')
    
    result = dbConn.checkClassApplication(class_id)
    return render_template('handle_applicants.html',username=username,result=result)

# 处理申请
@app.route('/response_application', methods=['POST','GET'])
def response_application():
    # 未登录则返回主页面
    if session.get('username') == None:
        return render_template('main_page.html')
    username = session.get('username')

    if request.method == 'POST':
        response = request.form.get("action")
        apply_id = request.form.get("apply_id")
    else:
        response = request.args.get("action")
        apply_id = request.args.get("apply_id")
    result = dbConn.dealWithClassApplication(apply_id, response)
    return render_template('handle_applicants.html',username=username,result=result)

# 移除班级成员
@app.route('/remove_member', methods=['POST','GET'])
def remove_member():
    # 未登录则返回主页面
    if session.get('username') == None:
        return render_template('main_page.html')
    
    execute_user = session.get('username')
    remove_user = request.json.get("member_name")

    class_data = dbConn.removeClassMember(remove_user, execute_user)
    return render_template('admin_class.html',class_data=class_data)

# 前往留言页面
@app.route('/to_messages', methods=['POST','GET'])
def to_messages():
    # 未登录则返回主页面
    if session.get('username') == None:
        return render_template('main_page.html')
    
    username = session.get('username')
    result = dbConn.checkClassMessages(username)
    is_admin = dbConn.checkIsAdmin(username)
    result['is_admin'] = is_admin

    return render_template('messages.html',username=username,result=result)

# 前往我的留言
@app.route('/to_my_messages', methods=['POST','GET'])
def to_my_messages():
    # 未登录则返回主页面
    if session.get('username') == None:
        return render_template('main_page.html')
    username = session.get('username')
    result = dbConn.checkUserMessages(username)

    return render_template('my_messages.html',username=username,result=result)

# 删除个人留言
@app.route('/delete_my_message', methods=['POST','GET'])
def delete_my_message():
    # 未登录则返回主页面
    if session.get('username') == None:
        return render_template('main_page.html')
    username = session.get('username')

    if request.args == 'POST':
        msg_id=request.form.get('msg_id')
    else:
        msg_id=request.args.get('msg_id')

    dbConn.deleteMessages(msg_id)
    result = dbConn.checkUserMessages(username)

    return render_template('my_messages.html',username=username,result=result)

# 前往新留言页面
@app.route('/to_new_message', methods=['POST','GET'])
def to_new_message():
    # 未登录则返回主页面
    if session.get('username') == None:
        return render_template('main_page.html')
    username = session.get('username')

    return render_template('new_message.html',username=username)

# 发布新的留言
@app.route('/pub_message', methods=['POST','GET'])
def pub_message():
    # 未登录则返回主页面
    if session.get('username') == None:
        return render_template('main_page.html')
    username = session.get('username')

    if request.form == 'POST':
        content = request.form.get('content')
    else:
        content = request.args.get('content')

    dbConn.pubMessage(username, content)
    return render_template('new_message.html',username=username)

# 删除班级留言
@app.route('/delete_class_message', methods=['POST','GET'])
def delete_class_message():
    # 未登录则返回主页面
    if session.get('username') == None:
        return render_template('main_page.html')
    username = session.get('username')

    if request.method == 'POST':
        msg_id = request.form.get('msg_id')
    else:
        msg_id = request.args.get('msg_id')
    dbConn.deleteMessages(msg_id)
    result = dbConn.checkClassMessages(username)
    is_admin = dbConn.checkIsAdmin(username)
    result['is_admin'] = is_admin
    return render_template('messages.html',result=result,username=username)

# 前往搜索用户页面
@app.route('/to_search_user',methods=['POST','GET'])
def to_search_user():
    # 未登录则返回主页面
    if session.get('username') == None:
        return render_template('main_page.html')
    username = session.get('username')

    return render_template('search_user.html',username=username)

# 搜索用户
@app.route('/search_user',methods=['POST','GET'])
def search_user():
    # 未登录则返回主页面
    if session.get('username') == None:
        return render_template('main_page.html')
    username = session.get('username')

    if request.method == 'POST':
        option = request.form.get("category")
        data = request.form.get('query')
    else:
        option = request.args.get("category")
        data = request.args.get('query')

    result = dbConn.searchUser(data, option)
    is_admin = dbConn.checkIsAdmin(username)
    return render_template('search_user.html',result=result,is_admin=is_admin)

# 更新点赞信息
@app.route('/update_hail_status', methods=['POST', 'GET'])
def update_hail_status():
    # 未登录则返回主页面
    if session.get('username') == None:
        return render_template('main_page.html')
    username = session.get('username')

    mode = request.json.get('mode')  
    msg_id = request.json.get('msg_id')
    
    dbConn.updateHailStatus(username, msg_id, mode)
    return jsonify({'status': 'success'})

# 提交评论信息
@app.route('/send_comment', methods=['POST', 'GET'])
def send_comment():
    # 未登录则返回主页面
    if session.get('username') == None:
        return render_template('main_page.html')
    username = session.get('username')

    content = request.json.get('content')
    msg_id = request.json.get('msg_id')
    dbConn.sendComment(username, msg_id, content)
    return jsonify({'status': 'success'})

# 邀请好友加入班级
@app.route('/invite_buddy', methods=['POST', 'GET'])
def invite_buddy():
    # 未登录则返回主页面
    if session.get('username') == None:
        return render_template('main_page.html')
    inviter = session.get('username')
    if request.method == 'POST':
        invitee = request.form.get('invitee')
    else:
        invitee = request.args.get('invitee')
    
    dbConn.inviteBuddy(inviter, invitee)
    return render_template('search_user.html',username=inviter)
    
# 退出登录
@app.route('/exit', methods=['POST', 'GET'])
def exit():
    session['username'] = None
    return render_template('main_page.html')


if __name__ == '__main__':
    app.run(debug=True)

    