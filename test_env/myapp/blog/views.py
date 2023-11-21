from django.http import JsonResponse
from rest_framework import permissions
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login
from rest_framework.viewsets import ModelViewSet
from django.contrib import messages
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework import status
from . models import *
from . model_serializers import *
from django.contrib.auth.models import User
from rest_framework import status
import re
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib.auth import update_session_auth_hash
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver


DATE_FORMAT=  'Y-m-d'
DATETIME_FORMAT = 'Y-m-d H:i:s'



#Create your views here.







class commentsViewSet(ModelViewSet):
    
    queryset = comments.objects.all()
    serializer_class  = commentsSerializer
    
    
    
    
@receiver([post_save, post_delete], sender=comments)

def update_post_comment_counts(sender, instance, **kwargs):
    instance.postId.update_comment_counts()
    
    
    
    
    
    
    
    
# با هر بار لایک کامنت تعداد ان آپدیت میشود 
def update_likes_count(self):
    
        self.likeCount = self.likes.count()
        self.save()    
        
    
    
PROHIBITED_WORDS = ["word1","word2","word3"]

# بخش ممنوع کردن کلمات
def contains_prohibited_words(text):
    
    for word in PROHIBITED_WORDS:
        if word in text:
            return True
    return False



#بخش ممنوع کردن گذاشتن لینک
def contains_url(text):
    url_pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
    return bool(url_pattern.search(text))

        
        #بخش اعتبار سنجی کلمات و لینک ها
def validate_comment_text(value):
    
        if contains_prohibited_words(value):
            
            raise ValidationError("کامنت شامل محتوای نامناسب میباشد")
        
        if contains_url(value):
            
            raise ValidationError("کامنت حاوی لینک میباشد")

    
    
    





class commentsLikeViewSet(ModelViewSet):
    queryset = commentsLike.objects.all()
    serializer_class = commentsLikeSerializer
    
 
 




class updateUsernameViewSet(ModelViewSet):
    
    queryset = updateUsername.objects.all()
    serializer_class = updateUsernameSerializer
    
    
    
    
    
def update_Username(request):
    
    if request.method == 'POST':
        
        current_username = request.POST['currentUsername']
        
        new_username = request.POST['newUsername']

        try:
            # Check if the currentUsername exists in the database
            user = updateUsername.objects.get(currentUsername=current_username)
            
            # Update the newUsername
            user.newUsername = new_username
            user.save()
            
            return JsonResponse({'message': 'نام کاربری با موفقیت تغییر کرد'})
        
        except updateUsername.DoesNotExist:
            return JsonResponse({'error': 'نام کاربری وجود ندارد'}, status=404)

    
    
   
        
        
        
        
        
        
    
    
    

class updatePasswordViewSet(ModelViewSet):
    
    queryset = updatePassword.objects.all()
    serializer_class = updatePasswordSerializer
    
    
    
    
    
    def updatePassword(request):
        
        if request.method == 'POST':
            
            current_password = request.POST['currentPassword']
            new_password = request.POST['newPassword']
            confirm_password = request.POST['confirmPassword']

            try:
                # Check if the current password matches the one in the database
                user = updatePassword.objects.get(currentPassword=current_password)

                # Check if the new password matches the confirmation password
                if new_password == confirm_password:
                    # Check if the new password meets the minimum length requirement
                    if len(new_password) >= 8:
                        # Update the new password
                        user.newPassword = new_password
                        user.save()
                        return JsonResponse({'message': 'رمز عبور با موفقیت به‌روزرسانی شد'})
                    else:
                        return JsonResponse({'error': 'رمز عبور جدید باید حداقل 8 کاراکتر داشته باشد'}, status=400)
                else:
                    return JsonResponse({'error': 'تأییدیه رمز عبور جدید مطابقت ندارد'}, status=400)

            except updatePassword.DoesNotExist:
                return JsonResponse({'error': 'رمز عبور فعلی اشتباه است'}, status=404)
    
    
    
    
    






class userRegisterViewSet(ModelViewSet):
       
       queryset = User.objects.all()
       serializer_class = userRegisterSerializer
       permission_classes =[IsAuthenticated]
    
       
       
       def userRegister(self, request):
    
            username = request.data.get('username')
            password = request.data.get('password')
            email = request.data.get('email')

            if User.objects.filter(username = username).exists():
                return Response({'message': 'نام کاربری قبلا ثبت شده'}, status=status.HTTP_400_BAD_REQUEST)

            if not email:
                return Response({'message': 'ایمیل صحیح وارد کنید'}, status=status.HTTP_400_BAD_REQUEST)

            if User.objects.filter(email=email).exists():
                
                return Response({'message': 'ایمیل قبلا ثبت شده'}, status=status.HTTP_400_BAD_REQUEST)

            password_pattern = re.compile(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$')
            
            if not password_pattern.match(password):
                return Response({'message': 'رمز عبور باید شامل حداقل 8 کاراکتر و یک عدد باشد'}, status=status.HTTP_400_BAD_REQUEST)

            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()

            if user is not None:
                return Response({'message': 'ثبت نام کاربر موفقیت آمیز بود'})
            else:
                return Response({'message': 'اعتبار سنجی کاربر ناموفق بود'}, status=status.HTTP_401_UNAUTHORIZED)
            
  
  
  
            
        
        
class userLoginViewSet(ModelViewSet):
    
    queryset = userLogin.objects.all()
    
    serializer_class = userLoginSerializer
    
    permission_classes = [IsAuthenticated]
    
    
    
    
def login(self, request):
    
    email = request.data.get('email')
    
    password = request.data.get('password')

    # Check if a user with the provided email exists in the database
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        # Raise an authentication error if the user doesn't exist
        raise AuthenticationFailed('کاربر یافت نشد')

    # Verify the password provided against the user's password
    if not user.check_password(password):
        # Raise an authentication error if the passwords don't match
        raise AuthenticationFailed('ایمیل و رمز عبور مطلابقت ندارند')

    # Log the user in and create a session
    login(request, user)

    return Response({'message': 'با موفقیت وارد شدید'}, status=status.HTTP_200_OK)
    
    
    
    
    
        
    









class allPostsViewSet(ModelViewSet):
    
    queryset = allPosts.objects.all()
    serializer_class = allPostsSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    
    
    def update_comment_counts(self):
     self.numComments = self.comments.count()
     self.numReplies = self.comments.exclude(commentReply=None).count()
     self.save()
    
    
    





class authorsViewSet(ModelViewSet):
    
    queryset = authors.objects.all()
    serializer_class = authorsSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly] 
    
    




    
    
    
    
    
    


class wallpapersViewSet(ModelViewSet):
    
    queryset = wallpapers.objects.all()
    serializer_class = wallpapersSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly] 
    
    
    







class albumsViewSet(ModelViewSet):
    
    queryset = albums.objects.all()
    serializer_class = albumsSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly] 
    
    
    
    




class soundTracksViewSet(ModelViewSet):
    
    queryset = soundTracks.objects.all()
    serializer_class = soundTracksSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly] 
    



   
   

 
 
 
 
   
    
    



















