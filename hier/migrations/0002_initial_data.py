from django.db import migrations


base_tags = [
    {"startswith": "aaa"},
    {"startswith": "tacacs"},
    {"startswith": "policy-map"},
    {"startswith": "class-map"},
    {"startswith": "logging"},
    {"startswith": "snmp-server"},
    {"startswith": "ntp"},
    {"startswith": "username"},
]


def iosxr_lineage(apps, schema_editor):
    global base_tags
    os = "iosxr"
    Lineage = apps.get_model('hier', 'Lineage')
    tags = [
        {"startswith": "ipv4 virtual address"},
        {"startswith": "nv"},
        {"startswith": "mirror"},
        {"startswith": "interface MgmtEth0"},
    ]
    base_tags = base_tags + tags

    for tag in base_tags:
        for k, v in tag.items():
            Lineage.objects.create(key=k, value=v, os=os)

    interface = Lineage.objects.create(key="startswith", value="interface", os=os)
    Lineage.objects.create(parent=interface, key="startswith", value="service-policy", os=os)


def ios_lineage(apps, schema_editor, base_tags=base_tags):
    os = "ios"
    Lineage = apps.get_model('hier', 'Lineage')

    for tag in base_tags:
        for k, v in tag.items():
            Lineage.objects.create(key=k, value=v, os=os)


def iosxe_lineage(apps, schema_editor, base_tags=base_tags):
    os = "iosxe"
    Lineage = apps.get_model('hier', 'Lineage')

    for tag in base_tags:
        for k, v in tag.items():
            Lineage.objects.create(key=k, value=v, os=os)


def eos_lineage(apps, schema_editor, base_tags=base_tags):
    os = "eos"
    Lineage = apps.get_model('hier', 'Lineage')

    for tag in base_tags:
        for k, v in tag.items():
            Lineage.objects.create(key=k, value=v, os=os)


class Migration(migrations.Migration):

    dependencies = [
        ('hier', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(iosxr_lineage),
        migrations.RunPython(ios_lineage),
        migrations.RunPython(iosxe_lineage),
        migrations.RunPython(eos_lineage)
    ]
