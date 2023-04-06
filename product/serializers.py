from rest_framework import serializers
from .models import Category, Product, Review, Tag
from rest_framework.exceptions import ValidationError


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = 'id stars text product_title'.split()

class ProductSerializer(serializers.ModelSerializer):

    # rating = ReviewSerializer(many=True)
    class Meta:
        model = Product
        fields = "id title description price category_name".split()


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = 'id name products_count products_list'.split()

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = 'title rating'.split()

'''VALIDATION'''

class ValidateProductSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=100)
    description = serializers.CharField(required=False)
    price = serializers.FloatField(min_value=0, max_value=255)
    category_id = serializers.IntegerField()
    tags = serializers.ListField(child=serializers.IntegerField())

    def create(self, validated_data):
        return Product.objects.create(**validated_data)

    # def update(self, instance, validated_data):



    '''EXTRA-TASK'''
    def validate_genres(self, tags):
        filtered_tags = Tag.objects.filter(id__in=tags) #QuerySet of existed tags
        if len(tags) == filtered_tags.count(): #validating
            return tags

        lst_ = {i['id'] for i in filtered_tags.values_list().values()} #creating set of existed tags

        raise ValidationError(f'This ids doesnt exist {set(tags).difference(lst_)}')   #collecting errors

    def validate_category_id(self, category_id):
        try:
            Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            raise ValidationError(f"Error! {category_id} does not exists")
        return category_id

class ValidateCategorySerializer(serializers.Serializer):
    name = serializers.CharField(max_length=30)

class ValidateReviewSerializer(serializers.Serializer):
    text = serializers.Serializer(required=False)
    stars = serializers.IntegerField(min_value=1, max_value=5)
    product_id = serializers.IntegerField()

    def validate_product_id(self, product_id):
        try:
            Review.objects.get(product_id=product_id)
        except Review.DoesNotExist:
            raise ValidationError('Review doesnt exist')