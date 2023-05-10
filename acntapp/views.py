from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import UserRegistrationSerializer,LoginSerializer,UserProfileSerializer,ChangePasswordSerializer,PasswordResetEmailSerializer,passwordResetSerializer
from django.contrib.auth import authenticate
from account.renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class UserRegistrationView(APIView):
    renderer_classes=[UserRenderer]
    def post(self,request):
        serializer=UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user=serializer.save()
            token=get_tokens_for_user(user)
            return Response({'token':token,'msg':'registration sucessfull'},status=status.HTTP_201_CREATED)
        return Response(serializer.erros,status=status.HTTP_400_BAD_REQUEST)
class LoginView(APIView):
    renderer_classes=[UserRenderer]
    def post(self,request):
        serializer=LoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
                email=serializer.data.get('email')
                password=serializer.data.get('password')
                user=authenticate(email=email,password=password)
                if user is not None:
                    token=get_tokens_for_user(user)
                    return Response({'token':token,'msg':'sucessfully login'},status=status.HTTP_200_OK)
                else:
                    return Response({'errors':{'none fields errors':['Email or password is not valid']}} ,status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)        

class UserProfileView(APIView):
    renderer_classes=[UserRenderer]
    permission_classes=[IsAuthenticated]
    def get(self,request):
        serializer=UserProfileSerializer(request.user)
        # if serializer.is_valid():
        return Response(serializer.data,status=status.HTTP_200_OK)

class UserChangePassword(APIView):
    renderer_classes=[UserRenderer]
    permission_classes=[IsAuthenticated]
    def post(self,request):
        serializer=ChangePasswordSerializer(data=request.data,
        context={'user':request.user})
        serializer.is_valid(raise_exception=True)
        return Response({'msg':'Password Changed Successfully'},status=status.HTTP_200_OK)
        # return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
class PasswordResetEmail(APIView):
    renderer_classes=[UserRenderer]
    def post(self,request):
        serializer=PasswordResetEmailSerializer(data=request.data)    
        if serializer.is_valid(raise_exception=True):
            return Response({'msg':'Password Reset Link Send.Check your Email'},status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
            
class PasswordResetView(APIView):
    def post(self,request,uid,token):
        serializer=passwordResetSerializer(data=request.data,
        context={'uid':uid,'token':token})
        if serializer.is_valid(raise_exception=True):
            return Response({'msg':'Password Reset successfully'},status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)



