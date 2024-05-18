from django.shortcuts import render
from django.views.generic import View
from decouple import config
from accounts.models import User
import csv
from django.contrib import messages
from asset.models import Equipment
from insurance.models import Insurance
from client.models import Client
from consumable.models import ConsumableV2, Supplier
from consumable.models import ConsumableCategory
from doctor.models import Doctor
from reception.models import Reception
from financial.models import Financial
from services.models import Service, ServiceCategory
from tasks.models import Task
# Create your views here.


class UserImportView(View):
    template_name = "import.html"
    default_password = config("DEFAULT_PASSWORD")

    def get(self, request):
        context = {
            "name": "کاربر",
            "import_sample": "/import/sample/user_import_sample.csv",
        }
        return render(request, self.template_name, context=context)

    def post(self, request):
        if request.method == "POST" and request.FILES.get("file"):
            file = request.FILES["file"]
            if file.name.endswith(".csv"):
                users_added = 0
                decoded_file = file.read().decode("utf-8")
                csv_data = csv.DictReader(decoded_file.splitlines(), delimiter=",")

                for row in csv_data:
                    email = row["email"]
                    first_name = row["first_name"]
                    last_name = row["last_name"]
                    phone_number = row["phone_number"]
                    is_superuser_str = row["is_superuser"]
                    is_staff_str = row["is_staff"]
                    is_active_str = row["is_active"]
                    national_id = row["national_id"]
                    address = row["address"]
                    date_of_birth = row["date_of_birth"]

                    # Convert string to boolean based on 0 and 1 values
                    is_superuser = is_superuser_str.strip() == "1"
                    is_staff = is_staff_str.strip() == "1"
                    is_active = is_active_str.strip() == "1"

                    user, created = User.objects.get_or_create(
                        email=email,
                        first_name=first_name,
                        last_name=last_name,
                        phone_number=phone_number,
                        is_superuser=is_superuser,
                        is_staff=is_staff,
                        is_active=is_active,
                        national_id=national_id,
                        address=address,
                        date_of_birth=date_of_birth,
                    )
                    if created:
                        user.set_password(self.default_password)
                        user.save()
                        users_added += 1
                messages.success(
                    self.request,
                    f"تعداد {users_added} کاربر با موفقیت به سیستم افزوده شد",
                )
            else:
                messages.error(
                    self.request,
                    f"هنگام وارد کردن فایل خطایی روی داده است. لطفا مطمئن شوید که فرمت فایل درست است..",
                )
        return render(request, self.template_name)


class EquipmentImportView(View):
    template_name = "import.html"

    def get(self, request):
        context = {
            "name": "تجهیزات پزشکی",
            "import_sample": "/import/sample/equipment_import_sample.csv",
        }

        return render(request, self.template_name, context=context)

    def post(self, request):
        if request.method == "POST" and request.FILES.get("file"):
            file = request.FILES["file"]
            if file.name.endswith(".csv"):
                _added = 0
                decoded_file = file.read().decode("utf-8")
                csv_data = csv.DictReader(decoded_file.splitlines(), delimiter=",")

                for row in csv_data:
                    name = row["name"]
                    manufacturer = row["manufacturer"]
                    model = row["model"]
                    serial_number = row["serial_number"]
                    acquisition_date = row["acquisition_date"]
                    warranty_expiry_date = row["warranty_expiry_date"]
                    location = row["location"]
                    is_available_str = row["is_available"]
                    description = row["description"]
                    last_maintenance_date = row["last_maintenance_date"]
                    created_by_id = row["created_by"]
                    created_by = User.objects.get(id=created_by_id)

                    # Convert string to boolean based on 0 and 1 values
                    is_available = is_available_str.strip() == "1"
                    equipment, created = Equipment.objects.get_or_create(
                        name=name,
                        manufacturer=manufacturer,
                        model=model,
                        serial_number=serial_number,
                        acquisition_date=acquisition_date,
                        warranty_expiry_date=warranty_expiry_date,
                        location=location,
                        description=description,
                        last_maintenance_date=last_maintenance_date,
                        created_by=created_by,
                        is_available=is_available,
                    )

                    if created:
                        equipment.save()
                        _added += 1
                messages.success(
                    self.request,
                    f"تعداد {_added} تجهیزات پزشکی با موفقیت به سیستم افزوده شد",
                )
            else:
                messages.error(
                    self.request,
                    f"هنگام وارد کردن فایل خطایی روی داده است. لطفا مطمئن شوید که فرمت فایل درست است..",
                )
        return render(request, self.template_name)


