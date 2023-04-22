from rest_framework.response import Response
from rest_framework import serializers
from . models import *
from rest_framework import status


#Account serialzer   
class UserRegister(serializers.ModelSerializer):
    #for confirmation password
    password2 = serializers.CharField(
        style={'input': 'password'}, write_only=True)
    
    class Meta:
        model = Account
        fields = ['username', 'email', 'password', 'password2', 'role' ]
    
    def save(self):
        selected_role = self.validated_data['role']
        print('dddddddddd', selected_role)

        register = Account(
            username    =   self.validated_data["username"],
            email       =   self.validated_data["email"],
            role        =   selected_role
        )
        password  = self.validated_data["password"]
        password2 = self.validated_data["password2"]

        if password != password2:
            raise serializers.ValidationError({'password':'password dosent match'})
        
        register.set_password(password)
        register.save()
        return register
    
class UserDataSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=Account
        fields = ['username', 'email']

class UserRightsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rights
        fields = '__all__'

class UserRolesSerializer(serializers.ModelSerializer):
    rights = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Role
        fields = '__all__'
    
    # Override create method to handle many-to-many relationship
    def create(self, validated_data):
        rights_data = validated_data.pop('rights', [])
        role = Role.objects.create(**validated_data)

        # Add Rights instances to Role's many-to-many relationship
        role.rights.set(rights_data)
        return role


