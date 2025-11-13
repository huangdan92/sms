import MySQLdb
from django.shortcuts import render, redirect
from django.http import JsonResponse
import re

# Create your views here.
# 任务信息列表处理函数
from sims.utils import capture_scroll_screenshot, extract_prometheus_with_regex, capture_scroll_screenshot_jvm


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
        prometheusyml_node = request.POST.get('prometheusyml_node', '')
        custom_config = request.POST.get('custom_config', '')  # 新增：获取自定义配置内容

        selected_targets = request.POST.getlist('selected_targets', [])
        custom_selected_targets = request.POST.getlist('custom_selected_targets', [])

        selected_targets_str = ','.join(selected_targets) if selected_targets else ''
        custom_selected_targets_str = ','.join(custom_selected_targets) if custom_selected_targets else ''

        print(str(type(selected_targets)))
        # print(str(type(custom_selected_targets[0])))
        # print('selected_targets=' + selected_targets)
        print('selected_targets_str=' + selected_targets_str)
        print('custom_selected_targets_str=' + custom_selected_targets_str)
        # print(student_name)
        # print(student_no)
        # print(prometheusyml_node)
        job_name, targets = extract_prometheus_with_regex(prometheusyml_node)
        job_name_jvm, targets_jvm = extract_prometheus_with_regex(custom_config)
        print(job_name)
        print(job_name_jvm)

        conn = MySQLdb.connect(host="172.20.10.5", user="root", passwd="rootroot", db="sms", charset='utf8mb4')
        with conn.cursor(cursorclass=MySQLdb.cursors.DictCursor) as cursor:
            cursor.execute(
                "INSERT INTO sims_student (student_no,student_name,job_name,selected_targets_str,custom_config_content,custom_selected_targets_str) "
                "values (%s,%s,%s,%s,%s,%s)",
                [student_no, student_name, job_name, selected_targets_str, job_name_jvm, custom_selected_targets_str])
            conn.commit()

            # capture_scroll_screenshot(job_name, selected_targets,
            #                           '/Users/huangdan/Downloads/scrolling_screenshot缩放.png',
            #                           student_name, student_no)
            if custom_selected_targets:
                for target_each in custom_selected_targets:
                    print(target_each)
                    capture_scroll_screenshot_jvm(job_name_jvm, target_each, student_name, student_no)

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


def parse_targets(request):
    if request.method == 'POST':
        yaml_content = request.POST.get('yaml_content', '')

        try:
            # 使用正则表达式提取targets
            targets_match = re.search(r'targets:\s*\[([^\]]+)\]', yaml_content)
            if targets_match:
                targets = [t.strip(' "\'') for t in targets_match.group(1).split(',')]
                return JsonResponse({'targets': targets})
            else:
                return JsonResponse({'error': '未找到targets配置'})
        except Exception as e:
            return JsonResponse({'error': f'解析失败: {str(e)}'})

    return JsonResponse({'error': '无效请求'})


# 确保在urls.py中添加对应的路由

def parse_custom_config(request):
    if request.method == 'POST':
        custom_content = request.POST.get('custom_content', '')

        try:
            # 这里添加您的自定义解析逻辑
            # 示例：解析IP地址和端口
            import re
            # 匹配IP:端口格式的内容
            targets = re.findall(r'\b(?:\d{1,3}\.){3}\d{1,3}:\d+\b', custom_content)

            # 去重
            unique_targets = list(set(targets))

            return JsonResponse({'targets': unique_targets})
        except Exception as e:
            return JsonResponse({'error': f'解析失败: {str(e)}'})

    return JsonResponse({'error': '无效请求'})