class ClientImportView(View):
    template_name = "import.html"

    def get(self, request):
        context = {
            "name": "بیماران",
            "import_sample": "/import/sample/client_import_sample.csv",
        }

        return render(request, self.template_name, context=context)

    def post(self, request):
        if request.method == "POST" and request.FILES.get("file"):
            file = request.FILES["file"]
            if file.name.endswith(".csv"):
                _added = 0
                decoded_file = file.read().decode("utf-8")
                csv_data = csv.DictReader(decoded_file.splitlines(), delimiter=",")

                for row in csv_data:
                    case_id = row["شماره پرونده"]
                    first_name = row["نام"]
                    last_name = row["نام خانوادگی"]
                    fathers_name = row["نام پدر"]
                    national_id = row["کد ملی"]
                    date_of_birth = row["تاریخ تولد"]
                    gender = row["جنسیت"]
                    phone_number = row["شماره تماس"]
                    address = row["آدرس"]
                    marital_status = row["وضعیت تاهل"]
                    emergency_contact_name = row["نام همراه ( شرایط اضطراری)"]
                    emergency_contact_number = row["شماره تماس همراه"]
                    surgeries = row["سابقه جراحی"]
                    allergies = row["حساسیت"]
                    medical_history = row["سوابق درمان"]
                    medications = row["سوابق دارویی"]
                    smoker = row["استعمال دخانیات"]
                    disease = row["بیماری"]
                    created_by_id = row["ایجاد کننده"]
                    insurance_id = row["بیمه"]
                    is_vip_str = row["VIP"]

                    if created_by_id == "":
                        created_by = None
                    elif User.objects.filter(id=created_by_id).exists():
                        created_by = User.objects.get(id=created_by_id)
                    else:
                        created_by = None

                    if insurance_id == "":
                        insurance = None
                    elif Insurance.objects.filter(id=insurance_id).exists():
                        insurance = User.objects.get(id=insurance_id)
                    else:
                        insurance = None

                    is_vip = is_vip_str.strip() == "1"

                    client, created = Client.objects.get_or_create(
                        case_id=case_id,
                        first_name=first_name,
                        last_name=last_name,
                        fathers_name=fathers_name,
                        national_id=national_id,
                        date_of_birth=date_of_birth,
                        gender=gender,
                        phone_number=phone_number,
                        address=address,
                        marital_status=marital_status,
                        emergency_contact_name=emergency_contact_name,
                        emergency_contact_number=emergency_contact_number,
                        surgeries=surgeries,
                        allergies=allergies,
                        medical_history=medical_history,
                        medications=medications,
                        smoker=smoker,
                        disease=disease,
                        insurance=insurance,
                        is_vip=is_vip,
                        created_by=created_by,
                    )

                    if created:
                        client.save()
                        _added += 1
                messages.success(
                    self.request, f"تعداد {_added}  بیمار با موفقیت به سیستم افزوده شد"
                )
            else:
                messages.error(
                    self.request,
                    f"هنگام وارد کردن فایل خطایی روی داده است. لطفا مطمئن شوید که فرمت فایل درست است..",
                )
        return render(request, self.template_name)


