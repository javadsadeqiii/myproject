from django.db import models
from django.contrib.auth.models import User
from django.conf.locale.en import formats as en_formats
from ckeditor.fields import RichTextField
from django.core.validators import FileExtensionValidator
from django.db.models.signals import pre_delete, post_save
from django.dispatch import receiver
from django.utils import timezone
from django.core.exceptions import ValidationError
import re
from django.http import JsonResponse
from django.contrib import messages
from rest_framework.exceptions import AuthenticationFailed
from django.http import HttpResponse



en_formats.DATETIME_FORMAT = 'Y-m-d'




# Create your models here.






class comments(models.Model):
    
    commentText = models.TextField(verbose_name="متن کامنت")
    
    commentReply = models.ForeignKey('self', blank=True, null=True, on_delete= models.CASCADE, related_name='replies',verbose_name="ریپلای")
    # این فیلد یک فیلد خود ارجاع هستش که به هر کامنت اجازه میده یه نظر والد (پاسخ به نظر دیگری ) داشته باشه
    
    createdAt = models.DateTimeField(auto_now_add=True, verbose_name="زمان و تاریخ انتشار کامنت")
    
    userId = models.ForeignKey( User,on_delete=models.CASCADE,related_name='users' ,verbose_name="آیدی کاربر")
    
    postId = models.ForeignKey('allPosts', on_delete=models.CASCADE, related_name='comments', verbose_name= "آیدی پست")
    
    likeCount = models.IntegerField(default=0, verbose_name="تعداد لایک‌ها")
    
    #postsComment = models.ForeignKey('allPosts', on_delete=models.CASCADE, related_name='comments', verbose_name= "آیدی پست")
       #یک رابطه کلید خارجی ایجاد میکند تا هر کامنت مختص یک پست مشخص باشد
       
    
    
    
class Meta:
        
     verbose_name = "کامنت"
     verbose_name_plural = "کامنت ها "






    
class commentsLike(models.Model):
    
    userId = models.ForeignKey(User, on_delete=models.CASCADE, related_name='commentLikes', verbose_name="آیدی کاربر")
    
    commentId = models.ForeignKey(comments, on_delete=models.CASCADE, related_name='likes', verbose_name="آیدی کامنت")
    
    
    
    
    
    
    class Meta:
        
        unique_together = ['user', 'comment'] # هر کاربر فقط یک بار میتواند کامنت را لایک کند

  
    
    class Meta:
        
        verbose_name = "لایک"
        verbose_name_plural = "لایک کامنت ها"

    
    
    

   
    
    
class updateUsername(models.Model):
    
    currentUsername = models.CharField(max_length=150)
    newUsername = models.CharField(max_length=150)
    
    
    
     





class updatePassword(models.Model):
    
    currentPassword = models.CharField(max_length=150)
    newPassword = models.CharField(max_length=150)
    confirmNewPassword = models.CharField(max_length=150)
    
    
    


    
    
    
class userLogin(models.Model):
    
    email = models.EmailField()
    password = models.CharField(max_length=128)
    
    
    
    
    
    
    

class allPostsTags(models.Model):
    
    postTags = models.CharField(max_length=70)
    
    
    
    
    class Meta:
        
        verbose_name = "تگ"
        
        verbose_name_plural ="تگ های جدول اصلی"
        

    def __str__(self):
        return self.postTags
    

    
    
    
    
    
