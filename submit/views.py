from django.shortcuts import render
from django.http import HttpResponse
from .models import SubmitForm, ComIns
import paramiko, time


# Create your views here.
def submitTask(request):
    return render(request, 'submit/submit.html')


def submitCasDat(request):
    if request.method == 'POST':
        formContext = SubmitForm(request.POST, request.FILES)
        if formContext.is_valid():
            # acqur
            task_title = formContext.cleaned_data['taskname']
            task_cas = formContext.cleaned_data['casfile']
            task_dat = formContext.cleaned_data['datfile']

            # write to database
            task = ComIns()
            task.title = task_title
            task.cas = task_cas
            task.dat = task_dat
            task.save()

            # writ jou file
            p = ComIns.objects.get(title=task_title)

            with open('/home/tiger/Projects/Django/Fluent/media/test.jou', 'w') as f:
                f.write('/file/read-case-data\n')
                casAddress = task_title + '.cas'
                casAddress = '/home/lion/Tiger/Fluent/' + casAddress + '\n'
                f.write(casAddress)
                f.write('\n')

            return render(request, 'submit/set_para.html')
    else:
        formContext = SubmitForm()
    return HttpResponse('upload fail')


def setPara(request):
    if request.method == 'POST':
        num = str(request.POST['iterateNum'])
        with open('/home/tiger/Projects/Django/Fluent/media/test.jou', 'r') as f:
            filename = f.readlines()
            filename = filename[1].split('/')[-1]
            filename = filename.split('.')[0]

        with open('/home/tiger/Projects/Django/Fluent/media/test.jou', 'a') as f:
            f.write('/solve/iterate\n')
            f.write(num + '\n')
            f.write('\n')
            f.write('/file/write-case-data\n')
            f.write('/home/lion/Tiger/Fluent/' + filename + '-' + num + '.cas\n')
            f.write('\n')
            f.write('/exit')

        with open('/home/tiger/Projects/Django/Fluent/media/test.sh','w') as f:
            f.write('#!/bin/bash\n')
            f.write('fluent 2d -g -i /home/lion/Tiger/Fluent/test.jou')

        # SSH
        host = "10.0.0.17"
        port = 22
        transport = paramiko.Transport((host, port))

        password = "airation"
        username = "lion"
        transport.connect(username=username, password=password)

        sftp = paramiko.SFTPClient.from_transport(transport)

        filepath = '/home/lion/Tiger/Fluent/test.cas'
        localpath = '/home/tiger/Projects/Django/Fluent/media/test.cas'
        sftp.put(localpath, filepath)

        filepath = '/home/lion/Tiger/Fluent/test.dat'
        localpath = '/home/tiger/Projects/Django/Fluent/media/test.dat'
        sftp.put(localpath, filepath)

        filepath = '/home/lion/Tiger/Fluent/test.jou'
        localpath = '/home/tiger/Projects/Django/Fluent/media/test.jou'
        sftp.put(localpath, filepath)

        filepath = '/home/lion/Tiger/Fluent/test.sh'
        localpath = '/home/tiger/Projects/Django/Fluent/media/test.sh'
        sftp.put(localpath, filepath)

        sftp.close()
        transport.close()

        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, 22, username=username, password=password)
        #ssh.exec_command("chmod +x /home/lion/Tiger/Fluent/test.sh")
        #ssh.exec_command("/home/lion/Tiger/Fluent/test.sh")
        #ssh.exec_command("fluent 2d -g -i /home/lion/Tiger/Fluent/test.jou")

        channel = ssh.invoke_shell()
        stdin = channel.makefile('wb')
        stdout = channel.makefile('rb')

        stdin.write('''
            chmod +x /home/lion/Tiger/Fluent/test.sh
            /home/lion/Tiger/Fluent/test.sh
        ''')
        time.sleep(5)

        stdout.close()
        stdin.close()

        ssh.close()

        return HttpResponse('task ok')
    else:
        return HttpResponse('task fail')
