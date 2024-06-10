import unittest
from models.author import Author
from models.article import Article
from models.magazine import Magazine

class TestModels(unittest.TestCase):
    def test_author_creation(self):
        author = Author(1, "John Doe")
        self.assertEqual(author.name, "John Doe")

    def test_article_creation(self):
        author = Author(1, "John Doe")  
        magazine = Magazine(1, "Tech Weekly", "Technology")  
        article = Article(author, magazine, "Test Title", "Test Content")
        self.assertEqual(article.title, "Test Title")

    def test_magazine_creation(self):
        magazine = Magazine(1, "Tech Weekly", "Technology")
        self.assertEqual(magazine.name, "Tech Weekly")
        self.assertEqual(magazine.category, "Technology")
        self.assertIsInstance(magazine.id, int)


    def test_get_author_by_id(self):
        new_author = Author.create('Jane Doe')
        author_id = new_author.id
        self.assertIsInstance(author_id, int)
        retrieved_author = Author.get_by_id(author_id)
        self.assertEqual(retrieved_author.name, 'Jane Doe')
        self.assertEqual(retrieved_author.id, author_id)

    def test_reject_change_after_instantiation(self):
        author = Author(1, 'John Doe')
        author.name = 'Jane Doe'
        self.assertEqual(author._name, 'John Doe')


    def test_magazine_id_setter_getter(self):
        magazine = Magazine(1, "Tech Weekly", "Technology")
        self.assertEqual(magazine.id, 1)
        magazine.id = "invalid" 

    def test_magazine_name_setter(self):
        magazine = Magazine(1, "Tech Weekly", "Technology")
        self.assertEqual(magazine.name, "Tech Weekly")
        magazine.name = 123  
        magazine.name = "A"  
        magazine.name = "A" * 17  

    def test_magazine_category_setter(self):
       magazine = Magazine(1, "Tech Weekly", "Technology")
       self.assertEqual(magazine.category, "Technology")
       magazine.category = "Science"  

    def test_article_title_constraints(self):
        author = Author(1, "John Doe")
        magazine = Magazine(1, "Tech Weekly", "Technology")
        self.assertEqual(Article(author, magazine, "Valid Title").title, "Valid Title")
        Article(author, magazine, "A" * 4)
        Article(author, magazine, "A" * 51)
        Article(author, magazine, 12345)

    def test_article_title_immutable(self):
        author = Author(1, "John Doe")
        magazine = Magazine(1, "Tech Weekly", "Technology")
        article = Article(author, magazine, "Immutable Title")
        self.assertEqual(article.title, "Immutable Title")
        self.assertFalse(article.set_title("New Title"))
        self.assertEqual(article.title, "Immutable Title")

    def test_get_author(self):
        author = Author.create("John Doe")
        magazine = Magazine.create("Tech Weekly", "Technology")
        article = Article(author, magazine, "Test Title", "Test Content")
        retrieved_author = article.get_author()

        self.assertEqual(retrieved_author['id'], author.id)
        self.assertEqual(retrieved_author['name'], author.name)

    def test_get_magazine(self):
        magazine = Magazine.create("Tech Weekly", "Technology")
        author = Author.create("John Doe")
        article = Article(author, magazine, "Test Title", "Test Content")
        retrieved_magazine = article.get_magazine()
        self.assertEqual(retrieved_magazine['id'], magazine.id)
        self.assertEqual(retrieved_magazine['name'], magazine.name)
        self.assertEqual(retrieved_magazine['category'], magazine.category)
    
    def test_articles(self):
        author = Author.create("John Doe")
        magazine = Magazine.create("Tech Weekly", "Technology")
        article1 = Article(author, magazine, "Article 1", "Content 1")
        article2 = Article(author, magazine, "Article 2", "Content 2")
        articles = author.articles()
        self.assertEqual(len(articles), 2)

    def test_magazines(self):
        author = Author.create("John Doe")
        magazine = Magazine.create("Tech Weekly", "Technology")
        article1 = Article(author, magazine, "Article 1", "Content 1")
        article2 = Article(author, magazine, "Article 2", "Content 2")
        magazines = author.magazines()
        self.assertEqual(len(magazines), 2)
    
    def test_articles_2(self):
        author = Author.create("John Doe")
        magazine = Magazine.create("Tech Weekly", "Technology")
        article1 = Article(author, magazine, "Article 1", "Content 1")
        article2 = Article(author, magazine, "Article 2", "Content 2")
        articles = magazine.articles()
        self.assertEqual(len(articles), 2)

    def test_contributors(self):
        author = Author.create("John Doe")
        magazine = Magazine.create("Tech Weekly", "Technology")
        article1 = Article(author, magazine, "Article 1", "Content 1")
        article2 = Article(author, magazine, "Article 2", "Content 2")
        contributors = magazine.contributors()
        self.assertEqual(len(contributors), 2)
    def test_article_titles(self):
        author = Author.create("John Doe")
        magazine = Magazine.create("Tech Weekly", "Technology")
        article1 = Article(author, magazine, "Article 1", "Content 1")
        article2 = Article(author, magazine, "Article 2", "Content 2")
        titles = magazine.article_titles()
        self.assertEqual(len(titles), 2)
    def test_article_titles_no_articles(self):
        magazine = Magazine.create("Tech Weekly", "Technology")
        titles = magazine.article_titles()
        self.assertIsNone(titles)
    def test_contributing_authors(self):
        author1 = Author.create("John Doe")
        author2 = Author.create("Jane Doe")
        magazine = Magazine.create("Tech Weekly", "Technology")
        article1 = Article(author1, magazine, "Article 1", "Content 1")
        article2 = Article(author2, magazine, "Article 2", "Content 2")
        contributing_authors = magazine.contributing_authors()
        self.assertEqual(contributing_authors, None)


    def test_contributing_authors_none(self):
        magazine = Magazine.create("Tech Weekly", "Technology")
        contributing_authors = magazine.contributing_authors()
        self.assertIsNone(contributing_authors)
       









if __name__ == "__main__":
    unittest.main()
