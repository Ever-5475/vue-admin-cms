from flask import Flask, jsonify, request
import jwt
import pymysql
import logging
from datetime import datetime, timedelta
from functools import wraps
from config import Config
from models import init_db, User, Article, Comment

app = Flask(__name__)
app.config.from_object(Config)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

init_db()

@app.errorhandler(Exception)
def handle_error(error):
    logger.error(f'Server error: {str(error)}')
    return jsonify({'code': 50000, 'message': '服务器内部错误'}), 500

def generate_token(user_id, role):
    payload = {
        'user_id': user_id,
        'role': role,
        'exp': datetime.utcnow() + timedelta(hours=Config.JWT_EXPIRATION_HOURS)
    }
    return jwt.encode(payload, Config.JWT_SECRET_KEY, algorithm='HS256')

def decode_token(token):
    try:
        payload = jwt.decode(token, Config.JWT_SECRET_KEY, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('X-Token')
        if not token:
            return jsonify({'code': 40001, 'message': 'Token is missing'}), 401

        payload = decode_token(token)
        if not payload:
            return jsonify({'code': 40002, 'message': 'Token is invalid or expired'}), 401

        return f(payload, *args, **kwargs)
    return decorated

def admin_required(f):
    """仅管理员可访问的接口装饰器"""
    @wraps(f)
    def decorated(payload, *args, **kwargs):
        if not payload or payload.get('role') != 'admin':
            return jsonify({'code': 40003, 'message': '权限不足，仅管理员可操作'}), 403
        return f(payload, *args, **kwargs)
    return decorated

def _get_current_user_info(payload):
    """从 token 获取当前用户完整信息"""
    if not payload or not payload.get('user_id'):
        return None
    return User.find_by_id(payload['user_id'])


@app.route('/vue-admin-template/user/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'code': 50000, 'message': '请求数据不能为空'})

        username = data.get('username', '').strip() if data.get('username') else ''
        password = data.get('password', '').strip() if data.get('password') else ''

        logger.info(f'🔐 登录尝试 - 用户名:"{username}", 密码长度:{len(password)}')

        if not username or not password:
            return jsonify({'code': 50000, 'message': '用户名和密码不能为空'})

        user = User.find_by_username(username)

        if user and user['password'] == password:
            token = generate_token(user['id'], user['role'])
            logger.info(f'✅ 用户 {username} (ID:{user["id"]}) 登录成功')
            return jsonify({
                'code': 20000,
                'data': {
                    'token': token
                }
            })
        else:
            logger.warning(f'❌ 登录失败 - 用户名: "{username}", 用户存在: {user is not None}')
            return jsonify({'code': 50000, 'message': '用户名或密码错误'}), 401
    except Exception as e:
        logger.error(f'❌ 登录异常: {str(e)}')
        import traceback
        logger.error(f'❌ 详细堆栈:\n{traceback.format_exc()}')
        return jsonify({'code': 50000, 'message': f'登录失败: {str(e)}'}), 500

@app.route('/vue-admin-template/user/info', methods=['GET'])
@token_required
def get_user_info(payload):
    user = User.find_by_id(payload['user_id'])
    if user:
        return jsonify({
            'code': 20000,
            'data': {
                'roles': [user['role']],
                'name': user['name'],
                'avatar': user['avatar']
            }
        })
    return jsonify({'code': 50000, 'message': '用户不存在'})

@app.route('/vue-admin-template/user/logout', methods=['POST'])
def logout():
    return jsonify({'code': 20000, 'data': 'success'})

@app.route('/vue-admin-template/user/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    name = data.get('name')

    if User.find_by_username(username):
        return jsonify({'code': 50001, 'message': '用户名已存在'})

    if name and User.find_by_name(name):
        return jsonify({'code': 50001, 'message': '该姓名已被其他用户使用'})

    user_id = User.create(username, password, 'user', name)
    token = generate_token(user_id, 'user')

    return jsonify({
        'code': 20000,
        'data': {
            'token': token
        }
    })

@app.route('/vue-admin-template/table/list', methods=['GET'])
@token_required
def get_table_list(payload):
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 10))

    result = Article.get_all(page, limit)
    return jsonify({
        'code': 20000,
        'data': result
    })

@app.route('/vue-admin-template/table/create', methods=['POST'])
@token_required
def create_article(payload):
    try:
        data = request.get_json()
        title = data.get('title')
        author = data.get('author')
        pageviews = data.get('pageviews', 0)
        status = data.get('status', 'draft')
        content = data.get('content', '')

        # 获取当前用户信息
        current_user = _get_current_user_info(payload)
        user_role = payload.get('role') if payload else 'user'

        # 普通用户只能使用自己的姓名作为作者
        if user_role != 'admin':
            if current_user:
                author = current_user.get('name') or current_user.get('username')
            else:
                return jsonify({'code': 40003, 'message': '无法获取用户信息'})
        elif not author:
            return jsonify({'code': 50002, 'message': '作者不能为空'})

        # 处理display_time字段（兼容多种格式）
        display_time_raw = data.get('display_time')
        display_time = None

        # 获取当前用户信息，普通用户只能使用自己的姓名
        current_user = _get_current_user_info(payload)
        user_role = payload.get('role') if payload else 'user'
        if user_role != 'admin':
            if current_user:
                data['author'] = current_user.get('name') or current_user.get('username')
            else:
                return jsonify({'code': 40003, 'message': '无法获取用户信息'})

        if display_time_raw is not None and display_time_raw != '' and str(display_time_raw).lower() != 'null':
            parsed_date = None
            formats = [
                '%Y-%m-%dT%H:%M:%S.%fZ',
                '%Y-%m-%dT%H:%M:%SZ',
                '%Y-%m-%dT%H:%M:%S.%f',
                '%Y-%m-%dT%H:%M:%S',
                '%Y-%m-%d %H:%M:%S',
                '%Y-%m-%d'
            ]
            for fmt in formats:
                try:
                    parsed_date = datetime.strptime(str(display_time_raw), fmt)
                    break
                except ValueError:
                    continue

            if parsed_date:
                display_time = parsed_date.strftime('%Y-%m-%d %H:%M:%S')
            else:
                logger.warning(f'⚠️ 无法解析日期格式，使用当前时间: {display_time_raw}')
                display_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        if not title or not author:
            return jsonify({'code': 50002, 'message': '标题和作者不能为空'})

        article_id = Article.create(title=title, author=author, pageviews=pageviews, status=status, content=content, display_time=display_time)
        logger.info(f'✅ 新建文章成功 - ID:{article_id}, 标题:{title}, 作者:{author} [已写入MySQL]')

        return jsonify({
            'code': 20000,
            'data': {
                'id': article_id
            }
        })
    except Exception as e:
        logger.error(f'❌ 新建文章失败: {str(e)}')
        return jsonify({'code': 50000, 'message': '新建文章失败'}), 500

@app.route('/vue-admin-template/table/update', methods=['POST'])
@token_required
def update_article(payload):
    try:
        data = request.get_json()
        logger.info(f'📝 收到更新文章请求: {data}')

        article_id = data.get('id')

        if not article_id:
            logger.warning('⚠️ 文章ID为空')
            return jsonify({'code': 50003, 'message': '文章ID不能为空'})

        article = Article.get_by_id(article_id)
        if not article:
            logger.warning(f'⚠️ 文章不存在: ID={article_id}')
            return jsonify({'code': 50004, 'message': '文章不存在'})

        # 处理display_time字段（兼容多种格式）
        display_time_raw = data.get('display_time')
        display_time = None

        if display_time_raw is not None and display_time_raw != '' and str(display_time_raw).lower() != 'null':
            # 尝试解析各种日期格式
            date_formats = [
                '%a, %d %b %Y %H:%M:%S GMT',   # HTTP Date: "Tue, 31 Dec 2024 23:59:59 GMT"
                '%Y-%m-%dT%H:%M:%S.%fZ',         # ISO 8601 with ms
                '%Y-%m-%dT%H:%M:%SZ',             # ISO 8601
                '%Y-%m-%d %H:%M:%S',              # Standard SQL: "2024-12-31 23:59:59"
                '%Y-%m-%d',                       # Date only: "2024-12-31"
                '%m/%d/%Y %H:%M:%S',              # US format: "12/31/2024 23:59:59"
                '%m/%d/%Y',                       # US date only: "12/31/2024"
            ]

            parsed_date = None
            for fmt in date_formats:
                try:
                    parsed_date = datetime.strptime(str(display_time_raw), fmt)
                    break
                except ValueError:
                    continue

            if parsed_date:
                display_time = parsed_date.strftime('%Y-%m-%d %H:%M:%S')
                logger.info(f'✅ 日期格式转换成功: "{display_time_raw}" → "{display_time}"')
            else:
                logger.warning(f'⚠️ 无法解析日期格式，使用原始值: {display_time_raw}')
                display_time = str(display_time_raw)  # 如果无法解析，尝试直接使用（可能数据库能处理）
        else:
            logger.info(f'📅 时间字段为空/None，将保持不变')

        # 执行更新
        result = Article.update(
            article_id,
            title=data.get('title'),
            author=data.get('author'),
            pageviews=data.get('pageviews'),
            status=data.get('status'),
            content=data.get('content'),
            display_time=display_time
        )

        if result:
            logger.info(f'✅ 更新文章成功 - ID:{article_id}, 新标题:{data.get("title")} [已更新MySQL]')
            return jsonify({'code': 20000, 'data': 'success'})
        else:
            logger.error(f'❌ 更新文章失败 - 数据库返回None')
            return jsonify({'code': 50005, 'message': '更新操作未生效'}), 500

    except Exception as e:
        logger.error(f'❌ 更新文章异常: {str(e)}')
        import traceback
        logger.error(f'❌ 详细堆栈: {traceback.format_exc()}')
        return jsonify({'code': 50000, 'message': f'更新文章失败: {str(e)}'}), 500

@app.route('/vue-admin-template/table/delete', methods=['POST'])
@token_required
def delete_article(payload):
    try:
        data = request.get_json()
        article_id = data.get('id')

        if not article_id:
            return jsonify({'code': 50003, 'message': '文章ID不能为空'})

        article = Article.get_by_id(article_id)
        if not article:
            return jsonify({'code': 50004, 'message': '文章不存在'})

        current_user = _get_current_user_info(payload)
        user_role = payload.get('role') if payload else 'user'
        is_admin = user_role == 'admin'
        is_author = bool(current_user and article.get('author') and (current_user.get('name') == article.get('author') or current_user.get('username') == article.get('author')))
        if not is_admin and not is_author:
            return jsonify({'code': 40003, 'message': '无权删除此文章（仅管理员或文章作者可操作）'}), 403

        if Article.delete(article_id):
            logger.info(f'✅ 删除文章成功 - ID:{article_id} [已从MySQL删除]')
            return jsonify({'code': 20000, 'data': 'success'})

        return jsonify({'code': 50004, 'message': '文章不存在'})
    except Exception as e:
        logger.error(f'❌ 删除文章失败: {str(e)}')
        return jsonify({'code': 50000, 'message': '删除文章失败'}), 500

@app.route('/vue-admin-template/table/detail', methods=['GET'])
@token_required
def get_article_detail(payload):
    try:
        article_id = request.args.get('id')
        logger.info(f'📝 获取文章详情请求: ID={article_id}')

        if not article_id:
            logger.warning('⚠️ 文章ID为空')
            return jsonify({'code': 50003, 'message': '文章ID不能为空'})

        article = Article.get_by_id(article_id)

        if article:
            # 增加浏览量
            try:
                conn = Config.get_db_connection()
                cursor = conn.cursor()
                cursor.execute('UPDATE articles SET pageviews = pageviews + 1 WHERE id = %s', (article_id,))
                conn.commit()
                cursor.close()
                conn.close()
                logger.info(f'📈 文章浏览量+1: ID={article_id}')
            except Exception as e:
                logger.warning(f'⚠️ 更新浏览量失败: {str(e)}')

            logger.info(f'✅ 获取文章详情成功: ID={article_id}, 标题={article.get("title", "")}')
            return jsonify({'code': 20000, 'data': article})

        logger.warning(f'⚠️ 文章不存在: ID={article_id}')
        return jsonify({'code': 50004, 'message': '文章不存在'})

    except Exception as e:
        logger.error(f'❌ 获取文章详情失败: {str(e)}')
        import traceback
        logger.error(f'❌ 详细错误:\n{traceback.format_exc()}')
        return jsonify({'code': 50000, 'message': f'获取文章详情失败: {str(e)}'}), 500

@app.route('/vue-admin-template/user/list', methods=['GET'])
@token_required
@admin_required
def get_user_list(payload):
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 10))
    username = request.args.get('username', '')
    role = request.args.get('role', '')
    result = User.get_all(page, limit, username, role)
    return jsonify({'code': 20000, 'data': result})

