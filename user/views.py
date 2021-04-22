from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.shortcuts import redirect
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout
from .models import Album, Cart, Category, Music, Group_music, Rate_music, Rate_album, Cart, Bill, UserInfotmation
from django.db.models import F
from django.db import connection
# Create your views here.
from django.http import HttpResponse
import base64
from django.core.files.base import ContentFile
def login(request):
	page = request.GET.get("page")
	return render(request, 'login.html', {"page":page})
def signUpPage(request):
	page = request.GET.get("page")
	return render(request, 'Sign up.html', {"page":page})
def index(request):
	if request.user.is_authenticated:
		return render(request, 'index.html', DataIndexUser())
	else:
		if request.method == 'POST':
		    username = request.POST.get('username','')
		    password = request.POST.get('password','')
		    page = request.POST.get('page','')
		    user = authenticate(username=username, password=password)
		    if(user is not None):
		    	request.session.set_expiry(86400)
		    	auth_login(request, user)
		    	return redirect(page)
		    else:
		    	error = {'error': 'The account or password is incorrect, please try again', "page":page}
		    	return render(request, 'login.html', error)
		else:
			return render(request, 'index.html', DataIndex())
def logout_view(request):
    logout(request)
    return redirect("/")
def search(request):
	if request.user.is_authenticated:
		search = request.POST.get('search','')
		music = Music.objects.filter(Name__icontains = search)
		rate_music = Rate_music.objects.filter(UserID = request.user.id, isLike = True)
		album = Album.objects.filter(UserID_id = request.user.id)
		music = {'music' : music, 'rate_music':rate_music, 'toolbar' : 'user/toolbarUser.html', 'album':album}
		return render(request, 'searchRe.html', music)
	else:
		search = request.POST.get('search','')
		music = Music.objects.filter(Name__icontains = search)
		rate_music = Rate_music.objects.filter(UserID = request.user.id, isLike = True)
		music = {'music' : music, 'rate_music':rate_music, 'toolbar' : 'toolbar.html'}
		return render(request, 'searchRe.html', music)
def createAlbumInterface(request):
	if request.user.is_authenticated:
		page = request.GET.get('page','')
		AllAlbum = {'toolbar' : 'user/toolbarUser.html', "page":page}
		return render(request, 'createAlbumInterface.html', AllAlbum)
	else:
		AllAlbum = {'toolbar' : 'toolbar.html'}
		return render(request, 'createAlbumInterface.html', AllAlbum)
def createAlbum(request):
	if request.user.is_authenticated:
		if request.method == 'POST':
			page = request.POST.get('page','')
			Name = request.POST.get('Name','')
			Description = request.POST.get('Description','')
			ImageAlbum = request.FILES['ImageAlbum']
			Album.objects.create(UserID_id = request.user.id, Name = Name, Description = Description, Public = False, Like = 0, Price = 0, Image  = ImageAlbum)
			return redirect(page)
		else:
			return render(request, 'login.html')
	else:
		return render(request, 'login.html')
def ViewAlbum(request):
	if request.user.is_authenticated:
		album = Album.objects.filter(Public = True)
		rate_album = Rate_album.objects.filter(UserID = request.user.id, isLike = True)
		AllAlbum = {'album' : album,'rate_album':rate_album, 'toolbar' : 'user/toolbarUser.html', 'title':'All album'}
		return render(request, 'album.html', AllAlbum)
	else:
		album = Album.objects.filter(UserID_id = None)
		AllAlbum = {'album' : album, 'yourAlbum':request.user.id, 'toolbar' : 'toolbar.html', 'title':'All album'}
		return render(request, 'album.html', AllAlbum)
def YourAlbum(request):
	if request.user.is_authenticated:
		album = Album.objects.filter(UserID_id = request.user.id)
		rate_album = Rate_album.objects.filter(UserID = request.user.id, isLike = True)
		AllAlbum = {'album' : album, 'rate_album':rate_album, 'toolbar' : 'user/toolbarUser.html', 'title':'Your Album'}
		return render(request, 'album.html', AllAlbum)
	else:
		page = request.GET.get("page")
		return render(request, 'login.html', {"page":page})
