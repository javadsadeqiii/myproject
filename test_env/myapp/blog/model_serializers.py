from rest_framework.serializers import ModelSerializer
from . models import *
from django.contrib.auth.models import User
from rest_framework import serializers
from datetime import datetime













class commentsSerializer(ModelSerializer):
    
    class Meta:
        
        model = comments
        fields = ('commentText','commentReply','createdAt','userId','postId','likeCount')






class commentsLikeSerializer(ModelSerializer):
    
    class Meta:
        
        model = commentsLike
        fields = ("userId","commentId")








class updateUsernameSerializer(ModelSerializer):
    
    class Meta:
        
        model = updateUsername
        fields=('currentUsername','newUsername')

    
    
    
    
class updatePasswordSerializer(ModelSerializer):
    
    class Meta:
        model = updatePassword
        fields= ('currentPassword','newPassword','confirmNewPassword')
    
    


class userRegisterSerializer(ModelSerializer):
       
       class Meta:
           model = User
           fields = ('username', 'password', 'email')
  
  
  
  
  
class userLoginSerializer(ModelSerializer):
    
    class Meta:
        
        model = userLogin
        fields = ('email','password')
        






class allPostsSerializer(serializers.ModelSerializer):
    
   

    class Meta:
        model = allPosts
        fields = '__all__'
       

        
        
        
        
        
        
        
class authorsSerializer(ModelSerializer):
    class Meta:
        model = authors
        
        fields = ('authorName','slug','about','avatar','email','expertise','date')
        
        
        
    

        
        


class wallpapersSerializer(ModelSerializer):
    class Meta :
        model = wallpapers
        fields = ('title','slug','idPost','date','thumbnail','device','image','resolution')
        
        
        
        
        
        
        
class albumsSerializer(ModelSerializer):
   
    class Meta : 
       
        model = albums
        
        fields = ('title','date','image','totalFileSize','zipFile','slug','description','soundTracks')
        
        
        
        
        


class soundTracksSerializer(ModelSerializer):
   
   class Meta :
      
      model = soundTracks
      
      fields = ('title','artists','duration','date','image','audioFile','fileSize','album')
   