@app.route('/vue-admin-template/user/<int:user_id>', methods=['GET'])
@token_required
def get_user_detail(payload, user_id):
    user = User.find_by_id(user_id)
    if user:
        return jsonify({'code': 20000, 'data': user})
    return jsonify({'code': 50004, 'message': '用户不存在'})

@app.route('/vue-admin-template/user/create', methods=['POST'])
@token_required
@admin_required
def create_user(payload):
    try:
        data = request.get_json()

        # 自动去除首尾空格
        username = data.get('username', '').strip() if data.get('username') else ''
        password = data.get('password', '').strip() if data.get('password') else ''
        name = data.get('name', '').strip() if data.get('name') else ''
        role = data.get('role', 'user').strip()
        avatar = data.get('avatar', '').strip() if data.get('avatar') else ''


        logger.info(f'📝 创建用户请求 - 用户名:"{username}", 密码长度:{len(password)}, 姓名:"{name}"')

        if not username or not password:
            return jsonify({'code': 50002, 'message': '用户名和密码不能为空'})

        # 检查用户名长度（防止全是空格）
        if len(username) < 2:
            return jsonify({'code': 50002, 'message': '用户名至少需要2个字符'})

        if User.find_by_username(username):
            return jsonify({'code': 50001, 'message': '用户名已存在'})

        if name and User.find_by_name(name):
            return jsonify({'code': 50001, 'message': '该姓名已被其他用户使用'})

        user_id = User.create(username, password, role, name, avatar)
        logger.info(f'✅ 新建用户成功 - ID:{user_id}, 用户名:"{username}", 角色:{role} [已写入MySQL]')
        return jsonify({'code': 20000, 'data': {'id': user_id}})
    except Exception as e:
        logger.error(f'❌ 新建用户失败: {str(e)}')
        import traceback
        logger.error(f'❌ 详细堆栈:\n{traceback.format_exc()}')
        return jsonify({'code': 50000, 'message': f'新建用户失败: {str(e)}'}), 500

