from database.connection import get_db_connection

class Author:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __repr__(self):
        return f'<Author {self.name}>'
    
    def get_name(self):
        return self._name
    
    def set_name(self, name):
        if type(name) != str:
            print("Name must be of type str")
            return 
        if len(name) == 0:
            print("Name must be longer than 0 characters")
            return 
        if hasattr(self, '_name'):
            print("Name cannot be changed after author is instantiated")
            return 
        self._name = name
    name = property(get_name, set_name)
    
    def get_id(self):
        return self._id
    
    def set_id(self, id):
          if type(id) != int:
            print("ID must be of type int")
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
        author_id = cursor.lastrowid
        conn.close()
        
        return cls(author_id, name)

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
        
        articles_rows = cursor.fetchall()
        conn.close()

        return articles_rows
    def magazines(self):
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute('''
        SELECT magazines.id, magazines.name, magazines.category
        FROM magazines
        INNER JOIN articles ON articles.magazine_id = magazines.id
        WHERE articles.author_id = ?
    ''', (self.id,))
        
        magazine_rows = cursor.fetchall()
        conn.close()

        return magazine_rows