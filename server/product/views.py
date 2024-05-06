from django.shortcuts import render,get_object_or_404
from rest_framework import generics, status,filters
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ProductSerializer
from .models import Product


# Create your views here.

class CreateView(APIView):
    serializer_class=ProductSerializer

    def post(self,req):
        serializer=self.serializer_class(data=req.data)

        if serializer.is_valid():
            name=serializer.validated_data.get("name")
            queryset1=Product.objects.filter(name=name)
            if queryset1.exists():
                return Response({"Bad Request":"Product with this name already exists"},status=status.HTTP_200_OK)
            else:
                serializer.save()
                return Response({"message":"Product Created successfully","data":serializer.data},status=status.HTTP_201_CREATED)
            
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def get(self,req):
        queryset=Product.objects.all()
        serializer=self.serializer_class(queryset,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
class DetailsView(APIView):
    serializer_class=ProductSerializer

    def get_id(self):
        id=self.kwargs.get("id")
        return id

    def get_object(self):
        try:
            id=self.get_id()
            product=Product.objects.get(id=id)
            return product
        except Product.DoesNotExist:
            return Response({"Bad Request":"Product does not exist"},status=status.HTTP_400_BAD_REQUEST)
    
    def get(self,req,*args, **kwargs):
        product=self.get_object()
        serializer=self.serializer_class(product)
        return Response({"data":serializer.data,"message":"Product found"},status=status.HTTP_200_OK)
    
    def patch(self,req,*args, **kwargs):
        product=self.get_object()
        serializer=self.serializer_class(product,data=req.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"Product Updated successfully","data":serializer.data},status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,req,*args, **kwargs):
        product=self.get_object()
        product.delete()
        return Response({"message":"Product Deleted successfully"},status=status.HTTP_200_OK)



class SearchView(APIView):
    serializer_class=ProductSerializer


    def get(self,req):
        name=req.query_params.get("name")
        queryset=Product.objects.filter(name=name)
        if not queryset.exists():
            return Response({"Bad Request":"Product does not exist"},status=status.HTTP_400_BAD_REQUEST)
        serializer=self.serializer_class(queryset,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

class SortView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [filters.OrderingFilter]
    search_fields = ['name','price']
    

class FilterView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'category','description']