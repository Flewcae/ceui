from rest_framework import generics, permissions, viewsets
from rest_framework.response import Response
from knox.models import AuthToken
from knox.views import LogoutView as KnoxLogoutView
from rest_framework.permissions import IsAuthenticated, AllowAny
from auths.models import Auths
from user.models import CustomUser
from .serializers import RegisterSerializer, LoginSerializer, UserSerializer
from django.contrib.auth import login
from rest_framework.decorators import action, permission_classes
from django.middleware import csrf


# Kullanıcı Kaydı
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user).data,
            "token": AuthToken.objects.create(user)[1]
        })

# Kullanıcı Girişi
class LoginAPI(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):

        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data
            login(request, user)
            permissions = {}
            group = user.groups.first()
            if group:
                auth = Auths.objects.filter(group=group).first()

                perms = auth.perms.all()
                print(perms)
                
                for perm in perms:
                    permissions[perm.page] = {
                        'view': perm.view,
                        'add': perm.add,
                        'change': perm.change,
                        'delete': perm.delete,
                    }
            
            return Response({
                "user": UserSerializer(user).data,
                "permissions":permissions,
                "token": AuthToken.objects.create(user)[1]
            })
        except Exception as e:
            return Response({'e':str(e)})

# Kullanıcı Çıkışı
class LogoutAPI(KnoxLogoutView):
    permission_classes = [permissions.IsAuthenticated]

class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):

        try:
            user = request.user
            login(request, user)
            permissions = {}
            group = user.groups.first()
            if group:
                auth = Auths.objects.filter(group=group).first()

                perms = auth.perms.all()
                print(perms)
                
                for perm in perms:
                    permissions[perm.page] = {
                        'view': perm.view,
                        'add': perm.add,
                        'change': perm.change,
                        'delete': perm.delete,
                    }
            return Response({
                "user": UserSerializer(user).data,
                "permissions":permissions,
                "token": AuthToken.objects.create(user)[1]
            })
        except AuthToken.DoesNotExist:
            print('geçersiz token')
            return Response({"error": "Geçersiz token."}, status=401)
        
    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def csrf(self,req):
        try:
            token = csrf.get_token(req)
            content = {
                'csrf': token

            }
            return Response(content)
        except Exception as e:
            print(e)
            return Response({'error':e})