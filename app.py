from flask import Flask, request, render_template,redirect, url_for,session
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

@app.route('/user_login',methods=['POST','GET'])
def user_login():
    if request.method=='POST':
        id=request.form['username']
        pw=request.form['password']
        res = dbConn.checkLogin(id, pw)
        if res['status'] == False:
            return render_template('user_login.html',message=res['msg'])
        else:
            session['info'] = res['info']
            return render_template('user_success.html',message=res['msg'],info=res['info'])

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

@app.route('/register',methods=['POST','GET'])
def register():
    if request.method=='POST':
        register_info=request.form
        res = dbConn.registerNewUser(register_info)
        if res['status'] == True:
            return render_template('user_login.html',message=res['msg'])
        else:
            return render_template('user_login.html',message=res['msg'])
    
#手上有全部信息  回到个人主页
@app.route('/return_userinfo')
def return_userinfo():
    info=session.get('info')
    return render_template('user_success.html',info=info)  

#手上只有用户名 先检索到个人信息 再返回  因为回到个人主页需要拿到全部信息
@app.route('/return_userinfo2')
def return_userinfo2():
    username=request.args.get('username')
    #找到个人信息给 user
    user=['用户名','邮箱','电话号码','年龄','工作','入学年份','密码'] 
    return render_template('user_success.html',info=user)


#修改信息路由操作
@app.route('/to_change_info')
def to_change_info():
    return render_template('change_info.html',message="请查看要修改的信息！",user=session['info'])

@app.route('/change_info',methods=['POST','GET'])
def change_info():
    if request.method=='POST':
        res = dbConn.modifyUserInfo(session['info'][0], request.form)
        if res['status'] == False:
            return render_template('change_info.html',message=res['msg'],user=session['info'])
            
        # ...
        else:
            #更新session
            info = [request.form['username'], request.form['email'], request.form['phone'], 
                    request.form['age'], request.form['job'], request.form['year'], session['info'][-1]]
            session['info'] = info
            return render_template('change_info.html',message=res['msg'],user=session['info'])

#修改密码操作 
@app.route('/to_change_password')
def to_change_password():
    username = session['info'][0]
    return render_template('change_password.html',user=username)

@app.route('/change_password',methods=['POST','GET'])
def change_password():
    if request.method=='POST':
        msg = dbConn.modifyPassword(request.form, session['info'][-1])
        
        if msg['status'] == False:
            return render_template('change_password.html', message=msg['msg'], user=request.form['user'])
        else:
            return render_template('user_login.html',message="密码已修改，请重新登录")


#查看班级信息路由操作
@app.route('/to_class_info')
def to_class_info():
    username=session['info'][0]
    #这里找到该用户的班级信息
    class_data = dbConn.checkUserCLassInfo(username)
    return render_template('class_info.html',class_data=class_data,username=username,is_admin=session['info'][-2])

#切换到班级邀请界面
@app.route('/to_invitation')
def to_invitation():
    username = session['info'][0]
    invite_info = dbConn.checkClassInvitation(username)
    return render_template("class_invitation.html", invite_info=invite_info)

#响应邀请
@app.route("/response_invitation", methods=['POST'])
def response_invitation():
    response = request.form.get("response")
    invite_id = request.form.get("invite_id")
    username = session['info'][0]
    invite_info = dbConn.responseClassInvitation(username, invite_id, response)
    return render_template("class_invitation.html", invite_info=invite_info)

# 切换到搜索班级界面
@app.route('/to_search_class')
def to_search_class():
    return render_template("search_class.html")
    

# 搜索班级
@app.route('/search_class')
def search_class():
    data = request.args.get("query")
    method = request.args.get("category")
    res = dbConn.searchClass(data, method)
    return render_template("search_class.html", result=res)

# 申请加入班级
@app.route('/apply_class', methods=['POST'])
def apply_class():
    username = session['info'][0]
    c_id = request.form.get("c_id")
    dbConn.applyForClass(username, c_id)
    return render_template("search_class.html")

#退出班级
@app.route('/outclass')
def out_class():
    username=session['info'][0]
    info = session['info']
    dbConn.quitClass(username)
    return render_template('user_success.html',info=info)


# 管理班级
@app.route('/to_admin_class')
def to_admin_class():
    username=session['info'][0]
    class_data = dbConn.checkUserCLassInfo(username)
    return render_template('admin_class.html',class_data=class_data,username=username)


