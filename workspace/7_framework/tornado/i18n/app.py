import tornado.ioloop
import tornado.web
import tornado.locale


class BaseHandler(tornado.web.RequestHandler):
    def get_user_locale(self):
        locale_code = self.path_kwargs.get("locale", "en_US")
        return tornado.locale.get(locale_code)


class LocaleHandler(BaseHandler):
    def get(self, locale):
        # Normalize and set locale
        locale = locale if locale in ("en_US", "ja_JP") else "en_US"
        self.locale = tornado.locale.get(locale)

        # Determine language switching
        if locale == "en_US":
            switch_locale = "ja_JP"
            flag = "🇯🇵"
            lang_name = "日本語"
        else:
            switch_locale = "en_US"
            flag = "🇺🇸"
            lang_name = "English"

        self.render("index.html",
                    current_locale=locale,
                    switch_locale=switch_locale,
                    lang_name=lang_name,
                    flag=flag,
                    product="Pro Suite",
                    author="Jay",
                    view=8880)


def make_app():
    return tornado.web.Application([
        (r"/(?P<locale>[a-z]{2}_[A-Z]{2})/about-us", LocaleHandler),
    ], template_path="templates")


if __name__ == "__main__":
    tornado.locale.load_translations("locale/")

    app = make_app()
    app.listen(8880)
    print("Server started at http://localhost:8880/en_US/about-us")
    tornado.ioloop.IOLoop.current().start()
