from django.utils.text import slugify


def generate_department_id(instance):
    
    if instance.department_id != '':
        return instance
    
    Klass = instance.__class__
    last_sibling = (
        Klass
        .objects
        .filter(parent=instance.parent)
        .exclude(pk=instance.pk)
        .last()
    )
    
    if last_sibling:
        instance.department_id = str(int(last_sibling.department_id) + 1)
        return instance

    if instance.parent is not None:
        instance.department_id = instance.parent.department_id + str(1)
        return instance
    
    instance.department_id = '1'
    return instance


def empty_departments(model) -> None:
  
      qs = model.objects.all()
      
      if not qs.exists():
        print('all departments has been deleted successfully')
        return
      
      criteria = [obj.delete() for obj in qs if obj.is_leaf_node()]
      
      if criteria:
          empty_departments(model)


def create_faculties(model):
    
    faculties = [
        'هندسة العمارة',
        'الهندسة المعلوماتية',
        'العلوم الادارية والمالية',
        'طب الأسنان',
        'الصيدلة',
        'الهندسة المدنية',
    ]
    
    for faculty_name in faculties:
        faculty_instance = model(
            name=faculty_name, 
            slug=slugify(faculty_name, allow_unicode=True), 
            parent=None
        )
        faculty_instance.save()
        
        dean_office_name = 'عمادة كلية ' + faculty_name
        dep = model(
            name=dean_office_name, 
            slug=slugify(dean_office_name, allow_unicode=True), 
            parent=faculty_instance,
        )
        dep.save()
        
        management_department_name = 'القسم الإداري ' + faculty_name
        management_department = model(
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
            obj = model(
                name=office_name,
                slug=slugify(office_name, allow_unicode=True),
                parent=management_department
            )
            obj.save()

        academic_department_name = 'القسم الأكاديمي ' + faculty_name
        academic_department = model(
            name=academic_department_name, 
            slug=slugify(academic_department_name, allow_unicode=True), 
            parent=faculty_instance,
        )
        academic_department.save()
        
        for idx in range(1, 4):
            office_name = 'قسم ' + str(idx) + ' ' + faculty_name
            obj = model(
                name=office_name,
                slug=slugify(office_name, allow_unicode=True),
                parent=academic_department
            )
            obj.save()