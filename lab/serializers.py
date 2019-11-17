from rest_framework import serializers
from lab.models import (
    Device,
    DeviceInterface,
    DevicePair,
    InterfaceMapper,
    RouteSwitchConfig,
)


class DeviceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Device
        fields = ['id', 'name', 'environment', 'os_type']


class DevicePairSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DevicePair
        fields = ['id', 'prod_device', 'lab_device']


class DeviceInterfaceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DeviceInterface
        fields = ['id', 'device', 'name']


class InterfaceMapperSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = InterfaceMapper
        fields = ['id', 'prod_device', 'lab_device']


class RouteSwitchConfigSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = RouteSwitchConfig
        fields = ['id', 'device', 'updated', 'text']
