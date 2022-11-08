from rest_framework import serializers
from .models import CustomUser, Transaction, Category


class CustomUserSerializers(serializers.ModelSerializer):
    password2 = serializers.CharField()

    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'password', 'password2']

    def save(self, *args, **kwargs):
        user = CustomUser(
            email=self.validated_data['email'],
            username=self.validated_data['username'],
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        if password != password2:
            raise serializers.ValidationError({password: "Пароль не совпадает"})
        user.set_password(password)
        user.save()
        return user


class CreateCategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name', 'id']

    def save(self, *args, **kwargs):
        request = self.context['request']
        category = self.Meta.model(**self.validated_data)
        category.save()
        if request.method == 'POST':
            user = CustomUser.objects.get(id=request.user.id)
            user.categories.add(category)
        return category


class CategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name', 'id']


class CustomUserSerializers1(serializers.ModelSerializer):
    count = serializers.SerializerMethodField(method_name='get_count')
    last_transactions = serializers.SerializerMethodField(method_name='get_last_transactions')
    categories = CategorySerializers(many=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'password', 'username', 'email', 'date_creation', 'date_update', 'payments_balance',
                  'categories', 'count', 'last_transactions']

    def get_count(self, obj):
        transactions = Transaction.objects.filter(user__id=obj.id)
        return transactions.count()

    def get_last_transactions(self, obj):
        transactions = Transaction.objects.filter(user__id=obj.id).order_by('-date_creation', 'time')[:5]
        serializer = TransactionSerializers(many=True, data=transactions)
        serializer.is_valid()
        return serializer.data


class ViewCustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'password', 'username', 'email', 'date_creation', 'date_update', ]


class TransactionSerializers(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['summary', 'description', 'organization', 'category']

    def save(self, *args, **kwargs):
        request = self.context['request']
        user = CustomUser.objects.get(id=request.user.id)
        if not self.validated_data['category'] in user.categories.all():
            raise Exception("Incorrect category")
        transaction = self.Meta.model(user=user, **self.validated_data)
        transaction.save()
        return transaction
