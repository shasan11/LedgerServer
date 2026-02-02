from core.utils.BaseModelViewSet import BaseModelViewSet
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
from .serializers import (
    DepartmentSerializer,
    DesignationSerializer,
    EmployeeSerializer,
    AttendanceSerializer,
    LeaveTypeSerializer,
    LeaveRequestSerializer,
    SalaryComponentSerializer,
    EmployeeSalaryComponentSerializer,
    PayrollPeriodSerializer,
    PayslipSerializer,
    PayslipLineSerializer,
)
from .filters import (
    DepartmentFilter,
    DesignationFilter,
    EmployeeFilter,
    AttendanceFilter,
    LeaveTypeFilter,
    LeaveRequestFilter,
    SalaryComponentFilter,
    EmployeeSalaryComponentFilter,
    PayrollPeriodFilter,
    PayslipFilter,
    PayslipLineFilter,
)


class DepartmentViewSet(BaseModelViewSet):
    queryset = Department.objects.select_related("branch").all()
    serializer_class = DepartmentSerializer
    filterset_class = DepartmentFilter
    search_fields = ["name", "code", "description"]


class DesignationViewSet(BaseModelViewSet):
    queryset = Designation.objects.select_related("department", "branch").all()
    serializer_class = DesignationSerializer
    filterset_class = DesignationFilter
    search_fields = ["name", "code", "description"]


class EmployeeViewSet(BaseModelViewSet):
    queryset = Employee.objects.select_related("user", "department", "designation", "branch").all()
    serializer_class = EmployeeSerializer
    filterset_class = EmployeeFilter
    search_fields = ["first_name", "last_name", "code", "email", "phone"]


class AttendanceViewSet(BaseModelViewSet):
    queryset = Attendance.objects.select_related("employee", "branch").all()
    serializer_class = AttendanceSerializer
    filterset_class = AttendanceFilter
    search_fields = ["note"]


class LeaveTypeViewSet(BaseModelViewSet):
    queryset = LeaveType.objects.select_related("branch").all()
    serializer_class = LeaveTypeSerializer
    filterset_class = LeaveTypeFilter
    search_fields = ["name", "code", "description"]


class LeaveRequestViewSet(BaseModelViewSet):
    queryset = LeaveRequest.objects.select_related("employee", "leave_type", "branch").all()
    serializer_class = LeaveRequestSerializer
    filterset_class = LeaveRequestFilter
    search_fields = ["reason", "note"]


class SalaryComponentViewSet(BaseModelViewSet):
    queryset = SalaryComponent.objects.select_related("branch").all()
    serializer_class = SalaryComponentSerializer
    filterset_class = SalaryComponentFilter
    search_fields = ["name", "code", "description"]


class EmployeeSalaryComponentViewSet(BaseModelViewSet):
    queryset = EmployeeSalaryComponent.objects.select_related("employee", "component").all()
    serializer_class = EmployeeSalaryComponentSerializer
    filterset_class = EmployeeSalaryComponentFilter
    search_fields = []


class PayrollPeriodViewSet(BaseModelViewSet):
    queryset = PayrollPeriod.objects.select_related("branch").all()
    serializer_class = PayrollPeriodSerializer
    filterset_class = PayrollPeriodFilter
    search_fields = ["code"]


class PayslipViewSet(BaseModelViewSet):
    queryset = Payslip.objects.select_related("payroll_period", "employee", "branch").prefetch_related("lines").all()
    serializer_class = PayslipSerializer
    filterset_class = PayslipFilter
    search_fields = ["note"]


class PayslipLineViewSet(BaseModelViewSet):
    queryset = PayslipLine.objects.select_related("payslip", "component").all()
    serializer_class = PayslipLineSerializer
    filterset_class = PayslipLineFilter
    search_fields = []