@app.route('/vue-admin-template/user/register', methods=['POST'])
def register_user():
    """公开注册接口，注册的账号默认为普通用户"""
    try:
        data = request.get_json()
        username = data.get('username', '').strip() if data.get('username') else ''
        password = data.get('password', '').strip() if data.get('password') else ''

        logger.info(f'📝 用户注册请求 - 用户名:"{username}", 密码长度:{len(password)}')

        if not username or not password:
            return jsonify({'code': 50002, 'message': '用户名和密码不能为空'})

        if len(username) < 2:
            return jsonify({'code': 50002, 'message': '用户名至少需要2个字符'})

        if len(password) < 6:
            return jsonify({'code': 50002, 'message': '密码不能少于6位'})

        if User.find_by_username(username):
            return jsonify({'code': 50001, 'message': '用户名已存在'})

        # 使用用户名作为姓名，检查姓名是否重复
        if User.find_by_name(username):
            return jsonify({'code': 50001, 'message': '该姓名已被其他用户使用'})

        user_id = User.create(username, password, 'user', username, '')
        logger.info(f'✅ 用户注册成功 - ID:{user_id}, 用户名:"{username}" [已写入MySQL]')
        return jsonify({'code': 20000, 'data': {'id': user_id}})
    except Exception as e:
        logger.error(f'❌ 用户注册失败: {str(e)}')
        return jsonify({'code': 50000, 'message': f'注册失败: {str(e)}'}), 500