class ConsumableImportView(View):
    template_name = "import.html"

    def get(self, request):
        context = {
            "name": "مواد مصرفی",
            "import_sample": "/import/sample/consumable_import_sample.csv",
        }

        return render(request, self.template_name, context=context)

    def post(self, request):
        if request.method == "POST" and request.FILES.get("file"):
            file = request.FILES["file"]
            if file.name.endswith(".csv"):
                _added = 0
                decoded_file = file.read().decode("utf-8")
                csv_data = csv.DictReader(decoded_file.splitlines(), delimiter=",")

                for row in csv_data:
                    name = row["عنوان"]
                    category_id = row["دسته بندی"]
                    unit = row["واحد اندازه گیری"]
                    minimum_stock_level = row["حداقل سطح موجودی"]
                    usage_notes = row["نحوه مصرف"]
                    storage_notes = row["نحوه نگهداری"]
                    description = row["توضیحات"]
                    reorder_quantity = row["سطح موجودی برای یادآوری سفارش مجدد"]
                    created_by_id = row["ایجاد کننده"]

                    if created_by_id == "":
                        created_by = None
                    elif User.objects.filter(id=created_by_id).exists():
                        created_by = User.objects.get(id=created_by_id)
                    else:
                        created_by = None

                    if category_id == "":
                        category = None
                    elif ConsumableCategory.objects.filter(id=category_id).exists():
                        category = ConsumableCategory.objects.get(id=category_id)
                    else:
                        category = None

                    consumable, created = ConsumableV2.objects.get_or_create(
                        name=name,
                        category=category,
                        unit=unit,
                        minimum_stock_level=minimum_stock_level,
                        usage_notes=usage_notes,
                        storage_notes=storage_notes,
                        description=description,
                        reorder_quantity=reorder_quantity,
                        created_by=created_by,
                    )

                    if created:
                        consumable.save()
                        _added += 1
                messages.success(
                    self.request,
                    f"تعداد {_added}  مواد مصرفی با موفقیت به سیستم افزوده شد",
                )
            else:
                messages.error(
                    self.request,
                    f"هنگام وارد کردن فایل خطایی روی داده است. لطفا مطمئن شوید که فرمت فایل درست است..",
                )
        return render(request, self.template_name)


class SupplierImportView(View):
    template_name = "import.html"

    def get(self, request):
        context = {
            "name": "تامین کنندکان",
            "import_sample": "/import/sample/supplier_import_sample.csv",
        }

        return render(request, self.template_name, context=context)

    def post(self, request):
        if request.method == "POST" and request.FILES.get("file"):
            file = request.FILES["file"]
            if file.name.endswith(".csv"):
                _added = 0
                decoded_file = file.read().decode("utf-8")
                csv_data = csv.DictReader(decoded_file.splitlines(), delimiter=",")

                for row in csv_data:
                    name = row["عنوان"]
                    contact_person = row["نام واسط"]
                    email = row["ایمیل"]
                    phone_number = row["شماره تلفن"]
                    address = row["آدرس"]
                    city = row["شهر"]
                    notes = row["یادداشت"]
                    created_by_id = row["ایجاد کننده"]

                    if created_by_id == "":
                        created_by = None
                    elif User.objects.filter(id=created_by_id).exists():
                        created_by = User.objects.get(id=created_by_id)
                    else:
                        created_by = None

                    supplier, created = Supplier.objects.get_or_create(
                        name=name,
                        contact_person=contact_person,
                        email=email,
                        phone_number=phone_number,
                        address=address,
                        city=city,
                        notes=notes,
                        created_by=created_by,
                    )

                    if created:
                        supplier.save()
                        _added += 1
                messages.success(
                    self.request,
                    f"تعداد {_added}تامین کنندکان با موفقیت به سیستم افزوده شد",
                )
            else:
                messages.error(
                    self.request,
                    f"هنگام وارد کردن فایل خطایی روی داده است. لطفا مطمئن شوید که فرمت فایل درست است..",
                )
        return render(request, self.template_name)


class DoctorImportView(View):
    template_name = "import.html"

    def get(self, request):
        context = {
            "name": "پزشکان",
            "import_sample": "/import/sample/doctor_import_sample.csv",
        }

        return render(request, self.template_name, context=context)

    def post(self, request):
        if request.method == "POST" and request.FILES.get("file"):
            file = request.FILES["file"]
            if file.name.endswith(".csv"):
                _added = 0
                decoded_file = file.read().decode("utf-8")
                csv_data = csv.DictReader(decoded_file.splitlines(), delimiter=",")

                for row in csv_data:
                    first_name = row["نام"]
                    last_name = row["نام خانوادگی"]
                    email = row["ایمیل"]
                    phone_number = row["شماره تماس"]
                    address = row["آدرس"]
                    specialization = row["تخصص"]
                    registration_number = row["شماره نظام پزشکی"]
                    is_active_str = row["وضعیت فعال بودن"]
                    created_by_id = row["ایجاد کننده"]

                    is_active = is_active_str.strip() == "1"

                    if created_by_id == "":
                        created_by = None
                    elif User.objects.filter(id=created_by_id).exists():
                        created_by = User.objects.get(id=created_by_id)
                    else:
                        created_by = None

                    doctor, created = Doctor.objects.get_or_create(
                        email=email,
                        phone_number=phone_number,
                        address=address,
                        first_name=first_name,
                        last_name=last_name,
                        specialization=specialization,
                        registration_number=registration_number,
                        is_active=is_active,
                        created_by=created_by,
                    )

                    if created:
                        doctor.save()
                        _added += 1
                messages.success(
                    self.request,
                    f"تعداد {_added}تامین کنندکان با موفقیت به سیستم افزوده شد",
                )
            else:
                messages.error(
                    self.request,
                    f"هنگام وارد کردن فایل خطایی روی داده است. لطفا مطمئن شوید که فرمت فایل درست است..",
                )
        return render(request, self.template_name)


