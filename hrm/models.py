from django.db import models
from django.conf import settings
from core.utils.coreModels import (
    UUIDPk,
    BranchScopedStampedOwnedActive,
    TransactionBasedBranchScopedStampedOwnedActive,
)


class Department(BranchScopedStampedOwnedActive):
    name = models.CharField(max_length=120)
    code = models.CharField(max_length=40, null=True, blank=True, db_index=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class Designation(BranchScopedStampedOwnedActive):
    name = models.CharField(max_length=120)
    code = models.CharField(max_length=40, null=True, blank=True, db_index=True)
    department = models.ForeignKey(Department, on_delete=models.PROTECT, null=True, blank=True, related_name="designations")
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class Employee(BranchScopedStampedOwnedActive):
    class EmploymentType(models.TextChoices):
        FULL_TIME = "full_time", "Full Time"
        PART_TIME = "part_time", "Part Time"
        CONTRACT = "contract", "Contract"
        INTERN = "intern", "Intern"

    code = models.CharField(max_length=60, null=True, blank=True, db_index=True)

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="employee_profiles",
    )

    first_name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=120, null=True, blank=True)

    phone = models.CharField(max_length=60, null=True, blank=True)
    email = models.CharField(max_length=150, null=True, blank=True)

    department = models.ForeignKey(Department, on_delete=models.PROTECT, null=True, blank=True, related_name="employees")
    designation = models.ForeignKey(Designation, on_delete=models.PROTECT, null=True, blank=True, related_name="employees")

    employment_type = models.CharField(max_length=20, choices=EmploymentType.choices, default=EmploymentType.FULL_TIME)
    join_date = models.DateField(null=True, blank=True)
    exit_date = models.DateField(null=True, blank=True)

    basic_salary = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name or ''}".strip()


class Attendance(BranchScopedStampedOwnedActive):
    employee = models.ForeignKey(Employee, on_delete=models.PROTECT, related_name="attendance")
    date = models.DateField(db_index=True)

    check_in = models.DateTimeField(null=True, blank=True)
    check_out = models.DateTimeField(null=True, blank=True)

    total_minutes = models.IntegerField(default=0)
    note = models.TextField(null=True, blank=True)

    class Meta:
        unique_together = ("employee", "date")

    def __str__(self):
        return f"{self.employee} - {self.date}"


class LeaveType(BranchScopedStampedOwnedActive):
    name = models.CharField(max_length=120)
    code = models.CharField(max_length=40, null=True, blank=True, db_index=True)
    paid = models.BooleanField(default=True)
    max_days_per_year = models.IntegerField(default=0)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class LeaveRequest(TransactionBasedBranchScopedStampedOwnedActive):
    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        SUBMITTED = "submitted", "Submitted"
        APPROVED = "approved", "Approved"
        REJECTED = "rejected", "Rejected"
        VOID = "void", "Void"

    employee = models.ForeignKey(Employee, on_delete=models.PROTECT, related_name="leave_requests")
    leave_type = models.ForeignKey(LeaveType, on_delete=models.PROTECT, related_name="leave_requests")

    from_date = models.DateField(db_index=True)
    to_date = models.DateField(db_index=True)
    days = models.DecimalField(max_digits=18, decimal_places=2, default=0)

    reason = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT, db_index=True)

    # override base total to keep consistent even if unused
    total = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    note = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.employee} {self.from_date}→{self.to_date}"


class SalaryComponent(BranchScopedStampedOwnedActive):
    class Type(models.TextChoices):
        EARNING = "earning", "Earning"
        DEDUCTION = "deduction", "Deduction"

    name = models.CharField(max_length=120)
    code = models.CharField(max_length=40, null=True, blank=True, db_index=True)
    type = models.CharField(max_length=20, choices=Type.choices, default=Type.EARNING, db_index=True)
    taxable = models.BooleanField(default=False)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class EmployeeSalaryComponent(UUIDPk):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="salary_components")
    component = models.ForeignKey(SalaryComponent, on_delete=models.PROTECT, related_name="employee_links")

    amount = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    active = models.BooleanField(default=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class PayrollPeriod(BranchScopedStampedOwnedActive):
    code = models.CharField(max_length=40, null=True, blank=True, db_index=True)
    start_date = models.DateField(db_index=True)
    end_date = models.DateField(db_index=True)
    locked = models.BooleanField(default=False)

    def __str__(self):
        return self.code or f"{self.start_date} - {self.end_date}"


class Payslip(TransactionBasedBranchScopedStampedOwnedActive):
    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        POSTED = "posted", "Posted"
        VOID = "void", "Void"

    payroll_period = models.ForeignKey(PayrollPeriod, on_delete=models.PROTECT, related_name="payslips")
    employee = models.ForeignKey(Employee, on_delete=models.PROTECT, related_name="payslips")

    status = models.CharField(max_length=10, choices=Status.choices, default=Status.DRAFT, db_index=True)

    gross_total = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    deduction_total = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    net_total = models.DecimalField(max_digits=18, decimal_places=2, default=0)

    # override base
    total = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    note = models.TextField(null=True, blank=True)

    class Meta:
        unique_together = ("payroll_period", "employee")

    def __str__(self):
        return f"{self.employee} - {self.payroll_period}"


class PayslipLine(UUIDPk):
    payslip = models.ForeignKey(Payslip, on_delete=models.CASCADE, related_name="lines")
    component = models.ForeignKey(SalaryComponent, on_delete=models.PROTECT, related_name="payslip_lines")

    amount = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
