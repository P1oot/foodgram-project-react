from .models import User
from recipes.models import Recipe
from rest_framework import serializers, validators


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        validators=[validators.UniqueValidator(queryset=User.objects.all())],
        required=True,
    )
    username = serializers.CharField(
        validators=[validators.UniqueValidator(queryset=User.objects.all())],
        required=True,
    )
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'password',
            'is_subscribed',
        )
        extra_kwargs = {'password': {'write_only': True}}

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return user.follower.filter(author=obj).exists()

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
    

class SetPasswordSerializer(serializers.Serializer):
    model = User
    new_password = serializers.CharField()
    current_password = serializers.CharField()


class ShortRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            # 'image',
            'cooking_time',
        )
        read_only_fields = '__all__',


class SubscriptionSerializer(serializers.ModelSerializer):
    recipes = ShortRecipeSerializer(many=True, read_only=True)
    is_subscribed = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count',
        )
        read_only_fields = '__all__',

    def get_is_subscribed(*args):
        return True
    
    def get_recipes_count(self, obj):
        return obj.recipes.count()