class FinancialImportView(View):
    template_name = "import.html"

    def get(self, request):
        context = {
            "name": "صورتحساب",
            "import_sample": "/import/sample/financial_import_sample.csv",
        }

        return render(request, self.template_name, context=context)

    def post(self, request):
        if request.method == "POST" and request.FILES.get("file"):
            file = request.FILES["file"]
            if file.name.endswith(".csv"):
                _added = 0
                decoded_file = file.read().decode("utf-8")
                csv_data = csv.DictReader(decoded_file.splitlines(), delimiter=",")

                for row in csv_data:
                    invoice_number = row["شماره صورتحساب"]
                    reception_id = row["شناسه پذیرش"]
                    insurance_range = row["درصد پوشش بیمه"]
                    discount = row["تخفیف"]
                    insurance_amount = row["مبلغ پوشش بیمه"]
                    service_price = row["مبلغ سرویس"]
                    service_tax = row["مالیات سرویس"]
                    service_price_final = row["مبلغ نهایی سرویس"]
                    consumable_price = row["هزینه مواد مصرفی"]
                    consumable_tax = row["مالیات مواد مصرفی"]
                    consumable_price_final = row["مبلغ نهایی مواد مصرفی"]
                    total_amount = row["مبلغ کل"]
                    final_amount = row["مبلغ نهایی"]
                    payment_status = row["وضعیت پرداخت"]
                    payment_received_date = row["تاریخ پرداخت"]
                    doctor_id = row["پزشک"]
                    doctors_wage = row["سهم پزشک"]
                    revenue = row["درآمد"]
                    created_by_id = row["ایجاد کننده"]

                    if created_by_id == "":
                        created_by = None
                    elif User.objects.filter(id=created_by_id).exists():
                        created_by = User.objects.get(id=created_by_id)
                    else:
                        created_by = None

                    if doctor_id == "":
                        doctor = None
                    elif Doctor.objects.filter(id=doctor_id).exists():
                        doctor = Doctor.objects.get(id=doctor_id)
                    else:
                        doctor = None

                    if reception_id == "":
                        reception = None
                    elif Reception.objects.filter(id=reception_id).exists():
                        reception = Reception.objects.get(id=reception_id)
                    else:
                        reception = None

                    financial, created = Financial.objects.get_or_create(
                        invoice_number=invoice_number,
                        reception=reception,
                        insurance_range=insurance_range,
                        discount=discount,
                        insurance_amount=insurance_amount,
                        service_price=service_price,
                        service_tax=service_tax,
                        service_price_final=service_price_final,
                        consumable_price=consumable_price,
                        consumable_tax=consumable_tax,
                        consumable_price_final=consumable_price_final,
                        total_amount=total_amount,
                        final_amount=final_amount,
                        payment_status=payment_status,
                        payment_received_date=payment_received_date,
                        doctor=doctor,
                        doctors_wage=doctors_wage,
                        revenue=revenue,
                        created_by=created_by,
                    )

                    if created:
                        financial.save()
                        _added += 1
                messages.success(
                    self.request,
                    f"تعداد {_added} صورتحساب با موفقیت به سیستم افزوده شد",
                )
            else:
                messages.error(
                    self.request,
                    f"هنگام وارد کردن فایل خطایی روی داده است. لطفا مطمئن شوید که فرمت فایل درست است..",
                )
        return render(request, self.template_name)


