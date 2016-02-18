from django.test import TestCase
from models import Product, Comment
from django.core.urlresolvers import reverse
from django.test import Client
from forms import CommentForm

client = Client()


class ProfileMethodTests(TestCase):

    def setUp(self):
        Product.objects.create(name='product',
                               slug='product',
                               description='description',
                               price='200').save()
        Product.objects.create(name='test',
                               slug='test',
                               description='test',
                               price='100').save()
        # get profile_detail page
        self.response = self.client.get(reverse('test_task:product_detail',
                                                args=['product']))

    def test_enter_profile_detail_page(self):
        """
        Test entering profile detail page
        """
        # if index page exists
        self.assertEqual(self.response.status_code, 200)

    def test_product(self):
        """
        Testing product shown in the page
        """
        # get product
        product = Product.objects.get(slug='product')
        # test context product detail view
        self.assertEqual(self.response.context['product'], product)
        # test product data exist on the main page
        # test product price on the page
        self.assertContains(self.response, u'200')
        # test product description on the page
        self.assertContains(self.response, u'Description')

    def test_non_another_product(self):
        """
        Test if exist another product in the page
        """
        # test if not another product on the peage
        self.assertNotEqual(self.response.context['product'],
                            Product.objects.get(slug='test'))
        self.assertNotIn('test', self.response.content)

    def test_html(self):
        """
        Testing valid html on the page
        """
        self.assertTrue('Add a comment'
                        in self.response.content)

    def test_index_template(self):
        """
        Testing valid html on the page
        """
        self.assertTemplateUsed(self.response,
                                'test_task/product_detail.html')

    def test_add_comment(self):
        """
        Testing add comment to product
        """
        # test if no comments in db
        comment_count = Comment.objects.count()
        self.assertEqual(comment_count, 0)
        product = Product.objects.first()
        form_data = {
            'product': product.id,
            'name': 'name',
            'comment': 'comment'
        }
        # add comment
        form = CommentForm(form_data)
        # test if form is valid
        self.assertTrue(form.is_valid())
        form.save()
        # count if new comment created
        updated_comment = Comment.objects.count()
        self.assertEqual(updated_comment, 1)
        comment = Comment.objects.first()
        self.assertEqual(comment.product, product)

    def test_no_data_add_comment(self):
        """
        Testing add comment to product
        """
        form_data = {
            'product': '',
            'name': '',
            'comment': ''
        }
        # add comment
        form = CommentForm(form_data)
        # test form fields required
        self.assertEqual([u'This field is required.'], form['product'].errors)
        self.assertEqual([u'This field is required.'], form['name'].errors)
        self.assertEqual([u'This field is required.'], form['comment'].errors)