@app.route('/vue-admin-template/user/self-update', methods=['POST'])
@token_required
def update_self(payload):
    try:
        data = request.get_json()
        user_id = payload.get('user_id')
        if not user_id:
            return jsonify({'code': 50003, 'message': '用户ID不能为空'})

        # 检查姓名是否被其他用户使用
        new_name = data.get('name')
        if new_name:
            current_user = User.find_by_id(user_id)
            if current_user and new_name != current_user.get('name'):
                existing_user = User.find_by_name(new_name)
                if existing_user and existing_user['id'] != user_id:
                    return jsonify({'code': 50001, 'message': '该姓名已被其他用户使用'})

        User.update(
            user_id,
            name=data.get('name'),
            password=data.get('password'),
            avatar=data.get('avatar')
        )
        logger.info(f'✅ 用户更新个人信息成功 - ID:{user_id} [已更新MySQL]')
        return jsonify({'code': 20000, 'data': 'success'})
    except Exception as e:
        logger.error(f'❌ 用户更新个人信息失败: {str(e)}')
        return jsonify({'code': 50000, 'message': '更新个人信息失败'}), 500

@app.route('/vue-admin-template/user/update', methods=['POST'])
@token_required
@admin_required
def update_user(payload):
    try:
        data = request.get_json()
        user_id = data.get('id')
        if not user_id:
            return jsonify({'code': 50003, 'message': '用户ID不能为空'})

        # 检查目标用户是否存在
        target_user = User.find_by_id(user_id)
        if not target_user:
            return jsonify({'code': 50004, 'message': '用户不存在'})

        # 检查是否为 admin 管理员账号
        if target_user['username'] == 'admin':
            # 禁止修改 admin 的用户名和角色
            if data.get('username') and data.get('username') != 'admin':
                logger.warning(f'️ 尝试修改 admin 管理员用户名，已拒绝')
                return jsonify({'code': 50006, 'message': '无法修改 admin 管理员用户名'})
            if data.get('role') and data.get('role') != 'admin':
                logger.warning(f'⚠️ 尝试修改 admin 管理员角色，已拒绝')
                return jsonify({'code': 50007, 'message': '无法修改 admin 管理员角色'})

        # 检查姓名是否被其他用户使用
        new_name = data.get('name')
        if new_name and new_name != target_user.get('name'):
            existing_user = User.find_by_name(new_name)
            if existing_user and existing_user['id'] != user_id:
                return jsonify({'code': 50001, 'message': '该姓名已被其他用户使用'})

        User.update(
            user_id,
            name=data.get('name'),
            password=data.get('password'),
            role=data.get('role'),
            avatar=data.get('avatar')
        )
        logger.info(f'✅ 更新用户成功 - ID:{user_id}, 新姓名:{data.get("name")} [已更新MySQL]')
        return jsonify({'code': 20000, 'data': 'success'})
    except Exception as e:
        logger.error(f'❌ 更新用户失败: {str(e)}')
        return jsonify({'code': 50000, 'message': '更新用户失败'}), 500

@app.route('/vue-admin-template/user/delete', methods=['POST'])
@token_required
@admin_required
def delete_user(payload):
    try:
        data = request.get_json()
        user_id = data.get('id')
        if not user_id:
            return jsonify({'code': 50003, 'message': '用户ID不能为空'})

        # 检查是否为 admin 管理员账号
        conn = Config.get_db_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute('SELECT username, role FROM users WHERE id = %s', (user_id,))
        target_user = cursor.fetchone()
        cursor.close()
        conn.close()

        if not target_user:
            return jsonify({'code': 50004, 'message': '用户不存在'})

        # 禁止删除 admin 管理员账号
        if target_user['username'] == 'admin':
            logger.warning(f'⚠️ 尝试删除 admin 管理员账号，已拒绝')
            return jsonify({'code': 50005, 'message': '无法删除 admin 管理员账号'})

        if User.delete(user_id):
            logger.info(f'✅ 删除用户成功 - ID:{user_id} [已从MySQL删除]')
            return jsonify({'code': 20000, 'data': 'success'})
        return jsonify({'code': 50004, 'message': '用户不存在'})
    except Exception as e:
        logger.error(f'❌ 删除用户失败: {str(e)}')
        return jsonify({'code': 50000, 'message': '删除用户失败'}), 500

