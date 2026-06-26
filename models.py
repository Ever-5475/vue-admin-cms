import pymysql
from config import Config
from datetime import datetime
import logging
import re

logger = logging.getLogger(__name__)

def _to_datetime(value):
    """
    统一转换各种时间格式（ISO 8601 / 日期字符串 / datetime 对象）
    为 MySQL DATETIME 可接受的 'YYYY-MM-DD HH:MM:SS' 字符串。
    返回 None 表示使用当前时间。
    """
    if value is None:
        return None
    if isinstance(value, datetime):
        return value.strftime('%Y-%m-%d %H:%M:%S')
    if isinstance(value, str):
        v = value.strip()
        if not v:
            return None
        # 尝试解析 ISO 8601 格式
        try:
            dt = datetime.fromisoformat(v.replace('Z', '+00:00'))
            return dt.strftime('%Y-%m-%d %H:%M:%S')
        except (ValueError, AttributeError):
            pass
        # 尝试解析常见日期格式
        patterns = [
            r'(\d{4})-(\d{2})-(\d{2})\s+(\d{2}):(\d{2}):(\d{2})',
            r'(\d{4})/(\d{2})/(\d{2})\s+(\d{2}):(\d{2}):(\d{2})',
            r'(\d{4})-(\d{2})-(\d{2})',
        ]
        for pattern in patterns:
            match = re.match(pattern, v)
            if match:
                groups = match.groups()
                if len(groups) == 6:
                    return f'{groups[0]}-{groups[1]}-{groups[2]} {groups[3]}:{groups[4]}:{groups[5]}'
                elif len(groups) == 3:
                    return f'{groups[0]}-{groups[1]}-{groups[2]} 00:00:00'
        # 如果包含 T 但没有时区信息，简单替换
        if 'T' in v:
            v = v.replace('T', ' ')
        return v
    return value

def get_db_connection():
    try:
        connection = pymysql.connect(
            host=Config.MYSQL_HOST,
            port=Config.MYSQL_PORT,
            user=Config.MYSQL_USER,
            password=Config.MYSQL_PASSWORD,
            database=Config.MYSQL_DB,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        return connection
    except Exception as e:
        logger.error(f'Database connection error: {str(e)}')
        raise

def init_db():
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(50) UNIQUE NOT NULL,
                    password VARCHAR(255) NOT NULL,
                    role VARCHAR(20) DEFAULT 'user',
                    name VARCHAR(50),
                    avatar VARCHAR(255),
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS articles (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    title VARCHAR(255) NOT NULL,
                    author VARCHAR(50) NOT NULL,
                    content TEXT,
                    pageviews INT DEFAULT 0,
                    status VARCHAR(20) DEFAULT 'draft',
                    display_time DATETIME,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                )
            ''')

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS comments (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    article_id INT NOT NULL,
                    username VARCHAR(50) NOT NULL,
                    email VARCHAR(100),
                    content TEXT NOT NULL,
                    status VARCHAR(20) DEFAULT 'pending',
                    parent_id INT DEFAULT NULL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    FOREIGN KEY (article_id) REFERENCES articles(id) ON DELETE CASCADE
                )
            ''')

            # 插入默认用户
            cursor.execute('SELECT COUNT(*) as count FROM users')
            result = cursor.fetchone()
            if result['count'] == 0:
                cursor.executemany('''
                    INSERT INTO users (username, password, role, name, avatar, created_at)
                    VALUES (%s, %s, %s, %s, %s, %s)
                ''', [
                    ('admin', '111111', 'admin', '管理员', '', '2026-06-22 14:58:00'),
                    ('test', '111111', 'user', '测试用户', '', '2026-06-22 14:58:30'),
                ])

            # 插入默认文章
            cursor.execute('SELECT COUNT(*) as count FROM articles')
            result = cursor.fetchone()
            if result['count'] == 0:
                articles_data = [
                    ('Vue.js 入门指南', '张三', '<p>Vue.js 是一套用于构建用户界面的渐进式框架。</p><p>核心库只关注视图层，不仅易于上手，还便于与第三方库或既有项目整合。</p>', 1234, 'published', '2024-01-15 10:00:00'),
                    ('Python Flask 后端开发实战', '李四', '<p>Flask 是一个轻量级的 Python Web 框架。</p><p>它被称为微框架，因为它不需要特定的工具或库。</p>', 5678, 'published', '2024-02-20 14:30:00'),
                    ('MySQL 性能优化技巧', '王五', '<p>数据库性能优化是后端开发中的重要环节。</p><p>本文介绍索引优化、查询优化等实用技巧。</p>', 9012, 'published', '2024-03-10 09:15:00'),
                    ('JavaScript 设计模式学习', '赵六', '<p>设计模式是软件开发中常见问题的解决方案。</p><p>本文介绍常见的设计模式及其在 JavaScript 中的应用。</p>', 3456, 'draft', '2024-04-05 16:45:00'),
                ]
                cursor.executemany('''
                    INSERT INTO articles (title, author, content, pageviews, status, display_time)
                    VALUES (%s, %s, %s, %s, %s, %s)
                ''', articles_data)

            # 插入默认评论
            cursor.execute('SELECT COUNT(*) as count FROM comments')
            result = cursor.fetchone()
            if result['count'] == 0:
                comments_data = [
                    (1, '读者小明', 'xiaoming@example.com', '这篇 Vue 入门文章写得太棒了！正是我需要的，感谢分享。', 'approved', None, '2024-01-16 08:30:00'),
                    (1, '前端爱好者', 'frontend@example.com', '建议增加一些 Vue3 Composition API 的示例会更有参考价值。', 'approved', None, '2024-01-17 12:15:00'),
                    (2, 'Pythoner', 'python@example.com', 'Flask 确实很轻量，配合 SQLAlchemy 用起来很舒服。', 'approved', None, '2024-02-21 19:40:00'),
                    (3, 'DBA 小王', 'dba@example.com', '索引优化那部分讲得很到位，最左前缀原则确实是新手最容易踩的坑。', 'pending', None, '2024-03-11 11:20:00'),
                    (3, 'admin', 'admin@example.com', '欢迎大家留言讨论，有问题也可以提出来~', 'approved', None, '2024-03-11 15:00:00'),
                ]
                cursor.executemany('''
                    INSERT INTO comments (article_id, username, email, content, status, parent_id, created_at)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                ''', comments_data)

        connection.commit()
        logger.info('Database initialized successfully')
    except Exception as e:
        logger.error(f'Database initialization error: {str(e)}')
        raise
    finally:
        if 'connection' in locals():
            connection.close()

