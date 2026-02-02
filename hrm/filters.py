import django_filters as filters
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


class DepartmentFilter(filters.FilterSet):
    branch = filters.UUIDFilter(field_name="branch_id")
    name = filters.CharFilter(field_name="name", lookup_expr="icontains")
    code = filters.CharFilter(field_name="code", lookup_expr="icontains")
    active = filters.BooleanFilter(field_name="active")

    class Meta:
        model = Department
        fields = ["branch", "name", "code", "active"]


class DesignationFilter(filters.FilterSet):
    branch = filters.UUIDFilter(field_name="branch_id")
    name = filters.CharFilter(field_name="name", lookup_expr="icontains")
    code = filters.CharFilter(field_name="code", lookup_expr="icontains")
    department = filters.UUIDFilter(field_name="department_id")
    active = filters.BooleanFilter(field_name="active")

    class Meta:
        model = Designation
        fields = ["branch", "name", "code", "department", "active"]


class EmployeeFilter(filters.FilterSet):
    branch = filters.UUIDFilter(field_name="branch_id")
    code = filters.CharFilter(field_name="code", lookup_expr="icontains")
    first_name = filters.CharFilter(field_name="first_name", lookup_expr="icontains")
    last_name = filters.CharFilter(field_name="last_name", lookup_expr="icontains")
    email = filters.CharFilter(field_name="email", lookup_expr="icontains")
    phone = filters.CharFilter(field_name="phone", lookup_expr="icontains")
    department = filters.UUIDFilter(field_name="department_id")
    designation = filters.UUIDFilter(field_name="designation_id")
    employment_type = filters.CharFilter(field_name="employment_type")
    join_date = filters.DateFromToRangeFilter(field_name="join_date")
    active = filters.BooleanFilter(field_name="active")

    class Meta:
        model = Employee
        fields = [
            "branch",
            "code",
            "first_name",
            "last_name",
            "email",
            "phone",
            "department",
            "designation",
            "employment_type",
            "join_date",
            "active",
        ]


class AttendanceFilter(filters.FilterSet):
    branch = filters.UUIDFilter(field_name="branch_id")
    employee = filters.UUIDFilter(field_name="employee_id")
    date = filters.DateFromToRangeFilter(field_name="date")
    active = filters.BooleanFilter(field_name="active")

    class Meta:
        model = Attendance
        fields = ["branch", "employee", "date", "active"]


class LeaveTypeFilter(filters.FilterSet):
    branch = filters.UUIDFilter(field_name="branch_id")
    name = filters.CharFilter(field_name="name", lookup_expr="icontains")
    code = filters.CharFilter(field_name="code", lookup_expr="icontains")
    paid = filters.BooleanFilter(field_name="paid")
    active = filters.BooleanFilter(field_name="active")

    class Meta:
        model = LeaveType
        fields = ["branch", "name", "code", "paid", "active"]


class LeaveRequestFilter(filters.FilterSet):
    branch = filters.UUIDFilter(field_name="branch_id")
    employee = filters.UUIDFilter(field_name="employee_id")
    leave_type = filters.UUIDFilter(field_name="leave_type_id")
    status = filters.CharFilter(field_name="status")
    from_date = filters.DateFromToRangeFilter(field_name="from_date")
    to_date = filters.DateFromToRangeFilter(field_name="to_date")
    approved = filters.BooleanFilter(field_name="approved")
    active = filters.BooleanFilter(field_name="active")

    class Meta:
        model = LeaveRequest
        fields = [
            "branch",
            "employee",
            "leave_type",
            "status",
            "from_date",
            "to_date",
            "approved",
            "active",
        ]


class SalaryComponentFilter(filters.FilterSet):
    branch = filters.UUIDFilter(field_name="branch_id")
    name = filters.CharFilter(field_name="name", lookup_expr="icontains")
    code = filters.CharFilter(field_name="code", lookup_expr="icontains")
    type = filters.CharFilter(field_name="type")
    taxable = filters.BooleanFilter(field_name="taxable")
    active = filters.BooleanFilter(field_name="active")

    class Meta:
        model = SalaryComponent
        fields = ["branch", "name", "code", "type", "taxable", "active"]


class EmployeeSalaryComponentFilter(filters.FilterSet):
    employee = filters.UUIDFilter(field_name="employee_id")
    component = filters.UUIDFilter(field_name="component_id")
    active = filters.BooleanFilter(field_name="active")

    class Meta:
        model = EmployeeSalaryComponent
        fields = ["employee", "component", "active"]


class PayrollPeriodFilter(filters.FilterSet):
    branch = filters.UUIDFilter(field_name="branch_id")
    code = filters.CharFilter(field_name="code", lookup_expr="icontains")
    start_date = filters.DateFromToRangeFilter(field_name="start_date")
    end_date = filters.DateFromToRangeFilter(field_name="end_date")
    locked = filters.BooleanFilter(field_name="locked")
    active = filters.BooleanFilter(field_name="active")

    class Meta:
        model = PayrollPeriod
        fields = ["branch", "code", "start_date", "end_date", "locked", "active"]


class PayslipFilter(filters.FilterSet):
    branch = filters.UUIDFilter(field_name="branch_id")
    payroll_period = filters.UUIDFilter(field_name="payroll_period_id")
    employee = filters.UUIDFilter(field_name="employee_id")
    status = filters.CharFilter(field_name="status")
    approved = filters.BooleanFilter(field_name="approved")
    active = filters.BooleanFilter(field_name="active")

    class Meta:
        model = Payslip
        fields = ["branch", "payroll_period", "employee", "status", "approved", "active"]


class PayslipLineFilter(filters.FilterSet):
    payslip = filters.UUIDFilter(field_name="payslip_id")
    component = filters.UUIDFilter(field_name="component_id")

    class Meta:
        model = PayslipLine
        fields = ["payslip", "component"]
