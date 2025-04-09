@receiver(post_save, sender=UserAccount)
def create_profile(sender, instance, created, **kwargs):
    if created:
        if instance.role == 'student':
            Student.objects.create(account=instance)
        elif instance.role == 'teacher':
            Teacher.objects.create(account=instance)
