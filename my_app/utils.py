from datetime import timedelta, date
from .models import Badge, UserBadge, Workout  

# Checks if badges should be awarded to a user based on their activity.
def check_and_award_badges(user):
    today = date.today()

    awarded_ids = set(UserBadge.objects.filter(user=user).values_list('badge_id', flat=True))

    # 5-Day Streak Badge
    streak_days = [today - timedelta(days=i) for i in range(5)]
    streak_workouts = Workout.objects.filter(user=user, date__in=streak_days).values_list('date', flat=True)
    if len(set(streak_workouts)) == 5: # Check if there are workouts for all 5 days
        badge = Badge.objects.get(name="🔥 5-Day Streak")
        if badge.id not in awarded_ids:
            UserBadge.objects.create(user=user, badge=badge)

    # 10 Total Workouts Badge
    if Workout.objects.filter(user=user).count() >= 10: # Check if the user has completed 10 workouts
        badge = Badge.objects.get(name="🌲 Trail Hunter")
        if badge.id not in awarded_ids:
            UserBadge.objects.create(user=user, badge=badge)

    # Pack Leader Badge - Joined a group
    if user.custom_groups.exists():   # Check if the user is part of any group
        badge = Badge.objects.get(name="🐾 Pack Leader")
        if badge.id not in awarded_ids:
            UserBadge.objects.create(user=user, badge=badge)

def ensure_badges_exist():
    badges = [ # List of badges to ensure exist in the database
        {"name": "🔥 5-Day Streak", "description": "Complete 5 days of workouts in a row.", "emoji": "🔥"},
        {"name": "🌲 Trail Hunter", "description": "Complete 10 total workouts.", "emoji": "🌲"},
        {"name": "🐾 Pack Leader", "description": "Joined a wolf pack group!", "emoji": "🐾"},
    ]

    for badge_data in badges: # Create or get each badge
        Badge.objects.get_or_create(
            name=badge_data["name"],
            defaults={
                "description": badge_data["description"],
                "emoji": badge_data["emoji"],
            }
        )