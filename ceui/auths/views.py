# views.py
import json
from rest_framework import viewsets,status,filters, serializers

from user.decorators import perm_required
from user.serializers import UserSerializer
from .models import *
from django.contrib.auth.models import Group
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from rest_framework.decorators import action
from django.utils.decorators import method_decorator
from user.models import CustomUser



class GroupSerializer(serializers.ModelSerializer):
    count = serializers.SerializerMethodField()

    class Meta:
        model = Group
        fields = 'name','count'

    def get_count(self, obj):
        return obj.account_users.count()


class PermSerializer(serializers.ModelSerializer):
    page_display = serializers.SerializerMethodField()
    class Meta:
        model = Perm
        fields = '__all__'

    def get_page_display(self, obj):
        return obj.get_page_display()  # Burada parantez eklemelisiniz.

class AuthsSerializer(serializers.ModelSerializer):
    perms = PermSerializer(many=True)
    group = GroupSerializer()
    members = serializers.SerializerMethodField()
    member_count = serializers.SerializerMethodField()
    class Meta:
        model = Auths
        fields = '__all__'
    
    def get_member_count(self, obj):
        # 'user_set' yerine 'account_users' kullanılmalı
        return obj.group.account_users.count()

    def get_members(self, obj):
        # 'group' alanı null olabilir, kontrol eklenmeli
        if obj.group:
            members = obj.group.account_users.all()
            return UserSerializer(members, many=True).data
        return []

@permission_classes([IsAuthenticated])
class AuthViewSet(viewsets.ModelViewSet):
    queryset = Auths.objects.all()
    serializer_class = AuthsSerializer
    filter_backends = [filters.SearchFilter]
    permission_classes = [IsAuthenticated]
    search_fields = ['group__name']

    @method_decorator(perm_required('view_auths'))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


    @method_decorator(perm_required('add_auths'))
    def create(self, request, *args, **kwargs):
        
        data = request.data
        print('dataaaaaa', data)
        auth_name = data.get('auth_name', None)
        page_list = []  # JSON hatası varsa boş liste döndür
        page_list_str = data.get('page_list', '[]')  # 'getlist' yerine 'get' kullanılmalı
        try:
            page_list = json.loads(page_list_str)  # JSON stringini Python listesine dönüştür
        except json.JSONDecodeError:
            page_list = []  # JSON hatası varsa boş liste döndür
        print('page_list',page_list)

        if auth_name and len(page_list) > 0:

            grup = Group.objects.create(
            name = auth_name
            )

            auths = Auths(
                group= grup
            )
            auths.save()

            for page in page_list:
                print(f'checkbox-{page}')
                page_checked = data.get(f'checkbox-{page}', None)
                print('page_checked',page_checked)



                if page_checked != None:
                    page_view = data.get(f'{page}-view', None)
                    page_add = data.get(f'{page}-add', None)
                    page_change = data.get(f'{page}-change', None)
                    page_delete = data.get(f'{page}-delete', None)

                    page_perm = Perm(
                        page = page,
                        view = True if page_view else False,
                        add = True if page_add else False,
                        change = True if page_change else False,
                        delete = True if page_delete else False
                    )
                    page_perm.save()
                    print('page_perm',page_perm)
                    auths.perms.add(page_perm)
            
            auths.save()

            serializer = AuthsSerializer(auths)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'Auth name and page list are required'}, status=status.HTTP_400_BAD_REQUEST)

    @method_decorator(perm_required('change_auths'))
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        data = request.data

        auth_name = data.get('auth_name', None)
        auth_id = data.get('auth_name', None)
        page_list = []  # JSON hatası varsa boş liste döndür
        page_list_str = data.get('page_list', '[]')  # 'getlist' yerine 'get' kullanılmalı
        try:
            page_list = json.loads(page_list_str)  # JSON stringini Python listesine dönüştür
        except json.JSONDecodeError:
            page_list = []  # JSON hatası varsa boş liste döndür

        if auth_id and len(page_list) > 0:
            
            instance.perms.all().delete()

            if auth_name:
                instance.group.name = auth_name
                instance.group.save()


            for page in page_list:
                page_checked = data.get(f'checkbox-{page}', None)


                if page_checked != None:
                    page_view = data.get(f'{page}-view', None)
                    page_add = data.get(f'{page}-add', None)
                    page_change = data.get(f'{page}-change', None)
                    page_delete = data.get(f'{page}-delete', None)

                    page_perm = Perm(
                        page = page,
                        view = True if page_view else False,
                        add = True if page_add else False,
                        change = True if page_change else False,
                        delete = True if page_delete else False
                    )
                    page_perm.save()
                    instance.perms.add(page_perm)
            
            instance.save()

            serializer = AuthsSerializer(instance)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Auth name and page list are required'}, status=status.HTTP_400_BAD_REQUEST)
      
    @method_decorator(perm_required('delete_auths'))
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        print(instance)
        instance.perms.all().delete()
        instance.group.delete()
        instance.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


    @method_decorator(perm_required('change_auths'))
    @action(detail=True, methods=['post'], url_path='authorize')
    def authorize(self, request, pk=None):
        auths = self.get_object()
        data = request.data
        authorize_id = data.get('authorize_id', None)

        try:
            user = CustomUser.objects.get(id = authorize_id)
            grup = auths.group
            user.groups.add(grup)
            user.save()
            print(f"Group {grup.name} added to user {user.email}.")
            
            serializer = AuthsSerializer(auths)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response({'error': f'{authorize_id} id numarasına sahip kullanıcı bulunamadı'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': f'Bir hata oluştu:{e}'}, status=status.HTTP_404_NOT_FOUND)
    
    @method_decorator(perm_required('change_autsh'))
    @action(detail=True, methods=['post'], url_path='revoke')
    def revoke(self, request, pk=None):
        auths = self.get_object()
        data = request.data
        revoke_id = data.get('revoke_id', None)

        try:
            user = CustomUser.objects.get(id = revoke_id)
            user.groups.clear()
            user.save()
            
            serializer = AuthsSerializer(auths)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response({'error': f'{revoke_id} id numarasına sahip kullanıcı bulunamadı'}, status=status.HTTP_404_NOT_FOUND)

    @method_decorator(perm_required('view_auths'))
    @action(detail=False, methods=['get'], url_path='path')
    def path(self, request):
        try:
            pages = Perm.SAYFA_CHOICES
            actions = Perm.YETKİ_CHOICES
            return Response({'pages':pages, 'actions':actions}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': f' Bir hata oluştu:{e}'}, status=status.HTTP_404_NOT_FOUND)


    @method_decorator(perm_required('view_auths'))
    @action(detail=False, methods=['get'], url_path='permission_map')
    def permission_map(self, request):
        try:
            user = request.user
            group = user.groups.first()
            auth = Auths.objects.filter(group=group).first()
            permissions = {}

            perms = auth.perms.all()
            print(perms)
            
            for perm in perms:
                permissions[perm.page] = {
                    'view': perm.view,
                    'add': perm.add,
                    'change': perm.change,
                    'delete': perm.delete,
                }
            return Response(permissions, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': f' Bir hata oluştu:{e}'}, status=status.HTTP_404_NOT_FOUND)






