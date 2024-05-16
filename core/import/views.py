from django.shortcuts import render
from django.views.generic import View
from decouple import config
from accounts.models import User
import csv
from django.contrib import messages
from asset.models import Equipment
from insurance.models import Insurance
from client.models import Client
from consumable.models import ConsumableV2
from consumable.models import ConsumableCategory
# Create your views here.


class UserImportView(View):
    template_name = "import.html"
    default_password = config("DEFAULT_PASSWORD")

    def get(self, request):
        context = {
            "name": "کاربر",
            "import_sample":'/import/sample/user_import_sample.csv',
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
                    self.request, f"تعداد {users_added} کاربر با موفقیت به سیستم افزوده شد"
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
            "import_sample":'/import/sample/equipment_import_sample.csv',
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
                    self.request, f"تعداد {_added} تجهیزات پزشکی با موفقیت به سیستم افزوده شد"
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
            "import_sample":'/import/sample/client_import_sample.csv',
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

                    if created_by_id == '':
                        created_by = None
                    elif User.objects.filter(id = created_by_id).exists():
                        created_by = User.objects.get(id = created_by_id)
                    else:
                        created_by = None

                    if insurance_id == '':
                        insurance = None
                    elif Insurance.objects.filter(id = insurance_id).exists():
                        insurance = User.objects.get(id = insurance_id)
                    else:
                        insurance = None

                    is_vip = is_vip_str.strip() == "1"

                    client, created = Client.objects.get_or_create(
                            case_id = case_id,
                            first_name = first_name , 
                            last_name = last_name , 
                            fathers_name = fathers_name , 
                            national_id = national_id , 
                            date_of_birth =date_of_birth , 
                            gender = gender , 
                            phone_number =phone_number , 
                            address =address , 
                            marital_status =marital_status , 
                            emergency_contact_name =emergency_contact_name , 
                            emergency_contact_number = emergency_contact_number , 
                            surgeries = surgeries , 
                            allergies = allergies , 
                            medical_history = medical_history , 
                            medications = medications , 
                            smoker = smoker , 
                            disease = disease , 
                            insurance = insurance , 
                            is_vip = is_vip,
                            created_by = created_by
                            
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
            "import_sample":'/import/sample/consumable_import_sample.csv',
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



                    if created_by_id == '':
                        created_by = None
                    elif User.objects.filter(id = created_by_id).exists():
                        created_by = User.objects.get(id = created_by_id)
                    else:
                        created_by = None


                    if category_id == '':
                        category = None
                    elif ConsumableCategory.objects.filter(id = category_id).exists():
                        category = ConsumableCategory.objects.get(id = category_id)
                    else:
                        category = None


                    consumable, created = ConsumableV2.objects.get_or_create(
                         
                            name  = name,
                            category =category ,
                            unit =unit ,
                            minimum_stock_level = minimum_stock_level,
                            usage_notes = usage_notes,
                            storage_notes = storage_notes,
                            description = description,
                            reorder_quantity =reorder_quantity ,
                            created_by = created_by,
                            
                    )

                    if created:
                        consumable.save()
                        _added += 1
                messages.success(
                    self.request, f"تعداد {_added}  مواد مصرفی با موفقیت به سیستم افزوده شد"
                )
            else:
                messages.error(
                    self.request,
                    f"هنگام وارد کردن فایل خطایی روی داده است. لطفا مطمئن شوید که فرمت فایل درست است..",
                )
        return render(request, self.template_name)