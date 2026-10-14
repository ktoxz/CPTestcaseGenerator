def dfs(employee, managers, groups):
    # قم بإضافة الموظف إلى مجموعة الأشخاص في نفس المجموعة
    groups.add(employee)
    # قم بفحص جميع الموظفين الذين يعلمهم الموظف الحالي
    for i in range(len(managers)):
        if managers[i] == employee:
            # قم بزيارة الموظف الذي يعلمه الموظف الحالي
            dfs(i+1, managers, groups)

def minimum_groups(n, managers):
    groups = set()
    # قم بتنفيذ البحث في العمق للموظفين
    for i in range(n):
        if managers[i] == -1:
            # قم بزيارة الموظف إذا لم يكن لديه مدير مباشر
            dfs(i+1, managers, groups)
    return len(groups)

# مثال الاستخدام:
n = 5
managers = [-1, 1, 2, 1, -1]
groups = minimum_groups(n, managers)
print(groups)  # الإخراج المتوقع: 3