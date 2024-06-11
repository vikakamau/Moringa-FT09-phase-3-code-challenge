from database.connection import get_db_connection

class Article:
    def __init__(self, author, magazine, title, content=None):
        self.author = author
        self.magazine = magazine
        self.title = title
        self.content = content
        if content is not None:
            self.create_article()

    def __repr__(self):
        return f'<Article {self.title}>'

    def create_article(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        author_id = self.author.id
        magazine_id = self.magazine.id

        cursor.execute('''
            INSERT INTO articles (title, content, author_id, magazine_id) VALUES (?, ?, ?, ?)
        ''', (self.title, self.content, author_id, magazine_id))
        
        conn.commit()
        self.id = cursor.lastrowid
        conn.close()

    def get_title (self):
        return self._title
    
    def set_title (self, title):
        if hasattr(self, '_title'):
            return False
        if type(title) is not str:
            return False
        if not (5 <= len(title) <= 50):
            return False
        self._title = title
        return True
    
    title = property(get_title, set_title)

    def get_author(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT authors.id, authors.name
            FROM articles
            INNER JOIN authors ON articles.author_id = authors.id
            WHERE articles.id = ?
        ''', (self.id,))
        
        author = cursor.fetchone()
        conn.close()

        return author
    
    def get_magazine(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT magazines.id, magazines.name, magazines.category
            FROM articles
            INNER JOIN magazines ON articles.magazine_id = magazines.id
            WHERE articles.id = ?
        ''', (self.id,))
        
        magazine = cursor.fetchone()
        conn.close()

        return magazine