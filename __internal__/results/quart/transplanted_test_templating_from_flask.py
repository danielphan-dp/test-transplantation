# Transplanted from tests/test_templating.py to test src/quart/templating.py

import pytest
from quart import Quart, render_template, render_template_string, stream_template_string
from jinja2 import TemplateNotFound
from markupsafe import Markup

@pytest.fixture
def app():
    app = Quart(__name__)
    app.config['TESTING'] = True

    @app.route("/")
    async def index():
        return await render_template("context_template.html", value=23)

    return app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.mark.asyncio
async def test_context_processing(app, client):
    @app.context_processor
    def context_processor():
        return {"injected_value": 42}

    @app.route("/")
    async def index():
        return await render_template("context_template.html", value=23)

    rv = await client.get("/")
    assert rv.data == b"<p>23|42"

@pytest.mark.asyncio
async def test_original_win(app, client):
    @app.route("/")
    async def index():
        return await render_template_string("{{ config }}", config=42)

    rv = await client.get("/")
    assert rv.data == b"42"

@pytest.mark.asyncio
async def test_simple_stream(app, client):
    @app.route("/")
    async def index():
        return await stream_template_string("{{ config }}", config=42)

    rv = await client.get("/")
    assert rv.data == b"42"

@pytest.mark.asyncio
async def test_request_less_rendering(app):
    app.config["WORLD_NAME"] = "Special World"

    @app.context_processor
    def context_processor():
        return dict(foo=42)

    rv = await render_template_string("Hello {{ config.WORLD_NAME }} {{ foo }}")
    assert rv == "Hello Special World 42"

@pytest.mark.asyncio
async def test_standard_context(app, client):
    @app.route("/")
    async def index():
        app_ctx = app.app_context()
        app_ctx.push()
        app_ctx.g.foo = 23
        app_ctx.session["test"] = "aha"
        return await render_template_string(
            """
            {{ request.args.foo }}
            {{ g.foo }}
            {{ config.DEBUG }}
            {{ session.test }}
        """
        )

    rv = await client.get("/?foo=42")
    assert rv.data.split() == [b"42", b"23", b"False", b"aha"]

@pytest.mark.asyncio
async def test_escaping(app, client):
    text = "<p>Hello World!"

    @app.route("/")
    async def index():
        return await render_template(
            "escaping_template.html", text=text, html=Markup(text)
        )

    lines = (await client.get("/")).data.splitlines()
    assert lines == [
        b"&lt;p&gt;Hello World!",
        b"<p>Hello World!",
        b"<p>Hello World!",
        b"<p>Hello World!",
        b"&lt;p&gt;Hello World!",
        b"<p>Hello World!",
    ]

@pytest.mark.asyncio
async def test_no_escaping(app, client):
    text = "<p>Hello World!"

    @app.route("/")
    async def index():
        return await render_template(
            "non_escaping_template.txt", text=text, html=Markup(text)
        )

    lines = (await client.get("/")).data.splitlines()
    assert lines == [
        b"<p>Hello World!",
        b"<p>Hello World!",
        b"<p>Hello World!",
        b"<p>Hello World!",
        b"&lt;p&gt;Hello World!",
        b"<p>Hello World!",
        b"<p>Hello World!",
        b"<p>Hello World!",
    ]

@pytest.mark.asyncio
async def test_escaping_without_template_filename(app):
    assert await render_template_string("{{ foo }}", foo="<test>") == "&lt;test&gt;"
    assert await render_template("mail.txt", foo="<test>") == "<test> Mail"

@pytest.mark.asyncio
async def test_macros(app):
    macro = await app.jinja_env.get_template("_macro.html").module.hello
    assert macro("World") == "Hello World!"

@pytest.mark.asyncio
async def test_template_filter(app):
    @app.template_filter()
    def my_reverse(s):
        return s[::-1]

    assert "my_reverse" in app.jinja_env.filters.keys()
    assert app.jinja_env.filters["my_reverse"] == my_reverse
    assert app.jinja_env.filters["my_reverse"]("abcd") == "dcba"

