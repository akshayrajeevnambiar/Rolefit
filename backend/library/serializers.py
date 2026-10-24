"""JSON for résumés and job descriptions.

The owner is not a field. The view sets it from the signed-in account,
so a request cannot hand a row to someone else.
"""

from rest_framework import serializers

from library.models import JobDescription, Resume


def require_paste(value: str) -> str:
    if not value.strip():
        raise serializers.ValidationError("Paste the text before saving.")
    return value


class ResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = ["id", "title", "text", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]

    def validate_title(self, value: str) -> str:
        return value.strip()

    def validate_text(self, value: str) -> str:
        return require_paste(value)


class JobDescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobDescription
        fields = [
            "id",
            "company",
            "role",
            "text",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def validate_company(self, value: str) -> str:
        company = value.strip()
        if not company:
            raise serializers.ValidationError("Name the company.")
        return company

    def validate_role(self, value: str) -> str:
        role = value.strip()
        if not role:
            raise serializers.ValidationError("Name the role.")
        return role

    def validate_text(self, value: str) -> str:
        return require_paste(value)
