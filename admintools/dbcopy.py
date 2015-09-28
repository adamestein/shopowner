import json

from django.conf import settings
from django.http import HttpResponse

from common.views.generic import NavigationTemplateView


class DBCopy(NavigationTemplateView):
    @staticmethod
    def copy(from_db, to_db):
        """ Copy database """

        # Make sure the 'sandbox' name has '_sandbox' in it and the 'release' version does not
        release = settings.DATABASES["default"]["NAME"]
        if release.find("_sandbox") > -1:
            release = release[:release.find("_sandbox")]

        sandbox = settings.DATABASES["default"]["NAME"]
        if sandbox.find("_sandbox") == -1:
            sandbox += "_sandbox"

        dbinfo = {
            "host": settings.DATABASES["default"]["HOST"],
            "user": settings.DATABASES["default"]["USER"],
            "password": settings.DATABASES["default"]["PASSWORD"],
            "oldname": sandbox if from_db == "sandbox" else release,
            "newname": sandbox if to_db == "sandbox" else release
        }

        from subprocess import Popen, PIPE

        # Open a connection to the database program that will be used to run the SQL commands
        cmd = "/usr/bin/mysql -h {host} -u {user} -p{password}".format(**dbinfo)

        sql_server = Popen(
            cmd,
            shell=True,
            stdin=PIPE,
        )

        # Remove the database if it exists and (re)create it
        cmd = "DROP DATABASE IF EXISTS `{newname}`; CREATE DATABASE `{newname}`;".format(**dbinfo)

        sql_server.communicate(cmd)

        # Copy the schema and data to the new database
        cmd = (
            "/usr/bin/mysqldump -h {host} -u {user} -p{password} --skip-comments --single-transaction {oldname} | "
            "/usr/bin/mysql -h {host} -u {user} -p{password} {newname}"
        ).format(**dbinfo)

        import os

        os.system(cmd)

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            self.copy(kwargs["from_db"], kwargs["to_db"])

            return HttpResponse(
                json.dumps({}),
                mimetype="application/javascript"
            )
        else:
            return super(DBCopy, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(DBCopy, self).get_context_data(**kwargs)
        context.update({
            "from_db": kwargs["from_db"],
            "to_db": kwargs["to_db"],
            "pmessage": "Copying <em>" + kwargs["from_db"] + "</em> to <strong>" +
                        kwargs["to_db"] + "</strong>",
            "ajax": self._create_ajax_script()
        })
        return context

    @staticmethod
    def _create_ajax_script():
        from common.ajax import Ajax

        script = Ajax()

        script.add("dbcopy")

        script.init_function(
            "dbcopy",
            """
                // Hide the completion message and show the progress bar
                $("#message").hide();
                $("#progress").show();

                // Make AJAX call to copy database
                ajax.send_request("");
            """
        )

        script.success_function(
            "dbcopy",
            """
                bar.togglePause();

                // Hide the progress bar and show the completion message
                $("#message").show();
                $("#progress").hide();
            """
        )

        return script