@app.route('/to_handle_apply')
def to_handle_apply():
    class_id=request.args.get('class_id')
    username=request.args.get('username')
    #这边检索到申请信息
    # 假设是 apply
    apply = {
    'class_applicants': [
        {'id': 1, 'name': 'Applicant 1', 'contact': 'applicant1@example.com'},
        {'id': 2, 'name': 'Applicant 2', 'contact': 'applicant2@example.com'},
        # 其他申请者...
    ]
}
    return render_template('handle_applicants.html',class_id=class_id,username=username,apply=apply,message="请处理以下信息")

@app.route('/approve_application')
def approve_application():
    new_id=request.args.get('apply_id')
    #同意申请
    class_id=request.args.get('class_id')
    #这边检索新的申请班级信息
    apply = {
    'class_applicants': [
        {'id': 1, 'name': 'Applicant 1', 'contact': 'applicant1@example.com'},
        # 其他申请者...
    ]
}
    username=request.args.get('username')
    return render_template('handle_applicants.html',class_id=class_id,username=username,apply=apply,message="处理成功")

@app.route('/reject_application')
def reject_application():
    new_id=request.args.get('apply_id')
    #拒绝申请
    class_id=request.args.get('class_id')
    #这边检索新的申请班级信息
    apply = {
    'class_applicants': [
        {'id': 1, 'name': 'Applicant 1', 'contact': 'applicant1@example.com'},
        # 其他申请者...
    ]
}
    username=request.args.get('username')
    return render_template('handle_applicants.html',class_id=class_id,username=username,apply=apply,message="处理成功")

# 移除操作
@app.route('/remove_member')
def remove_member():
    remove_user = request.args.get("member_name")
    execute_user = session['info'][0]

    class_data = dbConn.removeClassMember(remove_user, execute_user)

    return render_template('admin_class.html',class_data=class_data)


#留言页面
@app.route('/to_messages')
def to_messages():
    username=request.args.get('username')
    messages = [
    {
        'username': 'zhangsan',
        'contact': 'zhangsan@example.com',
        'content': '很高兴能和大家保持联系，希望以后多多交流！'
    },
    {
        'username': 'lisi',
        'contact': 'lisi@example.com',
        'content': '回想起在校的日子，真是令人怀念。期待下次校友聚会。'
    },
    {
        'username': 'wangwu',
        'contact': 'wangwu@example.com',
        'content': '希望大家在各自的工作岗位上都能取得成功。'
    },
    {
        'username': 'zhaoliu',
        'contact': 'zhaoliu@example.com',
        'content': '感谢母校的培养，愿母校越办越好。'
    },
    {
        'username': 'sunqi',
        'contact': 'sunqi@example.com',
        'content': '大家好，我是孙七，很高兴认识大家！'
    }
]
    return render_template('messages.html',username=username,messages=messages)

@app.route('/to_my_messages')
def to_my_messages():
    username=request.args.get('username')
    my_messages = [
        {
            'id':1,
            'title': '第一条消息标题',
            'date': '2024-06-30',
            'content': '这是第一条消息的内容。'
        },
        {
            'id':2,
            'title': '第二条消息标题',
            'date': '2024-06-29',
            'content': '这是第二条消息的内容。'
        },
        # Add more messages as needed
    ]

    return render_template('my_messages.html',username=username,my_messages=my_messages)

@app.route('/delete_my_message')
def delete_my_message():
    username=request.args.get('username')
    delete_id=request.args.get('message_id')
    my_messages = [
        {
            'id':1,
            'title': '第一条消息标题',
            'date': '2024-06-30',
            'content': '这是删除后，我的消息内容。'
        },
   
        # Add more messages as needed
    ]

    return render_template('my_messages.html',message="删除成功",username=username,my_messages=my_messages)
   

@app.route('/to_search_user',methods=['POST','GET'])
def to_search_user():
    username=request.args.get('username')
    # 这边根据上面两条信息检索用户
    search_results= [     ]
    return render_template('search_user.html',username=username,search_results=search_results)

@app.route('/search_user',methods=['POST','GET'])
def search_user():
    if request.method=='GET':
        query = request.args.get('query') #获取检索类型  班级  姓名 还是入学时间
        category = request.args.get('category')   #对应类型的值
        username=request.args.get('username')
        # 这边根据上面两条信息检索用户
        search_results= [
    {'name': '张三',  'contact': 123}]
        return render_template('search_user.html',message="搜索结果如下：",username=username,search_results=search_results)





if __name__ == '__main__':
    app.run(debug=True)

    