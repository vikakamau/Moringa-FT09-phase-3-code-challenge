from database.connection import get_db_connection
from models.author import Author

class Magazine:
    def __init__(self, id, name, category):
        self.id = id
        self.name = name
        self.category = category
        assert len(name)>= 2 and len(name)<=16


    def __repr__(self):
        return f'<Magazine {self.name}>'
    
    def get_name(self):
        return self._name

    def set_name(self, name: str):
        self._name = name
    name = property(get_name, set_name)
    
    def get_category(self):
        return self._category
    
    def set_category(self, category):
        if type(category) != str:
            return  
        if len(category) == 0:
            return 
        self._category = category

    category = property(get_category, set_category)
    
    def get_id(self):
        return self._id
    
    def set_id(self, id):
        if type(id) != int:
            return  
        self._id = id

    id = property(get_id, set_id)
    
    @classmethod
    def create(cls, name, category):
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO magazines (name, category) VALUES (?, ?)
        ''', (name, category))
        
        conn.commit()
        magazines_id = cursor.lastrowid
        conn.close()
        
        return cls(magazines_id, name, category)

    @classmethod
    def get_by_id(cls, magazine_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, name, category FROM magazines WHERE id = ?
        ''', (magazine_id,))
        
        fetch = cursor.fetchone()
        conn.close()
        
        if fetch:
            return cls(fetch['id'], fetch['name'], fetch['category'])
        else:
            return None
        
    def articles(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT articles.id, articles.title, articles.content, articles.author_id
            FROM articles
            WHERE articles.magazine_id = ?
        ''', (self.id,))

        articles = cursor.fetchall()
        conn.close()

        return articles
    
    def contributors(self):
        conn = get_db_connection()
        cursor = conn.cursor()   
        cursor.execute('''
            SELECT authors.id, authors.name
            FROM authors
            INNER JOIN articles ON articles.author_id = authors.id
            WHERE articles.magazine_id = ?
        ''', (self.id,))
        
        contributors_rows = cursor.fetchall()
        conn.close()
        

        return contributors_rows
    def article_titles(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT title FROM articles WHERE magazine_id = ?
        ''', (self.id,))
        titles = [row[0] for row in cursor.fetchall()]
        conn.close()
        if not titles:
           return None
        else:
            return titles
        
    def contributing_authors(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT authors.id, authors.name
            FROM articles
            INNER JOIN authors ON articles.author_id = authors.id
            WHERE articles.magazine_id = ?
            GROUP BY authors.id
            HAVING COUNT(*) > 2
        ''', (self.id,))
        authors_rows = cursor.fetchall()
        conn.close()

        if not authors_rows:
            return None

        contributing_authors = [Author(row['id'], row['name']) for row in authors_rows if type(row) is Author]
        return contributing_authors

