from django.contrib.auth.models import User
from django.db import migrations, models


class Migration(migrations.Migration):

	initial = True

	dependencies = [
	]

	def generate_superuser(apps, schema_editor):
		superuser = User.objects.create_superuser(
			username="admin",
			email="",
			password="password")

		superuser.save()

	operations = [
		migrations.RunPython(generate_superuser),
		migrations.CreateModel(
			name="SearchResult",
			fields=[
				(
					"id",
					models.AutoField(
						auto_created=True,
						primary_key=True,
						serialize=False,
						verbose_name="ID",
					),
				),
				("created_at", models.DateTimeField(auto_now_add=True)),
				("modified_at", models.DateTimeField(auto_now=True)),
				("title", models.CharField(max_length=100, db_index=True)),
				("description", models.TextField(blank=True, null=True)),
				(
					"publish_time",
					models.DateTimeField(
						blank=True, null=True, verbose_name="Video Pulish time (UTC)"
					),
				),
				("thumbnail_url", models.URLField(blank=True, null=True)),
				("video_id", models.CharField(unique=True, max_length=100))
			],
			options={"db_table": "search_result"},
		),
		migrations.CreateModel(
			name="APIKey",
			fields=[
				(
					"id",
					models.AutoField(
						auto_created=True,
						primary_key=True,
						serialize=False,
						verbose_name="ID",
					),
				),
				("created_at", models.DateTimeField(auto_now_add=True)),
				("modified_at", models.DateTimeField(auto_now=True)),
				("key", models.TextField(blank=True, null=True)),
				("is_active", models.BooleanField(db_index=True, default=True)),
			],
			options={"db_table": "api_key"}
		)
	]