class allPosts(models.Model):
    
    
    
    
    
    PLATFORM_CHOICES = (
        
        
     ('PC', 'PC'),
    
     ('android', "android"),
    
     ('IOS', 'ios'),
    
     ('xbox','xbox'),
    
     ('playStation','playstation'),
    
     ('others','others')
    
    
    )
    

    
    
    

    EVENT_STAGE_CHOICES = (
        
        
     ('E3', 'E3'),
        
     ('gameAwards','gameAwards'),
        
     ('blizzCon', 'blizzCon'),
        
     ('gamesCom','gamesCom'),
        
     ('tokyoGameShow','tokyoGameShow')
        
        
    )
    
    
    

    
    
    
    
    VIDEO_TYPE_CHOICES = (
        
        
        ('gameplays','gamePlays'),
        
        ('trailers','trailers'),
        
        ('blink','blink'),
        
        
    )
    
    
    
    
    title =  models.CharField(max_length=255, verbose_name="عنوان")
    
    slug = models.SlugField(max_length=100,unique=True,verbose_name="آدرس")
    
    content = RichTextField(verbose_name="محتوا")
    
    image = models.ImageField(upload_to='images/',verbose_name="تصویر تک صفحه ", null=True,help_text=" Image file must be lowerthan 200kb, preferably 100kb , Use it in WEBP format, and trasparent")
    
    platforms = models.CharField(max_length=30,null=True,blank=True, choices=PLATFORM_CHOICES,verbose_name='پلتفرم')
    
    date = models.DateTimeField(default=timezone.now)
    
    eventStage = models.CharField(max_length=40,null=True,choices=EVENT_STAGE_CHOICES, blank=True,verbose_name="برگزارکننده رویداد")
    
    videoType = models.CharField(max_length=40,null=True,choices=VIDEO_TYPE_CHOICES, blank=True,verbose_name="تایپ ویدیو")
    
    tags = models.ManyToManyField('allPostsTags',max_length=70,blank=True,verbose_name="تگ ها")
    
    ogImage = models.ImageField(upload_to='images/',help_text= "Image size must be at 1200*630",verbose_name="عکس انتشار")
    
    postSummary = models.TextField(help_text="Summary should be abotu 2 or 3 Sentences",verbose_name="خلاصه")
    
    comments = models.ForeignKey(comments, on_delete=models.CASCADE, related_name='posts', verbose_name= "کامنت ها")
    
    numComments = models.IntegerField(default=0, verbose_name="تعداد کامنت‌ها")
    
    numReplies = models.IntegerField(default=0, verbose_name="تعداد ریپلای‌ها")
    
    isEvent = models.BooleanField(default=False,null=True)
    
    isArticle = models.BooleanField(default=False,null=True)
    
    isVideo = models.BooleanField(default=False,null=True)
    
    isNews = models.BooleanField(default=False,null=True)
    
    isStory = models.BooleanField(default=False,null=True)
    
    
    
    
    def update_comment_counts(self):
     self.numComments = self.comments.count()
     self.numReplies = self.comments.exclude(commentReply=None).count()
     self.save()
    
    
    
    
    

    class Meta:
        
        verbose_name = "جدول پست ها"
        
        verbose_name_plural = "جدول همه پست ها"
        
        
    
    def __str__(self):
        
        return self.title
    
    
    
    
    
    

    
    
    



class authors(models.Model):
    
    
    
    
    EXPERTISE_CHOICES = (
        
    ('programmer', 'برنامه نویس'),
    
    ('contentCreator',"تولید کننده محتوا"),
    
    ('seoExpert',"کارشناس سئو"),
    
    ('designer',"طراح"),
    
    ('marketer',"بازاریاب"),
    
    ('gamer',"گیمر"),
    
    ('gameDesigner',"طراح بازی"),
    
    ('graphist',"گرافیست"),
    
    ('softWareExpert',"کارشناس نرم افزار"),
    
    ('hardWareExpert',"کارشناس سخت افزار")
    
    
    
    )
    
    
    authorName = models.CharField(max_length=60,verbose_name="نام")
    
    username = models.SlugField(verbose_name="آدرس",null=True)
    
    about = models.TextField(verbose_name="درباره نویسنده",default="")
    
    avatar = models.ImageField(default="",verbose_name="آواتار",help_text="avatar file must be lowerthan 100kb and maximum size is : 300*300 pixels")
    
    expertise = models.CharField(max_length=30,null=True,blank=True,choices=EXPERTISE_CHOICES,verbose_name="حوزه فعالیت")
    
   
    
    
    
    
     
    
    class Meta:
        
        verbose_name = "نویسنده"
        
        verbose_name_plural = "نویسندگان "
        
        
        
    
    def __str__(self):
        
        return self.title
    


    
    
    
    

class wallpapersTags(models.Model):
    
    wallpapersTags = models.CharField(max_length=70)
    
    
    
    
    class Meta:
        
        verbose_name = "تگ"
        
        verbose_name_plural ="تگ های والپیپر"
        

    def __str__(self):
        return self.wallpapersTags
    



    
    

