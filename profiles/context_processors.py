from .models import Profile, Relationship 


def profile_pic(request):
	if request.user.is_authenticated:
		profile = Profile.objects.get(user=request.user)
		pic = profile.avatar
		return {'picture':pic}
	return {}


def invatations_received_no(request):
	if request.user.is_authenticated:
		profile = Profile.objects.get(user=request.user)
		qs_count = Relationship.objects.invatations_received(profile).count()
		return {'invites_num':qs_count}
	return {}