@app.route('/vue-admin-template/report/overview', methods=['GET'])
@token_required
def get_report_overview(payload):
    try:
        conn = Config.get_db_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        # 基础统计
        cursor.execute('SELECT COUNT(*) as count FROM users')
        users_count = cursor.fetchone()['count']
        cursor.execute('SELECT COUNT(*) as count FROM articles')
        articles_count = cursor.fetchone()['count']
        cursor.execute('SELECT COUNT(*) as count FROM articles WHERE status="published"')
        published_count = cursor.fetchone()['count']
        cursor.execute('SELECT COUNT(*) as count FROM articles WHERE status="draft"')
        draft_count = cursor.fetchone()['count']
        cursor.execute('SELECT COUNT(*) as count FROM comments')
        comments_count = cursor.fetchone()['count']
        cursor.execute('SELECT COUNT(*) as count FROM comments WHERE status="approved"')
        comments_approved = cursor.fetchone()['count']
        cursor.execute('SELECT COUNT(*) as count FROM comments WHERE status="pending"')
        comments_pending = cursor.fetchone()['count']
        cursor.execute('SELECT SUM(pageviews) as total FROM articles')
        pageviews_total = cursor.fetchone()['total'] or 0
        # 按状态分布
        cursor.execute('SELECT status, COUNT(*) as count FROM articles GROUP BY status')
        status_dist = cursor.fetchall()
        # 按评论状态分布
        cursor.execute('SELECT status, COUNT(*) as count FROM comments GROUP BY status')
        comment_status_dist = cursor.fetchall()
        # 热门文章 TOP 10
        cursor.execute('SELECT id, title, author, pageviews FROM articles ORDER BY pageviews DESC LIMIT 10')
        top_articles = cursor.fetchall()
        # 作者文章数排行
        cursor.execute('SELECT author as name, COUNT(*) as count FROM articles GROUP BY author ORDER BY count DESC LIMIT 10')
        author_ranking = cursor.fetchall()
        conn.close()
        logger.info('✅ 获取综合报表数据成功')
        return jsonify({'code': 20000, 'data': {
            'users_count': users_count,
            'articles_count': articles_count,
            'published_count': published_count,
            'draft_count': draft_count,
            'comments_count': comments_count,
            'comments_approved': comments_approved,
            'comments_pending': comments_pending,
            'pageviews_total': pageviews_total,
            'status_dist': status_dist,
            'comment_status_dist': comment_status_dist,
            'top_articles': top_articles,
            'author_ranking': author_ranking
        }})
    except Exception as e:
        logger.error(f'❌ 获取综合报表失败: {str(e)}')
        return jsonify({'code': 50000, 'message': f'获取综合报表失败: {str(e)}'}), 500

@app.route('/vue-admin-template/report/hot-articles', methods=['GET'])
@token_required
def get_hot_articles(payload):
    try:
        conn = Config.get_db_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        # 获取热门TOP10文章（按浏览量排序）
        cursor.execute('SELECT id, title, pageviews FROM articles WHERE status="published" ORDER BY pageviews DESC LIMIT 10')
        hot_articles = cursor.fetchall()
        conn.close()
        logger.info('✅ 获取热门文章成功')
        return jsonify({'code': 20000, 'data': hot_articles})
    except Exception as e:
        logger.error(f'❌ 获取热门文章失败: {str(e)}')
        return jsonify({'code': 50000, 'message': f'获取热门文章失败: {str(e)}'}), 500

@app.route('/vue-admin-template/report/article', methods=['GET'])
@token_required
def get_report_article(payload):
    try:
        days = int(request.args.get('days', 30))
        conn = Config.get_db_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        # 文章总数
        cursor.execute('SELECT COUNT(*) as articles_count FROM articles')
        articles_count = cursor.fetchone()['articles_count']
        # 已发布数
        cursor.execute("SELECT COUNT(*) as published_count FROM articles WHERE status = 'published'")
        published_count = cursor.fetchone()['published_count']
        # 草稿数
        cursor.execute("SELECT COUNT(*) as draft_count FROM articles WHERE status = 'draft'")
        draft_count = cursor.fetchone()['draft_count']
        # 总浏览量
        cursor.execute('SELECT COALESCE(SUM(pageviews), 0) as pageviews_total FROM articles')
        pageviews_total = cursor.fetchone()['pageviews_total']
        # 按日期的文章发布趋势
        cursor.execute(f'''
            SELECT DATE_FORMAT(created_at, '%Y-%m-%d') as date, COUNT(*) as count
            FROM articles
            WHERE created_at >= DATE_SUB(NOW(), INTERVAL {days} DAY)
            GROUP BY DATE_FORMAT(created_at, '%Y-%m-%d')
            ORDER BY date ASC
        ''')
        article_trend = [{'date': row['date'], 'count': row['count']} for row in cursor.fetchall()]
        # 文章状态分布
        cursor.execute('SELECT status, COUNT(*) as count FROM articles GROUP BY status')
        status_dist = cursor.fetchall()
        # 文章列表（带浏览量和评论数）
        cursor.execute('''
            SELECT a.id, a.title, a.author, a.status, a.pageviews,
                (SELECT COUNT(*) FROM comments c WHERE c.article_id = a.id) as comment_count,
                a.created_at
            FROM articles a
            ORDER BY a.created_at DESC
            LIMIT 100
        ''')
        articles = cursor.fetchall()
        conn.close()
        logger.info(f'✅ 获取文章报表成功: {len(articles)} 条')
        return jsonify({'code': 20000, 'data': {
            'articles_count': articles_count,
            'published_count': published_count,
            'draft_count': draft_count,
            'pageviews_total': pageviews_total,
            'article_trend': article_trend,
            'status_dist': status_dist,
            'articles': articles
        }})
    except Exception as e:
        logger.error(f'❌ 获取文章报表失败: {str(e)}')
        return jsonify({'code': 50000, 'message': f'获取文章报表失败: {str(e)}'}), 500

