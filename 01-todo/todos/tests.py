from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from .models import Todo

class TodoModelTest(TestCase):
    def setUp(self):
        self.todo = Todo.objects.create(
            title="Test Todo",
            description="Test Description",
            due_date=timezone.now() + timedelta(days=1)
        )

    def test_todo_creation(self):
        """Test that a todo can be created"""
        self.assertEqual(self.todo.title, "Test Todo")
        self.assertEqual(self.todo.description, "Test Description")
        self.assertFalse(self.todo.is_completed)

    def test_todo_str(self):
        """Test the string representation of a todo"""
        self.assertEqual(str(self.todo), "Test Todo")

    def test_is_overdue(self):
        """Test the is_overdue method"""
        # Future due date - not overdue
        self.assertFalse(self.todo.is_overdue())
        
        # Past due date - overdue
        self.todo.due_date = timezone.now() - timedelta(days=1)
        self.todo.save()
        self.assertTrue(self.todo.is_overdue())
        
        # Completed todo - not overdue
        self.todo.is_completed = True
        self.todo.save()
        self.assertFalse(self.todo.is_overdue())


class TodoViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.todo = Todo.objects.create(
            title="Test Todo",
            description="Test Description"
        )

    def test_todo_list_view(self):
        """Test that the list view displays todos"""
        response = self.client.get(reverse('todo_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Todo")
        self.assertTemplateUsed(response, 'todos/home.html')

    def test_todo_create_view_get(self):
        """Test GET request to create view"""
        response = self.client.get(reverse('todo_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'todos/todo_form.html')

    def test_todo_create_view_post(self):
        """Test creating a new todo via POST"""
        response = self.client.post(reverse('todo_create'), {
            'title': 'New Todo',
            'description': 'New Description',
        })
        self.assertEqual(response.status_code, 302)  # Redirect after success
        self.assertTrue(Todo.objects.filter(title='New Todo').exists())

    def test_todo_update_view(self):
        """Test updating a todo"""
        response = self.client.post(
            reverse('todo_update', kwargs={'pk': self.todo.pk}),
            {
                'title': 'Updated Todo',
                'description': 'Updated Description',
            }
        )
        self.assertEqual(response.status_code, 302)
        self.todo.refresh_from_db()
        self.assertEqual(self.todo.title, 'Updated Todo')

    def test_todo_delete_view(self):
        """Test deleting a todo"""
        response = self.client.post(
            reverse('todo_delete', kwargs={'pk': self.todo.pk})
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Todo.objects.filter(pk=self.todo.pk).exists())

    def test_todo_toggle_complete(self):
        """Test toggling completion status"""
        # Initially not completed
        self.assertFalse(self.todo.is_completed)
        
        # Toggle to completed
        response = self.client.post(
            reverse('todo_toggle_complete', kwargs={'pk': self.todo.pk})
        )
        self.assertEqual(response.status_code, 302)
        self.todo.refresh_from_db()
        self.assertTrue(self.todo.is_completed)
        
        # Toggle back to incomplete
        response = self.client.post(
            reverse('todo_toggle_complete', kwargs={'pk': self.todo.pk})
        )
        self.todo.refresh_from_db()
        self.assertFalse(self.todo.is_completed)


class TodoFormTest(TestCase):
    def test_valid_form(self):
        """Test form with valid data"""
        from .forms import TodoForm
        data = {
            'title': 'Test Todo',
            'description': 'Test Description',
        }
        form = TodoForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        """Test form with missing required field"""
        from .forms import TodoForm
        data = {'description': 'Test Description'}
        form = TodoForm(data=data)
        self.assertFalse(form.is_valid())
