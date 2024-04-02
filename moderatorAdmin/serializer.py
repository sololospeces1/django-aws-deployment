
from rest_framework import serializers
from moderatorAdmin.models import Blog, User, Comment, Magazine, Category,Feedback, Role
from rest_framework import generics



# serializers.py
from rest_framework import serializers


# serializers.py
from rest_framework import serializers



class FeedbackSerializerUp(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = '__all__'

class BlogSerializerUp(serializers.ModelSerializer):
    feedback=FeedbackSerializerUp(many=True, read_only=True)

    class Meta:
        model = Blog
        fields = ['id']


class CategorySerializerA(serializers.ModelSerializer): 
    class Meta: 
        model = Category
        fields = ['name']

class CategorySerializer(serializers.ModelSerializer): 
    class Meta: 
        model = Category
        fields = "__all__"

class ManyCategorySerializer(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class BlogSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = Blog
        fields = ['is_approved', 'id']

class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ['content', 'blog_id']

    
        #read_only_fields = ['created_at']  # Ensures created_at is read-only

# class BlogSerializerFeedback(serializers.ModelSerializer):
#     feedbacks = FeedbackSerializerBlog(many=True, read_only=True)  # Nested FeedbackSerializer for one-to-many relationship

#     class Meta:
#         model = Blog
#         fields = ['id', 'title', 'content', 'feedbacks']


class BlogSerializer2(serializers.ModelSerializer): 
    class Meta: 
        model = Blog
        fields ="__all__"


# class FeedbackSerializer(serializers.ModelSerializer):
#    # blog = BlogSerializer(read_only=True)  # Nested representation of the related Author

#     class Meta:
#         model = Feedback
#         fields = ['feedbackContent']






class UserSerializerB(serializers.ModelSerializer): 
   #role=RoleSerializer(many=False, read_only=True)
   class Meta: 
    model = User
    fields = ['id', 'banned']

class RoleSerializer(serializers.ModelSerializer): 
   
    class Meta: 
        model = Role
        fields ="__all__"
class RoleSerializerMod(serializers.ModelSerializer): 
   
    class Meta: 
        model = Role
        fields =['id']

class UserRoleSerializer(serializers.ModelSerializer): 
    role=RoleSerializerMod()
    class Meta: 
        model = User
        fields = ['id','role']

    # def update(self, instance, validated_data):
    #     # Update the role_id field if provided in validated_data
    
    #     instance.role_id = 5
        
    #     instance.save()
    #     return instance
    # def update(self, instance, validated_data):
    #     #contacts_data = validated_data.pop('role')

    #     instance.user= validated_data.get('role', instance.role)
    #     instance.save()

    #     return instance
    
class UserSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = User
        fields = "__all__"


class CommentSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = Comment
        fields = "__all__"


class MagazineSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = Magazine
        fields = ['date_released', 'id']