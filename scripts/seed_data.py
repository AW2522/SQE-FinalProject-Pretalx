"""Seed synthetic test data for the SQE project (pretalx baseline).

Run through scripts/seed.sh (which sets PRETALX_DATA_DIR and runs `manage.py shell`).
Idempotent: safe to run twice. Synthetic data only.
"""
import datetime as dt

from django.utils.timezone import now
from django_scopes import scopes_disabled

from pretalx.event.domain.event import initialise_event
from pretalx.event.models import Event, Organiser, Team
from pretalx.person.models import User
from pretalx.person.enums import EmailVerificationState

PASSWORD = "SqeTest-2026!"
ACCOUNTS = {
    "admin": ("admin@sqe.test", "Admin Account"),
    "organiser": ("organiser@sqe.test", "Organiser Account"),
    "reviewer": ("reviewer@sqe.test", "Reviewer Account"),
    "speaker": ("speaker@sqe.test", "Speaker Account"),
}


def get_or_make_user(email, name, **extra):
    user = User.objects.filter(email=email).first()
    if user:
        return user
    user = User.objects.create_user(email=email, name=name, password=PASSWORD)
    user.email_verification_state = EmailVerificationState.VERIFIED
    for key, value in extra.items():
        setattr(user, key, value)
    user.save()
    return user


with scopes_disabled():
    admin = get_or_make_user(*ACCOUNTS["admin"], is_staff=True, is_administrator=True)
    orga_user = get_or_make_user(*ACCOUNTS["organiser"])
    reviewer_user = get_or_make_user(*ACCOUNTS["reviewer"])
    speaker_user = get_or_make_user(*ACCOUNTS["speaker"])

    organiser, _ = Organiser.objects.get_or_create(
        slug="sqe-org", defaults={"name": "SQE Test Organiser"}
    )
    event = Event.objects.filter(slug="sqe-conf").first()
    if event is None:
        today = dt.date.today()
        event = Event.objects.create(
            name="SQE Test Conference",
            slug="sqe-conf",
            organiser=organiser,
            date_from=today + dt.timedelta(days=60),
            date_to=today + dt.timedelta(days=62),
            email="organiser@sqe.test",
            is_public=True,
        )
    initialise_event(event)

    # CfP open for the whole baseline: opens in the past, deadline far in the future.
    cfp = event.cfp
    cfp.deadline = now() + dt.timedelta(days=365)
    cfp.save()

    orga_team, _ = Team.objects.get_or_create(
        organiser=organiser,
        name="Organisers",
        defaults=dict(
            all_events=True,
            can_change_submissions=True,
            can_change_event_settings=True,
            can_change_organiser_settings=True,
            can_change_teams=True,
            can_create_events=True,
        ),
    )
    orga_team.members.add(orga_user)
    review_team, _ = Team.objects.get_or_create(
        organiser=organiser,
        name="Reviewers",
        defaults=dict(all_events=True, is_reviewer=True, can_change_submissions=False),
    )
    review_team.members.add(reviewer_user)

print("Seeded event 'sqe-conf' with accounts:")
for role, (email, _name) in ACCOUNTS.items():
    print(f"  {role:10s} {email}  password: {PASSWORD}")