def ViewHotAlbum(request):
	if request.user.is_authenticated:
		album = Album.objects.filter(UserID_id = None).order_by(F('Like').desc())[:10]
		rate_album = Rate_album.objects.filter(UserID = request.user.id, isLike = True)
		AllAlbum = {'album' : album, 'toolbar' : 'user/toolbarUser.html', 'title':'Hot album', 'rate_album':rate_album}
		return render(request, 'album.html', AllAlbum)
	else:
		album = Album.objects.filter(UserID_id = None).order_by(F('Like').desc())[:10]
		AllAlbum = {'album' : album, 'toolbar' : 'toolbar.html', 'title':'Hot album'}
		return render(request, 'album.html', AllAlbum)
def NewAlbum(request):
	if request.user.is_authenticated:
		album = Album.objects.filter(UserID_id = None).order_by(F('id').asc())[:10]
		rate_album = Rate_album.objects.filter(UserID = request.user.id, isLike = True)
		AllAlbum = {'album' : album, 'toolbar' : 'user/toolbarUser.html', 'title':'New album', 'rate_album':rate_album}
		return render(request, 'album.html', AllAlbum)
	else:
		album = Album.objects.filter(UserID_id = None).order_by(F('id').asc())[:10]
		AllAlbum = {'album' : album, 'toolbar' : 'toolbar.html', 'title':'New album'}
		return render(request, 'album.html', AllAlbum)
def ViewCart(request):
	if request.user.is_authenticated:
		album = []
		with connection.cursor() as cursor:
			cursor.execute(
				"select user_album.Name, user_album.Price, user_album.Image, user_album.id, user_album.Like FROM user_album INNER JOIN user_cart on user_cart.AlbumID_id = user_album.id INNER JOIN auth_user ON user_cart.UserID_id = auth_user.id WHERE auth_user.id = '%s'" ,
				[request.user.id]
			)
			album = (cursor.fetchall())
		return render(request, 'user/Cart.html', {'cart':album})
	else:
		return render(request, 'login.html')
def ViewMusic(request):
	if request.user.is_authenticated:
		music = Music.objects.all().order_by(F('id').asc())
		rate_music = Rate_music.objects.filter(UserID = request.user.id, isLike = True)
		album = Album.objects.filter(UserID_id = request.user.id)
		music = {'music' : music, 'rate_music':rate_music, 'toolbar' : 'user/toolbarUser.html', 'album':album}
		return render(request, 'music.html', music)
	else:
		music = Music.objects.all().order_by(F('id').asc())
		rate_music = Rate_music.objects.filter(UserID = request.user.id, isLike = True)
		music = {'music' : music, 'rate_music':rate_music, 'toolbar' : 'toolbar.html'}
		return render(request, 'music.html', music)
def MusicChart(request):
	if request.user.is_authenticated:
		music = Music.objects.all().order_by("-Like")
		rate_music = Rate_music.objects.filter(UserID = request.user.id, isLike = True)
		album = Album.objects.filter(UserID_id = request.user.id)
		music = {'music' : music, 'rate_music':rate_music, 'toolbar' : 'user/toolbarUser.html', 'album':album}
		return render(request, 'MusicChart.html', music)
	else:
		music = Music.objects.all().order_by("-Like")
		rate_music = Rate_music.objects.filter(UserID = request.user.id, isLike = True)
		music = {'music' : music, 'rate_music':rate_music, 'toolbar' : 'toolbar.html'}
		return render(request, 'MusicChart.html', music)
def addMusic(request, idMusic, idAlbum):
	if request.user.is_authenticated:
		if(len(Group_music.objects.filter(Music_ID = idMusic, AlbumID = idAlbum)) == 0):
			Group_music.objects.create(Music_ID_id  = idMusic, AlbumID_id = idAlbum)
			priceMusic = Music.objects.filter(id = idMusic)[0].Price
			priceAlbum = Album.objects.filter(id = idAlbum)[0].Price
			Album.objects.filter(id = idAlbum).update(Price = int(priceAlbum) + int(priceMusic))
			response = HttpResponse()
			response.writelines('Add songs successfully')
			return response
		else:
			response = HttpResponse()
			response.writelines('The song already exists in the album')
			return response
	else:
		return render(request, 'login.html')