@pytest.mark.asyncio
async def test_add_template_filter(app):
    def my_reverse(s):
        return s[::-1]

    app.add_template_filter(my_reverse)
    assert "my_reverse" in app.jinja_env.filters.keys()
    assert app.jinja_env.filters["my_reverse"] == my_reverse
    assert app.jinja_env.filters["my_reverse"]("abcd") == "dcba"

@pytest.mark.asyncio
async def test_template_filter_with_name(app):
    @app.template_filter("strrev")
    def my_reverse(s):
        return s[::-1]

    assert "strrev" in app.jinja_env.filters.keys()
    assert app.jinja_env.filters["strrev"] == my_reverse
    assert app.jinja_env.filters["strrev"]("abcd") == "dcba"

@pytest.mark.asyncio
async def test_add_template_filter_with_name(app):
    def my_reverse(s):
        return s[::-1]

    app.add_template_filter(my_reverse, "strrev")
    assert "strrev" in app.jinja_env.filters.keys()
    assert app.jinja_env.filters["strrev"] == my_reverse
    assert app.jinja_env.filters["strrev"]("abcd") == "dcba"

@pytest.mark.asyncio
async def test_template_filter_with_template(app, client):
    @app.template_filter()
    def super_reverse(s):
        return s[::-1]

    @app.route("/")
    async def index():
        return await render_template("template_filter.html", value="abcd")

    rv = await client.get("/")
    assert rv.data == b"dcba"

@pytest.mark.asyncio
async def test_add_template_filter_with_template(app, client):
    def super_reverse(s):
        return s[::-1]

    app.add_template_filter(super_reverse)

    @app.route("/")
    async def index():
        return await render_template("template_filter.html", value="abcd")

    rv = await client.get("/")
    assert rv.data == b"dcba"

@pytest.mark.asyncio
async def test_template_filter_with_name_and_template(app, client):
    @app.template_filter("super_reverse")
    def my_reverse(s):
        return s[::-1]

    @app.route("/")
    async def index():
        return await render_template("template_filter.html", value="abcd")

    rv = await client.get("/")
    assert rv.data == b"dcba"

@pytest.mark.asyncio
async def test_add_template_filter_with_name_and_template(app, client):
    def my_reverse(s):
        return s[::-1]

    app.add_template_filter(my_reverse, "super_reverse")

    @app.route("/")
    async def index():
        return await render_template("template_filter.html", value="abcd")

    rv = await client.get("/")
    assert rv.data == b"dcba"

@pytest.mark.asyncio
async def test_template_test(app):
    @app.template_test()
    def boolean(value):
        return isinstance(value, bool)

    assert "boolean" in app.jinja_env.tests.keys()
    assert app.jinja_env.tests["boolean"] == boolean
    assert app.jinja_env.tests["boolean"](False)

@pytest.mark.asyncio
async def test_add_template_test(app):
    def boolean(value):
        return isinstance(value, bool)

    app.add_template_test(boolean)
    assert "boolean" in app.jinja_env.tests.keys()
    assert app.jinja_env.tests["boolean"] == boolean
    assert app.jinja_env.tests["boolean"](False)

@pytest.mark.asyncio
async def test_template_test_with_name(app):
    @app.template_test("boolean")
    def is_boolean(value):
        return isinstance(value, bool)

    assert "boolean" in app.jinja_env.tests.keys()
    assert app.jinja_env.tests["boolean"] == is_boolean
    assert app.jinja_env.tests["boolean"](False)

@pytest.mark.asyncio
async def test_add_template_test_with_name(app):
    def is_boolean(value):
        return isinstance(value, bool)

    app.add_template_test(is_boolean, "boolean")
    assert "boolean" in app.jinja_env.tests.keys()
    assert app.jinja_env.tests["boolean"] == is_boolean
    assert app.jinja_env.tests["boolean"](False)