class wallpapers(models.Model):
    
    
    DEVICE_CHOICES = (
        
        ('desktop','دسکتاپ'),
        
        ('mobile','موبایل')
    )
    
    
    

    
    RESOLUTION_CHOICES= (
        
        ('normal',"کیفیت معمولی"),
        
        ('highResolution',"کیفیت عالی")
        
    )
    
    
    
    title = models.CharField(max_length=80,verbose_name="عنوان")
    
    slug = models.SlugField(verbose_name="آدرس",unique=True,null=True)
    
    tags = models.ManyToManyField(wallpapersTags,blank=True,verbose_name="تگ ها")
    
    date = models.DateField(auto_now_add=True,verbose_name="تاریخ  انتشار")
    
    thumbnail = models.ImageField(upload_to='images/',verbose_name="تصویر تک صفحه",help_text=" Image file must be lowerthan 200kb, preferably 100kb , Use it in WEBP format and transparent")
    
    device = models.CharField(max_length=60,blank=True,null=True,choices=DEVICE_CHOICES,verbose_name="نوع دستگاه ")
    
    image = models.ImageField(upload_to='wallpapers/',verbose_name="فایل والپیپر",null=True,help_text=" Image file must belowerthan 200kb, preferably 100kb , Use it in WEBP format")
    
    resolution = models.CharField(max_length=50,blank=True,null=True,choices=RESOLUTION_CHOICES,verbose_name="کیفیت")
    
    
    
    


    class Meta:
        
        verbose_name = "والپیپر"
        
        verbose_name_plural ="والپیپرها"
    
    
    def __str__(self):
        return self.title
    
    
    
    
    
    
    

class albumPlatforms(models.Model):
    
    platforms = models.CharField(max_length=70,verbose_name="پلتفرم")
    
    
    
    class Meta:
        
        verbose_name = "پلتفرم آلبوم"
        
        verbose_name_plural ="پلتفرم آلبوم ها"
    
    
    def __str__(self):
        return self.platforms
    
    

    

class albumsTags(models.Model):
    
    
    albumTags = models.CharField(max_length=70,verbose_name="تگ آلبوم")
    
    
    
    class Meta:
        
        verbose_name = "تگ آلبوم"
        
        verbose_name_plural ="تگ های آلبوم"
    
    
    def __str__(self):
        return self.albumTags
        
        





class albums(models.Model):
    
    
    title = models.CharField(max_length=240,verbose_name="عنوان")
    
    date = models.DateField(auto_now_add=True,verbose_name ="تاریخ  انتشار")
    
    image = models.ImageField(upload_to='images/',verbose_name="کاور آلبوم", null=True,help_text=" Image file must be lowerthan 200kb, preferably 100kb , Use it in WEBP format and transparent")
    
    platforms = models.ManyToManyField(albumPlatforms,blank=True)
    
    tags = models.ManyToManyField(albumsTags,verbose_name="تگ ها")
    
    totalFileSize = models.FloatField(null=True,blank=True,verbose_name="حجم فایل")
    
    zipFile = models.FileField(upload_to='zipfiles/',verbose_name="فایل زیپ")
    
    slug = models.SlugField(verbose_name="آدرس",unique=True,null=True)
    
    description = models.TextField(verbose_name="متن توضیحی")
    
    soundTracks = models.ManyToManyField('soundTracks', verbose_name="ساندترک ها")
        
    
    
    
    
    def __str__(self):
        
        return self.title
    
    
    
    class Meta:
        
        verbose_name = "آلبوم"
        
        verbose_name_plural =" آلبوم موسیقی ها"
    
    
    def __str__(self):
        return self.title
    
    
    
    
    
    
    
    
    
    

class soundTracksTags(models.Model):
    
    
    soundTrackTags = models.CharField(max_length=70,verbose_name="تگ موسیقی")
    
    
    
    class Meta:
        
        verbose_name = "تگ موسیقی"
        
        verbose_name_plural ="تگ های موسیقی"
    
    
    def __str__(self):
        return self.soundTrackTags
        
    
    
    
    
    
    
    
    
class soundTracks(models.Model):
    
    
    title = models.CharField(max_length=240, verbose_name="عنوان")
    
    artists = models.CharField(max_length=300, verbose_name="آرتیست ها")
    
    duration = models.DurationField(null=True,blank=True,verbose_name="مدت زمان")
    
    date = models.DateField(auto_now_add=True,verbose_name ="تاریخ  انتشار")
    
    image = image = models.ImageField(upload_to='images/',verbose_name="کاور آلبوم", null=True, help_text=" Image file must be lowerthan 200kb, preferably 100kb , Use it in WEBP format and transparent")
    
    audioFile = models.FileField(upload_to='music/',verbose_name="فایل موسیقی")
    
    fileSize = models.FloatField(null=True,blank=True,verbose_name="حجم فایل")
    
    album = models.CharField(max_length=300,verbose_name="آلبوم")
    
    
    
    
  
    class Meta:
        
        verbose_name = "ساندترک"
        
        verbose_name_plural ="ساندترک ها"
    
    
    def __str__(self):
        return self.title
    
    
    
    
    
    
    