def deleteMusic(request, idMusic, idAlbum):
	if request.user.is_authenticated:
		priceMusic = Music.objects.filter(id = idMusic)[0].Price
		priceAlbum = Album.objects.filter(id = idAlbum)[0].Price
		Album.objects.filter(id = idAlbum).update(Price = int(priceAlbum) - int(priceMusic))
		Group_music.objects.filter(Music_ID = idMusic, AlbumID = idAlbum).delete()
		response = HttpResponse()
		response.writelines('Successfully deleted the song')
		return response
	else:
		return render(request, 'login.html')
def viewMusicInAlbum(request, id):
	if request.user.is_authenticated:
		music = []
		with connection.cursor() as cursor:
			cursor.execute(
				"SELECT user_music.Image, user_music.Name, user_music.Singer, user_music.Price, user_music.Like, user_music.Description, user_music.Music, user_music.id, user_album.Image, user_album.UserID_id, user_album.id, user_album.Name, user_album.Like  FROM user_music INNER JOIN user_group_music on user_group_music.Music_ID_id = user_music.id INNER JOIN user_album ON user_album.id = user_group_music.AlbumID_id WHERE user_album.id = '%s'" ,
				[id]
			)
			music.append(cursor.fetchall())
		album = Album.objects.filter(UserID_id = request.user.id)
		rate_music = Rate_music.objects.filter(UserID = request.user.id, isLike = True)
		rate_album = Rate_album.objects.filter(UserID = request.user.id, isLike = True)
		Allmusic = {'music' : music[0], 'toolbar' : 'user/toolbarUser.html', 'album':album,'rate_music':rate_music, "rate_album":rate_album}
		return render(request, 'viewMusicInAlbum.html', Allmusic)
	else:
		music = []
		with connection.cursor() as cursor:
			cursor.execute(
				"SELECT user_music.Image, user_music.Name, user_music.Singer, user_music.Price, user_music.Like, user_music.Description, user_music.Music, user_music.id, user_album.Image, user_album.UserID_id, user_album.id, user_album.Name, user_album.Like FROM user_music INNER JOIN user_group_music on user_group_music.Music_ID_id = user_music.id INNER JOIN user_album ON user_album.id = user_group_music.AlbumID_id WHERE user_album.id = '%s'" ,
				[id]
			)
			music.append(cursor.fetchall())
		Allmusic = {'music' : music[0], 'toolbar' : 'toolbar.html'}
		return render(request, 'viewMusicInAlbum.html', Allmusic)
def deleteYourAlbum(request,id):
	if request.user.is_authenticated:
		Album.objects.filter(id = id).delete()
		response = HttpResponse()
		response.writelines('Delete')
		return response
	else:
		return render(request, 'login.html')
def LikeMusic(request, id):
	if request.user.is_authenticated:
		validateMusic = Rate_music.objects.filter(UserID_id = request.user.id, Music_ID_id = id)
		if len(validateMusic) > 0:
			if len(Rate_music.objects.filter(UserID_id = request.user.id, Music_ID_id = id, isLike = True)) > 0:
				Rate_music.objects.filter(UserID_id = request.user.id, Music_ID_id = id).update(isLike = False)
				like = Music.objects.filter(id = id)[0].Like
				like = like - 1
				Music.objects.filter(id = id).update(Like = like)
				response = HttpResponse()
				response.writelines('disLike')
				return response
			else:
				Rate_music.objects.filter(UserID_id = request.user.id, Music_ID_id = id).update(isLike = True)
				like = Music.objects.filter(id = id)[0].Like
				like = like + 1
				Music.objects.filter(id = id).update(Like = like)
				response = HttpResponse()
				response.writelines('disLike')
				return response
		else:
			Rate_music.objects.create(Music_ID_id = id, UserID_id = request.user.id, isLike = True)
			like = Music.objects.filter(id = id)[0].Like
			like = like + 1
			Music.objects.filter(id = id).update(Like = like)
			response = HttpResponse()
			response.writelines('like')
			return response
	else:
		response = HttpResponse()
		response.writelines('Login')
		return response
