from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.models import User
from apps.comments.models import Review
from apps.comments.serializers import ReviewSerializer, CreateReviewSerializer
from apps.common.utils import set_dict_attr
from apps.shop.models import Product


tags = ['Reviews']


class BaseReviewView(APIView):
    """ Abstract View to add get_objects for all Views associated with Reviews
     P.S. I don`t want to create a new file
     """
    serializer_class = ReviewSerializer

    def get_object(self, slug):
        product = Product.objects.get_or_none(slug=slug)
        return product

    class Meta:
        abstract = True


class ReviewsView(BaseReviewView):
    @extend_schema(
        summary="Reviews Of Product Fetch",
        description="""
                        This endpoint returns all reviews of a product.
                    """,
        tags=tags
    )
    def get(self, request, *args, **kwargs):
        # product = self.get_object(slug=kwargs['slug'])
        # if not product:
        #     return Response(data={'message': 'Product does not exist!'}, status=404)
        # reviews = Review.objects.select_related('user', 'product').filter(product=product)
        # if not reviews:
        #     return Response(data={'message': 'There are no reviews of this product'}, status=404)
        # serializer = self.serializer_class(reviews, many=True)
        # return Response(data=serializer.data, status=200)

        product = Product.objects.get_or_none(slug=kwargs['slug'])
        if not product:
            return Response(data={"message": "Product does not exist"}, status=404)
        reviews = Review.objects.select_related("user", "product").filter(product=product)
        serializer = self.serializer_class(reviews, many=True)
        return Response(data=serializer.data, status=200)

    @extend_schema(
        summary='Create Review',
        description='''
                            This endpoint allows to create a review of a product
                        ''',
        tags=tags,
        request=CreateReviewSerializer,
        responses=CreateReviewSerializer,
    )
    def post(self, request, *args, **kwargs):
        serializer = CreateReviewSerializer(data=request.data)
        product = self.get_object(slug=kwargs['slug'])

        if Review.objects.filter(product=product, user=request.user).exists():
            return Response(data={'message': 'You have already evaluated this product'}, status=403)

        if not product:
            return Response(data={'message': 'The product does not exist!'}, status=404)

        if serializer.is_valid():
            data = serializer.validated_data

            if not product:
                return Response(data={'message': 'The product does not exist!'}, status=404)
            data['product'] = product
            data['user'] = request.user

            review = Review.objects.create(**data)
            serializer = self.serializer_class(review)
            return Response(data=serializer.validated_data, status=200)
        else:
            return Response(serializer.errors, status=400)


class ReviewView(BaseReviewView):

    @extend_schema(
        summary="Changing Review",
        description="""
                            This endpoint allows to change the review.
                        """,
        tags=tags,
        request=CreateReviewSerializer,
        responses=CreateReviewSerializer,
    )
    def put(self, request, *args, **kwargs):
        serializer = CreateReviewSerializer(data=request.data)
        product = self.get_object(kwargs['slug'])
        review = Review.objects.get_or_none(product=product, id=kwargs['id'])

        if not review:
            return Response(data={'message': 'The review does not exist!'}, status=404)
        if request.user.id != review.user.id:
            return Response(data={'message': 'Changing review is not allowed!'}, status=403)

        if serializer.is_valid():
            data = serializer.validated_data
            # product_slug = data.pop('product_slug', None)
            # product = self.get_object(slug=product_slug)
            data['product'] = product
            data['user'] = request.user

            review = set_dict_attr(review, data)
            review.save()

            serializer = ReviewSerializer(review)
            return Response(serializer.data, status=200)
        else:
            return Response(data=serializer.errors, status=400)

    @extend_schema(
        summary="Delete Review",
        description="""
                            This endpoint deletes the review.
                        """,
        tags=tags,
    )
    def delete(self, request, *args, **kwargs):
        product = self.get_object(slug=kwargs['slug'])

        if not product:
            return Response(data={'message': 'The product does not exist!'}, status=404)

        review = Review.objects.get_or_none(product=product, id=kwargs['id'])

        if not review:
            return Response(data={'message': 'The review does not exist!'}, status=404)
        if request.user.id != review.user.id:
            return Response(data={'message': 'Deletion is not allowed!'}, status=403)

        review.delete()
        return Response(data={'message': 'Review is successfully deleted'}, status=200)