@app.route('/vue-admin-template/report/comment', methods=['GET'])
@token_required
def get_report_comment(payload):
    try:
        days = int(request.args.get('days', 30))
        conn = Config.get_db_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        # 评论总数
        cursor.execute('SELECT COUNT(*) as comments_count FROM comments')
        comments_count = cursor.fetchone()['comments_count']
        # 已通过评论数
        cursor.execute("SELECT COUNT(*) as comments_approved FROM comments WHERE status = 'approved'")
        comments_approved = cursor.fetchone()['comments_approved']
        # 待审核评论数
        cursor.execute("SELECT COUNT(*) as comments_pending FROM comments WHERE status = 'pending'")
        comments_pending = cursor.fetchone()['comments_pending']
        # 已拒绝评论数
        cursor.execute("SELECT COUNT(*) as comments_rejected FROM comments WHERE status = 'rejected'")
        comments_rejected = cursor.fetchone()['comments_rejected']
        # 按日期的评论发布趋势
        cursor.execute(f'''
            SELECT DATE_FORMAT(created_at, '%Y-%m-%d') as date, COUNT(*) as count
            FROM comments
            WHERE created_at >= DATE_SUB(NOW(), INTERVAL {days} DAY)
            GROUP BY DATE_FORMAT(created_at, '%Y-%m-%d')
            ORDER BY date ASC
        ''')
        comment_trend = [{'date': row['date'], 'count': row['count']} for row in cursor.fetchall()]
        # 评论状态分布
        cursor.execute('SELECT status, COUNT(*) as count FROM comments GROUP BY status')
        status_dist = cursor.fetchall()
        # 评论最多的文章 TOP 10
        cursor.execute('''
            SELECT a.id, a.title, a.author,
                (SELECT COUNT(*) FROM comments c WHERE c.article_id = a.id) as comment_count
            FROM articles a
            ORDER BY comment_count DESC
            LIMIT 10
        ''')
        top_commented = cursor.fetchall()
        # 最近评论列表
        cursor.execute('''
            SELECT c.id, c.username, c.content, c.status, c.created_at, a.title as article_title
            FROM comments c
            LEFT JOIN articles a ON c.article_id = a.id
            ORDER BY c.created_at DESC
            LIMIT 50
        ''')
        recent_comments = cursor.fetchall()
        conn.close()
        logger.info(f'✅ 获取评论报表成功')
        return jsonify({'code': 20000, 'data': {
            'comments_count': comments_count,
            'comments_approved': comments_approved,
            'comments_pending': comments_pending,
            'comments_rejected': comments_rejected,
            'comment_trend': comment_trend,
            'status_dist': status_dist,
            'top_commented': top_commented,
            'recent_comments': recent_comments
        }})
    except Exception as e:
        logger.error(f'❌ 获取评论报表失败: {str(e)}')
        return jsonify({'code': 50000, 'message': f'获取评论报表失败: {str(e)}'}), 500

@app.route('/vue-admin-template/report/activity', methods=['GET'])
@token_required
def get_report_activity(payload):
    try:
        days = int(request.args.get('days', 30))
        conn = Config.get_db_connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        # 基础统计
        cursor.execute('SELECT COUNT(*) as users_count FROM users')
        users_count = cursor.fetchone()['users_count']
        cursor.execute('SELECT COUNT(*) as articles_count FROM articles')
        articles_count = cursor.fetchone()['articles_count']
        cursor.execute('SELECT COUNT(*) as comments_count FROM comments')
        comments_count = cursor.fetchone()['comments_count']
        # 文章状态分布
        cursor.execute('SELECT status, COUNT(*) as count FROM articles GROUP BY status')
        article_status = cursor.fetchall()
        # 评论状态分布
        cursor.execute('SELECT status, COUNT(*) as count FROM comments GROUP BY status')
        comment_status = cursor.fetchall()
        # 用户活跃度排行（按文章数）
        cursor.execute('SELECT u.username as name, COUNT(a.id) as count FROM users u LEFT JOIN articles a ON u.username = a.author GROUP BY u.id ORDER BY count DESC LIMIT 10')
        user_activity = cursor.fetchall()
        # 最近发布的文章
        cursor.execute('SELECT id, title, author, status, created_at FROM articles ORDER BY created_at DESC LIMIT 50')
        recent_articles = cursor.fetchall()
        conn.close()
        logger.info(f'✅ 获取活跃报表成功')
        return jsonify({'code': 20000, 'data': {
            'users_count': users_count,
            'articles_count': articles_count,
            'comments_count': comments_count,
            'article_status': article_status,
            'comment_status': comment_status,
            'user_activity': user_activity,
            'recent_articles': recent_articles
        }})
    except Exception as e:
        logger.error(f'❌ 获取活跃报表失败: {str(e)}')
        return jsonify({'code': 50000, 'message': f'获取活跃报表失败: {str(e)}'}), 500