def LikeAlbum(request, id):
	if request.user.is_authenticated:
		validateAlbum = Rate_album.objects.filter(UserID_id = request.user.id, AlbumID_id = id)
		if len(validateAlbum) > 0:
			if len(Rate_album.objects.filter(UserID_id = request.user.id, AlbumID_id = id, isLike = True)) > 0:
				Rate_album.objects.filter(UserID_id = request.user.id, AlbumID_id = id).update(isLike = False)
				like = Album.objects.filter(id = id)[0].Like
				like = like - 1
				Album.objects.filter(id = id).update(Like = like)
				response = HttpResponse()
				response.writelines('disLike')
				return response
			else:
				Rate_album.objects.filter(UserID_id = request.user.id, AlbumID_id = id).update(isLike = True)
				like = Album.objects.filter(id = id)[0].Like
				like = like + 1
				Album.objects.filter(id = id).update(Like = like)
				response = HttpResponse()
				response.writelines('disLike')
				return response
		else:
			Rate_album.objects.create(AlbumID_id = id, UserID_id = request.user.id, isLike = True)
			like = Album.objects.filter(id = id)[0].Like
			like = like + 1
			Album.objects.filter(id = id).update(Like = like)
			response = HttpResponse()
			response.writelines('like')
			return response
	else:
		response = HttpResponse()
		response.writelines('Login')
		return response
def addCart(request, id):
	if request.user.is_authenticated:
		NumberAlbum = Cart.objects.filter(UserID_id = request.user.id, AlbumID_id = id)
		if len(NumberAlbum) == 0:
			Cart.objects.create(UserID_id = request.user.id, AlbumID_id = id)
			response = HttpResponse()
			response.writelines('Add cart successfully')
			return response
		else:
			response = HttpResponse()
			response.writelines('The album already in the cart')
			return response	
	else:
		response = HttpResponse()
		response.writelines('Login')
		return response
def deleteCart(request, id):
	if request.user.is_authenticated:
		Cart.objects.filter(UserID_id = request.user.id, AlbumID_id = id).delete();
		return redirect('/ViewCart')
	else:
		return render(request, 'login.html')

def bill(request, totalPrice):
	if request.user.is_authenticated:
		albumID = request.GET.getlist('albumID[]','')
		album = []
		for i in albumID:
			album.append(Album.objects.filter(id = i))
		data = {'album':album, 'toolbar' : 'user/toolbarUser.html', 'totalPrice':totalPrice}
		return render(request, 'user/bill.html', data)
	else:
		return render(request, 'login.html')
def saveBill(request):
	if request.user.is_authenticated:
		albumID = request.POST.getlist('Album','')
		for i in albumID:
			Cart.objects.filter(AlbumID_id = i, UserID_id =request.user.id).delete()
		bill = request.POST.get('image')
		format, imgstr = bill.split(';base64,') 
		ext = format.split('/')[-1]
		data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
		Bill.objects.create(UserID_id = request.user.id, Bill = data, Shipped = False)
		return redirect('/')
	else:
		return render(request, 'login.html')
def Contact(request):
	if request.user.is_authenticated:
		music = {'toolbar' : 'user/toolbarUser.html'}
		return render(request, 'contact.html', music)
	else:
		music = {'toolbar' : 'toolbar.html'}
		return render(request, 'contact.html', music)
def MusicPurchaseHistory(request):
	if request.user.is_authenticated:
		MusicPurchaseHistory = Bill.objects.filter(UserID_id = request.user.id).order_by("-Date")
		return render(request, 'user/MusicPurchaseHistory.html', {"MusicPurchaseHistory":MusicPurchaseHistory})
	else:
		return redirect('/login')
def DataIndexUser():
	newAlbum = Album.objects.filter(UserID_id = None).order_by(F('id').asc())[:4]
	hotAlbum = Album.objects.filter(UserID_id = None).order_by(F('Like').desc())[:4]
	Allmusic = {'newAlbum': newAlbum, "hotAlbum":hotAlbum, 'toolbar' : 'user/toolbarUser.html'}
	return Allmusic
