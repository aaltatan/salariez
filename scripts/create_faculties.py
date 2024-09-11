from django.utils.text import slugify

from apps.departments.models import Department


def run():
    
    faculties = [
        'هندسة العمارة',
        'الهندسة المعلوماتية',
        'العلوم الادارية والمالية',
        'طب الأسنان',
        'الصيدلة',
        'الهندسة المدنية',
    ]
    
    for faculty_name in faculties:
        faculty_instance = Department(
            name=faculty_name, 
            slug=slugify(faculty_name, allow_unicode=True), 
            parent=None
        )
        faculty_instance.save()
        
        dean_office_name = 'عمادة كلية ' + faculty_name
        dep = Department(
            name=dean_office_name, 
            slug=slugify(dean_office_name, allow_unicode=True), 
            parent=faculty_instance,
        )
        dep.save()
        
        management_department_name = 'القسم الإداري ' + faculty_name
        management_department = Department(
            name=management_department_name, 
            slug=slugify(management_department_name, allow_unicode=True), 
            parent=faculty_instance,
        )
        management_department.save()
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
            obj = Department(
                name=office_name,
                slug=slugify(office_name, allow_unicode=True),
                parent=management_department
            )
            obj.save()

        academic_department_name = 'القسم الأكاديمي ' + faculty_name
        academic_department = Department(
            name=academic_department_name, 
            slug=slugify(academic_department_name, allow_unicode=True), 
            parent=faculty_instance,
        )
        academic_department.save()
        
        for idx in range(1, 4):
            office_name = 'قسم ' + str(idx) + ' ' + faculty_name
            obj = Department(
                name=office_name,
                slug=slugify(office_name, allow_unicode=True),
                parent=academic_department
            )
            obj.save()