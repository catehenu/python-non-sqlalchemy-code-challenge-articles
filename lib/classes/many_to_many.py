class Author:
    def __init__(self, name, author_type='General'):
        # Initializing the author with a name and type (Senior, Junior, etc.)
        self.name = name
        self.author_type = author_type

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, new_name):
        if hasattr(self, '_name'):
            raise AttributeError('Name cannot be changed after instantiation.')
        if isinstance(new_name, str) and len(new_name) > 0:
            self._name = new_name
        else:
            raise ValueError('Name must be a non-empty string.')

    def articles(self):
        return [article for article in Article.all if article.author == self]

    def magazines(self):
        return list({article.magazine for article in self.articles()})

    def add_article(self, magazine, title):
        return Article(self, magazine, title)

    def topic_areas(self):
        areas = list({magazine.category for magazine in self.magazines()})
        return areas if areas else None

    def __str__(self):
        return f"{self.name} ({self.author_type})"


class SeniorAuthor(Author):
    def __init__(self, name):
        super().__init__(name, author_type="Senior")


class JuniorAuthor(Author):
    def __init__(self, name):
        super().__init__(name, author_type="Junior")


class Magazine:
    all = []

    def __init__(self, name, category, magazine_type='General'):
        self.name = name
        self.category = category
        self.magazine_type = magazine_type
        Magazine.all.append(self)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, new_name):
        if isinstance(new_name, str) and 2 <= len(new_name) <= 16:
            self._name = new_name
        else:
            raise ValueError('Name must be a string between 2 and 16 characters.')

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, new_category):
        if isinstance(new_category, str) and len(new_category) > 0:
            self._category = new_category
        else:
            raise ValueError('Category must be a non-empty string.')

    def articles(self):
        return [article for article in Article.all if article.magazine == self]

    def contributors(self):
        return list({article.author for article in self.articles()})

    def article_titles(self):
        titles = [article.title for article in self.articles()]
        return titles if titles else None

    def contributing_authors(self):
        author_counts = {}
        for article in self.articles():
            author_counts[article.author] = author_counts.get(article.author, 0) + 1
        return [author for author, count in author_counts.items() if count > 2] or None

    @classmethod
    def top_publisher(cls):
        if not Article.all:
            return None
        article_count = {}
        for article in Article.all:
            article_count[article.magazine] = article_count.get(article.magazine, 0) + 1
        max_count = max(article_count.values())
        top_magazines = [magazine for magazine, count in article_count.items() if count == max_count]
        return top_magazines[0] if top_magazines else None

    def __str__(self):
        return f"{self.name} ({self.magazine_type})"


class TechMagazine(Magazine):
    def __init__(self, name, category="Technology"):
        super().__init__(name, category, magazine_type="Tech")


class LifestyleMagazine(Magazine):
    def __init__(self, name, category="Lifestyle"):
        super().__init__(name, category, magazine_type="Lifestyle")


class Article:
    all = []

    def __init__(self, author, magazine, title):
        self.author = author
        self.magazine = magazine
        self.title = title
        Article.all.append(self)

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, new_title):
        if hasattr(self, '_title'):
            raise AttributeError('Title cannot be changed after the article is created.')
        if isinstance(new_title, str) and 5 <= len(new_title) <= 50:
            self._title = new_title
        else:
            raise ValueError('Title must be a string between 5 and 50 characters.')

    @property
    def author(self):
        return self._author

    @author.setter
    def author(self, new_author):
        if isinstance(new_author, Author):
            self._author = new_author
        else:
            raise TypeError('Author must be an instance of Author.')

    @property
    def magazine(self):
        return self._magazine

    @magazine.setter
    def magazine(self, new_magazine):
        if isinstance(new_magazine, Magazine):
            self._magazine = new_magazine
        else:
            raise TypeError('Magazine must be an instance of Magazine.')


# Example usage
# Creating authors
author1 = SeniorAuthor("Alice")
author2 = JuniorAuthor("Bob")

# Creating magazines
magazine1 = TechMagazine("TechToday")
magazine2 = LifestyleMagazine("LivingWell")

# Authors adding articles
author1.add_article(magazine1, "Future of AI")
author1.add_article(magazine2, "Health Tips for 2024")
author2.add_article(magazine1, "Latest in AI Research")
author2.add_article(magazine2, "Stress Management")

# Print information about authors, magazines, and articles
print(f"Articles by {author1.name}:")
for article in author1.articles():
    print(f"  {article.title} in {article.magazine.name}")

print(f"\nArticles by {author2.name}:")
for article in author2.articles():
    print(f"  {article.title} in {article.magazine.name}")

# Print magazine contributors
print(f"\nContributors to {magazine1.name}:")
for contributor in magazine1.contributors():
    print(f"  {contributor.name}")

print(f"\nContributors to {magazine2.name}:")
for contributor in magazine2.contributors():
    print(f"  {contributor.name}")

# Print top publisher
top_magazine = Magazine.top_publisher()
if top_magazine:
    print(f"\nTop publisher is: {top_magazine.name}")
