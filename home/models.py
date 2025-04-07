from django.db import models
import uuid
from django.contrib.auth.models import User

# Create your models here.

class Basemodel(models.Model):
    uid= models.UUIDField(primary_key= True, editable= False, default= uuid.uuid4)
    created_at= models.DateField(auto_now_add= True)
    updated_at= models.DateField(auto_now= True)


    class Meta:
        abstract= True


class Blog(Basemodel):
    user= models.ForeignKey(User , on_delete= models.CASCADE, related_name= "blogs")
    title= models.CharField(max_length=500)
    blog_text= models.TextField()
    main_image= models.ImageField(upload_to= "blog_image/")
    like_count= models.PositiveIntegerField(default= 0)



    def __str__(self):
        return self.title
    
class Comment(Basemodel):
    user= models.ForeignKey(User, on_delete= models.CASCADE)
    blog= models.ForeignKey(Blog, on_delete= models.CASCADE, related_name= "comments")
    comment= models.TextField(default= "")


    def __str__(self):
        return f"{self.user.username} - {self.blog.title}"
    

class Like(Basemodel):
    user= models.ForeignKey(User, on_delete= models.CASCADE, related_name= 'likes', null= True, blank= True)
    blog= models.ForeignKey(Blog, on_delete= models.CASCADE, related_name= 'likes', null= True, blank= True)
    
    class Meta:
        unique_together= ['user', 'blog']

    def save(self, *args, **kwargs):
        if not self.pk:
            self.blog.like_count += 1
            self.blog.save()
        super().save(*args, **kwargs)


    def delete(self, *args, **kwargs):
        self.blog.like_count -= 1
        self.blog.save()
        super().delete(*args, **kwargs)

