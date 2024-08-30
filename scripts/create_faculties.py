from django.utils.text import slugify

from apps.departments.models import Department


def run():
    
    faculties = [
        'طب الأسنان',
        'الصيدلة',
        'هندسة العمارة',
        'الهندسة المدنية',
        'الهندسة المعلوماتية',
        'العلوم الادارية والمالية',
    ]
    
    for faculty_name in faculties:
        faculty_instance = Department.objects.create(
            name=faculty_name, 
            slug=slugify(faculty_name, allow_unicode=True), 
            parent=None
        )
        
        dean_office_name = 'عمادة كلية ' + faculty_name
        Department.objects.create(
            name=dean_office_name, 
            slug=slugify(dean_office_name, allow_unicode=True), 
            parent=faculty_instance,
        )
        
        management_department_name = 'القسم الإداري ' + faculty_name
        management_department = Department.objects.create(
            name=management_department_name, 
            slug=slugify(management_department_name, allow_unicode=True), 
            parent=faculty_instance,
        )
        management_offices = [
            'سكرتاريا',
            'امتحانات',
            'شؤون طلاب',
            'مكتبة',
            'مكتب الجودة',
            'البوفيه',
        ]
        
        for o in management_offices:
            office_name = f'{o} {faculty_name}'
            Department.objects.create(
                name=office_name,
                slug=slugify(office_name, allow_unicode=True),
                parent=management_department
            )

        academic_department_name = 'القسم الأكاديمي ' + faculty_name
        academic_department = Department.objects.create(
            name=academic_department_name, 
            slug=slugify(academic_department_name, allow_unicode=True), 
            parent=faculty_instance,
        )
        
        for idx in range(1, 4):
            office_name = 'قسم ' + str(idx) + ' ' + faculty_name
            Department.objects.create(
                name=office_name,
                slug=slugify(office_name, allow_unicode=True),
                parent=academic_department
            )