class bazi100Team(models.Model):
    
    
    
    
    
    EXPERTISE_CHOICES = (
        
        
    ('programmer', 'برنامه نویس'),
    
    ('contentCreator',"تولید کننده محتوا"),
    
    ('seoExpert',"کارشناس سئو"),
    
    ('designer',"طراح"),
    
    ('marketer',"بازاریاب"),
    
    ('gamer',"گیمر"),
    
    ('gameDesigner',"طراح بازی"),
    
    ('graphist',"گرافیست"),
    
    ('softWareExpert',"کارشناس نرم افزار"),
    
    ('hardWareExpert',"کارشناس سخت افزار")
    
    
    
    )
    
    
    
    POSITION_CHOICES = (
        
        ('developer','developer'),
        
        ('author','author'),
        
        ('advertisement','advertisement'),
        
        ('cameraman','cameraman'),
        
        ('soicials','socials')
        
        
        
        
    )
    
    
    
    
   
    
    position = models.CharField(max_length=80,choices=POSITION_CHOICES,blank=True,null=True,verbose_name="سمت")
    
    memberName = models.CharField(max_length=80,verbose_name="اسم کاربر")
    
    expertise = models.CharField(max_length=70,choices=EXPERTISE_CHOICES,verbose_name="حرفه")
    
    username = models.CharField(max_length=80,verbose_name="نام کاربری",help_text="Usernames can contain letters(a-z),numbers(0-9),and periods(.).Usernames cannot contain an ampersand(&),equals sings(=),underscore(_),aposterophe('),dash(-),plus sign(+),comma(,),brackets(<,>),or more than one period(.) in a row")
    
    avatar = models.ImageField(upload_to='images/',verbose_name="آواتار",null=True,help_text="Avatar file must be lowerthan 100kb and maximum size is : 300*300 pixels")
    
    linkedin = models.CharField(max_length=80,verbose_name="لینکدین")
    
    instagram = models.CharField(max_length=80,verbose_name="اینستاگرام")
    
    twitter = models.CharField(max_length=80,verbose_name="توییتر")
    
    email = models.EmailField(max_length=80,verbose_name="ایمیل")
    
    about = models.TextField(verbose_name="درباره")
    
    
    
    
    
    class Meta:
        
        verbose_name = "تیم بازی 100"
        
        verbose_name_plural = "تیم بازی 100"
    
    
    def __str__(self):
        return self.memberName 
    
    
    
    
    
    



class advertisements(models.Model):
    
    TYPE_CHOICES = (
        
        ('100A','100A'),
        
        ('100B', '100B'),
        
        ('100C','100C'),
        
        ('100F','100F'),
        
        ('100G','100G'),
        
        ('100H','100H')
        
    )
    
    
    adType= models.CharField(max_length=80,choices=TYPE_CHOICES,verbose_name="نوع تبلیغ")
    
    brandName = models.CharField(max_length=80,verbose_name="نام برند")
    
    brandLink = models.URLField(verbose_name="لینک برند")
    
    adFile = models.FileField(upload_to='filetype/', validators=[FileExtensionValidator(['gif', 'jpg'])], help_text="Uploaded file must be .gif or .jpg",verbose_name="فایل تبلیغ")
    
    textAd = models.TextField(verbose_name="متن تبلیغ")
    
    isTextAd = models.BooleanField(default=False)
    
    startsDate = models.DateField(verbose_name="تاریخ شروع تبلیغ")
    
    endsDate = models.DateField(verbose_name="تاریخ پایان تبلیغ")
    
    shouldDelete = models.BooleanField(default=False)
    

    
    
    class Meta:
        verbose_name = "تبلیغ"
        verbose_name_plural = "تبلیغات"
    
    def __str__(self):
        return self.brandName
    
    
    
    
    
@receiver(post_save, sender=advertisements)

def delete_ad(sender, instance, created,**kwargs):
    
     if not created and instance.endsDate <= timezone.now().date():
         
        instance.delete()
        
        post_save.connect(delete_ad, sender= advertisements)
        
        
        
        
        
        


        

    
    
    
    

    
    
    
    
    
    
    
    

    
        

    
    
    
        
  
     
      
   


    

     
