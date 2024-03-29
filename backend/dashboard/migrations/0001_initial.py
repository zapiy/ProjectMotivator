# Generated by Django 3.2.16 on 2022-10-26 06:25

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BotUserModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('platform', models.CharField(choices=[('TG', 'Telegram'), ('SLC', 'Slack')], db_index=True, default='TG', max_length=15)),
                ('internal_id', models.CharField(db_index=True, max_length=100)),
                ('login', models.CharField(max_length=100, null=True)),
                ('full_name', models.CharField(max_length=150, null=True)),
                ('user_token', models.UUIDField(db_index=True, default=uuid.uuid4, unique=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'bot_users',
            },
        ),
        migrations.CreateModel(
            name='BotWebChatProducts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('REAL', 'Real'), ('VIRTUAL', 'Virtual')], default='REAL', max_length=20)),
                ('image', models.ImageField(upload_to='images/motivator/')),
                ('name', models.CharField(max_length=200)),
                ('price', models.PositiveIntegerField(default=0)),
                ('count', models.PositiveIntegerField(default=0)),
                ('promo_codes', models.TextField(null=True)),
                ('is_infinity', models.BooleanField(default=False)),
                ('owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='auth.usermodel')),
            ],
            options={
                'db_table': 'web_shop_products',
            },
        ),
        migrations.CreateModel(
            name='BotWebChatShopHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_issued', models.BooleanField(default=False)),
                ('buy_time', models.DateTimeField(auto_now=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sales_history', to='dashboard.botwebchatproducts')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shop_history', to='dashboard.botusermodel')),
            ],
            options={
                'db_table': 'web_shop_history',
            },
        ),
        migrations.CreateModel(
            name='BotUserBalanceModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state', models.CharField(choices=[('NORMAL', 'Normal'), ('LEAVE', 'Leave')], default='NORMAL', max_length=15)),
                ('current_balance', models.IntegerField(default=10)),
                ('safe_balance', models.IntegerField(default=0)),
                ('clear_time', models.DateTimeField(null=True)),
                ('binded', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bot_bills', to='auth.usermodel')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='balances', to='dashboard.botusermodel')),
            ],
            options={
                'db_table': 'bot_user_balance',
            },
        ),
        migrations.CreateModel(
            name='BotTransferHistoryModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField(default=1)),
                ('transfer_time', models.DateTimeField(auto_now_add=True)),
                ('u_from', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='spends', to='dashboard.botuserbalancemodel')),
                ('u_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='refills', to='dashboard.botuserbalancemodel')),
            ],
            options={
                'db_table': 'bot_transfer_history',
            },
        ),
        migrations.CreateModel(
            name='BotChatModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('platform', models.CharField(choices=[('TG', 'Telegram'), ('SLC', 'Slack')], db_index=True, default='TG', max_length=15)),
                ('internal_id', models.CharField(db_index=True, max_length=100)),
                ('full_name', models.CharField(max_length=170, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('admin', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='bot_chats', to='auth.usermodel')),
                ('users', models.ManyToManyField(related_name='chats', to='dashboard.BotUserModel')),
            ],
            options={
                'db_table': 'bot_chats',
            },
        ),
    ]
