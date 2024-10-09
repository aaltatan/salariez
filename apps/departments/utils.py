from apps.base.utils import views


class Deleter(views.Deleter):
    def can_delete_condition(self):
        conditions = [
            not self.instance.children.all().exists(),
            not self.instance.employees.all().exists(),
        ]
        return all(conditions)


def generate_department_id(instance):
    
    if instance.department_id != '':
        return instance
    
    Klass = instance.__class__
    last_sibling = (
        Klass
        .objects
        .filter(parent=instance.parent)
        .order_by('department_id')
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


def create_departments(model, cc_model):
    
    cost_centers = [
        cc_model.objects.get(cost_center_accounting_id=2), # arch
        cc_model.objects.get(cost_center_accounting_id=3), # it
        cc_model.objects.get(cost_center_accounting_id=4), # mang
        cc_model.objects.get(cost_center_accounting_id=5), # dent
        cc_model.objects.get(cost_center_accounting_id=6), # pharm
        cc_model.objects.get(cost_center_accounting_id=7), # civil
    ]
    
    for cc in cost_centers:
        dept_instance = model(
            name=cc.name, 
            cost_center=cc,
            parent=None
        )
        dept_instance.save()
        
        dean_office_name = 'عمادة كلية ' + cc.name
        dep = model(
            name=dean_office_name, 
            cost_center=cc,
            parent=dept_instance,
        )
        dep.save()
        
        management_department_name = 'القسم الإداري ' + cc.name
        management_department = model(
            name=management_department_name, 
            cost_center=cc,
            parent=dept_instance,
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
            office_name = f'{o} {cc.name}'
            obj = model(
                name=office_name,
                cost_center=cc,
                parent=management_department
            )
            obj.save()

        academic_department_name = 'القسم الأكاديمي ' + cc.name
        academic_department = model(
            name=academic_department_name, 
            cost_center=cc,
            parent=dept_instance,
        )
        academic_department.save()
        
        for idx in range(1, 4):
            office_name = 'قسم ' + str(idx) + ' ' + cc.name
            obj = model(
                name=office_name,
                cost_center=cc,
                parent=academic_department
            )
            obj.save()