def DataIndex():
	newAlbum = Album.objects.filter(UserID_id = None).order_by(F('id').asc())[:4]
	hotAlbum = Album.objects.filter(UserID_id = None).order_by(F('Like').desc())[:4]
	Allmusic = {'newAlbum': newAlbum, "hotAlbum":hotAlbum, 'toolbar' : 'toolbar.html'}
	return Allmusic
def signUpInterface(request):
	return render(request, 'Sign up.html')
def signUp(request):
	if request.method == 'POST':
	    username = request.POST.get('username','')
	    password = request.POST.get('password','')
	    email = request.POST.get('email','')
	    user = User.objects.create(username=username, email = email, is_superuser = False, is_staff = False, is_active = True)
	    user.set_password(password)
	    user.save()
	    user = authenticate(username=username, password=password)
	    if(user is not None):
	    	request.session.set_expiry(86400)
	    	auth_login(request, user)
	    	return redirect('/')
	    else:
	    	return render(request, 'login.html')
	else:
		return render(request, 'index.html', DataIndex())
def ChangePasswordInterface(request):
	return render(request, 'ChangePassword.html')
def ChangePassword(request):
	if request.user.is_authenticated:
		if request.method == 'POST':
			password = request.POST.get('password','')
			oldPassword = request.POST.get('oldPassword','')
			user = authenticate(username=request.user.username, password=oldPassword)
			if(user is not None):
				user = User.objects.get(id = request.user.id)
				user.set_password(password)
				user.save()
				user = authenticate(username=request.user.username, password=password)
				if(user is not None):
					request.session.set_expiry(86400)
					auth_login(request, user)
					return redirect('/')
				else:
					return redirect('/login')
			else:
				return render(request, 'ChangePassword.html', {"error":"Old password is incorrect"})
		else:
			return render(request, 'index.html', DataIndex())
	else:
		return redirect('/login')
def ViewProfile(request):
	if request.user.is_authenticated:
		userInfotmation = UserInfotmation.objects.filter(UserID_id = request.user.id)
		if(len(userInfotmation) == 0):
			return render(request, 'profile.html')
		else:
			user = User.objects.get(id = request.user.id)
			userInfotmation = UserInfotmation.objects.get(UserID_id = request.user.id)
			print(userInfotmation)
			data = {'user':user, 'userInfotmation':userInfotmation}
			return render(request, 'profile.html', data)
	else:
		return redirect('/login')
def saveInformation(request):
	if request.user.is_authenticated:
		Name = request.POST.get('Name','')
		DOB = request.POST.get('DOB','')
		Gender = request.POST.get('Gender','')
		Address = request.POST.get('Address','')
		Email = request.POST.get('Email','')
		Phone = request.POST.get('Phone','')
		Username = request.POST.get('Username','')
		# Password = request.POST.get('Password','')
		userInfotmation = UserInfotmation.objects.filter(UserID_id = request.user.id)
		if(len(userInfotmation) == 0):
			UserInfotmation.objects.create(UserID_id = request.user.id, Name = Name, DateofBirth = DOB, Gender = Gender, Address = Address, Phone = Phone)
			return redirect('/ViewProfile')
		else:
			UserInfotmation.objects.filter(UserID_id = request.user.id).update(UserID_id = request.user.id, Name = Name, DateofBirth = DOB, Gender = Gender, Address = Address, Phone = Phone)
			user = User.objects.get(id = request.user.id)
			user.username = Username
			user.email = Email
			# user.set_password(Password)
			# user.save()
			# print(Gender)
			# user = authenticate(username=request.user.username, password=Password)
			# if(user is not None):
			# 	request.session.set_expiry(86400)
			# 	auth_login(request, user)
			# 	user = User.objects.get(id = request.user.id)
			# 	userInfotmation = UserInfotmation.objects.filter(UserID_id = request.user.id)
			# 	data = {'user':user, 'userInfotmation':userInfotmation}
			# 	return redirect('/ViewProfile')
			# else:
			# 	return render(request, 'login.html')
			return redirect('/ViewProfile')
	else:
		return redirect('/login')
def CheckLogin(request):
	if request.user.is_authenticated:
		response = HttpResponse()
		response.writelines('Logged')
		return response
	else:
		response = HttpResponse()
		response.writelines('Login')
		return response

