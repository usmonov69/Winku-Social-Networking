from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile, Relationship


@receiver(post_save, sender=User)
def post_save_create_user(sender, instance, created, **kvargs):
	# print("sender", sender)
	# print("instance", instance)
	if created:
		Profile.objects.create(user=instance)


@receiver(post_save, sender=Relationship)
def post_save_relationship(sender, instance, created, **kwargs):
	sender_ = instance.sender
	receiver_ = instance.receiver
	if instance.status == 'accepted':
		sender_.friends.add(receiver_.user)
		receiver_.friends.add(sender_.user)
		sender_.save()
		receiver_.save()


@receiver(pre_delete, sender=Relationship)
def pre_delete_remove_friends(sender, instance, **kwargs):
	sender = instance.sender
	receiver = instance.receiver
	sender.friends.remove(receiver.user)
	receiver.friends.remove(sender.user)
	sender.save()
	receiver.save()
