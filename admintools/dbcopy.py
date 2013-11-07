from django.conf import settings
from common.views.generic import NavigationTemplateView

class DBCopy(NavigationTemplateView):
    dbnames = {
        "release":  "hhincwe_finance",
        "sandbox":  "hhincwe_finance_sandbox",
    }

    def copy(self, from_db, to_db):
        """ Copy database """

        dbinfo = {
            "host":         settings.DATABASES["default"]["HOST"],
            "user":         settings.DATABASES["default"]["USER"],
            "password":     settings.DATABASES["default"]["PASSWORD"],
            "oldname":      self.dbnames[from_db],
            "newname":      self.dbnames[to_db]
        }

        from subprocess import Popen, PIPE

        # Open a connection to the database program that will be used
        # to run the SQL commands
        cmd = """
            /usr/bin/mysql -h %(host)s -u %(user)s -p%(password)s
        """ % dbinfo

        sql_server = Popen(
            cmd,
            shell = True,
            stdin = PIPE,
        )

        # Remove the database if it exists and (re)create it
        db_cmd = """
            DROP DATABASE IF EXISTS `%(newname)s`;
            CREATE DATABASE `%(newname)s`;
            quit
        """ % dbinfo

        sql_server.communicate(db_cmd)

        # Copy the schema and data to the new database
        cmd = """
            /usr/bin/mysqldump -h %(host)s -u %(user)s -p%(password)s --skip-comments --single-transaction %(oldname)s | /usr/bin/mysql -h %(host)s -u %(user)s -p%(password)s %(newname)s
        """ % dbinfo

        import os

        os.system(cmd)

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            self.copy(kwargs["from_db"], kwargs["to_db"])

            from django.http import HttpResponse
            from django.utils import simplejson
            
            return HttpResponse(
                simplejson.dumps({}),
                mimetype = "application/javascript"
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

    def _create_ajax_script(self):
        from common.ajax import ajax

        ajax = ajax()

        ajax.add("dbcopy")

        ajax.init_function(
            "dbcopy",
            """
                // Hide the completion message and show the progress bar
                $("#message").hide();
                $("#progress").show();

                // Make AJAX call to copy database
                ajax.send_request("");
            """
        )

        ajax.success_function(
            "dbcopy",
            """
                bar.togglePause();

                // Hide the progress bar and show the completion message
                $("#message").show();
                $("#progress").hide();
            """
        )

        return ajax

