# Generated by Django 2.1.3 on 2018-12-02 18:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Friendship',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('source', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='friend_source', to='profiles.Profile')),
                ('target', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='friend_target', to='profiles.Profile')),
            ],
            options={
                'ordering': ('-updated_at',),
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='FriendshipInvitation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('invited', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='friendships_friendshipinvitation_invited', to='profiles.Profile')),
                ('inviting', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='friendships_friendshipinvitation_inviting', to='profiles.Profile')),
            ],
            options={
                'ordering': ('-updated_at',),
                'abstract': False,
            },
        ),
    ]