class User:
    @staticmethod
    def find_by_username(username):
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
                return cursor.fetchone()
        finally:
            connection.close()

    @staticmethod
    def find_by_id(user_id):
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute('SELECT id, username, role, name, avatar FROM users WHERE id = %s', (user_id,))
                return cursor.fetchone()
        finally:
            connection.close()

    @staticmethod
    def find_by_name(name):
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute('SELECT * FROM users WHERE name = %s', (name,))
                return cursor.fetchone()
        finally:
            connection.close()

    @staticmethod
    def create(username, password, role='user', name=None, avatar=None):
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                default_avatar = avatar or ''
                cursor.execute('''
                    INSERT INTO users (username, password, role, name, avatar)
                    VALUES (%s, %s, %s, %s, %s)
                ''', (username, password, role, name or username, default_avatar))
                connection.commit()
                return cursor.lastrowid
        finally:
            connection.close()

    @staticmethod
    def get_all(page=1, limit=10, username='', role=''):
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                query = 'SELECT id, username, role, name, avatar, created_at FROM users WHERE 1=1'
                params = []
                if username:
                    query += ' AND username LIKE %s'
                    params.append(f'%{username}%')
                if role:
                    query += ' AND role = %s'
                    params.append(role)
                query += ' ORDER BY created_at DESC'
                cursor.execute(query, params)
                all_users = cursor.fetchall()
                total = len(all_users)
                start = (page - 1) * limit
                users_page = all_users[start:start + limit]
                return {'total': total, 'items': users_page}
        finally:
            connection.close()

    @staticmethod
    def update(user_id, name=None, password=None, role=None, avatar=None):
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                user = User.find_by_id(user_id)
                if not user:
                    return None
                updates = []
                params = []
                if name is not None:
                    updates.append('name=%s')
                    params.append(name)
                if password is not None:
                    updates.append('password=%s')
                    params.append(password)
                if role is not None:
                    updates.append('role=%s')
                    params.append(role)
                if avatar is not None:
                    updates.append('avatar=%s')
                    params.append(avatar)
                if updates:
                    params.append(user_id)
                    cursor.execute(f'UPDATE users SET {", ".join(updates)} WHERE id=%s', params)
                    connection.commit()
                return user_id
        finally:
            connection.close()

    @staticmethod
    def delete(user_id):
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute('DELETE FROM users WHERE id = %s', (user_id,))
                connection.commit()
                return cursor.rowcount > 0
        finally:
            connection.close()