class InsuranceImportView(View):
    template_name = "import.html"

    def get(self, request):
        context = {
            "name": "بیمه",
            "import_sample": "/import/sample/insurance_import_sample.csv",
        }

        return render(request, self.template_name, context=context)

    def post(self, request):
        if request.method == "POST" and request.FILES.get("file"):
            file = request.FILES["file"]
            if file.name.endswith(".csv"):
                _added = 0
                decoded_file = file.read().decode("utf-8")
                csv_data = csv.DictReader(decoded_file.splitlines(), delimiter=",")

                for row in csv_data:
                    name = row["عنوان"]
                    policy_number = row["شناسه"]
                    insurance_company = row["سازمان ارائه دهنده"]
                    deductible = row["قابل کسر"]
                    copay = row["پرداخت مشترک(copay)"]
                    max_annual_coverage = row["حداکثر پوشش سالانه"]
                    policy_type = row["نوع سیاست گذاری"]
                    notes = row["یادداشت"]
                    created_by_id = row["ایجاد کننده"]

                    if created_by_id == "":
                        created_by = None
                    elif User.objects.filter(id=created_by_id).exists():
                        created_by = User.objects.get(id=created_by_id)
                    else:
                        created_by = None

                    insurance, created = Insurance.objects.get_or_create(
                        name=name,
                        policy_number=policy_number,
                        insurance_company=insurance_company,
                        deductible=deductible,
                        copay=copay,
                        max_annual_coverage=max_annual_coverage,
                        policy_type=policy_type,
                        notes=notes,
                        created_by=created_by,
                    )

                    if created:
                        insurance.save()
                        _added += 1
                messages.success(
                    self.request, f"تعداد {_added}  بیمه  با موفقیت به سیستم افزوده شد"
                )
            else:
                messages.error(
                    self.request,
                    f"هنگام وارد کردن فایل خطایی روی داده است. لطفا مطمئن شوید که فرمت فایل درست است..",
                )
        return render(request, self.template_name)



class ReceptionImportView(View):
    template_name = "import.html"

    def get(self, request):
        context = {
            "name": "پذیرش",
            "import_sample": "/import/sample/reception_import_sample.csv",
        }

        return render(request, self.template_name, context=context)

    def post(self, request):
        if request.method == "POST" and request.FILES.get("file"):
            file = request.FILES["file"]
            if file.name.endswith(".csv"):
                _added = 0
                decoded_file = file.read().decode("utf-8")
                csv_data = csv.DictReader(decoded_file.splitlines(), delimiter=",")

                for row in csv_data:
                    client_id = row["شناسه بیمار"]
                    service_id = row["شناسه سرویس"]
                    status = row["وضعیت"]
                    reason = row["علت مراجعه"]
                    payment_type = row["نوع پرداخت"]
                    payment_status = row["وضعیت پرداخت"]
                    created_by_id = row["ایجاد کننده"]
                    jalali_date = row['تاریخ پذیرش']

                    if created_by_id == "":
                        created_by = None
                    elif User.objects.filter(id=created_by_id).exists():
                        created_by = User.objects.get(id=created_by_id)
                    else:
                        created_by = None

                    if client_id == "":
                        client = None
                    elif Client.objects.filter(id=client_id).exists():
                        client = Client.objects.get(id=client_id)
                    else:
                        client = None

                    if service_id == "":
                        service = None
                    elif Service.objects.filter(id=service_id).exists():
                        service = Service.objects.get(id=service_id)
                    else:
                        service = None

                    reception, created = Reception.objects.get_or_create(
                        client = client, 
                        service =service , 
                        status = status, 
                        reason =reason , 
                        payment_type = payment_type, 
                        payment_status = payment_status, 
                        created_by=created_by,
                        jalali_date = jalali_date
                    )

                    if created:
                        reception.save()
                        _added += 1
                messages.success(
                    self.request, f"تعداد {_added}  پذیرش  با موفقیت به سیستم افزوده شد"
                )
            else:
                messages.error(
                    self.request,
                    f"هنگام وارد کردن فایل خطایی روی داده است. لطفا مطمئن شوید که فرمت فایل درست است..",
                )
        return render(request, self.template_name)