@app.route('/vue-admin-template/db/stats', methods=['GET'])
@token_required
def get_db_stats(payload):
    conn = Config.get_db_connection()
    cursor = conn.cursor()
    try:
        # 用户总数
        cursor.execute('SELECT COUNT(*) as count FROM users')
        users_count = cursor.fetchone()['count']

        # 文章总数
        cursor.execute('SELECT COUNT(*) as count FROM articles')
        articles_count = cursor.fetchone()['count']

        # 评论数量
        cursor.execute('SELECT COUNT(*) as count FROM comments')
        comments_count = cursor.fetchone()['count']

        # 总浏览量（所有文章的 pageviews 之和）
        try:
            cursor.execute('SELECT COALESCE(SUM(pageviews), 0) as total FROM articles')
            pageviews_total = cursor.fetchone()['total']
        except Exception:
            # 如果 pageviews 字段不存在，用文章数量替代
            pageviews_total = articles_count * 10

        stats = {
            'users': users_count,
            'articles': articles_count,
            'comments': comments_count,
            'pageviews': pageviews_total
        }

        logger.info(f'📊 实时统计 - 用户:{users_count}, 文章:{articles_count}, 评论:{comments_count}, 总浏览量:{pageviews_total}')
        return jsonify({'code': 20000, 'data': stats})
    except Exception as e:
        logger.error(f'❌ 获取数据库统计失败: {str(e)}')
        return jsonify({'code': 50000, 'message': f'获取统计失败: {str(e)}'}), 500
    finally:
        conn.close()

@app.route('/vue-admin-template/db/tables', methods=['GET'])
@token_required
def get_db_tables(payload):
    table_name = request.args.get('table')
    if not table_name:
        return jsonify({'code': 50003, 'message': '请指定表名 (table=users/articles/comments)'})
    valid_tables = ['users', 'articles', 'comments']
    if table_name not in valid_tables:
        return jsonify({'code': 50003, 'message': f'无效的表名，可选: {valid_tables}'})
    conn = Config.get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(f'SELECT * FROM {table_name} ORDER BY id DESC LIMIT 20')
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        data = []
        for row in rows:
            item = {}
            for i, col in enumerate(columns):
                value = row[i]
                item[col] = str(value) if value else ''
            data.append(item)
        logger.info(f'📋 查看表 {table_name}: 返回 {len(data)} 条记录')
        return jsonify({
            'code': 20000,
            'data': {
                'table': table_name,
                'columns': columns,
                'records': data,
                'total_count': len(data)
            }
        })
    except Exception as e:
        logger.error(f'❌ 查看表数据错误: {str(e)}')
        return jsonify({'code': 50000, 'message': f'查询{table_name}表失败'}), 500
    finally:
        conn.close()




# ============ 评论 API ============

def _get_current_username(payload):
    """从 token payload 中获取当前用户名（payload 只有 user_id 和 role，需要查用户表）"""
    if not payload or not payload.get('user_id'):
        return None
    user = User.find_by_id(payload['user_id'])
    if user:
        return user.get('name') or user.get('username')
    return None

@app.route('/vue-admin-template/comments/by-article', methods=['GET'])
@token_required
def get_comments_by_article(payload):
    try:
        article_id = request.args.get('article_id')
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 50))
        approved_only = request.args.get('approved_only', 'false').lower() == 'true'
        if not article_id:
            return jsonify({'code': 50003, 'message': '文章ID不能为空'})
        result = Comment.get_by_article(int(article_id), page, limit, approved_only)
        for item in result['items']:
            if item.get('created_at'):
                item['created_at'] = str(item['created_at'])
            if item.get('updated_at'):
                item['updated_at'] = str(item['updated_at'])
        logger.info(f'💬 获取文章 {article_id} 评论成功: {result["total"]} 条')
        return jsonify({'code': 20000, 'data': result})
    except Exception as e:
        logger.error(f'❌ 获取评论失败: {str(e)}')
        return jsonify({'code': 50000, 'message': f'获取评论失败: {str(e)}'}), 500

@app.route('/vue-admin-template/comments/list', methods=['GET'])
@token_required
def get_comment_list(payload):
    try:
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 20))
        status = request.args.get('status', '')
        article_id = request.args.get('article_id', '')
        result = Comment.get_all(page, limit, status, article_id)
        for item in result['items']:
            if item.get('created_at'):
                item['created_at'] = str(item['created_at'])
            if item.get('updated_at'):
                item['updated_at'] = str(item['updated_at'])
        logger.info(f'📋 评论管理列表: {result["total"]} 条')
        return jsonify({'code': 20000, 'data': result})
    except Exception as e:
        logger.error(f'❌ 获取评论列表失败: {str(e)}')
        return jsonify({'code': 50000, 'message': f'获取评论列表失败: {str(e)}'}), 500

@app.route('/vue-admin-template/comments/create', methods=['POST'])
@token_required
def create_comment(payload):
    try:
        data = request.get_json()
        article_id = data.get('article_id')
        # 前端传的 username 优先，否则从 token 查询
        username = data.get('username') or _get_current_username(payload) or '匿名用户'
        content = data.get('content')
        email = data.get('email', '')
        parent_id = data.get('parent_id')
        if not article_id or not content:
            return jsonify({'code': 50002, 'message': '文章ID和评论内容不能为空'})
        user_role = payload.get('role') if payload else 'user'
        status = 'approved' if user_role == 'admin' else 'pending'
        comment_id = Comment.create(int(article_id), username, content, email, status, parent_id)
        if comment_id is None:
            return jsonify({'code': 50004, 'message': '文章不存在'})
        logger.info(f'✅ 新建评论成功 - ID:{comment_id}, 文章:{article_id}, 状态:{status}')
        return jsonify({'code': 20000, 'data': {'id': comment_id, 'status': status}})
    except Exception as e:
        logger.error(f'❌ 新建评论失败: {str(e)}')
        return jsonify({'code': 50000, 'message': f'新建评论失败: {str(e)}'}), 500

