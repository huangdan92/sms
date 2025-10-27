import MySQLdb
from django.shortcuts import render, redirect

# Create your views here.
# 任务信息列表处理函数
from sims.utils import capture_scroll_screenshot


def index(request):
    student_no = request.GET.get('student_no', '')
    student_name = request.GET.get('student_name', '')

    sql = "SELECT id,student_no,student_name FROM sims_student WHERE 1=1 "
    if student_no.strip() != '':
        sql = sql + " and student_no = '" + student_no + "'"
    if student_name.strip() != '':
        sql = sql + " and student_name = '" + student_name + "'"

    print(sql)
    conn = MySQLdb.connect(host="172.20.10.5", user="root", passwd="rootroot", db="sms", charset='utf8mb4')
    with conn.cursor(cursorclass=MySQLdb.cursors.DictCursor) as cursor:
        cursor.execute(sql)
        students = cursor.fetchall()
    return render(request, 'student/index.html', {'students': students,
                                                  'student_name': student_name, 'student_no': student_no})


# 任务信息新增处理函数
def add(request):
    if request.method == 'GET':
        return render(request, 'student/add.html')
    else:
        student_no = request.POST.get('student_no', '')
        student_name = request.POST.get('student_name', '')
        print(student_name)
        print(student_no)

        conn = MySQLdb.connect(host="172.20.10.5", user="root", passwd="rootroot", db="sms", charset='utf8mb4')
        with conn.cursor(cursorclass=MySQLdb.cursors.DictCursor) as cursor:
            cursor.execute("INSERT INTO sims_student (student_no,student_name) "
                           "values (%s,%s)", [student_no, student_name])
            conn.commit()

            capture_scroll_screenshot(
                'http://172.20.10.5:3000/d/xfpJB9FGz/node-exporter-dashboard-en-20201010-starsl-cn?orgId=1&from=1761532554000&to=1761532602000&var-origin_prometheus=&var-job=%E8%99%9A%E6%8B%9F%E6%9C%BA%E5%B0%BE%E5%8F%B75&var-hostname=All&var-node=172.20.10.5:8100&var-device=All&var-interval=2m&var-maxmount=%2F&var-show_hostname=localhost.localdomain&var-total=1',
                '/Users/huangdan/Downloads/scrolling_screenshot缩放.png', student_name, student_no)

        return redirect('../')


# 任务信息修改处理函数
def edit(request):
    if request.method == 'GET':
        id = request.GET.get("id")
        conn = MySQLdb.connect(host="172.20.10.5", user="root", passwd="rootroot", db="sms", charset='utf8mb4')
        with conn.cursor(cursorclass=MySQLdb.cursors.DictCursor) as cursor:
            cursor.execute("SELECT id,student_no,student_name FROM sims_student where id =%s", [id])
            student = cursor.fetchone()
        return render(request, 'student/edit.html', {'student': student})
    else:
        id = request.POST.get("id")
        student_no = request.POST.get('student_no', '')
        student_name = request.POST.get('student_name', '')
        conn = MySQLdb.connect(host="172.20.10.5", user="root", passwd="rootroot", db="sms", charset='utf8mb4')
        with conn.cursor(cursorclass=MySQLdb.cursors.DictCursor) as cursor:
            cursor.execute("UPDATE sims_student set student_no=%s,student_name=%s where id =%s",
                           [student_no, student_name, id])
            conn.commit()
        return redirect('../')


# 任务信息删除处理函数
def delete(request):
    id = request.GET.get("id")
    conn = MySQLdb.connect(host="172.20.10.5", user="root", passwd="rootroot", db="sms", charset='utf8mb4')
    with conn.cursor(cursorclass=MySQLdb.cursors.DictCursor) as cursor:
        cursor.execute("DELETE FROM sims_student WHERE id =%s", [id])
        conn.commit()
    return redirect('../')