class ServiceImportView(View):
    template_name = "import.html"

    def get(self, request):
        context = {
            "name": "سرویس",
            "import_sample": "/import/sample/service_import_sample.csv",
        }

        return render(request, self.template_name, context=context)

    def post(self, request):
        if request.method == "POST" and request.FILES.get("file"):
            file = request.FILES["file"]
            if file.name.endswith(".csv"):
                _added = 0
                decoded_file = file.read().decode("utf-8")
                csv_data = csv.DictReader(decoded_file.splitlines(), delimiter=",")

                for row in csv_data:
                    name = row["عنوان"]
                    doctor_id = row["شناسه پزشک"]
                    doctors_wage_percentage = row["درصد سهم پزشک"]
                    description = row["توضیحات"]
                    category_id = row["شناسه دسته بندی"]
                    duration = row["مدت زمان تقریبی"]
                    price = row["مبلغ سرویس"]
                    preparation_instructions = row["دستورالعمل های آماده سازی"]
                    documentation_requirements = row["ملزومات مستندسازی"]
                    is_active_str = row["وضعیت فعال بودن"]
                    therapeutic_measures = row["اقدامات درمانی"]
                    recommendations = row["توصیه ها"]
                    appointment_per_day = row["ظرفیت نوبت دهی در روز"]
                    created_by_id = row["ایجاد کننده"]

                    if created_by_id == "":
                        created_by = None
                    elif User.objects.filter(id=created_by_id).exists():
                        created_by = User.objects.get(id=created_by_id)
                    else:
                        created_by = None

                    if doctor_id == "":
                        doctor = None
                    elif Doctor.objects.filter(id=doctor_id).exists():
                        doctor = Doctor.objects.get(id=doctor_id)
                    else:
                        doctor = None

                    if category_id == "":
                        category = None
                    elif ServiceCategory.objects.filter(id=category_id).exists():
                        category = ServiceCategory.objects.get(id=category_id)
                    else:
                        category = None
                    is_active = is_active_str.strip() == "1"

                    service, created = Service.objects.get_or_create(
                        name = name,
                        doctor =doctor,
                        doctors_wage_percentage = doctors_wage_percentage,
                        description =description ,
                        category =category ,
                        duration = duration,
                        price =price ,
                        preparation_instructions = preparation_instructions,
                        documentation_requirements =documentation_requirements ,
                        is_active = is_active,
                        therapeutic_measures = therapeutic_measures,
                        recommendations = recommendations,
                        appointment_per_day =appointment_per_day ,
                        created_by=created_by,
                    )

                    if created:
                        service.save()
                        _added += 1
                messages.success(
                    self.request, f"تعداد {_added}  سرویس  با موفقیت به سیستم افزوده شد"
                )
            else:
                messages.error(
                    self.request,
                    f"هنگام وارد کردن فایل خطایی روی داده است. لطفا مطمئن شوید که فرمت فایل درست است..",
                )
        return render(request, self.template_name)
    

class TaskImportView(View):
    template_name = "import.html"

    def get(self, request):
        context = {
            "name": "تسک",
            "import_sample": "/import/sample/task_import_sample.csv",
        }

        return render(request, self.template_name, context=context)

    def post(self, request):
        if request.method == "POST" and request.FILES.get("file"):
            file = request.FILES["file"]
            if file.name.endswith(".csv"):
                _added = 0
                decoded_file = file.read().decode("utf-8")
                csv_data = csv.DictReader(decoded_file.splitlines(), delimiter=",")

                for row in csv_data:
                    title = row["عنوان تسک"]
                    type = row["نوع تسک"]
                    status = row["وضعیت"]
                    priority = row["فوریت"]
                    description = row["توضیحات"]
                    assign_to_id = row["کارشناس بررسی کننده"]
                    answer = row["پاسخ کارشناس"]
                    reopen_message = row["دلیل باز کردن مجدد"]
                    created_by_id = row["ایجاد کننده"]

                    if created_by_id == "":
                        created_by = None
                    elif User.objects.filter(id=created_by_id).exists():
                        created_by = User.objects.get(id=created_by_id)
                    else:
                        created_by = None

                    if assign_to_id == "":
                        assign_to = None
                    elif User.objects.filter(id=assign_to_id).exists():
                        assign_to = User.objects.get(id=assign_to_id)
                    else:
                        assign_to = None


                    task, created = Task.objects.get_or_create(
                        title = title,
                        type =type ,
                        status = status,
                        priority =priority ,
                        description = description,
                        assign_to =assign_to ,
                        answer = answer,
                        reopen_message = reopen_message,
                        created_by=created_by,
                    )

                    if created:
                        task.save()
                        _added += 1
                messages.success(
                    self.request, f"تعداد {_added}  تسک  با موفقیت به سیستم افزوده شد"
                )
            else:
                messages.error(
                    self.request,
                    f"هنگام وارد کردن فایل خطایی روی داده است. لطفا مطمئن شوید که فرمت فایل درست است..",
                )
        return render(request, self.template_name)