@pytest.mark.asyncio
async def test_template_test_with_template(app, client):
    @app.template_test()
    def boolean(value):
        return isinstance(value, bool)

    @app.route("/")
    async def index():
        return await render_template("template_test.html", value=False)

    rv = await client.get("/")
    assert b"Success!" in rv.data

@pytest.mark.asyncio
async def test_add_template_test_with_template(app, client):
    def boolean(value):
        return isinstance(value, bool)

    app.add_template_test(boolean)

    @app.route("/")
    async def index():
        return await render_template("template_test.html", value=False)

    rv = await client.get("/")
    assert b"Success!" in rv.data

@pytest.mark.asyncio
async def test_template_test_with_name_and_template(app, client):
    @app.template_test("boolean")
    def is_boolean(value):
        return isinstance(value, bool)

    @app.route("/")
    async def index():
        return await render_template("template_test.html", value=False)

    rv = await client.get("/")
    assert b"Success!" in rv.data

@pytest.mark.asyncio
async def test_add_template_test_with_name_and_template(app, client):
    def is_boolean(value):
        return isinstance(value, bool)

    app.add_template_test(is_boolean, "boolean")

    @app.route("/")
    async def index():
        return await render_template("template_test.html", value=False)

    rv = await client.get("/")
    assert b"Success!" in rv.data

@pytest.mark.asyncio
async def test_add_template_global(app):
    @app.template_global()
    def get_stuff():
        return 42

    assert "get_stuff" in app.jinja_env.globals.keys()
    assert app.jinja_env.globals["get_stuff"] == get_stuff
    assert app.jinja_env.globals["get_stuff"]() == 42

    rv = await render_template_string("{{ get_stuff() }}")
    assert rv == "42"

@pytest.mark.asyncio
async def test_custom_template_loader():
    class MyQuart(Quart):
        def create_global_jinja_loader(self):
            from jinja2 import DictLoader

            return DictLoader({"index.html": "Hello Custom World!"})

    app = MyQuart(__name__)

    @app.route("/")
    async def index():
        return await render_template("index.html")

    client = app.test_client()
    rv = await client.get("/")
    assert rv.data == b"Hello Custom World!"

@pytest.mark.asyncio
async def test_iterable_loader(app, client):
    @app.context_processor
    def context_processor():
        return {"whiskey": "Jameson"}

    @app.route("/")
    async def index():
        return await render_template(
            [
                "no_template.xml",  # should skip this one
                "simple_template.html",  # should render this
                "context_template.html",
            ],
            value=23,
        )

    rv = await client.get("/")
    assert rv.data == b"<h1>Jameson</h1>"

@pytest.mark.asyncio
async def test_templates_auto_reload(app):
    # debug is False, config option is None
    assert app.debug is False
    assert app.config["TEMPLATES_AUTO_RELOAD"] is None
    assert app.jinja_env.auto_reload is False
    # debug is False, config option is False
    app = Quart(__name__)
    app.config["TEMPLATES_AUTO_RELOAD"] = False
    assert app.debug is False
    assert app.jinja_env.auto_reload is False
    # debug is False, config option is True
    app = Quart(__name__)
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    assert app.debug is False
    assert app.jinja_env.auto_reload is True
    # debug is True, config option is None
    app = Quart(__name__)
    app.config["DEBUG"] = True
    assert app.config["TEMPLATES_AUTO_RELOAD"] is None
    assert app.jinja_env.auto_reload is True
    # debug is True, config option is False
    app = Quart(__name__)
    app.config["DEBUG"] = True
    app.config["TEMPLATES_AUTO_RELOAD"] = False
    assert app.jinja_env.auto_reload is False
    # debug is True, config option is True
    app = Quart(__name__)
    app.config["DEBUG"] = True
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    assert app.jinja_env.auto_reload is True

@pytest.mark.asyncio
async def test_custom_jinja_env():
    class CustomEnvironment(Quart.jinja_environment):
        pass

    class CustomQuart(Quart):
        jinja_environment = CustomEnvironment

    app = CustomQuart(__name__)
    assert isinstance(app.jinja_env, CustomEnvironment)