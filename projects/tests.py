from django.test import TestCase
from django.contrib.auth import get_user_model
from projects.models import Project, ProjectMember, Comment

User = get_user_model()

class ProjectModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )
        self.project = Project.objects.create(
            title='Test Project',
            description='Test Description',
            owner=self.user
        )

    def test_project_creation(self):
        self.assertEqual(self.project.title, 'Test Project')
        self.assertEqual(self.project.description, 'Test Description')
        self.assertEqual(self.project.owner, self.user)
        self.assertTrue(self.project.created_at)
        self.assertTrue(self.project.updated_at)

    def test_project_update(self):
        updated_title = "Updated Project"
        self.project.title = updated_title
        self.project.save()
        self.assertEqual(self.project.title, updated_title)

    def test_project_delete(self):
        project_id = self.project.id
        self.project.delete()
        with self.assertRaises(Project.DoesNotExist):
            Project.objects.get(id=project_id)


class ProjectMemberModelTest(TestCase):
    def setUp(self):
        self.owner = User.objects.create_user(
            email='owner@example.com',
            password='testpass123'
        )
        self.member = User.objects.create_user(
            email='member@example.com',
            password='testpass123'
        )
        self.project = Project.objects.create(
            title='Test Project',
            description='Test Description',
            owner=self.owner
        )
        self.project_member = ProjectMember.objects.create(
            project=self.project,
            user=self.member,
            role='EDITOR'
        )

    def test_project_member_creation(self):
        self.assertEqual(self.project_member.project, self.project)
        self.assertEqual(self.project_member.user, self.member)
        self.assertEqual(self.project_member.role, 'EDITOR')
        self.assertTrue(self.project_member.joined_at)


    def test_unique_project_user_combination(self):
        # Test that we can't create duplicate project-user combinations
        with self.assertRaises(Exception):
            ProjectMember.objects.create(
                project=self.project,
                user=self.member,
                role='READER'
            )

    def test_project_member_role_update(self):
        self.project_member.role = 'READER'
        self.project_member.save()
        self.assertEqual(self.project_member.role, 'READER')

    def test_project_member_delete(self):
        member_id = self.project_member.id
        self.project_member.delete()
        with self.assertRaises(ProjectMember.DoesNotExist):
            ProjectMember.objects.get(id=member_id)


class CommentModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123'
        )
        self.project = Project.objects.create(
            title='Test Project',
            description='Test Description',
            owner=self.user
        )
        self.comment = Comment.objects.create(
            project=self.project,
            user=self.user,
            text='Test Comment'
        )

    def test_comment_creation(self):
        self.assertEqual(self.comment.project, self.project)
        self.assertEqual(self.comment.user, self.user)
        self.assertEqual(self.comment.text, 'Test Comment')
        self.assertTrue(self.comment.created_at)
        self.assertTrue(self.comment.updated_at)

    def test_comment_update(self):
        updated_text = "Updated Comment"
        self.comment.text = updated_text
        self.comment.save()
        self.assertEqual(self.comment.text, updated_text)

    def test_comment_delete(self):
        comment_id = self.comment.id
        self.comment.delete()
        with self.assertRaises(Comment.DoesNotExist):
            Comment.objects.get(id=comment_id)

    def test_comment_cascade_delete_on_project_deletion(self):
        self.project.delete()
        with self.assertRaises(Comment.DoesNotExist):
            Comment.objects.get(id=self.comment.id)
