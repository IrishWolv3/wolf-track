from datetime import timedelta, date
from django.utils.timezone import now
from .models import Badge, UserBadge, Workout, Group  # Adjust import paths as necessary
from .models import Workout  # or wherever you store workouts

def check_and_award_badges(user):
    today = date.today()

    # Avoid double-awarding
    awarded_ids = set(UserBadge.objects.filter(user=user).values_list('badge_id', flat=True))

    # 1. 5-Day Streak Badge
    streak_days = [today - timedelta(days=i) for i in range(5)]
    streak_workouts = Workout.objects.filter(user=user, date__in=streak_days).values_list('date', flat=True)
    if len(set(streak_workouts)) == 5:
        badge = Badge.objects.get(name="🔥 5-Day Streak")
        if badge.id not in awarded_ids:
            UserBadge.objects.create(user=user, badge=badge)

    # 2. 10 Total Workouts
    if Workout.objects.filter(user=user).count() >= 10:
        badge = Badge.objects.get(name="🌲 Trail Hunter")
        if badge.id not in awarded_ids:
            UserBadge.objects.create(user=user, badge=badge)

    # 3. Pack Leader Badge - Joined a group
    if user.groups.exists():
        badge = Badge.objects.get(name="🐾 Pack Leader")
        if badge.id not in awarded_ids:
            UserBadge.objects.create(user=user, badge=badge)
