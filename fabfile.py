from fabric.api import env
from fabric.contrib.files import comment, exists, local, run, uncomment
from fabric.contrib.project import rsync_project

env.hosts = ["ssh.alwaysdata.com", ]
env.password = "5Px07y9h"
env.user = "stein"

appname = "ShopOwner_Apps"

wwwdir = "/home/stein/www/"             # Top level directory
destdir = wwwdir + appname              # Directory to install
modulesdir = "/home/stein/modules"      # Directory for 3rd party modules


def collect_static_files():
    # Collect all the static files in one place
    run("PYTHONPATH=" + modulesdir + " python " + destdir + "/manage.py collectstatic --noinput -l")


# Deploy development version
def dev():
    prereq()
    deploy()
    update_settings(False)
    collect_static_files()


# Deploy files to remote server
def deploy():
    # List of files to exclude deploying to remote
    exclude = [
        ".git",
        ".gitignore",
        "fabfile.py*",
        "migrations",
        "*.pyc",
        "*.log",
        "*.swp",
        "*.bak",
        "tests*",
        "testall",
        "datadumper.js"
    ]

    # Only copy what's needed
    rsync_project(destdir, "./", delete=True, exclude=exclude, extra_opts="--delete-excluded -L")


# Install prerequisite packages if needed
def prereq():
    if not exists(modulesdir):
        run("mkdir -p " + modulesdir)

    easy_install_cmd = "PYTHONPATH=" + modulesdir + \
                       " easy_install-2.6 --no-deps --install-dir " + modulesdir

    if not exists(modulesdir + "/django_db_file_storage-*.egg"):
        run(easy_install_cmd + " django-db-file-storage")

    if not exists(modulesdir + "/importlib-*.egg"):
        run(easy_install_cmd + " importlib")

    if not exists(modulesdir + "/django_localflavor-*egg"):
        run(easy_install_cmd + " django-localflavor")


# Deploy production version
def prod():
    prereq()
    deploy()
    update_settings()
    collect_static_files()

    # Migrate the DB (no problem if nothing needs to be done)
    local("RELEASE=1 ./manage.py migrate inventory")
    local("RELEASE=1 ./manage.py migrate sales")


# Update the Django settings file as appropriate for this deployment
def update_settings(isprod=True):
    # Remove packages not needed on remote server (and not available anyway)
    comment(destdir + "/system/settings.py", r"^.*django_extensions")
    comment(destdir + "/system/settings.py", r"^.*south")
    comment(destdir + "/system/settings.py", r"^.*localflavor")
    comment(destdir + "/system/settings.py", r"^.*django_behave")

    # Set up for remote
    comment(destdir + "/system/settings.py", r"^.*Local Setting")
    uncomment(destdir + "/system/settings.py", r"^.*Remote Setting")

    if isprod:
        # Comment out debugging
        comment(destdir + "/system/settings.py", r"^.*Dev Setting")
        uncomment(destdir + "/system/settings.py", r"^.*Prod Setting")

