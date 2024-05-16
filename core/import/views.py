from django.shortcuts import render
from django.views.generic import View
from decouple import config
from accounts.models import User
import csv
from django.contrib import messages
from asset.models import Equipment

# Create your views here.


class UserImportView(View):
    template_name = "import.html"
    default_password = config("DEFAULT_PASSWORD")

    def get(self, request):
        context = {
            "name": "کاربر",  # Add any variables you need here
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
                    is_staff = row["is_staff"]
                    is_active = row["is_active"]
                    national_id = row["national_id"]
                    address = row["address"]
                    date_of_birth = row["date_of_birth"]

                    # Convert string to boolean based on 0 and 1 values
                    is_superuser = is_superuser_str.strip() == "1"
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
                    self.request, f"{users_added} User(s) successfully added"
                )
            else:
                messages.error(
                    self.request,
                    f"There was an error importing the file. Please make sure the file format is correct.",
                )
        return render(request, self.template_name)


class EquipmentImportView(View):
    template_name = "import.html"

    def get(self, request):
        context = {
            "name": "تجهیزات پزشکی", 
            "import_sample":'/../attachments/import-sample/equipment_import_sample.csv'     
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
                messages.success(self.request, f"{_added} User(s) successfully added")
            else:
                messages.error(
                    self.request,
                    f"There was an error importing the file. Please make sure the file format is correct.",
                )
        return render(request, self.template_name)
