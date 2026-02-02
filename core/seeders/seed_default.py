import os

from django.db import transaction


def seed_all_defaults(schema_name: str = "default"):
    try:
        from django.contrib.auth import get_user_model
        from accounting.models import AccountType, COA
        from master.models import Branch, Currency, TaxClass, TaxRate, MasterData
    except Exception:
        return

    with transaction.atomic():
        # ---- Branch defaults ----
        main_branch, _ = Branch.objects.get_or_create(
            code="MAIN",
            defaults={
                "name": "Main Branch",
                "is_head_office": True,
                "active": True,
                "is_system_generated": True,
            },
        )

        if not main_branch.is_head_office:
            main_branch.is_head_office = True
            main_branch.save(update_fields=["is_head_office"])

        User = get_user_model()
        User.objects.filter(is_superuser=True, branch__isnull=True).update(branch=main_branch)

        if not User.objects.filter(is_superuser=True).exists():
            default_username = os.getenv("DEFAULT_SUPERUSER_USERNAME", "admin")
            default_email = os.getenv("DEFAULT_SUPERUSER_EMAIL", "admin@example.com")
            default_password = os.getenv("DEFAULT_SUPERUSER_PASSWORD", "admin123")
            User.objects.create_superuser(
                username=default_username,
                email=default_email,
                password=default_password,
                branch=main_branch,
            )

        # ---- Currency defaults ----
        default_currencies = [
            {"code": "USD", "name": "US Dollar", "symbol": "$", "is_base": True},
            {"code": "AED", "name": "UAE Dirham", "symbol": "AED"},
            {"code": "NPR", "name": "Nepalese Rupee", "symbol": "NPR"},
            {"code": "EUR", "name": "Euro", "symbol": "€"},
            {"code": "GBP", "name": "British Pound", "symbol": "£"},
            {"code": "INR", "name": "Indian Rupee", "symbol": "₹"},
        ]
        has_base = Currency.objects.filter(is_base=True).exists()
        for row in default_currencies:
            defaults = {
                "name": row["name"],
                "symbol": row["symbol"],
                "is_system_generated": True,
                "is_base": row.get("is_base", False) and not has_base,
            }
            Currency.objects.get_or_create(code=row["code"], defaults=defaults)

        # ---- Tax defaults ----
        tax_classes = [
            {"name": "No Tax", "code": "NONE"},
            {"name": "VAT", "code": "VAT"},
            {"name": "GST", "code": "GST"},
        ]
        tax_class_map = {}
        for row in tax_classes:
            tax_class, _ = TaxClass.objects.get_or_create(
                code=row["code"],
                defaults={
                    "name": row["name"],
                    "description": f"{row['name']} class",
                    "is_system_generated": True,
                },
            )
            tax_class_map[row["code"]] = tax_class

        tax_rates = [
            {"tax_class": "NONE", "name": "No Tax (0%)", "rate_percent": 0},
            {"tax_class": "VAT", "name": "VAT Standard (5%)", "rate_percent": 5},
            {"tax_class": "VAT", "name": "VAT Zero (0%)", "rate_percent": 0},
            {"tax_class": "GST", "name": "GST Standard (18%)", "rate_percent": 18},
        ]
        for row in tax_rates:
            TaxRate.objects.get_or_create(
                tax_class=tax_class_map[row["tax_class"]],
                name=row["name"],
                defaults={
                    "rate_percent": row["rate_percent"],
                    "inclusive": False,
                    "is_system_generated": True,
                },
            )

        # ---- MasterData defaults ----
        master_defaults = {
            "lead-source": [
                "Facebook",
                "Instagram",
                "LinkedIn",
                "X (Twitter)",
                "YouTube",
                "TikTok",
                "WhatsApp",
                "Snapchat",
                "Pinterest",
            ],
            "deal-stage": ["Lead", "Qualified", "Proposal", "Won", "Lost"],
            "tds-type": [
                "Contractor",
                "Professional Fees",
                "Rent",
                "Commission",
                "Interest",
                "Salary",
                "Purchase of Goods",
                "Technical Services",
                "Dividend",
            ],
            "custom-fields": ["Custom Fields"],
            "suggest-selling-price": ["Recent Selling Price", "Fixed Selling Price"],
            "product-price-basis": ["Inclusive of VAT", "Exclusive of VAT"],
            "negative-cash-balance": ["Reject", "Warn", "Do Nothing"],
            "negative-item-balance": ["Reject", "Warn", "Do Nothing"],
            "credit-limit-exceeds": ["Reject", "Warn", "Do Nothing"],
        }

        for key, names in master_defaults.items():
            for name in names:
                MasterData.objects.get_or_create(
                    key=key,
                    name=name,
                    defaults={"active": True, "is_system_generated": True},
                )

        # ---- Chart of Accounts defaults (per branch) ----
        account_types = {
            "asset": ("Asset", AccountType.Category.ASSET, AccountType.NormalBalance.DR),
            "liability": ("Liability", AccountType.Category.LIABILITY, AccountType.NormalBalance.CR),
            "equity": ("Equity", AccountType.Category.EQUITY, AccountType.NormalBalance.CR),
            "income": ("Income", AccountType.Category.INCOME, AccountType.NormalBalance.CR),
            "expense": ("Expense", AccountType.Category.EXPENSE, AccountType.NormalBalance.DR),
        }
        account_type_map = {}
        for key, (name, category, balance) in account_types.items():
            account_type, _ = AccountType.objects.get_or_create(
                name=name,
                defaults={
                    "category": category,
                    "normal_balance": balance,
                    "is_system_generated": True,
                },
            )
            account_type_map[key] = account_type

        coa_template = [
            {"code": "1000", "name": "Assets", "type": "asset", "parent": None, "is_group": True},
            {"code": "1100", "name": "Current Assets", "type": "asset", "parent": "1000", "is_group": True},
            {"code": "1110", "name": "Cash", "type": "asset", "parent": "1100"},
            {"code": "1120", "name": "Bank", "type": "asset", "parent": "1100"},
            {"code": "1200", "name": "Accounts Receivable", "type": "asset", "parent": "1000"},
            {"code": "2000", "name": "Liabilities", "type": "liability", "parent": None, "is_group": True},
            {"code": "2100", "name": "Current Liabilities", "type": "liability", "parent": "2000", "is_group": True},
            {"code": "2200", "name": "Accounts Payable", "type": "liability", "parent": "2000"},
            {"code": "3000", "name": "Equity", "type": "equity", "parent": None, "is_group": True},
            {"code": "4000", "name": "Income", "type": "income", "parent": None, "is_group": True},
            {"code": "4100", "name": "Freight Income", "type": "income", "parent": "4000"},
            {"code": "4200", "name": "Service Income", "type": "income", "parent": "4000"},
            {"code": "5000", "name": "Expenses", "type": "expense", "parent": None, "is_group": True},
            {"code": "5100", "name": "Operating Expenses", "type": "expense", "parent": "5000", "is_group": True},
            {"code": "5110", "name": "Salaries", "type": "expense", "parent": "5100"},
            {"code": "5120", "name": "Rent", "type": "expense", "parent": "5100"},
            {"code": "5130", "name": "Utilities", "type": "expense", "parent": "5100"},
        ]

        for branch in Branch.objects.all():
            if COA.objects.filter(branch=branch).exists():
                continue

            by_code = {}

            for row in [r for r in coa_template if r["parent"] is None]:
                obj, _ = COA.objects.get_or_create(
                    branch=branch,
                    code=row["code"],
                    defaults={
                        "name": row["name"],
                        "description": "",
                        "account_type": account_type_map[row["type"]],
                        "is_group": row.get("is_group", False),
                        "is_system": True,
                        "is_system_generated": True,
                    },
                )
                by_code[row["code"]] = obj

            for row in [r for r in coa_template if r["parent"] is not None]:
                parent_obj = by_code.get(row["parent"])
                obj, _ = COA.objects.get_or_create(
                    branch=branch,
                    code=row["code"],
                    defaults={
                        "name": row["name"],
                        "description": "",
                        "parent": parent_obj,
                        "account_type": account_type_map[row["type"]],
                        "is_group": row.get("is_group", False),
                        "is_system": True,
                        "is_system_generated": True,
                    },
                )
                by_code[row["code"]] = obj
