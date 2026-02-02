import uuid
from rest_framework import serializers
from core.utils.AdaptedBulkListSerializer import BulkModelSerializer
from .models import (
    Department,
    Designation,
    Employee,
    Attendance,
    LeaveType,
    LeaveRequest,
    SalaryComponent,
    EmployeeSalaryComponent,
    PayrollPeriod,
    Payslip,
    PayslipLine,
)


class ReadablePKField(serializers.PrimaryKeyRelatedField):
    """Shows readable string in response while still being PK-based."""

    def __init__(self, *args, **kwargs):
        self._placeholder_queryset = object()
        if kwargs.get("queryset") is None and not kwargs.get("read_only", False):
            kwargs["queryset"] = self._placeholder_queryset
        super().__init__(*args, **kwargs)

    def get_queryset(self):
        queryset = self.queryset
        if queryset is self._placeholder_queryset:
            return None
        if hasattr(queryset, "all"):
            return queryset.all()
        return queryset

    def to_representation(self, value):
        return {"id": str(value.pk), "label": str(value)}


class DepartmentSerializer(BulkModelSerializer):
    class Meta:
        model = Department
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user_add", "history", "is_system_generated")


class DesignationSerializer(BulkModelSerializer):
    department = ReadablePKField(queryset=Department.objects.all(), required=False, allow_null=True)

    class Meta:
        model = Designation
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user_add", "history", "is_system_generated")


class EmployeeSerializer(BulkModelSerializer):
    user = ReadablePKField(queryset=None, required=False, allow_null=True)
    department = ReadablePKField(queryset=Department.objects.all(), required=False, allow_null=True)
    designation = ReadablePKField(queryset=Designation.objects.all(), required=False, allow_null=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from django.contrib.auth import get_user_model

        self.fields["user"].queryset = get_user_model().objects.all()

    class Meta:
        model = Employee
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user_add", "history", "is_system_generated")


class AttendanceSerializer(BulkModelSerializer):
    employee = ReadablePKField(queryset=Employee.objects.all())

    class Meta:
        model = Attendance
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user_add", "history", "is_system_generated")


class LeaveTypeSerializer(BulkModelSerializer):
    class Meta:
        model = LeaveType
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user_add", "history", "is_system_generated")


class LeaveRequestSerializer(BulkModelSerializer):
    employee = ReadablePKField(queryset=Employee.objects.all())
    leave_type = ReadablePKField(queryset=LeaveType.objects.all())

    class Meta:
        model = LeaveRequest
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user_add", "history", "is_system_generated")


class SalaryComponentSerializer(BulkModelSerializer):
    class Meta:
        model = SalaryComponent
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user_add", "history", "is_system_generated")


class EmployeeSalaryComponentSerializer(BulkModelSerializer):
    employee = ReadablePKField(queryset=Employee.objects.all())
    component = ReadablePKField(queryset=SalaryComponent.objects.all())

    class Meta:
        model = EmployeeSalaryComponent
        fields = "__all__"
        read_only_fields = ("id", "created", "updated")


class PayrollPeriodSerializer(BulkModelSerializer):
    class Meta:
        model = PayrollPeriod
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user_add", "history", "is_system_generated")


class PayslipLineSerializer(BulkModelSerializer):
    id = serializers.UUIDField(required=False)
    component = ReadablePKField(queryset=SalaryComponent.objects.all())

    class Meta:
        model = PayslipLine
        fields = ("id", "payslip", "component", "amount", "created", "updated")
        read_only_fields = ("payslip", "created", "updated")


class PayslipSerializer(BulkModelSerializer):
    payroll_period = ReadablePKField(queryset=PayrollPeriod.objects.all())
    employee = ReadablePKField(queryset=Employee.objects.all())
    lines = PayslipLineSerializer(many=True, required=False)

    class Meta:
        model = Payslip
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user_add", "history", "is_system_generated")

    def _ensure_line_uuid(self, line):
        if not line.get("id"):
            line["id"] = uuid.uuid4()
        return line

    def create(self, validated_data):
        lines_data = validated_data.pop("lines", [])
        obj = Payslip.objects.create(**validated_data)

        for line in lines_data:
            line = self._ensure_line_uuid(line)
            PayslipLine.objects.create(payslip=obj, **line)

        return obj

    def update(self, instance, validated_data):
        lines_data = validated_data.pop("lines", None)

        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()

        if lines_data is not None:
            instance.lines.all().delete()
            for line in lines_data:
                line = self._ensure_line_uuid(line)
                PayslipLine.objects.create(payslip=instance, **line)

        return instance
