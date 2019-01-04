from fabric.api import env,run
from fabric.operations import sudo
from fabric.tasks import execute

GIT_REPO = "https://github.com/wangcai-a/django_blog.git"

# 填写你自己的主机对应的域名
env.host_string = 'www.peng1.wang'


env.user = 'peng1'
env.password = '123456'

# 一般情况下为 22 端口，如果非 22 端口请查看你的主机服务提供商提供的信息
env.port = '22'


def deploy():
    source_folder = '/home/peng1/sites/peng1/django_blog'

    run('cd %s && git pull' % source_folder)
    run("""
        cd {} &&
        ../env/bin/pip install -r requirements.txt &&
        ../env/bin/python3 manage.py collectstatic --noinput &&
        ../env/bin/python3 manage.py migrate
        """.format(source_folder))
    sudo('supervisorctl restart peng1')
    sudo('service nginx reload')


if __name__ == '__main__':
    deploy()