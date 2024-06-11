from database.connection import get_db_connection

class Author:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __repr__(self):
        return f'<Author {self.name}>'
    
    def get_name(self):
        return self._name
    
    def set_name(self, name: str):
        assert len(name)>= 0
        if hasattr(self, '_name'):
            return 
        self._name = name
    name = property(get_name, set_name)
    
    def get_id(self):
        return self._id
    
    def set_id(self, id):
          if type(id) != int:
            return  
          self._id = id

    id = property(get_id, set_id)

    @classmethod
    def create(cls, name):
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO authors (name) VALUES (?)
        ''', (name,))
        
        conn.commit()
        authors_id = cursor.lastrowid
        conn.close()
        
        return cls(authors_id, name)

    @classmethod
    def get_by_id(cls, author_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, name FROM authors WHERE id = ?
        ''', (author_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return cls(row['id'], row['name'])
        else:
            return None
    def articles(self):
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT articles.id, articles.title, articles.content, articles.magazine_id
            FROM articles
            INNER JOIN authors ON articles.author_id = authors.id
            WHERE authors.id = ?
        ''', (self.id,))
        
        articles = cursor.fetchall()
        conn.close()

        return articles
    def magazines(self):
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute('''
        SELECT magazines.id, magazines.name, magazines.category
        FROM magazines
        INNER JOIN articles ON articles.magazine_id = magazines.id
        WHERE articles.author_id = ?
    ''', (self.id,))
        
        magazines = cursor.fetchall()
        conn.close()

        return magazines