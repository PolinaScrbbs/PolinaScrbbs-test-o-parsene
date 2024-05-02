from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response

from .models import Product
from .serializers import ProdictSerializer
from .parser import parsing_products

class ProductView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProdictSerializer
    url = 'https://www.ozon.ru/seller/proffi-1/products/?miniapp=seller_1'

    def post(self, request, *args, **kwargs):
        products_count = request.data.get('products_count')
        try:
            if products_count:
                if products_count < 0:
                    return Response("products_count не может быть меньше 0", status=status.HTTP_400_BAD_REQUEST)
                elif products_count > 50:
                    return Response("products_count не может быть больше 50", status=status.HTTP_400_BAD_REQUEST)
                
                created_count = parsing_products(self.url, products_count)

                return Response(f"Создано {created_count} продуктов", status=status.HTTP_201_CREATED)
            else:
                created_count = parsing_products(self.url, 10)
                return Response(f"Создано {created_count} продуктов", status=status.HTTP_201_CREATED)
        except ValueError:
            return Response("Некорректное значение параметра products_count", status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(f"Произошла ошибка: {e}", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
      
    def get(self, request, *args, **kwargs):
        product_id = kwargs.get('product_id', None)

        if product_id:
            try: 
                product = Product.objects.get(pk=product_id)
                serializer = self.serializer_class(product, context={'request': request})
                return Response(serializer.data, status=status.HTTP_200_OK)
            except ObjectDoesNotExist:
                return Response("Продукт не найден", status=status.HTTP_404_NOT_FOUND)
        else:
            products = Product.objects.all()
            serializer = self.serializer_class(products, context={'request': request}, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

