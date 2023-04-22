from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from . models import *
from rest_framework.authtoken.models import Token
from . serializers import *
from rest_framework.permissions import IsAuthenticated
from django.http import Http404
from rest_framework import viewsets
# Create your views here.

# CLASS TO CREATE A USER
class register(APIView):
    def post(self, request, format=None):
        serializer = UserRegister(data = request.data)
        user=request.data
        datas={}
        if serializer.is_valid():
            acc = serializer.save()
            if acc:
                datas['response'] = 'registered'
                datas['username'] = acc.username
                datas['email'] = acc.email
            # Retrieve or create a token associated with the 'acc' user using Django's 'Token' model,and store the token and a boolean flag 'create' in 'token' variable
                token, create = Token.objects.get_or_create(user=acc)
                # Add a 'token' key with value 'token.key' to 'datas'
                datas['token'] = token.key
                return Response( status=status.HTTP_201_CREATED)
            else:
                print('Error',acc)    
        else:
            datas= serializer.errors
        return Response(datas)


# CLASS THAT PERFORMS CRUD ON USERS MODEL
class userDetails(APIView):
    permission_classes=[IsAuthenticated,]

    def get_object(self, pk):
        try:
            return Account.objects.get(pk=pk)
        except:
            raise Http404
    
    # GET request to fetch a Users
    def get(self, request, pk, format=None):
        userData = self.get_object(pk)
        serializer = UserDataSerializer(userData)
        return Response(serializer.data)
    
    # PUT request to update a User with associated Role
    def put(self,request,pk,format=None):
        current_user_role = self.request.user
        print('Current User :', current_user_role)
        print('Current Users Role :', current_user_role.role)
        # Get the member instance being updated
        instance = self.get_object(pk)
        print('Instance :', instance)
        print('Instance Role :', instance.role)

        # Check if the member being updated is the same as the current user
        if (instance == self.request.user) or (current_user_role.role.name=='Technician' and instance != current_user_role):
            raise serializers.ValidationError("You are not allowed to edit your own role.")
        
        elif instance.role == current_user_role.role:
            raise serializers.ValidationError("You are not allowed to edit same role users.")
        
        elif instance.role.name == 'Super Admin':
            raise serializers.ValidationError({'role': "You cannot edit your superior's role."})
        
        elif  current_user_role.role.name=='Operator' and instance.role.name != 'Technician':
            raise serializers.ValidationError({'role':'You are not allowed to edit other than technicians.'})
        
        # elif :
        #     raise serializers.ValidationError({'role':'You are a Technician hence not allowed to edit other than technicians.'})
        
        userData = self.get_object(pk)
        serializer = UserDataSerializer(userData, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response({'message':'error', 'error':serializer.errors})
    
    # DELETE request to destroy a User with associated Role
    def delete(self,request,pk,format=None):
        current_user_role = self.request.user
        print('Current User :', current_user_role)
        print('Current Users Role :', current_user_role.role)
        # Get the member instance being updated
        instance = self.get_object(pk)
        print('Instance :', instance)
        print('Instance Role :', instance.role)
        
        # if instance == self.request.user:
        #     raise serializers.ValidationError("You are not allowed to edit your own role.")
        if instance.role == current_user_role:
            raise serializers.ValidationError("You are not allowed to delete same role users.")
        elif instance.role.name == 'Super Admin':
            raise serializers.ValidationError("You are not allowed to delete Super Admin")
        elif instance.role.name == 'Admin' and current_user_role.role.name !='Super Admin':
            raise serializers.ValidationError("You are not allowed to delete Admin")
        elif current_user_role.role.name == 'Technician':
            raise serializers.ValidationError("You are not allowed to delete anyone")
        elif current_user_role.role.name == 'Operator' and instance.role.name != 'Technician':
            raise serializers.ValidationError("You are not allowed to delete superior users.")
            
        userData = self.get_object(pk)
        userData.delete()
        return Response({'message':'User deleted successfully'})


class userRoles(APIView):
    permission_classes=[IsAuthenticated,]
    def get_object(self, pk):
        try:
            return Role.objects.get(pk=pk)
        except:
            raise Http404
        
    def get(self, request, pk, format=None):
        userData = self.get_object(pk)
        serializer = UserRolesSerializer(userData)
        return Response(serializer.data)


# CLASS THAT PERFORMS CRUD ON ROLES MODEL
class RoleViewSet(viewsets.ModelViewSet):
    permission_classes=[IsAuthenticated,]
    queryset = Role.objects.all()
    serializer_class = UserRolesSerializer
    
    # POST request to create a Role with associated Rights
    def post(self, request, *args, **kwargs):

        current_user = self.request.user
        print('Current User :', current_user)
        print('Current Users Role :', current_user.role.name)

        if current_user.role.name != "Super Admin" or current_user.role.name != "Admin":
            raise serializers.ValidationError({'role':'You are not allowed to create right.'})
        
        # Extracting the data from the request
        role_data = request.data
        rights_data = role_data.pop('rights', [])  # Extracting rights data, empty list if not provided
        print('Role Data',role_data)
        print('Rights Data',rights_data)

        # Create the Role instance  
        role_serializer = self.get_serializer(data=role_data)
        role_serializer.is_valid(raise_exception=True)
        role = role_serializer.save()

        # Create the Rights instances and associate with the Role
        for right_data in rights_data:
            right = Rights.objects.get(pk=right_data)  # Get Rights instance by primary key
            role.rights.add(right)  # Add the Right to the Role's many-to-many relationship
        
        return Response(role_serializer.data, status=status.HTTP_201_CREATED)
    
    # UPDATE request to update a Role with associated Rights
    def update(self,request,pk=None,):

        current_user = self.request.user
        print('Current User :', current_user)
        print('Current Users Role :', current_user.role.name)

        if current_user.role.name != "Super Admin" or current_user.role.name != "Admin":
            raise serializers.ValidationError({'role':'You are not allowed to create role.'})
        
        role_instance = self.get_object()  # Get the Role instance to be updated
        serializer = self.get_serializer(role_instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        # Update the many-to-many relationship
        rights_data = request.data.get('rights', [])
        role_instance.rights.set(rights_data)
        return Response(serializer.data, {'message':'error', 'error':serializer.errors})

    # DELETE request to delete a Role with associated Rights
    def delete(self, request, pk, format=None):
        try:
            current_user = self.request.user
            print('Current User :', current_user)
            print('Current Users Role :', current_user.role.name)

            if current_user.role.name != "Super Admin" or current_user.role.name != "Admin":
                raise serializers.ValidationError({'role':'You are not allowed to delete any roles.'})
            
            rights_data = self.get_queryset().get(pk=pk)
            rights_data.delete()
            return Response({'message': 'Role deleted successfully'})
        except Rights.DoesNotExist:
            raise Http404
        

# CLASS THAT PERFORMS CRUD ON RIGHTS MODEL
class RightsViewSet(viewsets.ModelViewSet):
    permission_classes=[IsAuthenticated,]
    queryset = Rights.objects.all()
    serializer_class = UserRightsSerializer

    # POST request to create a Right 
    def post(self, request, *args, **kwargs):
        current_user = self.request.user
        print('Current User :', current_user)
        print('Current Users Role :', current_user.role.name)

        if current_user.role.name != "Super Admin" or current_user.role.name != "Admin":
            raise serializers.ValidationError({'role':'You are not allowed to create right.'})
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def perform_create(self, serializer):
        serializer.save()

    # UPDATE request to update a Right
    def update(self,request,pk,format=None):

        current_user = self.request.user
        print('Current User :', current_user)
        print('Current Users Role :', current_user.role.name)

        if current_user.role.name != "Super Admin" or current_user.role.name != "Admin":
            raise serializers.ValidationError({'role':'You are not allowed to update right.'})
        
        rightsData = self.get_object(pk)
        serializer = UserRightsSerializer(rightsData, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response({'message':'error', 'error':serializer.errors})
    
    # DELETE request to delete a Right
    def delete(self,request,pk,format=None):
        try:
            current_user = self.request.user
            print('Current User :', current_user)
            print('Current Users Role :', current_user.role.name)

            if current_user.role.name != "Super Admin" or current_user.role.name != "Admin":
                raise serializers.ValidationError({'role':'You are not allowed to delete any right.'})
            rights_data = self.get_queryset().get(pk=pk)
            rights_data.delete()
            return Response({'message': 'Right deleted successfully'})
        except Rights.DoesNotExist:
            raise Http404
    
