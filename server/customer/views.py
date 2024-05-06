from django.shortcuts import render,get_object_or_404
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import CustomerSerializer,CustomerLoginSerializer
from .models import Customer
from rest_framework import filters
from django.contrib.auth.hashers import check_password, make_password
from rest_framework_simplejwt.tokens import RefreshToken



# Create your views here.
class LoginView(APIView):
    serializer_class = CustomerLoginSerializer

    def post(self, req):
        serializer = self.serializer_class(data=req.data)
        if serializer.is_valid():
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            # print(type)

            queryset = Customer.objects.filter(email=email)
            if queryset.exists():
                user = queryset[0]
                if check_password(password, user.password):
                    refresh = RefreshToken.for_user(user)
                    return Response({
                        'refresh': str(refresh),
                        'access': str(refresh.access_token)
                    }, status=status.HTTP_200_OK)

            return Response({
                'Bad Request': 'Invalid credentials'
            }, status=status.HTTP_404_NOT_FOUND)

        return Response({
            'Bad request': 1
        }, status=status.HTTP_400_BAD_REQUEST)


class CreateView(APIView):
    serializer_class=CustomerSerializer

    def post(self,req):
        serializer=self.serializer_class(data=req.data)

        if serializer.is_valid():
            email=serializer.validated_data.get("email")
            queryset1=Customer.objects.filter(email=email)
            if queryset1.exists():
                return Response({"Bad Request":"Customer with this email id already exists"},status=status.HTTP_403_FORBIDDEN)
            else:
                phone=serializer.validated_data.get("phone")
                queryset2=Customer.objects.filter(phone=phone)
                if queryset2.exists():
                    return Response({"Bad Request":"Customer with this phone number already exists"},status=status.HTTP_403_FORBIDDEN)
                password=serializer.validated_data.get("password")
                hashed=make_password(password)
                serializer.validated_data["password"]=hashed
                serializer.save()
                user = Customer.objects.get(email=email)
                refresh = RefreshToken.for_user(user)
                return Response({"message":"Customer data Created successfully",
                                 "data":serializer.data,
                                 'refresh': str(refresh),
                                 'access': str(refresh.access_token)
                                }, status=status.HTTP_201_CREATED)
                                
            
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def get(self,req):
        queryset=Customer.objects.all()
        serializer=self.serializer_class(queryset,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
class DetailsView(APIView):
    serializer_class=CustomerSerializer

    def get_id(self):
        id=self.kwargs.get("id")
        return id

    def get_object(self):
        try:
            id=self.kwargs.get("id")
            # print(id)
            customer=Customer.objects.get(id=id)
            return customer
        except Customer.DoesNotExist:
            return Response({"Bad Request":"Customer does not exist"},status=status.HTTP_400_BAD_REQUEST)
    
    def get(self,req,*args, **kwargs):
        # print(self.kwargs.get("id"))
        Customer=self.get_object()
        serializer=self.serializer_class(Customer)
        return Response({"data":serializer.data,"message":"Customer data found"},status=status.HTTP_200_OK)
    
    def patch(self,req,*args, **kwargs):
        Customer=self.get_object()
        serializer=self.serializer_class(Customer,data=req.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"Customer data Updated successfully","data":serializer.data},status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,req,*args, **kwargs):
        Customer=self.get_object()
        Customer.delete()
        return Response({"message":"Customer data Deleted successfully"},status=status.HTTP_200_OK)


class SearchView(APIView):
    serializer_class=CustomerSerializer


    def get(self,req):
        name=req.query_params.get("name")
        queryset=Customer.objects.filter(name=name)
        if not queryset.exists():
            return Response({"Bad Request":"Customer does not exist"},status=status.HTTP_400_BAD_REQUEST)
        serializer=self.serializer_class(queryset,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

class SortView(generics.ListAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    filter_backends = [filters.OrderingFilter]
    search_fields = ['name','email']
    

class FilterView(generics.ListAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'email']

    