class Article:
    @staticmethod
    def get_all(page=1, limit=10):
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                offset = (page - 1) * limit
                cursor.execute('SELECT COUNT(*) as total FROM articles')
                total = cursor.fetchone()['total']
                cursor.execute('SELECT * FROM articles ORDER BY created_at DESC LIMIT %s OFFSET %s', (limit, offset))
                items = cursor.fetchall()
                return {'total': total, 'items': items}
        finally:
            connection.close()

    @staticmethod
    def get_by_id(article_id):
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute('SELECT * FROM articles WHERE id = %s', (article_id,))
                return cursor.fetchone()
        finally:
            connection.close()

    @staticmethod
    def create(title, author, pageviews=0, status='draft', content=None, display_time=None):
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                parsed_display_time = _to_datetime(display_time) or datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                cursor.execute('''
                    INSERT INTO articles (title, author, content, pageviews, status, display_time)
                    VALUES (%s, %s, %s, %s, %s, %s)
                ''', (title, author, content or '', pageviews, status, parsed_display_time))
                connection.commit()
                return cursor.lastrowid
        finally:
            connection.close()

    @staticmethod
    def update(article_id, title=None, author=None, pageviews=None, status=None, content=None, display_time=None):
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                article = Article.get_by_id(article_id)
                if not article:
                    return None

                title = title if title is not None else article['title']
                author = author if author is not None else article['author']
                pageviews = pageviews if pageviews is not None else article['pageviews']
                status = status if status is not None else article['status']
                content = content if content is not None else article.get('content', '')
                raw_display_time = display_time if display_time not in (None, '') else article['display_time']
                parsed_display_time = _to_datetime(raw_display_time)
                if parsed_display_time is None:
                    parsed_display_time = article.get('display_time') or datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                cursor.execute('''
                    UPDATE articles SET title=%s, author=%s, content=%s, pageviews=%s, status=%s, display_time=%s
                    WHERE id=%s
                ''', (title, author, content, pageviews, status, parsed_display_time, article_id))
                connection.commit()
                return article_id
        finally:
            connection.close()

    @staticmethod
    def delete(article_id):
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute('DELETE FROM articles WHERE id = %s', (article_id,))
                connection.commit()
                return cursor.rowcount > 0
        finally:
            connection.close()

class Comment:
    @staticmethod
    def get_by_article(article_id, page=1, limit=50, approved_only=False):
        """获取指定文章的评论（按时间倒序，支持分页）"""
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                where = 'WHERE c.article_id = %s'
                params = [article_id]
                if approved_only:
                    where += " AND c.status = 'approved'"
                cursor.execute(f'SELECT COUNT(*) as total FROM comments c {where}', params)
                total = cursor.fetchone()['total']
                offset = (page - 1) * limit
                cursor.execute(f'''
                    SELECT c.*, a.title as article_title, a.author as article_author
                    FROM comments c
                    LEFT JOIN articles a ON c.article_id = a.id
                    {where}
                    ORDER BY c.created_at DESC
                    LIMIT %s OFFSET %s
                ''', params + [limit, offset])
                items = cursor.fetchall()
                return {'total': total, 'items': items}
        finally:
            connection.close()

    @staticmethod
    def get_all(page=1, limit=20, status='', article_id=''):
        """管理端：获取所有评论（支持筛选）"""
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                where = 'WHERE 1=1'
                params = []
                if status:
                    where += ' AND c.status = %s'
                    params.append(status)
                if article_id:
                    where += ' AND c.article_id = %s'
                    params.append(int(article_id))
                cursor.execute(f'SELECT COUNT(*) as total FROM comments c {where}', params)
                total = cursor.fetchone()['total']
                offset = (page - 1) * limit
                cursor.execute(f'''
                    SELECT c.*, a.title as article_title, a.author as article_author
                    FROM comments c
                    LEFT JOIN articles a ON c.article_id = a.id
                    {where}
                    ORDER BY c.created_at DESC
                    LIMIT %s OFFSET %s
                ''', params + [limit, offset])
                items = cursor.fetchall()
                return {'total': total, 'items': items}
        finally:
            connection.close()

    @staticmethod
    def get_by_id(comment_id):
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute('SELECT * FROM comments WHERE id = %s', (comment_id,))
                return cursor.fetchone()
        finally:
            connection.close()

    @staticmethod
    def create(article_id, username, content, email='', status='pending', parent_id=None):
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                # 检查文章是否存在
                cursor.execute('SELECT id FROM articles WHERE id = %s', (article_id,))
                if not cursor.fetchone():
                    return None
                cursor.execute('''
                    INSERT INTO comments (article_id, username, email, content, status, parent_id)
                    VALUES (%s, %s, %s, %s, %s, %s)
                ''', (article_id, username, email or '', content, status, parent_id))
                connection.commit()
                return cursor.lastrowid
        finally:
            connection.close()

    @staticmethod
    def update(comment_id, content=None, status=None):
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                comment = Comment.get_by_id(comment_id)
                if not comment:
                    return None
                content = content if content is not None else comment['content']
                status = status if status is not None else comment['status']
                cursor.execute('''
                    UPDATE comments SET content=%s, status=%s, updated_at=CURRENT_TIMESTAMP
                    WHERE id=%s
                ''', (content, status, comment_id))
                connection.commit()
                return comment_id
        finally:
            connection.close()

    @staticmethod
    def delete(comment_id):
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute('DELETE FROM comments WHERE id = %s', (comment_id,))
                connection.commit()
                return cursor.rowcount > 0
        finally:
            connection.close()

    @staticmethod
    def count_by_article(article_id, status=None):
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                if status:
                    cursor.execute('SELECT COUNT(*) as total FROM comments WHERE article_id = %s AND status = %s',
                                   (article_id, status))
                else:
                    cursor.execute('SELECT COUNT(*) as total FROM comments WHERE article_id = %s', (article_id,))
                return cursor.fetchone()['total']
        finally:
            connection.close()
