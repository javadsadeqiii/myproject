from typing import Self
from django.contrib import admin
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin




# Register your models here.






class commentsAdmin(admin.ModelAdmin):
    
    list_display = ('id','userId','postId','likeCount')
    
    ordering = ('id',)
    

admin.site.register(comments, commentsAdmin)





class commentsLikeAdmin(admin.ModelAdmin):
    
    list_display = ('userId','commentId')
    ordering = ('id',)
    
admin.site.register(commentsLike,commentsLikeAdmin)










    
class CustomUserAdmin(admin.ModelAdmin):
    
       list_display = ('id', 'username', 'email', 'first_name', 'last_name', 'date_joined', 'is_staff')
       
       ordering = ('id',)
       
       
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

  






class authorsAdmin(admin.ModelAdmin):
    
    list_display = ('authorName','id','username','expertise','about')

    list_filter = (['authorName'])
    
    search_fields = ('username',)
    
    ordering = ('id',)
    
    

admin.site.register(authors, authorsAdmin)




    
    
    
    
    

class allPostsAdmin(admin.ModelAdmin):
    
    
    list_display = ('id','title','slug','platforms','date')
    
    list_filter = ('title','id')
    
    ordering = ('id',)
    



admin.site.register(allPosts, allPostsAdmin)









class allPostsTagsAdmin(admin.ModelAdmin):
    
    list_display = ('postTags',)
    
    
admin.site.register(allPostsTags, allPostsTagsAdmin)










class wallpapersTagsAdmin(admin.ModelAdmin):
    
    list_display = ('wallpapersTags',)
    
    
admin.site.register(wallpapersTags, wallpapersTagsAdmin)










class wallpapersAdmin(admin.ModelAdmin):
    
    
    
    list_display = ('title','id','device','resolution','date')
    
    list_filter = ('title','id')
    
    ordering = ('id',)
    


admin.site.register(wallpapers, wallpapersAdmin)











class soundTracksTagsAdmin(admin.ModelAdmin):
    
    list_display = ('soundTrackTags',)


admin.site.register(soundTracksTags, soundTracksTagsAdmin)








class soundTracksAdmin(admin.ModelAdmin):
    
    
    
    list_display = ('title','id','artists','album','date')
    
    list_filter = ('title','id')
    
    ordering = ('id',)
    


admin.site.register(soundTracks, soundTracksAdmin)








class albumPlatformsAdmin(admin.ModelAdmin):
    
    list_display = ('platforms',)


admin.site.register(albumPlatforms, albumPlatformsAdmin)












class albumsTagsAdmin(admin.ModelAdmin):
    
    list_display = ('albumTags',)
    
    
admin.site.register(albumsTags, albumsTagsAdmin)









class albumsAdmin(admin.ModelAdmin):
    
    
    
    list_display = ('title','id','date','slug','date')
    
    list_filter = ('title','id')
    
    ordering = ('id',)
    


admin.site.register(albums, albumsAdmin)









class bazi100TeamAdmin(admin.ModelAdmin):
    
    
    
    list_display = ('id','position','email','expertise')
    
    list_filter = ('id',)
    
    ordering = ('id',)
    


admin.site.register(bazi100Team, bazi100TeamAdmin)










class advertisementsAdmin(admin.ModelAdmin):
    
    
    
    list_display = ('adType','brandName','brandLink','startsDate','endsDate')
    
    list_filter = ('endsDate',)
    
    ordering = ('endsDate',)
    


admin.site.register(advertisements, advertisementsAdmin)


