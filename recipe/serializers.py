from rest_framework import serializers

from .models import Recipe, RecipeCategory, RecipeLike, get_default_recipe_category


class RecipeCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeCategory
        fields = ('id', 'name')


class RecipeSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(read_only=True)
    username = serializers.SerializerMethodField()
    category_name = serializers.SerializerMethodField()
    category = RecipeCategorySerializer(required=False)
    total_number_of_likes = serializers.SerializerMethodField()
    total_number_of_bookmarks = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ('id', 'category', 'category_name', 'picture', 'title', 'desc',
                  'cook_time', 'ingredients', 'procedure', 'author', 'username',
                  'total_number_of_likes', 'total_number_of_bookmarks')

    def get_username(self, obj):
        return obj.author.username

    def get_category_name(self, obj):
        return obj.category.name

    def get_total_number_of_likes(self, obj):
        return obj.get_total_number_of_likes()

    def get_total_number_of_bookmarks(self, obj):
        return obj.get_total_number_of_bookmarks()

    def create(self, validated_data):
        category_data = validated_data.pop('category', None)  # Get category data if exists
        if category_data:
            category_instance, created = RecipeCategory.objects.get_or_create(
                **category_data
            )
        else:
            # Use the default category if no category is provided
            category_instance = get_default_recipe_category()

        recipe_instance = Recipe.objects.create(
            **validated_data, category=category_instance
        )
        return recipe_instance
        # category = validated_data.pop('category',None)
        # category_instance, created = RecipeCategory.objects.get_or_create(
        #     **category)
        # recipe_instance = Recipe.objects.create(
        #     **validated_data, category=category_instance)
        # return recipe_instance

    def update(self, instance, validated_data):
        if 'category' in validated_data:
            nested_serializer = self.fields['category']
            nested_instance = instance.category
            nested_data = validated_data.pop('category')

            nested_serializer.update(nested_instance, nested_data)

        return super(RecipeSerializer, self).update(instance, validated_data)


class RecipeLikeSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = RecipeLike
        fields = ('id', 'user', 'recipe')