@app.route('/vue-admin-template/comments/update', methods=['POST'])
@token_required
def update_comment(payload):
    try:
        data = request.get_json()
        comment_id = data.get('id')
        content = data.get('content')
        status = data.get('status')
        if not comment_id:
            return jsonify({'code': 50003, 'message': '评论ID不能为空'})
        comment = Comment.get_by_id(int(comment_id))
        if not comment:
            return jsonify({'code': 50004, 'message': '评论不存在'})
        # 权限：admin 或文章作者才能操作
        article = Article.get_by_id(comment['article_id'])
        current_user = _get_current_username(payload)
        user_role = payload.get('role') if payload else 'user'
        is_author = bool(article and current_user and current_user == article.get('author'))
        if user_role != 'admin' and not is_author:
            return jsonify({'code': 50005, 'message': '无权限操作此评论（仅管理员或文章作者可操作）'}), 403
        result = Comment.update(int(comment_id), content=content, status=status)
        if result:
            logger.info(f'✅ 更新评论成功 - ID:{comment_id}')
            return jsonify({'code': 20000, 'data': 'success'})
        return jsonify({'code': 50005, 'message': '更新评论失败'}), 500
    except Exception as e:
        logger.error(f'❌ 更新评论失败: {str(e)}')
        return jsonify({'code': 50000, 'message': f'更新评论失败: {str(e)}'}), 500

@app.route('/vue-admin-template/comments/approve', methods=['POST'])
@token_required
def approve_comment(payload):
    try:
        data = request.get_json()
        comment_id = data.get('id')
        status = data.get('status', 'approved')
        if not comment_id:
            return jsonify({'code': 50003, 'message': '评论ID不能为空'})
        comment = Comment.get_by_id(int(comment_id))
        if not comment:
            return jsonify({'code': 50004, 'message': '评论不存在'})
        article = Article.get_by_id(comment['article_id'])
        current_user = _get_current_username(payload)
        user_role = payload.get('role') if payload else 'user'
        is_author = bool(article and current_user and current_user == article.get('author'))
        if user_role != 'admin' and not is_author:
            return jsonify({'code': 50005, 'message': '无权限审核此评论'}), 403
        result = Comment.update(int(comment_id), status=status)
        if result:
            logger.info(f'✅ 评论审核完成 - ID:{comment_id}, 状态:{status}')
            return jsonify({'code': 20000, 'data': 'success'})
        return jsonify({'code': 50005, 'message': '审核失败'}), 500
    except Exception as e:
        logger.error(f'❌ 评论审核失败: {str(e)}')
        return jsonify({'code': 50000, 'message': f'审核失败: {str(e)}'}), 500

@app.route('/vue-admin-template/comments/delete', methods=['POST'])
@token_required
def delete_comment(payload):
    try:
        data = request.get_json()
        comment_id = data.get('id')
        if not comment_id:
            return jsonify({'code': 50003, 'message': '评论ID不能为空'})
        comment = Comment.get_by_id(int(comment_id))
        if not comment:
            return jsonify({'code': 50004, 'message': '评论不存在'})
        article = Article.get_by_id(comment['article_id'])
        current_user = _get_current_username(payload)
        user_role = payload.get('role') if payload else 'user'
        is_author = bool(article and current_user and current_user == article.get('author'))
        if user_role != 'admin' and not is_author:
            return jsonify({'code': 50005, 'message': '无权限删除此评论'}), 403
        if Comment.delete(int(comment_id)):
            logger.info(f'✅ 删除评论成功 - ID:{comment_id}')
            return jsonify({'code': 20000, 'data': 'success'})
        return jsonify({'code': 50004, 'message': '评论不存在'})
    except Exception as e:
        logger.error(f'❌ 删除评论失败: {str(e)}')
        return jsonify({'code': 50000, 'message': f'删除评论失败: {str(e)}'}), 500

@app.route('/vue-admin-template/comments/count', methods=['GET'])
@token_required
def count_comments(payload):
    try:
        article_id = request.args.get('article_id')
        if not article_id:
            return jsonify({'code': 50003, 'message': '文章ID不能为空'})
        total = Comment.count_by_article(int(article_id))
        approved = Comment.count_by_article(int(article_id), 'approved')
        pending = Comment.count_by_article(int(article_id), 'pending')
        return jsonify({
            'code': 20000,
            'data': {'total': total, 'approved': approved, 'pending': pending}
        })
    except Exception as e:
        logger.error(f'❌ 获取评论统计失败: {str(e)}')
        return jsonify({'code': 50000, 'message': f'获取评论统计失败: {str(e)}'}), 500

if __name__ == '__main__':
    logger.info('🚀 Flask 后端启动 - 所有 CRUD 操作将实时写入 MySQL 数据库')
    logger.info('📦 数据库配置: mysql://{}:{}/{}'.format(Config.MYSQL_HOST, Config.MYSQL_PORT, Config.MYSQL_DB))
    app.run(host='0.0.0.0', port=5000, debug=True)
