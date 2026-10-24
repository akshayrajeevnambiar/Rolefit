"""An analysis may only join rows that belong to the same account."""

import pytest
from django.core.exceptions import ValidationError
from django.db import IntegrityError

from accounts.models import User
from library.models import Analysis, JobDescription, Resume

pytestmark = pytest.mark.django_db

PASSWORD = "a-long-test-password-1"


def account(email: str) -> User:
    return User.objects.create_user(email=email, password=PASSWORD)


def resume_for(owner: User, text: str = "Git") -> Resume:
    return Resume.objects.create(owner=owner, text=text)


def description_for(owner: User, text: str = "Python") -> JobDescription:
    return JobDescription.objects.create(
        owner=owner,
        company="Northwind Health",
        role="Backend engineer",
        text=text,
    )


def test_analysis_rejects_another_accounts_resume() -> None:
    alice = account("alice@example.com")
    bob = account("bob@example.com")
    analysis = Analysis(
        owner=bob,
        resume=resume_for(alice),
        job_description=description_for(bob),
    )
    with pytest.raises(ValidationError):
        analysis.save()
    assert Analysis.objects.count() == 0


def test_analysis_rejects_another_accounts_description() -> None:
    alice = account("alice@example.com")
    bob = account("bob@example.com")
    analysis = Analysis(
        owner=alice,
        resume=resume_for(alice),
        job_description=description_for(bob),
    )
    with pytest.raises(ValidationError):
        analysis.save()
    assert Analysis.objects.count() == 0


def test_analysis_stores_one_accounts_own_pair() -> None:
    alice = account("alice@example.com")
    analysis = Analysis(
        owner=alice,
        resume=resume_for(alice),
        job_description=description_for(alice),
    )
    analysis.save()
    assert Analysis.objects.filter(owner=alice).count() == 1


def test_one_pair_cannot_be_stored_twice() -> None:
    alice = account("alice@example.com")
    resume = resume_for(alice)
    description = description_for(alice)
    Analysis.objects.create(owner=alice, resume=resume, job_description=description)
    with pytest.raises(IntegrityError):
        Analysis.objects.create(
            owner=alice,
            resume=resume,
            job_description=description,
        )


def test_deleting_a_resume_deletes_its_analysis() -> None:
    alice = account("alice@example.com")
    resume = resume_for(alice)
    Analysis.objects.create(
        owner=alice,
        resume=resume,
        job_description=description_for(alice),
    )
    resume.delete()
    assert Analysis.objects.count() == 0
