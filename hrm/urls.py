from django.urls import path, include
from rest_framework_bulk.routes import BulkRouter
from .views import (
    DepartmentViewSet,
    DesignationViewSet,
    EmployeeViewSet,
    AttendanceViewSet,
    LeaveTypeViewSet,
    LeaveRequestViewSet,
    SalaryComponentViewSet,
    EmployeeSalaryComponentViewSet,
    PayrollPeriodViewSet,
    PayslipViewSet,
    PayslipLineViewSet,
)

router = BulkRouter()
router.register(r"departments", DepartmentViewSet, basename="department")
router.register(r"designations", DesignationViewSet, basename="designation")
router.register(r"employees", EmployeeViewSet, basename="employee")
router.register(r"attendance", AttendanceViewSet, basename="attendance")
router.register(r"leave-types", LeaveTypeViewSet, basename="leave-type")
router.register(r"leave-requests", LeaveRequestViewSet, basename="leave-request")
router.register(r"salary-components", SalaryComponentViewSet, basename="salary-component")
router.register(r"employee-salary-components", EmployeeSalaryComponentViewSet, basename="employee-salary-component")
router.register(r"payroll-periods", PayrollPeriodViewSet, basename="payroll-period")
router.register(r"payslips", PayslipViewSet, basename="payslip")
router.register(r"payslip-lines", PayslipLineViewSet, basename="payslip-line")

urlpatterns = [
    path("", include(router.urls)),
]
