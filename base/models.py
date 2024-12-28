from django.db import models

class GeneratedImage(models.Model):
    prompt = models.TextField()
    user_prompt = models.TextField()
    image_data = models.TextField() 
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.prompt
    