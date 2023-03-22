from unittest import TestCase
from app import app
from models import db, User, Tag, Post, PostTag

# Change blogly to blogly_test on app.py when using unittest (issue unresolved as of now)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()

class UserViewTestCase(TestCase):
    """Tests for proper loading of content on pages."""
    def setUp(self):
        """Create a tag, user and post."""
        PostTag.query.delete()
        Post.query.delete()
        User.query.delete()
        Tag.query.delete()
        
        
        user = User(first_name='Bob', last_name='Smith',image_url='https://wompampsupport.azureedge.net/fetchimage?siteId=7575&v=2&jpgQuality=100&width=700&url=https%3A%2F%2Fi.kym-cdn.com%2Fphotos%2Fimages%2Fnewsfeed%2F002%2F488%2F659%2F18a.jpg')
        tag = Tag(name='funny')
        post = Post(title='Post', content='This is a post.',user=user,tags=[tag])

        db.session.add(user)
        db.session.add(tag)
        db.session.add(post)

        db.session.commit()

        self.tag = tag
        self.user_id = user.id
        self.tag_id = tag.id
        self.post_id = post.id

    def tearDown(self):
        """Clean up fouled transaction."""

        db.session.rollback()

    def test_list_users(self):
        with app.test_client() as client:
            resp = client.get("/users")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Bob Smith', html)

    def test_show_user(self):
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Bob Smith</h1>', html)
    
    def test_add_user(self):
         with app.test_client() as client:
             d = {"first_name": "Woody", "last_name":"fromToyStory","image_url":"www.google.com"}
             resp = client.post("/users/new", data=d, follow_redirects=True)
             html = resp.get_data(as_text=True)
             self.assertEqual(resp.status_code, 200)
             self.assertIn("Woody fromToyStory", html)
    
    def test_edit_user(self):
        with app.test_client() as client:
            d = {"first_name": "edittedfirstname", "last_name":"edittedlastname","image_url":"idk"}
            resp = client.post(f"/users/{self.user_id}/edit", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("edittedfirstname edittedlastname", html)

    def test_list_tags(self):
        with app.test_client() as client:
            resp = client.get("/")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('funny', html)

    def test_edit_tag(self):
        with app.test_client() as client:
             d = {"name":"veryfunny"}
             resp = client.post(f"/tags/{self.tag_id}/edit", data=d, follow_redirects=True)
             html = resp.get_data(as_text=True)
             self.assertEqual(resp.status_code, 200)
             self.assertIn("veryfunny", html)            

    def test_show_tags(self):
        with app.test_client() as client:
            resp = client.get(f"/tags/{self.tag_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>funny</h1>', html)

    def test_add_tag(self):
        with app.test_client() as client:
             d = {"name":"cool"}
             resp = client.post(f"/tags/new", data=d, follow_redirects=True)
             html = resp.get_data(as_text=True)
             self.assertEqual(resp.status_code, 200)
             self.assertIn("cool", html)   

    def test_list_posts(self):
        with app.test_client() as client:
            resp = client.get("/")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('This is a post.', html)
    
    def test_show_post(self):
        with app.test_client() as client:
            resp = client.get(f"/posts/{self.post_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<p>This is a post.</p>', html)
    
    def test_add_post(self):
        with app.test_client() as client:
            d = {"title":"newposttitle", "content":"new post content","tags":f"{self.tag_id}"}
            resp = client.post(f"/users/{self.tag_id}/posts/new", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("newposttitle", html)

    def test_edit_post(self):
        with app.test_client() as client:
            d = {"title":"edittedposttitle","content":"editted post content","tags":f"{self.tag_id}"}
            resp = client.post(f"posts/{self.post_id}/edit", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code,200)
            self.assertIn("<h1>edittedposttitle</h1>", html)

