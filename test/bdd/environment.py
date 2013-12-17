import logging

from splinter.browser import Browser

def after_all(context):
    # Quit the browser if there were no errors
    if not context.failed:
        context.browser.quit()
        context.browser = None

def after_feature(context, feature):
    # Cause each feature to log in within the first scenario, so log out after
    # feature is done.  No need to log out if there was a failure AND the
    # 'stop' flag is used.  In that case, we want to leave the browser up at
    # the point where the failure was.
    if not context.failed or not context.config.stop:
        context.browser.visit(context.config.server_url + "/shopowner/accounts/logout/")

def after_tag(context, tag):
    if tag == "pause":
        context.pause = False

def before_all(context):
    # In case logging is not captured
    if not context.config.log_capture:
        logging.basicConfig(level=logging.DEBUG)

    # Default to firefox if not set
    browser = "firefox" if not context.config.browser else context.config.browser

    context.browser = Browser(browser)

def before_step(context, step):
    if "pause" in context and context.pause:
        raw_input("Press Enter to execute this step ...")

def before_tag(context, tag):
    if tag == "pause":
        context.pause = True

